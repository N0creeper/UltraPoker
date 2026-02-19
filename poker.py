import random
import sys
import time
import algorythme
import ia
import graphique
import pygame


SMALL_BLIND_BASE = 5
BIG_BLIND_BASE = 10

blind_multiplier = 1
round_number = 1

jetons = [1000] * 6
ia_players = {0, 1, 2, 3, 4}
bouton = 5

ecran = graphique.creer_fenetre()
clock = pygame.time.Clock()

def nom_main(score_tuple):
    """Retourne le nom textuel d'une main à partir du tuple de score."""
    rank = score_tuple[0]
    noms = {
        1: "Hauteur",
        2: "Paire",
        3: "Double Paire",
        4: "Brelan",
        5: "Suite",
        6: "Couleur",
        7: "Full",
        8: "Carré",
        9: "Quinte Flush",
    }
    return noms.get(rank, "Main inconnue")


def new_deck():
    """Crée un nouveau jeu de 52 cartes au format 'VVC'."""
    couleurs = ["C", "D", "P", "T"]
    valeurs = ["01","02","03","04","05","06","07","08","09","10","11","12","13"]
    return [v + c for v in valeurs for c in couleurs]


def tirer_carte(deck):
    """Tire aléatoirement une carte du paquet et la retire."""
    i = random.randrange(len(deck))
    return deck.pop(i)


def position_joueur(i, bouton, n_players=6):
    """Calcule la position d'un joueur en fonction du bouton."""
    positions = ["BTN", "SB", "BB", "UTG", "MP", "CO"]
    return positions[(i - bouton) % n_players]


def init_pot_manager(n_players):
    """Initialise le gestionnaire de pot pour n joueurs."""
    return {
        "n": n_players,
        "contributions": [0] * n_players,
        "folded": [False] * n_players,
        "all_in": [False] * n_players,
    }


def pot_add_bet(pm, player, amount):
    """Ajoute une mise au pot pour un joueur donné."""
    pm["contributions"][player] += amount


def pot_fold(pm, player):
    """Marque un joueur comme ayant foldé dans le pot manager."""
    pm["folded"][player] = True


def pot_set_all_in(pm, player):
    """Marque un joueur comme all-in dans le pot manager."""
    pm["all_in"][player] = True


def pot_build_side_pots(pm):
    """Construit la liste des side-pots à partir des contributions."""
    n = pm["n"]
    contrib = pm["contributions"][:]
    folded = pm["folded"]
    pots = []

    while True:
        active = [c for i, c in enumerate(contrib) if c > 0 and not folded[i]]
        if not active:
            break

        m = min(active)
        pot_amount = 0
        eligible = []

        for i in range(n):
            if contrib[i] > 0:
                take = min(contrib[i], m)
                pot_amount += take
                contrib[i] -= take
                if not folded[i]:
                    eligible.append(i)

        pots.append({"amount": pot_amount, "eligible": eligible})

    return pots


# ---------------------------------------------------------
# SHOWDOWN VISUEL
# ---------------------------------------------------------
def afficher_showdown(mains, board, pm):
    """Affiche le showdown visuel et montre les forces des mains."""
    graphique.showdown_mode = True

    for i in range(6):
        if not pm["folded"][i] and jetons[i] > 0:
            score = algorythme.meilleure_main(mains[i] + board)
            graphique.hand_strengths[i] = nom_main(score)

    graphique.dessiner_table(ecran)
    graphique.dessiner_joueurs(ecran, jetons)
    graphique.afficher_board(ecran, board)
    graphique.afficher_pot(ecran, sum(pm["contributions"]))
    graphique.afficher_round(ecran, round_number)

    for i in range(6):
        if not pm["folded"][i] and jetons[i] > 0:
            x, y = graphique.PLAYER_POS[i]
            graphique.afficher_main(ecran, mains[i], x, y)
            graphique.afficher_force_main(ecran, i)

    graphique.rafraichir(ecran)
    pygame.time.wait(2500)

    graphique.showdown_mode = False
    graphique.hand_strengths.clear()


def tour_encheres(mains, jetons, pm, board, bouton, small_blind, big_blind):
    """Gère un tour d'enchères (preflop/postflop) et retourne (fini,mises)."""
    n = len(mains)
    mises = [0] * n
    big = 0
    acted = [False] * n
    boutons = None

    if not board:
        sb = (bouton + 1) % n
        bb = (bouton + 2) % n

        sb_bet = min(small_blind, jetons[sb])
        jetons[sb] -= sb_bet
        mises[sb] += sb_bet
        pot_add_bet(pm, sb, sb_bet)

        bb_bet = min(big_blind, jetons[bb])
        jetons[bb] -= bb_bet
        mises[bb] += bb_bet
        pot_add_bet(pm, bb, bb_bet)

        big = max(sb_bet, bb_bet)

    current = (bouton + 3) % n

    while True:

        graphique.jetons_global = jetons
        graphique.folded_global = pm["folded"]

        if len(board) >= 3:
            score = algorythme.meilleure_main(mains[5] + board)
            graphique.hand_strengths[5] = nom_main(score)

        graphique.dessiner_table(ecran)
        graphique.dessiner_joueurs(ecran, jetons)
        graphique.afficher_board(ecran, board)
        graphique.afficher_pot(ecran, sum(pm["contributions"]))
        graphique.afficher_round(ecran, round_number)

        for i in range(n):
            graphique.afficher_main_joueur(ecran, mains[i], i)
            graphique.afficher_mise_joueur(ecran, i, mises[i])

        if current == 5:
            boutons = graphique.dessiner_boutons(ecran)
        else:
            boutons = None

        graphique.rafraichir(ecran)
        clock.tick(60)

        folded = pm["folded"]
        all_in = pm["all_in"]
        contributions = pm["contributions"]

        if all(folded[i] or jetons[i] <= 0 for i in ia_players):
            return True, mises

        actifs = [i for i in range(n) if not folded[i] and jetons[i] > 0]
        if len(actifs) == 1:
            return True, mises

        if all(
            folded[i] or all_in[i] or (acted[i] and mises[i] == big) or jetons[i] <= 0
            for i in range(n)
        ):
            return False, mises

        if folded[current] or all_in[current] or jetons[current] <= 0:
            current = (current + 1) % n
            continue

        to_call = big - mises[current]

        if current in ia_players:

            graphique.afficher_action_joueur(ecran, current, "Réfléchit…")
            graphique.rafraichir(ecran)
            pygame.time.wait(400)

            action = ia.decision(
                main=mains[current],
                board=board,
                jetons=jetons[current],
                mise_a_suivre=to_call,
                pot=sum(contributions),
                position=position_joueur(current, bouton, n),
            )

            if action == "a":
                txt = "Se couche"
            elif action == "s":
                txt = "Suit / Check"
            else:
                txt = f"Relance {action}"

            graphique.afficher_action_joueur(ecran, current, txt)
            graphique.rafraichir(ecran)
            pygame.time.wait(600)

        else:
            if boutons is None:
                current = (current + 1) % n
                continue

            action = graphique.attendre_action_joueur(boutons)
            if action == "r":
                action = graphique.demander_relance(ecran)

        acted[current] = True

        if action == "a":
            pot_fold(pm, current)
            current = (current + 1) % n
            continue

        if action == "s":
            if to_call > 0:
                call_amount = min(jetons[current], to_call)
                mises[current] += call_amount
                jetons[current] -= call_amount
                pot_add_bet(pm, current, call_amount)
                if jetons[current] == 0:
                    pot_set_all_in(pm, current)
            current = (current + 1) % n
            continue

        if isinstance(action, int):
            raise_amount = min(action, jetons[current])
            mises[current] += raise_amount
            jetons[current] -= raise_amount
            pot_add_bet(pm, current, raise_amount)

            if jetons[current] == 0:
                pot_set_all_in(pm, current)

            if mises[current] > big:
                big = mises[current]
                for i in range(n):
                    if (
                        i != current
                        and not folded[i]
                        and not all_in[i]
                        and jetons[i] > 0
                    ):
                        acted[i] = False

            current = (current + 1) % n
            continue

# ---------------------------------------------------------
# SHOWDOWN LOGIQUE
# ---------------------------------------------------------
def showdown(mains, board, pm):
    """Résout le showdown logique et retourne les gains par joueur."""
    pots = pot_build_side_pots(pm)
    folded = pm["folded"]

    results = {}
    for i, main in enumerate(mains):
        if not folded[i] and jetons[i] > 0:
            results[i] = algorythme.meilleure_main(main + board)

    gains = [0] * len(mains)

    for pot in pots:
        eligibles = pot["eligible"]
        best_score = None
        winners = []

        for p in eligibles:
            if jetons[p] <= 0:
                continue
            score = results[p]
            if best_score is None or score > best_score:
                best_score = score
                winners = [p]
            elif score == best_score:
                winners.append(p)

        share = pot["amount"] // len(winners)
        remainder = pot["amount"] % len(winners)

        for w in winners:
            gains[w] += share
        for i in range(remainder):
            gains[winners[i]] += 1

    return gains


# ---------------------------------------------------------
# UNE MAIN COMPLÈTE
# ---------------------------------------------------------
def game():
    """Exécute une main complète (préflop → river) et met à jour l'état des jetons."""
    global jetons, bouton, round_number, blind_multiplier

    n = len(jetons)
    if n < 2:
        sys.exit()

    if round_number % 10 == 0 and blind_multiplier < 8:
        blind_multiplier *= 2

    small_blind = SMALL_BLIND_BASE * blind_multiplier
    big_blind = BIG_BLIND_BASE * blind_multiplier

    deck = new_deck()
    mains = [[] for _ in range(n)]
    board = []

    for i in range(n):
        mains[i].append(tirer_carte(deck))
        mains[i].append(tirer_carte(deck))

    pm = init_pot_manager(n)

    fini, _ = tour_encheres(mains, jetons, pm, board, bouton, small_blind, big_blind)
    if fini:
        afficher_showdown(mains, board, pm)
        gains = showdown(mains, board, pm)
        for i, g in enumerate(gains):
            jetons[i] += g
        bouton = (bouton + 1) % n
        round_number += 1
        pygame.time.wait(800)
        return

    _ = tirer_carte(deck)
    board += [tirer_carte(deck), tirer_carte(deck), tirer_carte(deck)]
    pygame.time.wait(500)

    fini, _ = tour_encheres(mains, jetons, pm, board, bouton, small_blind, big_blind)
    if fini:
        afficher_showdown(mains, board, pm)
        gains = showdown(mains, board, pm)
        for i, g in enumerate(gains):
            jetons[i] += g
        bouton = (bouton + 1) % n
        round_number += 1
        pygame.time.wait(800)
        return

    _ = tirer_carte(deck)
    board.append(tirer_carte(deck))
    pygame.time.wait(500)

    fini, _ = tour_encheres(mains, jetons, pm, board, bouton, small_blind, big_blind)
    if fini:
        afficher_showdown(mains, board, pm)
        gains = showdown(mains, board, pm)
        for i, g in enumerate(gains):
            jetons[i] += g
        bouton = (bouton + 1) % n
        round_number += 1
        pygame.time.wait(800)
        return

    _ = tirer_carte(deck)
    board.append(tirer_carte(deck))
    pygame.time.wait(500)

    fini, _ = tour_encheres(mains, jetons, pm, board, bouton, small_blind, big_blind)

    afficher_showdown(mains, board, pm)
    gains = showdown(mains, board, pm)
    for i, g in enumerate(gains):
        jetons[i] += g

    bouton = (bouton + 1) % n
    round_number += 1
    pygame.time.wait(800)


# ---------------------------------------------------------
# BOUCLE PRINCIPALE
# ---------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game()
    clock.tick(60)
