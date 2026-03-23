#Projet : UltraPoker
#Auteurs : Noam, Ancelin, Damian, Gabriel
import poker
import pygame
import sys
import os
import graphique

# Changer le répertoire de travail vers le répertoire du script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

pygame.init()

LARGEUR = 1000
HAUTEUR = 700

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT_TABLE = (0, 120, 0)

police = pygame.font.SysFont(None, 48)
police_menu = pygame.font.SysFont(None, 36)

def afficher_menu(ecran):
    """
    Affiche le menu principal avec les boutons.
    
    Args:
        ecran (pygame.Surface): Surface de jeu
    
    Returns:
        str: Action choisie ("jouer", "regles", "quitter")
    """
    # Dessiner l'arrière-plan du menu
    if hasattr(graphique, 'images_cartes') and "table_menu" in graphique.images_cartes:
        ecran.blit(graphique.images_cartes["table_menu"], (0, 0))
    else:
        ecran.fill(VERT_TABLE)
    
    boutons = {
        "jouer": pygame.Rect(400, 250, 200, 60),
        "regles": pygame.Rect(400, 350, 200, 60),
        "quitter": pygame.Rect(400, 450, 200, 60),
    }

    # Titre
    titre = police.render("UltraPoker", True, BLANC)
    ecran.blit(titre, (LARGEUR//2 - titre.get_width()//2, 100))
    
    # Boutons
    for action, rect in boutons.items():
        pygame.draw.rect(ecran, (100, 100, 100), rect)
        pygame.draw.rect(ecran, BLANC, rect, 2)
        
        if action == "jouer":
            texte = "Jouer"
        elif action == "regles":
            texte = "Règles"
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
        # Dessiner l'arrière-plan du menu
        if hasattr(graphique, 'images_cartes') and "table_menu" in graphique.images_cartes:
            ecran.blit(graphique.images_cartes["table_menu"], (0, 0))
        else:
            ecran.fill(VERT_TABLE)
        
        # Message de défaite
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
        "RÈGLES DU POKER TEXAS HOLD'EM",
        "",
        "Objectif: Avoir la meilleure main de 5 cartes.",
        "",
        "Déroulement:",
        "1. Distribution de 2 cartes privées (hole cards)",
        "2. Enchères pré-flop",
        "3. Flop: 3 cartes communes révélées",
        "4. Enchères",
        "5. Turn: 1 carte commune révélée",
        "6. Enchères",
        "7. River: 1 carte commune révélée",
        "8. Enchères finales",
        "9. Showdown: révélation des mains",
        "",
        "Combinaisons (du plus fort au plus faible):",
        "- Quinte Flush Royale",
        "- Quinte Flush",
        "- Carré",
        "- Full House",
        "- Couleur",
        "- Suite",
        "- Brelan",
        "- Double Paire",
        "- Paire",
        "- Carte Haute",
        "",
        "Appuyez sur une touche pour revenir au menu"
    ]
    
    while True:
        # Dessiner l'arrière-plan du menu
        if hasattr(graphique, 'images_cartes') and "table_menu" in graphique.images_cartes:
            ecran.blit(graphique.images_cartes["table_menu"], (0, 0))
        else:
            ecran.fill(VERT_TABLE)
        
        y = 50
        for ligne in regles:
            if ligne == "RÈGLES DU POKER TEXAS HOLD'EM":
                txt = police.render(ligne, True, BLANC)
            else:
                txt = police_menu.render(ligne, True, BLANC)
            ecran.blit(txt, (50, y))
            y += 30
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def main():
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("UltraPoker")
    
    poker.initialiser_ecran(ecran)
    
    while True:
        action = afficher_menu(ecran)
        
        if action == "jouer":
            result = poker.Partie()
            if result == "game_over":
                # Afficher un message de défaite
                afficher_game_over(ecran)
        elif action == "regles":
            afficher_regles(ecran)
        elif action == "quitter":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()