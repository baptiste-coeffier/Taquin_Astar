# Résolution d'un taquin 8*8



# Description
Ce programme résout le jeu du taquin 8 (8-puzzle) en utilisant l'algorithme de recherche A*. Le but du jeu est de réarranger une grille de 3x3 pour qu'elle corresponde à l'état final ([0,1,2,3,4,5,6,7,8]) en déplaçant une case vide (représentée par 8).

Le programme utilise des heuristiques comme la distance de Manhattan et le nombre de Hamming pour calculer la qualité des solutions et optimiser la recherche.

# Fonctionnalités
A Algorithm* : Utilisation de la recherche A* pour trouver la solution optimale en explorant des états voisins.
Heuristiques :
Distance de Manhattan.
Hamming (nombre de cases mal placées).
Solvabilité : Vérifie si une configuration initiale est solvable.
Mélange Aléatoire : Génère des états initiaux aléatoires du taquin pour tester l'algorithme.
Traçage du chemin : Affiche le chemin de résolution du taquin, étape par étape.
Structure des classes et fonctions principales
Etat : Représente un état du taquin avec son plateau et ses attributs comme l'heuristique (g et f).
dist_elem(t) : Calcule la distance entre chaque case et sa position finale.
manathan(t, k) : Calcule l'heuristique de Manhattan pour un état donné.
hamming(t) : Calcule le nombre de cases mal placées.
valid(t) : Vérifie la solvabilité du taquin.
but(taq) : Vérifie si l'état actuel est l'état final.
graphSearch(etat_initial, k=6) : Algorithme A* pour explorer les états voisins et trouver la solution.
chemin(s) : Retrace et affiche le chemin complet de la résolution.
melange(length) : Mélange les cases du taquin de manière aléatoire.
Exécution
Le programme teste l'algorithme sur des configurations aléatoires du taquin sur un nombre d'itérations défini (it = 10000). Les métriques mesurées incluent :

Le nombre d'états non solvables.
La taille moyenne de la frontière et des états explorés.
Le temps total et moyen d'exécution.
La longueur moyenne des solutions.

# Résultats
À la fin de l'exécution, le programme affichera les résultats suivants :

Nombre d'états insolubles.
Nombre moyen d'états dans la frontière et explorés.
Temps moyen d'exécution.
Longueur moyenne des solutions.
