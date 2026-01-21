import random
import algorythme

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
jetons = [1500, 1500, 1500, 1500, 1495, 1490]
mises = [0, 0, 0, 0, 5, 10]


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
    global mains, jetons, mises
    gagnant_index = j[0]
    main_gagnante = mains[gagnant_index]
    analyse = algorythme.algorythme5c(main_gagnante + middle)
    texte = description_combinaison(analyse)
    jetons[gagnant_index] += p
    print("Gagnant :", main_gagnante)
    print("Combinaison :", texte)
    print("Jetons :", jetons)
    print("fin")


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
    actions_depuis_relance = 0
    big = max(mises)

    while True:
        joueurs_actifs = [k for k in range(len(mains)) if mains[k] != "F"]
        for i in range(len(mains)):
            if mains[i] == "F":
                continue
            print("Board :", board)
            print("Main :", mains[i])
            print("Pot :", pot)
            print("Jetons :", jetons[i])
            print("Call =", big)
            print("Mise perso =", mises[i])

            w = True
            while w:
                r = input("Action? (f=fold, c=call/check, sinon montant relance) ")

                if r == "f":
                    mains[i] = "F"
                    w = False
                    continue

                elif r == "c":
                    diff = big - mises[i]
                    if diff <= jetons[i]:
                        jetons[i] -= diff
                        mises[i] = big
                        actions_depuis_relance += 1
                        w = False
                    else:
                        print("Pas assez de jetons")
                    continue

                else:
                    try:
                        r = int(r)
                    except ValueError:
                        print("invalide")
                        continue

                    if r >= big and r <= jetons[i] + mises[i]:
                        diff = r - mises[i]
                        jetons[i] -= diff
                        mises[i] = r
                        big = r
                        actions_depuis_relance = 0
                        w = False
                    else:
                        print("invalide")

            joueurs_actifs = [k for k in range(len(mains)) if mains[k] != "F"]

            if len(joueurs_actifs) == 1:
                return True, pot, mises

            if actions_depuis_relance == len(joueurs_actifs):
                return False, pot, mises


def game():
    global mains, middle, jetons, mises

    pot = 0
    creation_mains(mains)
    creation_mid(middle)

    fini, pot, mises = tour_encheres(mains, mises, jetons, pot, [])
    if fini:
        fin([i for i in range(len(mains)) if mains[i] != "F"], pot)
        return

    pot += sum(mises)
    mises = [0] * 6

    fini, pot, mises = tour_encheres(mains, mises, jetons, pot, middle[:3])
    if fini:
        fin([i for i in range(len(mains)) if mains[i] != "F"], pot)
        return

    pot += sum(mises)
    mises = [0] * 6

    fini, pot, mises = tour_encheres(mains, mises, jetons, pot, middle[:4])
    if fini:
        fin([i for i in range(len(mains)) if mains[i] != "F"], pot)
        return

    pot += sum(mises)
    mises = [0] * 6

    fini, pot, mises = tour_encheres(mains, mises, jetons, pot, middle[:5])
    if fini:
        fin([i for i in range(len(mains)) if mains[i] != "F"], pot)
        return

    pot += sum(mises)

    joueurs_actifs = [i for i in range(len(mains)) if mains[i] != "F"]
    mains_actives = [mains[i] for i in joueurs_actifs]

    gagnant = verification_gagnant(mains_actives, middle)
    fin([joueurs_actifs[mains_actives.index(gagnant[1])]], pot)


game()
