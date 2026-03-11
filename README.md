# 🎰 Poker Texas Hold'em

Un simulateur de poker Texas Hold'em en Python avec interface graphique Pygame. Jouez contre 5 adversaires IA avec une stratégie basée sur les ranges de poker professionnels.

## 📋 Caractéristiques

- ✅ **Jeu complet**: Préflop, Flop, Turn, River avec gestion complète des enchères
- ✅ **5 IA intelligentes**: Utilisant des ranges de poker GTO-inspirés
- ✅ **Interface graphique**: Affichage Pygame de la table, des cartes et des actions
- ✅ **Gestion avancée du pot**: Support des side-pots pour les situations all-in
- ✅ **Évaluation de mains**: Algorithme complet pour évaluer toutes les combinaisons de poker
- ✅ **Contrôle facile**: Interface intuitive pour relancer, suivre ou se coucher

## 🎯 Règles du Jeu

- **Joueurs**: 1 humain (position 5) + 5 IA
- **Stack initial**: 1000 jetons
- **Blinds**: 5/10 jetons (augmentent tous les 10 rounds)
- **Objectif**: Gagner le pot en ayant la meilleure main ou en forçant les autres à abandonner

### Combinaisons (du meilleur au pire)

1. Quinte Flush (5 cartes consécutives de même couleur)
2. Carré (4 cartes identiques)
3. Full (Brelan + Paire)
4. Couleur (5 cartes de même couleur)
5. Suite (5 cartes consécutives)
6. Brelan (3 cartes identiques)
7. Double Paire (2 paires)
8. Paire
9. Hauteur (carte la plus haute)

## 🚀 Démarrage

### Prérequis

- Python 3.13+
- Pygame 2.6.1+
- Linux, macOS ou Windows

### Installation

```bash
# Cloner ou télécharger le projet
cd Poker

# Installer les dépendances
pip install pygame
```

### Lancer le jeu

```bash
python poker.py
```

## 🎮 Comment Jouer

1. **Vous êtes Joueur 5** (en bas de l'écran)
2. Attendez votre tour d'action
3. **Boutons disponibles**:
   - **Fold (Se coucher)**: Abandonner la main actuelle
   - **Check/Call**: Suivre la mise actuelle ou checker si pas de mise
   - **Raise (Relancer)**: Augmenter la mise
4. Les IA joueront automatiquement après vous
5. Le gagnant reçoit le pot

## 📁 Structure du Projet

```
poker.py          → Boucle principale, gestion des enchères et du jeu
algorythme.py     → Évaluation des mains de poker
graphique.py      → Interface Pygame et rendu graphique
ia.py             → Stratégie et décisions des IA
README.md         → Ce fichier
Assets/           → Images des cartes (52 cartes + dos)
```

### Description des Modules

#### `poker.py`
- Gestion du jeu principal et des rounds
- Gestion du pot et des blinds
- Gestion des tours d'enchères (preflop, flop, turn, river)
- Showdown et distribution des gains

#### `algorythme.py`
- Évaluation des mains de poker (cotes 1-9)
- Détection des combinaisons (paires, brelans, suites, etc.)
- Détermination de la meilleure main possible

#### `graphique.py`
- Rendu de la table avec Pygame
- Affichage des cartes et positions des joueurs
- Interface utilisateur interactive avec boutons

#### `ia.py`
- Ranges preflop et postflop basés sur la stratégie GTO
- Évaluation des positions (UTG, MP, CO, BTN, SB, BB)
- Évaluation postflop basée sur la force de la main
- Gestion des tirages (flush draws, straight draws)

## 🧠 Stratégie IA

L'IA suit une stratégie inspirée par les meilleures pratiques du poker professionnel:

- **Preflop**: Joue selon les ranges établis pour chaque position
- **Postflop**: Ajuste sa stratégie selon:
  - La force de la main (nuts, strong, medium, weak, air)
  - La présence de tirages (flush ou quinte)
  - La taille du pot et les mises courantes

## 🐛 Gestion d'Erreurs

Le jeu gère correctement les situations critiques:
- Everyone fold → le pot va à la bonne personne
- All-in avec piles différentes → création automatique de side pots
- Évaluation des mains avec moins de 5 cartes → score minimal

## 📊 Format des Cartes

Les cartes utilisent la notation `VVCC`:
- **VV**: Valeur (01-13, où 01=As, 13=Roi)
- **CC**: Couleur (C=Cœur, D=Carreau, P=Pique, T=Trèfle)

Exemple: `01C` = As de Cœur, `12D` = Dame de Carreau

## 📝 Notation Poker

- **AA, KK, JJ**: Paires (ex: une paire d'As)
- **AKs**: Cartes hautes assorties (As-Roi même couleur)
- **JTo**: Cartes hautes non-assorties (Valet-10 couleurs différentes)

## ✨ Points d'Amélioration Possibles

- [ ] Sauvegarde de statistiques de jeu
- [ ] Difficulté réglable (ranges IA plus serées ou plus larges)
- [ ] Mode multijoueur en réseau
- [ ] Animation des cartes
- [ ] Historique des mains

## 📜 Licence

Projet scolaire - NSI 2026

## 🤝 Auteur

Créé pour le projet NSI 1eF 2026
