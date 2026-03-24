#Projet : UltraPoker
#Auteurs : Noam, Ancelin, Damian, Gabriel
import pygame
import os
import sys
import poker

pygame.init()

LARGEUR = 1000
HAUTEUR = 700
VERT_TABLE = (0, 120, 0)
BLANC = (255, 255, 255)
JAUNE = (255, 215, 0)

police = pygame.font.SysFont(None, 48)
police_menu = pygame.font.SysFont(None, 32)
police_small = pygame.font.SysFont(None, 24)

CARD_WIDTH = 70
CARD_HEIGHT = 105

police = pygame.font.SysFont(None, 24)
police_small = pygame.font.SysFont(None, 20)

images_cartes = {}

jetons_global = []
folded_global = []
showdown_mode = False
hand_strengths = {}

PLAYER_POS = {
    0: (120, 440),
    1: (120, 140),
    2: (430, 80),
    3: (740, 140),
    4: (740, 440),
    5: (430, 480),
}


def charger_images():
    """
    Charge les images des cartes depuis le dossier Assets.
    
    Args:
        None
    
    Returns:
        None (remplit le dictionnaire images_cartes)
    """
    dossier = os.path.join(os.path.dirname(__file__), "..", "Data", "Assets")
    for fichier in os.listdir(dossier):
        if fichier.endswith(".png"):
            nom = fichier.replace(".png", "")
            chemin = os.path.join(dossier, fichier)
            img = pygame.image.load(chemin).convert_alpha()
            img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
            images_cartes[nom] = img

    if "Dos" in images_cartes:
        images_cartes["dos"] = images_cartes["Dos"]
    
    try:
        table_game_path = os.path.join(dossier, "Table_game.png")
        images_cartes["table_game"] = pygame.image.load(table_game_path).convert()
        images_cartes["table_game"] = pygame.transform.scale(images_cartes["table_game"], (LARGEUR, HAUTEUR))
    except pygame.error:
        print("Erreur: Impossible de charger Table_game.png")
    
    try:
        table_menu_path = os.path.join(dossier, "Table_Menu.png")
        images_cartes["table_menu"] = pygame.image.load(table_menu_path).convert()
        images_cartes["table_menu"] = pygame.transform.scale(images_cartes["table_menu"], (LARGEUR, HAUTEUR))
    except pygame.error:
        print("Erreur: Impossible de charger Table_Menu.png")


def creer_fenetre():
    """
    Crée la fenêtre Pygame du jeu.
    
    Args:
        None
    
    Returns:
        pygame.Surface: La surface principale du jeu
    """
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Poker Texas Hold'em")
    charger_images()
    return ecran


def dessiner_table(ecran):
    """
    Dessine l'arrière-plan de la table de jeu.
    
    Args:
        ecran (pygame.Surface): Surface à remplir
    
    Returns:
        None
    """
    if "table_game" in images_cartes:
        ecran.blit(images_cartes["table_game"], (0, 0))
    else:
        ecran.fill(VERT_TABLE)


def dessiner_joueurs(ecran, jetons):
    """
    Affiche les informations de jetons pour chaque joueur actif.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        jetons (list): Jetons de chaque joueur
    
    Returns:
        None
    """
    for i in range(6):
        if jetons[i] <= 0:
            continue
        x, y = PLAYER_POS[i]
        txt = police.render(f"{poker.player_names[i]} : {jetons[i]} jetons", True, BLANC)
        ecran.blit(txt, (x, y - 28))


def afficher_carte(ecran, code, x, y):
    """
    Affiche l'image d'une carte à l'écran.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        code (str): Code de la carte (ex: "01C")
        x (int): Coordonnée X
        y (int): Coordonnée Y
    
    Returns:
        None
    """
    if code in images_cartes:
        ecran.blit(images_cartes[code], (x, y))


def afficher_main(ecran, main, x, y):
    """
    Affiche jusqu'à deux cartes d'une main.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        main (list): Liste des cartes
        x (int): Coordonnée X de départ
        y (int): Coordonnée Y de départ
    
    Returns:
        None
    """
    if len(main) >= 1:
        afficher_carte(ecran, main[0], x, y)
    if len(main) >= 2:
        afficher_carte(ecran, main[1], x + CARD_WIDTH + 8, y)


def afficher_main_joueur(ecran, main, joueur_id):
    """
    Affiche la main d'un joueur (cache les IA hors showdown).
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        main (list): 2 cartes du joueur
        joueur_id (int): Index du joueur
    
    Returns:
        None
    """
    if not jetons_global:
        return
    if jetons_global[joueur_id] <= 0:
        return

    x, y = PLAYER_POS[joueur_id]

    if showdown_mode:
        afficher_main(ecran, main, x, y)
        afficher_force_main(ecran, joueur_id)
        return

    if folded_global and folded_global[joueur_id]:
        return

    if joueur_id != 5:
        afficher_main(ecran, ["dos", "dos"], x, y)
    else:
        afficher_main(ecran, main, x, y)

    if joueur_id == 5:
        afficher_force_main(ecran, joueur_id)


def afficher_force_main(ecran, joueur_id):
    """
    Affiche la force de la main sous les cartes du joueur.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        joueur_id (int): Index du joueur
    
    Returns:
        None
    """
    if joueur_id not in hand_strengths:
        return

    x, y = PLAYER_POS[joueur_id]
    txt = police_small.render(hand_strengths[joueur_id], True, JAUNE)
    ecran.blit(txt, (x, y + CARD_HEIGHT + 5))


def afficher_board(ecran, board):
    """
    Affiche les cartes communes centrées à l'écran.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        board (list): Cartes communes
    
    Returns:
        None
    """
    start_x = LARGEUR // 2 - (len(board) * (CARD_WIDTH + 10)) // 2
    y = HAUTEUR // 2 - CARD_HEIGHT // 2 - 20
    for i, carte in enumerate(board):
        afficher_carte(ecran, carte, start_x + i * (CARD_WIDTH + 10), y)


def afficher_pot(ecran, montant):
    """
    Affiche le montant du pot au-dessus du board.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        montant (int): Montant du pot
    
    Returns:
        None
    """
    txt = police.render(f"Pot : {montant}", True, BLANC)
    x = LARGEUR // 2 - txt.get_width() // 2
    y = HAUTEUR // 2 - CARD_HEIGHT - 50
    ecran.blit(txt, (x, y))


def afficher_round(ecran, round_number):
    """
    Affiche le numéro du round en haut à droite.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        round_number (int): Numéro du round
    
    Returns:
        None
    """
    txt = police.render(f"Round : {round_number}", True, BLANC)
    ecran.blit(txt, (LARGEUR - txt.get_width() - 20, 20))


def afficher_mise_joueur(ecran, joueur_id, mise):
    """
    Affiche la mise courante d'un joueur.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        joueur_id (int): Index du joueur
        mise (int): Montant de la mise
    
    Returns:
        None
    """
    if mise <= 0:
        return
    if not jetons_global or jetons_global[joueur_id] <= 0:
        return

    x, y = PLAYER_POS[joueur_id]
    txt = police.render(str(mise), True, JAUNE)
    ecran.blit(txt, (x + CARD_WIDTH * 2 + 20, y + CARD_HEIGHT // 2 - 10))


def afficher_action_joueur(ecran, joueur_id, texte):
    """
    Affiche une action textuelle pour le joueur.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        joueur_id (int): Index du joueur
        texte (str): Action à afficher ("Fold", "Check", etc.)
    
    Returns:
        None
    """
    if not jetons_global or jetons_global[joueur_id] <= 0:
        return
    x, y = PLAYER_POS[joueur_id]
    zone = pygame.Rect(x - 10, y - 60, 230, 28)
    pygame.draw.rect(ecran, (0, 0, 0), zone)
    pygame.draw.rect(ecran, BLANC, zone, 1)
    txt = police.render(texte, True, BLANC)
    ecran.blit(txt, (x, y - 55))


def dessiner_boutons(ecran):
    """
    Dessine les boutons d'action pour le joueur humain.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
    
    Returns:
        dict: Dictionnaire des rectangles des boutons
    """
    y = PLAYER_POS[5][1] + CARD_HEIGHT + 15 + 25

    boutons = {
        "a": pygame.Rect(300, y, 140, 45),
        "s": pygame.Rect(460, y, 140, 45),
        "r": pygame.Rect(620, y, 140, 45),
        "lobby": pygame.Rect(50, 50, 150, 40),
    }

    pygame.draw.rect(ecran, (200, 50, 50), boutons["a"])
    pygame.draw.rect(ecran, (50, 200, 50), boutons["s"])
    pygame.draw.rect(ecran, (50, 50, 200), boutons["r"])
    pygame.draw.rect(ecran, (150, 150, 150), boutons["lobby"])

    ecran.blit(police.render("Abandonner", True, BLANC), (315, y + 12))
    ecran.blit(police.render("Suivre / Check", True, BLANC), (475, y + 12))
    ecran.blit(police.render("Relancer", True, BLANC), (645, y + 12))
    ecran.blit(police_small.render("Lobby", True, BLANC), (85, 60))

    return boutons


def demander_relance(ecran):
    """
    Demande au joueur de saisir un montant de relance.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
    
    Returns:
        int: Montant saisi par le joueur
    """
    montant = ""
    zone = pygame.Rect(350, 350, 300, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and montant and montant.isdigit():
                    return int(montant)
                elif event.key == pygame.K_BACKSPACE:
                    montant = montant[:-1]
                elif event.unicode.isdigit():
                    montant += event.unicode

        pygame.draw.rect(ecran, (0, 0, 0), zone)
        pygame.draw.rect(ecran, BLANC, zone, 2)
        txt = police.render("Montant : " + montant, True, BLANC)
        ecran.blit(txt, (360, 370))
        
        pygame.display.flip()


def attendre_action_joueur(boutons):
    """
    Attend une interaction souris sur les boutons d'action.
    
    Args:
        boutons (dict): Dictionnaire des rectangles des boutons
    
    Returns:
        str: Action choisie ("a", "s", "r", ou "lobby")
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if boutons["a"].collidepoint(x, y):
                    return "a"
                if boutons["s"].collidepoint(x, y):
                    return "s"
                if boutons["r"].collidepoint(x, y):
                    return "r"
                if boutons["lobby"].collidepoint(x, y):
                    return "lobby"


def rafraichir(ecran):
    """
    Rafraîchit l'affichage Pygame.
    
    Args:
        ecran (pygame.Surface): Surface à rafraîchissir
    
    Returns:
        None
    """
    pygame.display.flip()
