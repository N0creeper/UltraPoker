import random
import algorythme


def eval_preflop(main, position, mise_a_suivre, jetons, pot):
    def convertir(main):
        v1 = int(main[0][:2])
        v2 = int(main[1][:2])
        c1 = main[0][2]
        c2 = main[1][2]
        valeurs = {1: "A", 13: "K", 12: "Q", 11: "J", 10: "T", 9: "9", 8: "8", 7: "7", 6: "6", 5: "5", 4: "4", 3: "3", 2: "2"}
        l1, l2 = valeurs[v1], valeurs[v2]
        suited = (c1 == c2)
        if v1 == v2:
            return l1 + l2
        if v1 > v2:
            return l1 + l2 + ("s" if suited else "o")
        else:
            return l2 + l1 + ("s" if suited else "o")
    notation = convertir(main)
    RAISE = {
        "UTG": ["AA","KK","QQ","JJ","TT","99","88","77","AKs","AQs","AJs","ATs","AKo","AQo","KQs","KJs"],
        "MP": ["AA","KK","QQ","JJ","TT","99","88","77","66","AKs","AQs","AJs","ATs","A9s","A8s","AKo","AQo","AJo","ATo","KQs","KJs","KTs","QJs","QTs","JTs","T9s","98s"],
        "CO": ["AA","KK","QQ","JJ","TT","99","88","77","66","55","AKs","AQs","AJs","ATs","A9s","A8s","A7s","AKo","AQo","AJo","ATo","A9o","KQs","KJs","KTs","K9s","QJs","QTs","Q9s","JTs","J9s","T9s","98s","87s","76s","65s"],
        "BTN": ["AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s","AKo","AQo","AJo","ATo","A9o","A8o","A7o","KQs","KJs","KTs","K9s","K8s","QJs","QTs","Q9s","JTs","J9s","J8s","T9s","98s","87s","76s","65s","54s"],
        "SB": ["AA","KK","QQ","JJ","TT","99","88","77","66","55","AKs","AQs","AJs","ATs","A9s","A8s","A7s","AKo","AQo","AJo","ATo","KQs","KJs","KTs","QJs","QTs","JTs","T9s","98s","87s","76s"],
        "BB": ["AA","KK","QQ","JJ","TT","99","88","77","66","55","44","AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s","AKo","AQo","AJo","ATo","A9o","A8o","KQs","KJs","KTs","K9s","K8s","QJs","QTs","Q9s","JTs","J9s","J8s","T9s","98s","87s","76s","65s"]
    }
    CALL = {
        "UTG": ["AJs","ATs","A9s","KQs","KJs","QJs","JTs","T9s","99","88","77","66"],
        "MP": ["ATs","A9s","A8s","KQs","KJs","QJs","JTs","T9s","98s","77","66","55"],
        "CO": ["A9s","A8s","A7s","A6s","KTs","QTs","JTs","T9s","98s","87s","76s","65s","66","55","44"],
        "BTN": ["A8s","A7s","A6s","A5s","A4s","A3s","A2s","KTs","K9s","QTs","Q9s","JTs","J9s","T9s","98s","87s","76s","65s","54s","55","44","33","22"],
        "SB": ["A9s","A8s","A7s","A6s","KTs","QTs","JTs","T9s","98s","87s","76s","55","44","33","22"],
        "BB": ["A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s","KTs","QTs","JTs","T9s","98s","87s","76s","65s","54s","55","44","33","22"]
    }
    if notation in RAISE[position]:
        base_action = "raise"
    elif notation in CALL[position]:
        base_action = "call"
    else:
        base_action = "fold"
    SPR = jetons / max(1, pot)
    if SPR < 4:
        if base_action == "call":
            base_action = "raise"
    elif SPR > 20:
        if base_action == "raise" and notation in ["TT", "99", "88"]:
            base_action = "call"
    if mise_a_suivre > jetons * 0.75:
        return "fold"
    if mise_a_suivre == 0:
        if base_action == "raise":
            return "raise_small"
        if base_action == "call":
            return "call"
        return "fold"
    if base_action == "fold":
        if random.random() < 0.20:
            return "call"
        return "fold"
    if base_action == "call":
        if random.random() < 0.10:
            return "raise_small"
        return "call"
    if base_action == "raise":
        if mise_a_suivre < jetons * 0.15:
            return "raise_big"
        return "raise_small"
    return "fold"


def board_texture(board):
    valeurs = sorted(int(c[:2]) for c in board)
    couleurs = [c[2] for c in board]

    flush_count = max(couleurs.count(x) for x in set(couleurs))
    if flush_count >= 3:
        flush = "complete"
    elif flush_count == 2:
        flush = "possible"
    else:
        flush = "none"

    gaps = valeurs[-1] - valeurs[0]
    if gaps <= 4:
        straight = "wet"
    elif gaps <= 6:
        straight = "semi"
    else:
        straight = "dry"

    paired = len(valeurs) != len(set(valeurs))

    if paired:
        texture = "paired"
    elif flush == "complete" or straight == "wet":
        texture = "wet"
    elif flush == "possible" or straight == "semi":
        texture = "semi_dry"
    else:
        texture = "dry"

    return {"texture": texture, "flush": flush, "straight": straight, "paired": paired}


def relative_strength(main, board):
    analyse = algorythme.algorythme5c(main + board)
    comb = analyse["combinaison"]

    if analyse["straight_flush"]:
        return "nuts"
    if "carre" in comb or "full" in comb:
        return "nuts"
    if analyse["flush"] or analyse["straight"]:
        return "strong"
    if "brelan" in comb:
        return "strong"
    if "double paire" in comb:
        return "medium"
    if "paire" in comb:
        return "medium"
    return "air"


def compute_sizing(texture, spr):
    if spr < 3:
        return "all_in"
    if texture == "dry":
        return "small"
    if texture == "semi_dry":
        return "medium"
    if texture == "wet":
        return "big"
    if texture == "paired":
        return "small"
    return "small"


def postflop_action(main, board, jetons, mise_a_suivre, pot, position, nb_joueurs):
    texture = board_texture(board)
    strength = relative_strength(main, board)
    spr = jetons / max(1, pot)

    po = pot_odds(mise_a_suivre, pot)
    fe = fold_equity(mise_a_suivre, pot)
    bl = blockers(main, board)
    sb = semi_bluff_equity(main, board)

    if nb_joueurs > 2:
        if strength in ["air", "weak"]:
            return "f" if mise_a_suivre > 0 else "c"
        if strength == "medium":
            return "c"
        if strength == "strong":
            return "c" if mise_a_suivre > 0 else "bet_small"
        if strength == "nuts":
            return "bet_big"

    if strength == "air":
        if fe + bl > 0.6 and mise_a_suivre == 0:
            return "bet_small"
        return "f" if mise_a_suivre > 0 else "c"

    if strength == "weak":
        if po < 0.25:
            return "c"
        return "f"

    if strength == "medium":
        if mise_a_suivre == 0:
            return "bet_small"
        if mise_a_suivre <= pot * 0.3:
            return "c"
        return "f"

    if strength == "strong":
        if mise_a_suivre == 0:
            return "bet_medium"
        if sb > 0.5 or mise_a_suivre <= pot * 0.6:
            return "raise_small"
        return "c"
    if strength == "nuts":
        if mise_a_suivre == 0:
            return "bet_big"
        return "raise_big"

    return "c"


def pot_odds(mise_a_suivre, pot):
    if mise_a_suivre <= 0:
        return 0
    return mise_a_suivre / (pot + mise_a_suivre)


def fold_equity(mise, pot, agressivite=0.5):
    if mise <= 0:
        return 0
    return agressivite * (mise / (pot + mise))


def semi_bluff_equity(main, board):
    couleurs = [c[2] for c in main + board]
    valeurs = sorted(int(c[:2]) for c in main + board)

    flush_draw = max(couleurs.count(x) for x in set(couleurs)) == 4

    straight_draw = False
    for i in range(len(valeurs) - 3):
        if valeurs[i + 3] - valeurs[i] <= 4:
            straight_draw = True

    if flush_draw and straight_draw:
        return 1.0
    if flush_draw:
        return 0.7
    if straight_draw:
        return 0.5
    return 0


def blockers(main, board):
    valeurs = [int(c[:2]) for c in main]
    couleurs = [c[2] for c in main]

    board_couleurs = [c[2] for c in board]
    board_valeurs = [int(c[:2]) for c in board]

    score = 0

    for c in couleurs:
        if board_couleurs.count(c) >= 2:
            score += 0.3

    for v in valeurs:
        if any(abs(v - b) <= 1 for b in board_valeurs):
            score += 0.3

    if max(valeurs) >= max(board_valeurs):
        score += 0.2

    return min(score, 1)

def decision(main, board, jetons, mise_a_suivre, pot, position):
    if len(board) == 0:
        intention = eval_preflop(main, position, mise_a_suivre, jetons, pot)
        if intention == "fold":
            return "f"
        if intention == "call":
            return "c"
        if intention == "raise_small":
            base = mise_a_suivre if mise_a_suivre > 0 else 10
            montant = min(jetons, max(int(base * 2.5), base + 10))
            return montant
        if intention == "raise_big":
            base = mise_a_suivre if mise_a_suivre > 0 else 10
            montant = min(jetons, max(int(base * 3.5), base + 25))
            return montant
        return "c"
    nb_joueurs = 6
    action = postflop_action(main, board, jetons, mise_a_suivre, pot, position, nb_joueurs)
    if action == "f":
        return "f"
    if action == "c":
        return "c"
    if action == "bet_small":
        return min(jetons, max(1, pot // 3))
    if action == "bet_medium":
        return min(jetons, max(1, pot // 2))
    if action == "bet_big":
        return min(jetons, max(1, pot * 2 // 3))
    if action == "raise_small":
        return min(jetons, max(mise_a_suivre * 2, mise_a_suivre + 1))
    if action == "raise_big":
        return min(jetons, max(mise_a_suivre * 3, mise_a_suivre + 1))
    return "c"
