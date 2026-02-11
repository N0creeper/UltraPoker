import random
import sys
import time
import algorythme
import ia

SMALL_BLIND = 5
BIG_BLIND = 10

INITIAL_CHIPS = 1000
jetons = [INITIAL_CHIPS] * 6
ia_players = {0, 1, 2, 3, 4}
bouton = 5


def new_deck():
    """Crée un nouveau jeu de cartes."""
    couleurs = ["C", "D", "P", "T"]
    valeurs = [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
    ]
    deck = [valeur + couleur for valeur in valeurs for couleur in couleurs]
    return deck


def tirer_carte(deck):
    """Tire une carte aléatoire du jeu."""
    if not deck:
        return None
    i = random.randrange(len(deck))
    return deck.pop(i)


def position_joueur(i, bouton, n_players=6):
    """Détermine la position du joueur en fonction de l'index et du bouton."""
    positions = ["BTN", "SB", "BB", "UTG", "MP", "CO"]
    index_position = (i - bouton) % n_players
    return positions[index_position]


def init_pot_manager(n_players):
    """Initialise le gestionnaire de pot."""
    return {
        "n": n_players,
        "contributions": [0] * n_players,
        "folded": [False] * n_players,
        "all_in": [False] * n_players,
    }


def pot_add_bet(pot_manager, player, amount):
    """Ajoute une mise au pot pour un joueur."""
    pot_manager["contributions"][player] += amount


def pot_fold(pot_manager, player):
    """Indique qu'un joueur s'est couché."""
    pot_manager["folded"][player] = True


def pot_set_all_in(pot_manager, player):
    """Indique qu'un joueur est all-in."""
    pot_manager["all_in"][player] = True


def pot_build_side_pots(pot_manager):
    """Construit les pots secondaires."""
    n = pot_manager["n"]
    contrib = pot_manager["contributions"][:]
    folded = pot_manager["folded"]
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


def afficher_action(message):
    """
    Affiche la désision du joueur/ia
    """
    print(message)
    time.sleep(5)


def tour_encheres(mains, jetons, pot_manager, board, bouton):
    """
    Fait un tours d'enchère 
    """
    n = len(mains)

    if not board:
        start = (bouton + 3) % n
    else:
        start = (bouton + 1) % n

    mises = [0] * n
    big = 0
    current = start
    acted = [False] * n

    while True:

        folded = pot_manager["folded"]
        all_in = pot_manager["all_in"]
        contributions = pot_manager["contributions"]

        actifs = [i for i in range(n) if not folded[i]]

        if len(actifs) == 1:
            return True, mises

        if all(folded[i] or all_in[i] or (acted[i] and mises[i] == big) for i in range(n)):
            return False, mises

        if folded[current] or all_in[current]:
            current = (current + 1) % n
            continue

        to_call = big - mises[current]

        if (
            not board
            and sum(contributions) == SMALL_BLIND + BIG_BLIND
            and position_joueur(current, bouton) not in ["SB", "BB"]
        ):
            to_call = 0

        print("\n==============================")
        print(
            f"Joueur {current} ({'IA' if current in ia_players else 'HUMAIN'}) - Position {position_joueur(current, bouton, n)}"
        )
        if current not in ia_players:
            print("Main :", mains[current])
        print("Board :", board)
        print("Pot courant :", sum(contributions))
        print("Mise actuelle :", mises[current])
        print("Doit payer :", to_call)
        print("Jetons restants :", jetons[current])
        print("==============================")

        if current in ia_players:
            action = ia.decision(
                main=mains[current],
                board=board,
                jetons=jetons[current],
                mise_a_suivre=to_call,
                pot=sum(contributions),
                position=position_joueur(current, bouton, n),
            )
            print("Action IA :", action)
        else:
            action = input("Action? (f=fold, c=call/check, sinon montant relance) ")

        acted[current] = True

        if action == "f":
            afficher_action(f"Joueur {current} FOLD")
            pot_fold(pot_manager, current)
            current = (current + 1) % n
            continue

        if action == "c":
            if to_call > 0:
                call_amount = min(jetons[current], to_call)
                mises[current] += call_amount
                jetons[current] -= call_amount
                pot_add_bet(pot_manager, current, call_amount)

                if jetons[current] == 0:
                    pot_set_all_in(pot_manager, current)
                    afficher_action(f"Joueur {current} ALL-IN (call)")
                else:
                    afficher_action(f"Joueur {current} CALL ({mises[current]})")
            else:
                afficher_action(f"Joueur {current} CHECK")

            current = (current + 1) % n
            continue

        try:
            target = int(action)
        except ValueError:
            print("Action invalide.")
            continue

        if target <= mises[current]:
            print("Relance trop petite.")
            continue

        raise_amount = min(target - mises[current], jetons[current])

        mises[current] += raise_amount
        jetons[current] -= raise_amount
        pot_add_bet(pot_manager, current, raise_amount)

        if jetons[current] == 0:
            pot_set_all_in(pot_manager, current)
            afficher_action(f"Joueur {current} ALL-IN à {mises[current]}")
        else:
            if to_call == 0:
                afficher_action(f"Joueur {current} BET à {mises[current]}")
            else:
                afficher_action(f"Joueur {current} RAISE à {mises[current]}")

        if mises[current] > big:
            big = mises[current]
            for i in range(n):
                if i != current and not folded[i] and not all_in[i]:
                    acted[i] = False

        current = (current + 1) % n


def showdown(mains, board, pot_manager):
    """Détermine le(s) gagnant(s) et distribue le pot."""
    pots = pot_build_side_pots(pot_manager)
    folded = pot_manager["folded"]

    results = {}
    for i, main in enumerate(mains):
        if not folded[i]:
            results[i] = algorythme.meilleure_main(main + board)

    gains = [0] * len(mains)

    for pot in pots:
        eligibles = pot["eligible"]
        best_score = None
        winners = []

        for p in eligibles:
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


def game():
    """Gère une main de poker."""
    global jetons, bouton

    n = len(jetons)
    if n < 2:
        print("Tournoi terminé : moins de 2 joueurs.")
        sys.exit(0)

    deck = new_deck()
    mains = [[] for _ in range(n)]
    board = []

    positions = [position_joueur(i, bouton, n) for i in range(n)]
    print("=== Début de la main ===")
    for i in range(n):
        statut = "IA" if i in ia_players else "HUMAIN"
        print(
            f"Joueur {i} ({statut}) -> Position: {positions[i]} ; Jetons: {jetons[i]}"
        )
    print("========================")
    time.sleep(5)

    for i in range(n):
        mains[i].append(tirer_carte(deck))
        mains[i].append(tirer_carte(deck))

    pm = init_pot_manager(n)

    for i in range(n):
        pos = position_joueur(i, bouton, n)
        if pos == "SB":
            mise = min(jetons[i], SMALL_BLIND)
            jetons[i] -= mise
            pot_add_bet(pm, i, mise)
        elif pos == "BB":
            mise = min(jetons[i], BIG_BLIND)
            jetons[i] -= mise
            pot_add_bet(pm, i, mise)

    fini, _ = tour_encheres(mains, jetons, pm, board, bouton)
    if fini:
        gains = showdown(mains, board, pm)
        for i, g in enumerate(gains):
            jetons[i] += g
        afficher_fin(mains, board, gains)
        bouton = (bouton + 1) % n
        return

    _ = tirer_carte(deck)
    board.append(tirer_carte(deck))
    board.append(tirer_carte(deck))
    board.append(tirer_carte(deck))

    fini, _ = tour_encheres(mains, jetons, pm, board, bouton)
    if fini:
        gains = showdown(mains, board, pm)
        for i, g in enumerate(gains):
            jetons[i] += g
        afficher_fin(mains, board, gains)
        bouton = (bouton + 1) % n
        return

    _ = tirer_carte(deck)
    board.append(tirer_carte(deck))

    fini, _ = tour_encheres(mains, jetons, pm, board, bouton)
    if fini:
        gains = showdown(mains, board, pm)
        for i, g in enumerate(gains):
            jetons[i] += g
        afficher_fin(mains, board, gains)
        bouton = (bouton + 1) % n
        return

    _ = tirer_carte(deck)
    board.append(tirer_carte(deck))

    fini, _ = tour_encheres(mains, jetons, pm, board, bouton)
    gains = showdown(mains, board, pm)
    for i, g in enumerate(gains):
        jetons[i] += g
    afficher_fin(mains, board, gains)
    bouton = (bouton + 1) % n


def afficher_fin(mains, board, gains):
    """Affiche les résultats de la main."""
    print("========== FIN DE LA MAIN ==========")
    print("Board :", board)
    for i, main in enumerate(mains):
        print(f"{"IA" if i in ia_players else "Joueur"} {i} : {main} | Gain: {gains[i]} | Stack: {jetons[i]}")
    print("====================================")
    time.sleep(5)


while True:
    game()
