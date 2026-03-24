#Projet : UltraPoker
#Auteurs : Noam, Ancelin, Damian, Gabriel
import poker
import pygame
import sys
import os
import graphique

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.mixer.init()


LARGEUR = 1000
HAUTEUR = 700
BLEU_CLAIR = (100,255,255)
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT_TABLE = (0, 120, 0)

police = pygame.font.SysFont(None, 48)
police_menu = pygame.font.SysFont(None, 32)

pseudo = "Vous"
volume = 0.5

def afficher_menu(ecran):
    """
    Affiche le menu principal avec les boutons.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
    
    Returns:
        str: Action choisie ("jouer", "regles", "quitter")
    """
    if hasattr(graphique, 'images_cartes') and "table_menu" in graphique.images_cartes:
        ecran.blit(graphique.images_cartes["table_menu"], (0, 0))
    else:
        ecran.fill(VERT_TABLE)
    
    boutons = {
        "jouer": pygame.Rect(400, 200, 200, 60),
        "regles": pygame.Rect(400, 280, 200, 60),
        "parametres": pygame.Rect(400, 360, 200, 60),
        "quitter": pygame.Rect(400, 440, 200, 60),
    }

    titre = police.render("UltraPoker", True, BLANC)
    ecran.blit(titre, (LARGEUR//2 - titre.get_width()//2, 100))
    
    for action, rect in boutons.items():
        pygame.draw.rect(ecran, (100, 100, 100), rect)
        pygame.draw.rect(ecran, BLANC, rect, 2)
        
        if action == "jouer":
            texte = "Jouer"
        elif action == "regles":
            texte = "Règles"
        elif action == "parametres":
            texte = "Paramètres"
        elif action == "quitter":
            texte = "Quitter"
            
        txt_surface = police_menu.render(texte, True, BLANC)
        ecran.blit(txt_surface, (rect.centerx - txt_surface.get_width()//2, 
                               rect.centery - txt_surface.get_height()//2))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for action, rect in boutons.items():
                    if rect.collidepoint(x, y):
                        return action


def afficher_game_over(ecran):
    """
    Affiche l'écran de fin de partie quand le joueur n'a plus de jetons.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
    """
    while True:
        if hasattr(graphique, 'images_cartes') and "table_menu" in graphique.images_cartes:
            ecran.blit(graphique.images_cartes["table_menu"], (0, 0))
        else:
            ecran.fill(VERT_TABLE)
        
        game_over_text = police.render("Game Over", True, (255, 0, 0))
        ecran.blit(game_over_text, (LARGEUR//2 - game_over_text.get_width()//2, 200))
        
        message_text = police_menu.render("Vous n'avez plus de jetons !", True, BLANC)
        ecran.blit(message_text, (LARGEUR//2 - message_text.get_width()//2, 250))
        
        retour_text = police_menu.render("Appuyez sur une touche pour retourner au menu", True, BLANC)
        ecran.blit(retour_text, (LARGEUR//2 - retour_text.get_width()//2, 350))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return


def afficher_regles(ecran):
    """
    Affiche les règles du jeu.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
    """
    regles = [
        "RÈGLES DU TEXAS HOLD'EM",
        "",
        "    Le Texas Hold'em est la variante de poker la plus jouée au monde.",
        "Chaque joueur reçoit deux cartes privatives, qu'il est le seul à voir.",
        "Cinq cartes communes sont ensuite révélées progressivement au centre",
        "de la table : d'abord le flop (trois cartes), puis le turn (une carte)",
        "et enfin la river (une carte).",
        "L'objectif est de former la meilleure main possible de cinq cartes",
        "en combinant ses cartes privatives avec les cartes communes.",
        "    Avant chaque main, deux joueurs posent des mises obligatoires :",
        "la petite blind et la grosse blind.",
        "Après la distribution, un premier tour d'enchères commence.",
        "À chaque étape de révélation des cartes, un nouveau tour d'enchères",
        "a lieu, où les joueurs peuvent se coucher, suivre ou relancer.",
        "    Le coup se termine soit lorsqu'un seul joueur reste en lice,",
        "soit à l'abattage, où les mains sont comparées selon la hiérarchie",
        "classique : paire (2 cartes de même valeur), double paire (2 paires),",
        "brelan (3 cartes de même valeur), suite (5 cartes avec des nombres",
        "qui se suivent, ex: 2,3,4,5,6), couleur (avoir 5 cartes de même signe),",
        "full (avoir une paire et un brelan), carré (avoir les 4 cartes de même",
        "valeur), quinte flush (avoir une suite et une couleur), etc.",
        "",
        "Cliquez sur Retour ou appuyez sur une touche pour revenir au menu"
    ]
    
    while True:
        if hasattr(graphique, 'images_cartes') and "table_menu" in graphique.images_cartes:
            ecran.blit(graphique.images_cartes["table_menu"], (0, 0))
        else:
            ecran.fill(VERT_TABLE)
        
        y = 50
        for ligne in regles:
            if ligne == "RÈGLES DU POKER TEXAS HOLD'EM":
                txt = police.render(ligne, True, BLANC)
                shadow = police.render(ligne, True, NOIR)
            else:
                txt = police_menu.render(ligne, True, BLANC)
                shadow = police_menu.render(ligne, True, NOIR)
            ecran.blit(shadow, (51, y + 1))
            ecran.blit(txt, (50, y))
            y += 30
        
        bouton_retour = pygame.Rect(650, 25, 200, 60)
        pygame.draw.rect(ecran, (100, 100, 100), bouton_retour)
        pygame.draw.rect(ecran, BLANC, bouton_retour, 2)
        texte_retour = police_menu.render("Retour", True, BLANC)
        ecran.blit(texte_retour, (bouton_retour.centerx - texte_retour.get_width()//2, 
                                  bouton_retour.centery - texte_retour.get_height()//2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if bouton_retour.collidepoint(x, y):
                    return
            if event.type == pygame.KEYDOWN:
                return

def afficher_parametres(ecran):
    """
    Affiche le menu des paramètres.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
    """
    global pseudo, volume
    
    while True:
        if hasattr(graphique, 'images_cartes') and "table_menu" in graphique.images_cartes:
            ecran.blit(graphique.images_cartes["table_menu"], (0, 0))
        else:
            ecran.fill(VERT_TABLE)
        
        titre = police.render("Paramètres", True, BLANC)
        ecran.blit(titre, (LARGEUR//2 - titre.get_width()//2, 100))
        
        pseudo_txt = police_menu.render(f"Pseudo: {pseudo}", True, BLANC)
        ecran.blit(pseudo_txt, (200, 200))
        
        btn_pseudo = pygame.Rect(500, 190, 200, 50)
        pygame.draw.rect(ecran, (100, 100, 100), btn_pseudo)
        pygame.draw.rect(ecran, BLANC, btn_pseudo, 2)
        txt_p = police_menu.render("Changer", True, BLANC)
        ecran.blit(txt_p, (btn_pseudo.centerx - txt_p.get_width()//2, btn_pseudo.centery - txt_p.get_height()//2))
        
        vol_txt = police_menu.render(f"Volume: {int(volume * 100)}%", True, BLANC)
        ecran.blit(vol_txt, (200, 300))
        
        btn_vol_moins = pygame.Rect(500, 290, 50, 50)
        pygame.draw.rect(ecran, (100, 100, 100), btn_vol_moins)
        pygame.draw.rect(ecran, BLANC, btn_vol_moins, 2)
        ecran.blit(police_menu.render("-", True, BLANC), (btn_vol_moins.centerx - 10, btn_vol_moins.centery - 15))
        
        btn_vol_plus = pygame.Rect(560, 290, 50, 50)
        pygame.draw.rect(ecran, (100, 100, 100), btn_vol_plus)
        pygame.draw.rect(ecran, BLANC, btn_vol_plus, 2)
        ecran.blit(police_menu.render("+", True, BLANC), (btn_vol_plus.centerx - 10, btn_vol_plus.centery - 15))
        
        btn_retour = pygame.Rect(400, 500, 200, 60)
        pygame.draw.rect(ecran, (100, 100, 100), btn_retour)
        pygame.draw.rect(ecran, BLANC, btn_retour, 2)
        txt_r = police_menu.render("Retour", True, BLANC)
        ecran.blit(txt_r, (btn_retour.centerx - txt_r.get_width()//2, btn_retour.centery - txt_r.get_height()//2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if btn_pseudo.collidepoint(x, y):
                    nouveau_pseudo = demander_texte(ecran, "Nouveau pseudo:")
                    if nouveau_pseudo:
                        pseudo = nouveau_pseudo
                        poker.pseudo = pseudo
                elif btn_vol_moins.collidepoint(x, y):
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif btn_vol_plus.collidepoint(x, y):
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif btn_retour.collidepoint(x, y):
                    return
            if event.type == pygame.KEYDOWN:
                return

def demander_texte(ecran, prompt):
    """
    Demande à l'utilisateur de saisir du texte.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
        prompt (str): Texte d'invite
    
    Returns:
        str: Texte saisi
    """
    texte = ""
    zone = pygame.Rect(300, 300, 400, 60)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return texte
                elif event.key == pygame.K_BACKSPACE:
                    texte = texte[:-1]
                elif event.unicode.isalnum() or event.unicode in " -_":
                    texte += event.unicode
        
        pygame.draw.rect(ecran, (0, 0, 0), zone)
        pygame.draw.rect(ecran, BLANC, zone, 2)
        txt = police_menu.render(prompt + " " + texte, True, BLANC)
        ecran.blit(txt, (310, 320))
        pygame.display.flip()

def main():
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("UltraPoker")
    
    poker.initialiser_ecran(ecran)
    
    pygame.mixer.music.load(os.path.join("..", "Data", "Musics", "lobby.mp3"))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
    
    while True:
        action = afficher_menu(ecran)
        
        if action == "jouer":
            if poker.player_has_died:
                poker.jetons = [1000] * 6
                poker.player_has_died = False
                poker.round_number = 1
                poker.blind_multiplier = 1
                poker.player_names = [""] * 6
            
            pygame.mixer.music.stop()
            pygame.mixer.music.load(os.path.join("..", "Data", "Musics", "game.mp3"))
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            
            result = poker.Partie()
            
            pygame.mixer.music.stop()
            pygame.mixer.music.load(os.path.join("..", "Data", "Musics", "lobby.mp3"))
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            
            if result == "game_over":
                afficher_game_over(ecran)
        elif action == "regles":
            afficher_regles(ecran)
        elif action == "parametres":
            afficher_parametres(ecran)
        elif action == "quitter":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()