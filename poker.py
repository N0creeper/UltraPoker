import random
import algorythme
import ia
import os 
import time
import sys

cards = [
    "01C","01D","01P","01T",
    "02C","02D","02P","02T",
    "03C","03D","03P","03T",
    "04C","04D","04P","04T",
    "05C","05D","05P","05T",
    "06C","06D","06P","06T",
    "07C","07D","07P","07T",
    "08C","08D","08P","08T",
    "09C","09D","09P","09T",
    "10C","10D","10P","10T",
    "11C","11D","11P","11T",
    "12C","12D","12P","12T",
    "13C","13D","13P","13T",
]

mains = [[], [], [], [], [], []]
middle = []
jetons = [1000, 1000, 1000, 1000, 1000, 1000]
mises = [0, 0, 0, 0, 5, 10]
ia_players = [0,1,2,3,4]
bouton = 5


def position_joueur(i):
    global bouton
    positions = ["BTN", "SB", "BB", "UTG", "MP", "CO"]
    index_position = (i - bouton) % 6
    return positions[index_position]


def creation_mains(liste):
    global cards
    for i in liste:
        a = random.randint(0, len(cards) - 1)
        i.append(cards[a])
        cards.pop(a)
        a = random.randint(0, len(cards) - 1)
        i.append(cards[a])
        cards.pop(a)
    return liste


def creation_mid(mid):
    for i in range(5):
        a = random.randint(0, len(cards) - 1)
        mid.append(cards[a])
        cards.pop(a)
    return mid


def description_combinaison(resultat):
    comb = resultat["combinaison"]
    if resultat["straight_flush"]:
        return f"Quinte flush hauteur {resultat['straight'][1]}"
    if "carre" in comb:
        return f"Carré de {comb['carre'][0]}"
    if "full" in comb:
        return f"Full : {comb['full'][0]} par {comb['full'][1]}"
    if resultat["flush"]:
        return "Couleur"
    if resultat["straight"]:
        return f"Suite hauteur {resultat['straight'][1]}"
    if "brelan" in comb:
        return f"Brelan de {comb['brelan'][0]}"
    if "double paire" in comb:
        p1, p2 = sorted(comb["double paire"], reverse=True)
        return f"Double paire : {p1} et {p2}"
    if "paire" in comb:
        return f"Paire de {comb['paire'][0]}"
    return f"Hauteur {resultat['high']}"


def fin(j, p):
    global mains, jetons, mises,middle
    gagnant_index = j[0]
    main_gagnante = mains[gagnant_index]
    analyse = algorythme.algorythme5c(main_gagnante + middle)
    texte = description_combinaison(analyse)
    jetons[gagnant_index] += p
    clear_screen()
    print("Gagnant :", main_gagnante)
    print("Combinaison :", texte)
    print("Jetons :", jetons)
    print("fin")
    print("Board",middle)
    time.sleep(10)

def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception:
        print("\n" * 50)

def mise_pot(m, p):
    for i in m:
        p += i
    return p


def verification_gagnant(ms, md):
    mains_verifs = []
    for main in ms:
        mains_verifs.append((algorythme.meilleure_main(main + md), main))
    print(mains_verifs)
    print(max(mains_verifs))
    return max(mains_verifs)


def tour_encheres(mains, mises, jetons, pot, board):
    n = len(mains)
    big = max(mises)
    acted = [False] * n
    for i in range(n):
        if mises[i] == big:
            acted[i] = True

    loop_guard = 0
    MAX_LOOPS = 1000

    while True:
        loop_guard += 1
        if loop_guard > MAX_LOOPS:
            print("Erreur: trop d'itérations dans le tour d'enchères, on force la fin.")
            return False, pot, mises

        joueurs_actifs = [k for k in range(n) if mains[k] != "F"]
        if len(joueurs_actifs) == 1:
            return True, pot, mises
        if all(acted[k] for k in joueurs_actifs):
            return False, pot, mises
        if len(board) == 0:
            start_idx = (bouton + 3) % n
        else:
            start_idx = (bouton + 1) % n
        for k in range(n):
            i = (start_idx + k) % n
            if mains[i] == "F":
                continue
            if acted[i] and mises[i] == big:
                continue
            if i not in ia_players:
                print("Board :", board)
                print("Main :", mains[i])
                print("Pot :", pot)
                print("Jetons :", jetons[i])
                print("Call =", big)
                print("Mise perso =", mises[i])
            w = True
            while w:
                to_call = big - mises[i]
                if i in ia_players:
                    print(f"[DEBUG] joueur {i} to_call={to_call} mises[i]={mises[i]} big={big} jetons={jetons[i]}")
                    r = ia.decision(
                        main = mains[i],
                        board = board,
                        jetons = jetons[i],
                        mise_a_suivre = to_call,
                        pot = pot,
                        position = position_joueur(i)
                    )
                    print(f"[DEBUG] IA {i} reponse: {r}")
                    if isinstance(r, int):
                        if r == big:
                            diff = big - mises[i]
                            if diff <= jetons[i]:
                                jetons[i] -= diff
                                mises[i] = big
                                acted[i] = True
                                w = False
                                break
                            else:
                                mains[i] = "F"
                                acted[i] = True
                                w = False
                                break
                        if r > big:
                            if r <= mises[i] + jetons[i]:
                                diff = r - mises[i]
                                jetons[i] -= diff
                                mises[i] = r
                                big = r
                                acted = [False] * n
                                acted[i] = True
                                w = False
                                break
                            else:
                                mains[i] = "F"
                                acted[i] = True
                                w = False
                                break
                        print("invalide")
                        continue
                else:
                    r = input("Action? (f=fold, c=call/check, sinon montant relance) ")
                print(f"RESULTAT de {i}:", r)
                if r == "f":
                    mains[i] = "F"
                    acted[i] = True
                    w = False
                    break
                if r == "c":
                    diff = big - mises[i]
                    if diff <= jetons[i]:
                        jetons[i] -= diff
                        mises[i] = big
                        acted[i] = True
                        w = False
                        break
                    else:
                        print("Pas assez de jetons pour caller, fold forcé.")
                        mains[i] = "F"
                        acted[i] = True
                        w = False
                        break
                try:
                    r_int = int(r)
                except Exception:
                    print("invalide")
                    continue
                if r_int >= big and r_int <= jetons[i] + mises[i]:
                    diff = r_int - mises[i]
                    jetons[i] -= diff
                    mises[i] = r_int
                    big = r_int
                    acted = [False] * n
                    acted[i] = True
                    w = False
                    break
                else:
                    print("invalide")
                    continue
            joueurs_actifs = [k for k in range(n) if mains[k] != "F"]
            if len(joueurs_actifs) == 1:
                return True, pot, mises
            if all(acted[k] for k in joueurs_actifs):
                return False, pot, mises

def eliminate_players():
    global jetons, ia_players, bouton

    old_n = len(jetons)
    old_humans = [i for i in range(old_n) if i not in ia_players]

    keep_indices = [i for i, j in enumerate(jetons) if j > 0]

    if len(keep_indices) < 2:
        return False

    eliminated_humans = [h for h in old_humans if h not in keep_indices]
    if eliminated_humans:
        print("Un joueur humain a été éliminé. Arrêt du programme.")
        sys.exit(0)

    new_jetons = [jetons[i] for i in keep_indices]

    new_ia_players = []
    for new_idx, old_idx in enumerate(keep_indices):
        if old_idx in ia_players:
            new_ia_players.append(new_idx)

    if bouton in keep_indices:
        bouton = keep_indices.index(bouton)
    else:
        next_idx = None
        for idx in keep_indices:
            if idx > bouton:
                next_idx = idx
                break
        if next_idx is None:
            next_idx = keep_indices[0]
        bouton = keep_indices.index(next_idx)
    jetons = new_jetons
    ia_players = new_ia_players

    return True


def game():
    global cards, mains, middle, mises, bouton, ia_players, jetons

    cards = [
        "01C","01D","01P","01T",
        "02C","02D","02P","02T",
        "03C","03D","03P","03T",
        "04C","04D","04P","04T",
        "05C","05D","05P","05T",
        "06C","06D","06P","06T",
        "07C","07D","07P","07T",
        "08C","08D","08P","08T",
        "09C","09D","09P","09T",
        "10C","10D","10P","10T",
        "11C","11D","11P","11T",
        "12C","12D","12P","12T",
        "13C","13D","13P","13T",
    ]

    n = len(jetons)
    if n < 2:
        print("Tournoi terminé : moins de 2 joueurs restants.")
        return

    mains = [[] for _ in range(n)]
    middle = []
    mises = [0] * n
    pot = 0

    clear_screen()
    positions = [position_joueur(i) for i in range(n)]
    print("=== Début de la main ===")
    for idx, pos in enumerate(positions):
        statut = "IA" if idx in ia_players else "HUMAIN"
        print(f"Joueur {idx} ({statut}) -> Position: {pos} ; Jetons: {jetons[idx]}")
    print("========================")

    for i in range(n):
        pos = position_joueur(i)
        if pos == "SB":
            mises[i] = 5
            jetons[i] -= 5
        elif pos == "BB":
            mises[i] = 10
            jetons[i] -= 10

    creation_mains(mains)
    creation_mid(middle)

    fini, pot, mises = tour_encheres(mains, mises, jetons, pot, [])
    if fini:
        pot += sum(mises)
        fin([i for i in range(len(mains)) if mains[i] != "F"], pot)
        if not eliminate_players():
            print("Fin du tournoi.")
            return
        bouton = (bouton + 1) % len(jetons)
        return

    pot += sum(mises)
    mises = [0] * n

    fini, pot, mises = tour_encheres(mains, mises, jetons, pot, middle[:3])
    if fini:
        pot += sum(mises)
        fin([i for i in range(len(mains)) if mains[i] != "F"], pot)
        if not eliminate_players():
            print("Fin du tournoi.")
            return
        bouton = (bouton + 1) % len(jetons)
        return

    pot += sum(mises)
    mises = [0] * n

    fini, pot, mises = tour_encheres(mains, mises, jetons, pot, middle[:4])
    if fini:
        pot += sum(mises)
        fin([i for i in range(len(mains)) if mains[i] != "F"], pot)
        if not eliminate_players():
            print("Fin du tournoi.")
            return
        bouton = (bouton + 1) % len(jetons)
        return

    pot += sum(mises)
    mises = [0] * n

    fini, pot, mises = tour_encheres(mains, mises, jetons, pot, middle[:5])
    if fini:
        pot += sum(mises)
        fin([i for i in range(len(mains)) if mains[i] != "F"], pot)
        if not eliminate_players():
            print("Fin du tournoi.")
            return
        bouton = (bouton + 1) % len(jetons)
        return

    pot += sum(mises)

    joueurs_actifs = [i for i in range(len(mains)) if mains[i] != "F"]
    mains_actives = [mains[i] for i in joueurs_actifs]
    gagnant = verification_gagnant(mains_actives, middle)
    fin([joueurs_actifs[mains_actives.index(gagnant[1])]], pot)

    if not eliminate_players():
        print("Fin du tournoi.")
        return
    bouton = (bouton + 1) % len(jetons)

while True:
    game()