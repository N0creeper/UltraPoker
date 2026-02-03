import random
import algorythme

RANGES = {
    "UTG": {
        "OPEN": {
            "AA","KK","QQ","JJ","TT","99","88","77","66",
            "AKs","AQs","AJs","ATs","A9s","A8s",
            "AKo","AQo","AJo",
            "KQs","KJs",
            "QJs","JTs","T9s"
        },
        "CALL": {
            "55","44","33","22",
            "A7s","A6s","A5s",
            "KTs","QTs","J9s","98s"
        },
        "THREE_BET": {
            "AA","KK","QQ","JJ","TT","AKs","AQs","AKo"
        }
    },

    "MP": {
        "OPEN": {
            "AA","KK","QQ","JJ","TT","99","88","77","66","55",
            "AKs","AQs","AJs","ATs","A9s","A8s",
            "AKo","AQo","AJo","ATo",
            "KQs","KJs","KTs",
            "QJs","QTs",
            "JTs","T9s","98s"
        },
        "CALL": {
            "44","33","22",
            "A7s","A6s","A5s","A4s",
            "K9s","Q9s","J9s","T9s","98s"
        },
        "THREE_BET": {
            "AA","KK","QQ","JJ","TT","AKs","AQs","AKo","AQo"
        }
    },

    "CO": {
        "OPEN": {
            "22","33","44","55","66","77","88","99","TT","JJ","QQ","KK","AA",
            "A2s","A3s","A4s","A5s","A6s","A7s","A8s","A9s","ATs","AJs","AQs","AKs",
            "A2o","A3o","A4o","A5o","A6o","A7o","A8o","A9o","ATo","AJo","AQo","AKo",
            "K5s","K6s","K7s","K8s","K9s","KTs","KJs","KQs",
            "K9o","KTo","KJo","KQo",
            "Q8s","Q9s","QTs","QJs",
            "Q9o","QTo",
            "J8s","J9s","JTs",
            "J9o",
            "T8s","T9s",
            "T9o",
            "97s","98s",
            "86s","87s",
            "75s","76s",
            "64s","65s",
            "54s"
        },
        "CALL": {
            "A2s","A3s","A4s","A5s",
            "K8s","K7s",
            "Q8s","J8s",
            "T8o","98o","87o"
        },
        "THREE_BET": {
            "AA","KK","QQ","JJ","TT","AKs","AQs","AKo"
        }
    },

    "BTN": {
        "OPEN": {
            "22","33","44","55","66","77","88","99","TT","JJ","QQ","KK","AA",
            "A2s","A3s","A4s","A5s","A6s","A7s","A8s","A9s","ATs","AJs","AQs","AKs",
            "A2o","A3o","A4o","A5o","A6o","A7o","A8o","A9o","ATo","AJo","AQo","AKo",
            "K2s","K3s","K4s","K5s","K6s","K7s","K8s","K9s","KTs","KJs","KQs",
            "K7o","K8o","K9o","KTo",
            "Q4s","Q5s","Q6s","Q7s","Q8s","Q9s","QTs","QJs",
            "Q8o","Q9o","QTo",
            "J6s","J7s","J8s","J9s","JTs",
            "J8o","J9o",
            "T6s","T7s","T8s","T9s",
            "T8o","T9o",
            "96s","97s","98s","87s","86s","75s","64s","54s",
            "98o","87o"
        },
        "CALL": {
            "54s","64s","75s","86s","97s"
        },
        "THREE_BET": {
            "AA","KK","QQ","JJ","TT","AKs","AQs","AKo"
        }
    },

    "SB": {
        "OPEN": {
            "22","33","44","55","66","77","88","99","TT","JJ","QQ","KK","AA",
            "A2s","A3s","A4s","A5s","A6s","A7s","A8s","A9s","ATs","AJs","AQs","AKs",
            "A2o","A3o","A4o","A5o","A6o","A7o","A8o","A9o","ATo","AJo","AQo","AKo",
            "K2s","K3s","K4s","K5s","K6s","K7s","K8s","K9s","KTs","KJs","KQs",
            "K8o","K9o","KTo",
            "Q5s","Q6s","Q7s","Q8s","Q9s","QTs","QJs",
            "Q9o","QTo",
            "J7s","J8s","J9s","JTs",
            "T7s","T8s","T9s",
            "97s","98s",
            "86s","87s",
            "75s","76s",
            "64s","65s",
            "54s"
        },
        "CALL": {
            "A2s","A3s","A4s","A5s","54s","65s"
        },
        "THREE_BET": {
            "AA","KK","QQ","JJ","TT","AKs","AKo"
        }
    },

    "BB": {
        "OPEN": set(),
        "CALL": {
            "22","33","44","55","66","77",
            "A2s+","A2o+",
            "K2s+","K7o+",
            "Q4s+","Q8o+",
            "J6s+","J8o+",
            "T6s+","T8o+",
            "96s+","86s+","75s+","64s+","54s",
            "98o","87o"
        },
        "THREE_BET": {
            "AA","KK","QQ","JJ","TT","AKs","AKo"
        }
    }
}

def convertir_notation(main):
    v1 = int(main[0][:2])
    v2 = int(main[1][:2])
    c1 = main[0][2]
    c2 = main[1][2]

    valeurs = {
        1:"A",13:"K",12:"Q",11:"J",10:"T",
        9:"9",8:"8",7:"7",6:"6",5:"5",
        4:"4",3:"3",2:"2"
    }

    l1, l2 = valeurs[v1], valeurs[v2]
    suited = (c1 == c2)

    if v1 == v2:
        return l1 + l2
    if v1 > v2:
        return l1 + l2 + ("s" if suited else "o")
    return l2 + l1 + ("s" if suited else "o")

def eval_preflop(main, position, mise_a_suivre, jetons, pot):
    notation = convertir_notation(main)
    R = RANGES[position]
    if mise_a_suivre == 0 and position not in ["SB", "BB"]:

        if notation in R["OPEN"]:
            return 25 
        return "f"

    if notation in R["THREE_BET"]:
        return max(mise_a_suivre * 3, mise_a_suivre + 20)

    if notation in R["CALL"]:
        if mise_a_suivre <= 0.25 * jetons:
            return "c"
        return "f"

    if position == "BB" and mise_a_suivre <= 0.20 * jetons:
        return "c"

    return "f"

def has_draw(main, board):
    couleurs = [c[2] for c in main + board]
    valeurs = sorted(int(c[:2]) for c in main + board)
    if couleurs and max(couleurs.count(x) for x in set(couleurs)) >= 4:
        return True
    if len(valeurs) >= 4:
        for i in range(len(valeurs) - 3):
            if valeurs[i+3] - valeurs[i] <= 4:
                return True
    return False


def postflop_action(main, board, jetons, mise_a_suivre, pot, position, nb_joueurs):
    analyse = algorythme.algorythme5c(main + board)
    comb = analyse["combinaison"]

    if analyse.get("straight_flush"):
        strength = "nuts"
    elif "carre" in comb or "full" in comb:
        strength = "nuts"
    elif analyse.get("flush") or analyse.get("straight"):
        strength = "strong"
    elif "brelan" in comb:
        strength = "strong"
    elif "double paire" in comb:
        strength = "medium"
    elif "paire" in comb:
        board_vals = [int(c[:2]) for c in board]
        if board_vals and comb["paire"][0] == max(board_vals):
            strength = "medium"
        else:
            strength = "weak"
    else:
        strength = "draw" if has_draw(main, board) else "air"

    if strength == "nuts":
        return "raise_big" if mise_a_suivre else "bet_big"
    if strength == "strong":
        return "raise_small" if mise_a_suivre else "bet_medium"
    if strength == "medium":
        return "c" if mise_a_suivre <= pot * 0.25 else "f"
    if strength == "draw":
        return "c" if mise_a_suivre <= pot * 0.3 else "f"
    if strength == "weak":
        return "c" if mise_a_suivre <= pot * 0.15 else "f"
    if strength == "air":
        return "bet_small" if mise_a_suivre == 0 else "f"

    return "c"

def decision(main, board, jetons, mise_a_suivre, pot, position):
    if len(board) == 0:
        action = eval_preflop(main, position, mise_a_suivre, jetons, pot)

        if action == "f":
            return "f"
        if action == "c":
            return "c"
        if isinstance(action, int):
            return min(jetons, max(action, mise_a_suivre + 1))
        return "c"
    
    action = postflop_action(main, board, jetons, mise_a_suivre, pot, position, 6)

    if action == "f":
        return "f"
    if action == "c":
        return "c"
    if action == "bet_small":
        return min(jetons, pot // 3)
    if action == "bet_medium":
        return min(jetons, pot // 2)
    if action == "bet_big":
        return min(jetons, (pot * 2) // 3)
    if action == "raise_small":
        return min(jetons, mise_a_suivre * 2)
    if action == "raise_big":
        return min(jetons, mise_a_suivre * 3)

    return "c"
