#Projet : UltraPoker
#Auteurs : Noam, Ancelin, Damian, Gabriel
from itertools import combinations


def cartes_to_listes(liste):
    """
    Sépare une liste de cartes en nombres et couleurs.
    
    Args:
        liste (list): Liste de cartes au format 'VVC'
    
    Returns:
        tuple: (nombres: list, couleurs: list)
    """
    clr = []
    nmbr = []
    for carte in liste:
        nmbr.append(int(carte[:2]))
        clr.append(carte[2])
    return nmbr, clr


def occurence(n):
    """
    Calcule l'occurrence de chaque nombre dans une liste.
    
    Args:
        n (list): Liste de nombres
    
    Returns:
        dict: Dictionnaire {valeur: count}
    """
    r = {}
    for i in n:
        if i in r:
            r[i] += 1
        else:
            r[i] = 1
    return r


def check_P_DP_B_F_C(o):
    """
    Vérifie présence de paires, double paires, brelans, fulls ou carrés.
    
    Args:
        o (dict): Dictionnaire d'occurrences
    
    Returns:
        dict: Dictionnaire avec combinaison trouvée
    """
    n2 = 0
    v2 = []
    n3 = 0
    v3 = []
    n4 = 0
    v4 = []
    for valeur, count in o.items():
        if count == 4:
            n4 += 1
            v4.append(valeur)
        if count == 3:
            n3 += 1
            v3.append(valeur)
        if count == 2:
            n2 += 1
            v2.append(valeur)
    if n4 == 1:
        return {"carre": v4}
    if n3 == 1:
        if n2 >= 1:
            return {"full": v3 + v2}
        else:
            return {"brelan": v3}
    if n2 == 1:
        return {"paire": v2}
    if n2 == 2:
        return {"double paire": v2}
    return {}


def check_flush(c):
    """
    Vérifie si les cartes forment une couleur.
    
    Args:
        c (list): Liste de couleurs
    
    Returns:
        bool: True si toutes les cartes ont la même couleur
    """
    temp = True
    for i in range(len(c)):
        if c[i] != c[0]:
            temp = False
    return temp


def check_straight(n):
    """
    Vérifie si les cartes forment une suite.
    
    Args:
        n (list): Liste de nombres
    
    Returns:
        tuple ou bool: (True, high_card) si suite, False sinon
    """
    temp = sorted(n)
    normal = True
    for i in range(len(temp) - 1):
        if temp[i] != temp[i + 1] - 1:
            normal = False
    if normal:
        return True, temp[-1]
    if 1 in temp:
        temp2 = temp.copy()
        temp2.remove(1)
        temp2.append(14)
        temp2 = sorted(temp2)
        high_ace = True
        for i in range(len(temp2) - 1):
            if temp2[i] != temp2[i + 1] - 1:
                high_ace = False
        if high_ace:
            return True, 14
    return False


def algorythme5c(carte):
    """
    Analyse une main de 5 cartes pour toutes les combinaisons.
    
    Args:
        carte (list): Liste de 5 cartes
    
    Returns:
        dict: Donne analysée avec combinaisons et caractéristiques
    """
    e = cartes_to_listes(carte)
    couleurs = e[1]
    nombres = e[0]
    occ = occurence(nombres)
    répété = check_P_DP_B_F_C(occ)
    flush = check_flush(couleurs)
    straight = check_straight(nombres)
    straight_flush = False
    if flush and straight:
        straight_flush = True
    high = max(nombres)
    if min(nombres) == 1:
        high = 1
    return {
        "combinaison": répété,
        "flush": flush,
        "straight": straight,
        "straight_flush": straight_flush,
        "high": high,
        "nombres": nombres,
    }


def score(car):
    """
    Calcule un score numérique pour une main de 5 cartes.
    
    Args:
        car (list): Liste de 5 cartes
    
    Returns:
        tuple: Score (rang, kickers) où rang 1-9
    """
    d = algorythme5c(car)
    comb = d["combinaison"]
    valeurs = sorted(d["nombres"], reverse=True)

    if d["straight_flush"]:
        return (9, d["high"])
    if "carre" in comb:
        v = comb["carre"][0]
        kickers = [x for x in valeurs if x != v]
        return (8, v, kickers[0])
    if "full" in comb:
        b = comb["full"][0]
        p = comb["full"][1]
        return (7, b, p)
    if d["flush"]:
        return (6, *valeurs)
    if d["straight"]:
        return (5, d["high"])
    if "brelan" in comb:
        v = comb["brelan"][0]
        kickers = [x for x in valeurs if x != v]
        return (4, v, kickers[0], kickers[1])
    if "double paire" in comb:
        p1, p2 = sorted(comb["double paire"], reverse=True)
        kicker = [x for x in valeurs if x != p1 and x != p2][0]
        return (3, p1, p2, kicker)
    if "paire" in comb:
        p = comb["paire"][0]
        kickers = [x for x in valeurs if x != p]
        return (2, p, *kickers)
    return (1, *valeurs)


def meilleure_main(cartes):
    """
    Détermine la meilleure main de 5 cartes possible.
    
    Args:
        cartes (list): Liste de 5 à 7 cartes
    
    Returns:
        tuple: Score de la meilleure main trouvée
    """
    if len(cartes) < 5:
        return (0,)
    
    best_score = None

    for combo in combinations(cartes, 5):
        s = score(list(combo))
        if best_score is None or s > best_score:
            best_score = s

    return best_score
