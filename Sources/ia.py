#Projet : UltraPoker
#Auteurs : Noam, Ancelin, Damian, Gabriel
import random
import algorythme

RANGES = {
    "OPEN": {
        "UTG": frozenset({
            "AA","KK","QQ","JJ","TT","99",
            "AKs","AQs","AJs","ATs",
            "A5s","A4s","A3s","A2s",
            "KQs","KJs",
            "QJs","JTs","T9s","98s","87s",
            "AKo","AQo"
        }),

        "MP": frozenset({
            "AA","KK","QQ","JJ","TT","99","88",
            "AKs","AQs","AJs","ATs","A9s",
            "A5s","A4s","A3s","A2s",
            "KQs","KJs","KTs",
            "QJs","QTs","JTs","T9s","98s","87s","76s",
            "AKo","AQo","AJo","KQo"
        }),

        "CO": frozenset({
            "AA","KK","QQ","JJ","TT","99","88","77",
            "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s",
            "A5s","A4s","A3s","A2s",
            "KQs","KJs","KTs","K9s",
            "QJs","QTs","Q9s",
            "JTs","J9s","T9s","98s","87s","76s","65s","54s",
            "AKo","AQo","AJo","ATo","KQo","KJo","QJo"
        }),

        "BTN": frozenset({
            "AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","22",
            "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
            "KQs","KJs","KTs","K9s","K8s","K7s","K6s","K5s","K4s","K3s","K2s",
            "QJs","QTs","Q9s","Q8s","Q7s","Q6s",
            "JTs","J9s","J8s","J7s",
            "T9s","T8s","T7s",
            "98s","97s","96s",
            "87s","86s","85s",
            "76s","75s","74s",
            "65s","64s","63s",
            "54s","53s","43s",
            "AKo","AQo","AJo","ATo","A9o","A8o","A7o","A6o","A5o","A4o","A3o","A2o",
            "KQo","KJo","KTo","K9o",
            "QJo","QTo","JTo"
        }),

        "SB": frozenset({
            "AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","22",
            "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
            "KQs","KJs","KTs","K9s","K8s","K7s","K6s","K5s","K4s","K3s","K2s",
            "QJs","QTs","Q9s","Q8s","Q7s","Q6s","Q5s","Q4s","Q3s","Q2s",
            "JTs","J9s","J8s","J7s","J6s",
            "T9s","T8s","T7s","T6s",
            "98s","97s","96s","95s",
            "87s","86s","85s","84s",
            "76s","75s","74s","73s",
            "65s","64s","63s","62s",
            "54s","53s","52s","43s","42s","32s",
            "AKo","AQo","AJo","ATo","A9o","A8o","A7o","A6o","A5o","A4o","A3o","A2o",
            "KQo","KJo","KTo","K9o","K8o","K7o","K6o","K5o","K4o","K3o","K2o",
            "QJo","QTo","Q9o","Q8o","Q7o",
            "JTo","J9o","J8o",
            "T9o","T8o",
            "98o","97o",
            "87o"
        })
    },
    "CALL":{
        "UTG": {
            "vs_MP": frozenset({"QQ","JJ","TT","99","AQs","AJs","KQs","AKo"}),
            "vs_CO": frozenset({"QQ","JJ","TT","99","AQs","AJs","ATs","KQs","AKo"}),
            "vs_BTN": frozenset({"QQ","JJ","TT","99","88","AQs","AJs","ATs","KQs","KJs","AKo","AQo"}),
            "vs_SB": frozenset({"QQ","JJ","TT","99","AQs","AJs","KQs","AKo"}),
            "vs_BB": frozenset({"QQ","JJ","TT","99","AQs","AJs","KQs","AKo"})
        },
        "MP": {
            "vs_CO": frozenset({"JJ","TT","99","88","AQs","AJs","ATs","KQs","AKo","AQo"}),
            "vs_BTN": frozenset({"JJ","TT","99","88","77","AQs","AJs","ATs","A9s","KQs","KJs","AKo","AQo","AJo"}),
            "vs_SB": frozenset({"JJ","TT","99","AQs","AJs","KQs","AKo"}),
            "vs_BB": frozenset({"JJ","TT","99","88","AQs","AJs","ATs","KQs","AKo","AQo"})
        },
        "CO": {
            "vs_BTN": frozenset({
                "TT","99","88","77",
                "AQs","AJs","ATs","A9s",
                "KQs","KJs","QJs",
                "AKo","AQo","AJo","KQo"
            }),
            "vs_SB": frozenset({
                "JJ","TT","99","88",
                "AQs","AJs","ATs",
                "KQs","KJs",
                "AKo","AQo"
            }),
            "vs_BB": frozenset({
                "JJ","TT","99","88","77",
                "AQs","AJs","ATs","A9s",
                "KQs","KJs","QJs",
                "AKo","AQo","AJo","KQo"
            })
        },
        "BTN": {
            "vs_SB": frozenset({
                "TT","99","88","77","66",
                "AQs","AJs","ATs","A9s","A8s",
                "KQs","KJs","KTs",
                "QJs","QTs",
                "JTs",
                "AKo","AQo","AJo","ATo","KQo","KJo","QJo"
            }),
            "vs_BB": frozenset({
                "TT","99","88","77","66",
                "AQs","AJs","ATs","A9s","A8s",
                "KQs","KJs","KTs",
                "QJs","QTs",
                "JTs",
                "AKo","AQo","AJo","ATo","KQo","KJo","QJo"
            })
        },
        "SB": {
            "vs_BB": frozenset({
                "JJ","TT","99","88","77",
                "AQs","AJs","ATs","A9s",
                "KQs","KJs",
                "QJs",
                "JTs",
                "AKo","AQo","AJo","KQo"
            })
        }
    },
    "BB_vs_OPEN":{
        "vs_UTG": frozenset({
            "AA","KK","QQ","JJ","TT","99","88","77","66",
            "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
            "KQs","KJs","KTs","K9s",
            "QJs","QTs",
            "JTs","J9s",
            "T9s","T8s",
            "98s","97s",
            "87s","86s",
            "76s","75s",
            "65s","64s",
            "54s","53s","43s",
            "AKo","AQo","AJo","ATo",
            "KQo"
        }),
        "vs_MP": frozenset({
            "AA","KK","QQ","JJ","TT","99","88","77","66","55",
            "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
            "KQs","KJs","KTs","K9s","K8s",
            "QJs","QTs","Q9s",
            "JTs","J9s","J8s",
            "T9s","T8s","T7s",
            "98s","97s","96s",
            "87s","86s","85s",
            "76s","75s","74s",
            "65s","64s","63s",
            "54s","53s","43s",
            "AKo","AQo","AJo","ATo","KQo","KJo","QJo"
        }),
        "vs_CO": frozenset({
            "AA","KK","QQ","JJ","TT","99","88","77","66","55","44",
            "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
            "KQs","KJs","KTs","K9s","K8s","K7s",
            "QJs","QTs","Q9s","Q8s",
            "JTs","J9s","J8s","J7s",
            "T9s","T8s","T7s","T6s",
            "98s","97s","96s","95s",
            "87s","86s","85s","84s",
            "76s","75s","74s","73s",
            "65s","64s","63s","62s",
            "54s","53s","52s","43s","42s","32s",
            "AKo","AQo","AJo","ATo","A9o","KQo","KJo","KTo","QJo","QTo","JTo"
        }),
        "vs_BTN": frozenset({
            "AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","22",
            "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
            "KQs","KJs","KTs","K9s","K8s","K7s","K6s","K5s","K4s","K3s","K2s",
            "QJs","QTs","Q9s","Q8s","Q7s","Q6s",
            "JTs","J9s","J8s","J7s","J6s",
            "T9s","T8s","T7s","T6s","T5s",
            "98s","97s","96s","95s","94s",
            "87s","86s","85s","84s","83s",
            "76s","75s","74s","73s","72s",
            "65s","64s","63s","62s",
            "54s","53s","52s","43s","42s","32s",
            "AKo","AQo","AJo","ATo","A9o","A8o","A7o","A6o","A5o","A4o","A3o","A2o",
            "KQo","KJo","KTo","K9o","K8o","K7o","K6o","K5o",
            "QJo","QTo","Q9o","Q8o",
            "JTo","J9o","J8o",
            "T9o","T8o",
            "98o","97o",
            "87o"
        }),
        "vs_SB": frozenset({
            "AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","22",
            "AKs","AQs","AJs","ATs","A9s","A8s","A7s","A6s","A5s","A4s","A3s","A2s",
            "KQs","KJs","KTs","K9s","K8s","K7s","K6s","K5s","K4s","K3s","K2s",
            "QJs","QTs","Q9s","Q8s","Q7s","Q6s","Q5s","Q4s","Q3s","Q2s",
            "JTs","J9s","J8s","J7s","J6s","J5s",
            "T9s","T8s","T7s","T6s","T5s","T4s",
            "98s","97s","96s","95s","94s",
            "87s","86s","85s","84s","83s",
            "76s","75s","74s","73s","72s",
            "65s","64s","63s","62s",
            "54s","53s","52s","43s","42s","32s",
            "AKo","AQo","AJo","ATo","A9o","A8o","A7o","A6o","A5o","A4o","A3o","A2o",
            "KQo","KJo","KTo","K9o","K8o","K7o","K6o","K5o","K4o",
            "QJo","QTo","Q9o","Q8o","Q7o",
            "JTo","J9o","J8o","J7o",
            "T9o","T8o","T7o",
            "98o","97o","96o",
            "87o","86o",
            "76o"
        })
    },
    "THREE_BET": {
        "UTG": {
            "vs_MP": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KQs"})
            },
            "vs_CO": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KQs","KJs"})
            },
            "vs_BTN": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KQs","KJs","QJs"})
            },
            "vs_SB": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KQs"})
            },
            "vs_BB": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KQs"})
            }
        },
        "MP": {
            "vs_UTG": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KQs"})
            },
            "vs_CO": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KJs","QJs"})
            },
            "vs_BTN": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KJs","QJs","JTs"})
            },
            "vs_SB": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KQs"})
            },
            "vs_BB": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KJs"})
            }
        },
        "CO": {
            "vs_UTG": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KQs"})
            },
            "vs_MP": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KJs","QJs"})
            },
            "vs_BTN": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","AKs","AQs","AJs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs","T9s"})
            },
            "vs_SB": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KJs","QJs"})
            },
            "vs_BB": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs"})
            }
        },
        "BTN": {
            "vs_UTG": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KQs"})
            },
            "vs_MP": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KJs","QJs"})
            },
            "vs_CO": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","AKs","AQs","AJs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs","T9s","98s"})
            },
            "vs_SB": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","AKs","AQs","AJs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs","T9s","98s","87s"})
            },
            "vs_BB": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","AKs","AQs","AJs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs","T9s","98s","87s"})
            }
        },
        "SB": {
            "vs_UTG": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s"})
            },
            "vs_MP": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KJs"})
            },
            "vs_CO": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","AKs","AQs","AJs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs"})
            },
            "vs_BTN": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","88","AKs","AQs","AJs","ATs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs","T9s","98s","87s"})
            },
            "vs_BB": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","88","AKs","AQs","AJs","ATs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs","T9s","98s","87s","76s"})
            }
        },
        "BB": {
            "vs_UTG": {
                "value": frozenset({"AA","KK","QQ","JJ","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s"})
            },
            "vs_MP": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","AKs","AQs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KJs"})
            },
            "vs_CO": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","AKs","AQs","AJs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs"})
            },
            "vs_BTN": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","88","AKs","AQs","AJs","ATs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs","T9s","98s","87s"})
            },
            "vs_SB": {
                "value": frozenset({"AA","KK","QQ","JJ","TT","99","88","AKs","AQs","AJs","ATs","AKo"}),
                "bluff": frozenset({"A5s","A4s","KTs","QTs","JTs","T9s","98s","87s","76s"})
            }
        }
    }
}


def convertir_notation(main):
    """
    Convertit une main en notation standard poker.
    
    Args:
        main (list): Deux cartes au format 'VVC'
    
    Returns:
        str: Notation standard (ex: 'AKs', 'JTo', 'AA')
    """
    v1 = int(main[0][:2])
    v2 = int(main[1][:2])
    c1 = main[0][2]
    c2 = main[1][2]

    valeurs = {
        1: "A",
        13: "K",
        12: "Q",
        11: "J",
        10: "T",
        9: "9",
        8: "8",
        7: "7",
        6: "6",
        5: "5",
        4: "4",
        3: "3",
        2: "2",
    }

    l1, l2 = valeurs[v1], valeurs[v2]

    suited = c1 == c2
    
    comp_v1 = 14 if v1 == 1 else v1
    comp_v2 = 14 if v2 == 1 else v2

    if v1 == v2:
        return l1 + l2
    if comp_v1 > comp_v2:
        return l1 + l2 + ("s" if suited else "o")
    return l2 + l1 + ("s" if suited else "o")


def eval_preflop(main, position, mise_a_suivre, jetons, pot):
    """
    Évalue une main preflop basée sur les ranges.
    
    Args:
        main (list): Deux cartes du joueur
        position (str): Position du joueur
        mise_a_suivre (int): Montant à suivre
        jetons (int): Jetons du joueur
        pot (int): Montant du pot
    
    Returns:
        str or int: "a" (fold), "s" (check/call), ou montant (raise)
    """

    notation = convertir_notation(main)

    if mise_a_suivre == 0 and position in RANGES["OPEN"]:
        if notation in RANGES["OPEN"][position]:
            return 25
        return "a"

    if position in RANGES["CALL"]:
        for vilain_pos in RANGES["CALL"][position]:
            if notation in RANGES["CALL"][position][vilain_pos]:
                if mise_a_suivre <= 0.25 * jetons:
                    return "s"
                return "a"

    if position == "BB":
        for vilain_pos in RANGES["BB_vs_OPEN"]:
            if notation in RANGES["BB_vs_OPEN"][vilain_pos]:
                if mise_a_suivre <= 0.20 * jetons:
                    return "s"
                return "a"

    if position in RANGES["THREE_BET"]:
        for vilain_pos in RANGES["THREE_BET"][position]:
            if notation in RANGES["THREE_BET"][position][vilain_pos]["value"]:
                return max(mise_a_suivre * 3, mise_a_suivre + 20)
            if notation in RANGES["THREE_BET"][position][vilain_pos]["bluff"]:
                return max(mise_a_suivre * 3, mise_a_suivre + 20)

    return "a"


def has_draw(main, board):
    """
    Vérifie si une main a un tirage couleur ou quinte.
    
    Args:
        main (list): Deux cartes du joueur
        board (list): Cartes communes
    
    Returns:
        bool: True si tirage présent, False sinon
    """
    couleurs = [c[2] for c in main + board]
    valeurs = sorted(int(c[:2]) for c in main + board)
    if couleurs and max(couleurs.count(x) for x in set(couleurs)) >= 4:
        return True
    if len(valeurs) >= 4:
        for i in range(len(valeurs) - 3):
            if valeurs[i + 3] - valeurs[i] <= 4:
                return True
    return False


def postflop_action(main, board, jetons, mise_a_suivre, pot, position, nb_joueurs):
    """
    Évalue la force de la main après le flop et détermine l'action à effectuer.
    
    Analyse la main actuelle contre le board pour détecter les tirages et classer
    la combinaison, puis retourne une action en fonction de la force estimée.
    
    Args:
        main (list): Les deux cartes du joueur au format ['VVCC', 'VVCC']
        board (list): Cartes communes du board au format ['VVCC', 'VVCC', ...]
        jetons (int): Taille de la pile de jetons du joueur
        mise_a_suivre (int): Mise courante à suivre (0 si aucune mise)
        pot (int): Montant total du pot
        position (str): Position du joueur ("UTG", "CO", "BTN", "SB", "BB", "SMALL_BLIND")
        nb_joueurs (int): Nombre de joueurs actifs dans la main
    
    Returns:
        str: Commande d'action - "raise_big", "raise_small", "bet_big", "bet_medium", "bet_small", "s" (suivre), "a" (coucher)
    """

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
        return "s" if mise_a_suivre <= pot * 0.25 else "a"
    if strength == "draw":
        return "s" if mise_a_suivre <= pot * 0.3 else "a"
    if strength == "weak":
        return "s" if mise_a_suivre <= pot * 0.15 else "a"
    if strength == "air":
        return "bet_small" if mise_a_suivre == 0 else "a"

    return "s"


def decision(main, board, jetons, mise_a_suivre, pot, position):
    """
    Fonction principale de décision qui route vers la stratégie appropriée.
    
    Oriente la prise de décision vers eval_preflop ou postflop_action selon l'état
    du board, puis convertit la commande d'action en montant de mise concret.
    
    Args:
        main (list): Les deux cartes du joueur au format ['VVCC', 'VVCC']
        board (list): Cartes communes (vide si préflop, 3 si flop, 4 si turn, 5 si river)
        jetons (int): Taille de la pile de jetons du joueur
        mise_a_suivre (int): Mise courante à suivre (0 si aucune mise)
        pot (int): Montant total du pot
        position (str): Position du joueur ("UTG", "CO", "BTN", "SB", "BB", "SMALL_BLIND")
    
    Returns:
        str or int: "a" (coucher), "s" (suivre/check), ou entier (montant de mise en jetons)
    """

    if len(board) == 0:
        action = eval_preflop(main, position, mise_a_suivre, jetons, pot)

        if action == "a":
            return "a"
        if action == "s":
            return "s"
        if isinstance(action, int):
            return min(jetons, max(action, mise_a_suivre + 1))
        return "s"

    action = postflop_action(main, board, jetons, mise_a_suivre, pot, position, 6)

    if action == "a":
        return "a"
    if action == "s":
        return "s"
    if action == "bet_big":
        return min(jetons, max(int(pot * 0.75), mise_a_suivre + 1))
    if action == "raise_big":
        return min(jetons, max(int(mise_a_suivre * 2.5), mise_a_suivre + 1))
    if action == "bet_medium":
        return min(jetons, max(int(pot * 0.5), mise_a_suivre + 1))
    if action == "raise_small":
        return min(jetons, max(int(mise_a_suivre * 1.5), mise_a_suivre + 1))
    if action == "bet_small":
        return min(jetons, max(int(pot * 0.25), mise_a_suivre + 1))
    return "s"