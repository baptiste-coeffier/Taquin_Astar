import random
from random import shuffle
import time

#===========================================#
#           definition de l'etat            #
#===========================================#
class Etat:
    def __init__(self, p):
        # configuration du plateau 
        self.pl = []
        # structure de l'arbre 
        self.parent = p
        self.chemin = "_"
        
        # valeur de l'heuristique g(.)
        self.g = 0
        # pour la file de priorite 
        self.f = 0

    def config(self, tab):
        self.pl = tab
        
    def get_parent(self):
        return self.parent

    def copy(self):
        copy = Etat(self.parent)
        copy.pl = self.pl[:]
        copy.parent = self.parent
        copy.chemin = self.chemin 
        copy.g = self.g
        copy.f = self.f
        return copy

#===========================================#
#           variables globales              #
#===========================================#

etat_initial = Etat(None) 
etat_initial.config([8,7,6,5,4,3,2,1,0])  #exemple

frontiere = []
explorer = []


# tab heuristique 
poids =[[36, 12, 12, 4, 1, 1, 4, 1, 0],
        [8, 7, 6, 5, 4, 3, 2, 1, 0],
        [8, 7, 6, 5, 4, 3, 2, 1, 0],
        [8, 7, 6, 5, 3, 2, 4, 1, 0],
        [8, 7, 6, 5, 3, 2, 4, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0]]

ro = [4, 1, 4, 1, 4, 1]

#===========================#
#       calcul de h(.)      #
#===========================#
def dist_elem(t):
    prout =[]
    # pour chaque case du taquin on va calculer a combien de case elle est de sa position finale 
    # puis la mettre dans un tableau que l'on va donner a manathan
    for k in range(len(t.pl)):
        l = t.pl.index(k) 
        prout.append(abs((k//3)-(l//3))+abs((k%3)-(l%3)))
    return prout

#fonction calculant la distance de manathan
def manathan(t, k):
    # on recupere la distance de chaque case par rapport a sa position finale
    elem = dist_elem(t)
    # variable de la somme
    lesExperts = 0
    for i in range(len(elem)) :
        #on va faire la somme de la distance de manathan en fonction de K qui defini l'heuristique du tableau de poids
        lesExperts += (poids[k-1][i] * elem[i]) 
    return lesExperts // ro[k-1]

def hamming(t):
    etat_final = [0,1,2,3,4,5,6,7,8]
    # His name is...
    johnCena = 0
    # tutututuuuuu tutututuuuuu 
    
    # pour chaque case du taquin on va faire la somme de si elle est a sa place sa valeur vaut 0 et 1 sinon
    for i in range(len(t.pl)):
        if t.pl[i] != etat_final[i]: johnCena += 1
    return johnCena

# definition de la fonction qui verifie la solvabilite du taquin initial
def valid(t): 
    taq =t.copy()
    n=0
    k = t.pl.index(8)
    v = 0
    if k==0:
        v=4
    elif k==1 or k==3:
        v=3
    elif k==2 or k==6 or k==4:
        v=2
    elif k==5 or k==7:
        v=1
    else:
        v=0
    for i in range(len(taq.pl)):
        temp = taq.pl.index(i)
        if i != temp :
            taq.pl[i], taq.pl[temp] = taq.pl[temp], taq.pl[i]
            n+=1
        
    if ((n%2) == 0 and (v%2) ==1) or ((n%2) == 1 and (v%2) ==0):
        t.chemin = t.chemin + "le taquin est insoluble"
        return False
    return True
    
# verifie si on est arriver a l'etat du but
def but(taq):
    for i in range(len(taq.pl)) :
        # le taquin final est une liste trier, 
        # donc il faut que l'indice du tableau corresponde a la valeur de sa case
        if not(i == taq.pl[i]) : 
            return 0 
    return 1


# definition de la fonction pour ajouter dans la frontiere 
def insertion(t):
    # pour inserer on va regarder chaque case de la frontiere
    # comparer le f de la frontiere avec le f de l'action 
    # jusqu'a obtenir un f plus grand dans la frontiere et on l'inserera a ce moment la 
    if len(frontiere)==0:
        frontiere.append(t)
    elif len(frontiere)==1:
        tesla = frontiere[0].f 
        if t.f < tesla:
            frontiere.insert(0, t)
        else:
            frontiere.insert(1, t)
        
        
    for i in range(len(frontiere)):
        thisIsElonMusk = frontiere[i].f 
        if i==0:
            if t.f < thisIsElonMusk:
                frontiere.insert(i, t)
                break

        elif i!= len(frontiere)-1: 
            if t.f < thisIsElonMusk or t.f == thisIsElonMusk:
                frontiere.insert(i, t)
                break
        else: 
            frontiere.insert(i+1, t)

# fonction qui regarde si il n'y a pas deja un même etat dans explorer
def doublon(t):
    for i in range(len(explorer)):
        #si le plateau courat est egale a un plateau deja expanser alors on ne le gradera pas 
        if t.pl == explorer[i].pl :
            return True
    return False

# fonction qui va definir les mouvements de la tuile 
def moveP(t) :
    k = t.pl.index(8)
    move = []
    # disjonction des cas en fonction de la place de la case vide
    # on notes les actions possibles sous forme de caracteres
    if   k == 0 : move.extend(["S", "E"])
    elif k == 1 : move.extend(["S", "E", "O"])
    elif k == 2 : move.extend(["S", "O"])
    elif k == 3 : move.extend(["N", "S", "E"])
    elif k == 4 : move.extend(["N", "S", "E", "O"])
    elif k == 5 : move.extend(["N", "S", "O"])
    elif k == 6 : move.extend(["N", "E"])
    elif k == 7 : move.extend(["N", "E", "O"])
    elif k == 8 : move.extend(["N", "O"])
    return move

# fonction qui va creer les nouveaux taquins possibles
def expansion(t, m):
    expanser = []
    k = t.pl.index(8)
    # en fonction du tableau m des actions possibles, 
    # on va creer tous autant de nouveau taquin qui auront le taquin courant en pere 
    while m!=[]:
        taq = t.copy()
        if m[0] == "N" :
            taq.pl[k-3], taq.pl[k] = taq.pl[k], taq.pl[k-3]
        elif m[0] == "S": 
            taq.pl[k+3], taq.pl[k] = taq.pl[k], taq.pl[k+3]
        elif m[0] == "E" :
            taq.pl[k+1], taq.pl[k] = taq.pl[k], taq.pl[k+1]
        elif m[0] == "O" :
            taq.pl[k-1], taq.pl[k] = taq.pl[k], taq.pl[k-1]
        taq.parent = t 
        taq.g = t.g+1
        expanser.append(taq)
        taq.chemin += m.pop(0)
    return expanser

# fonction pour melanger le taquin
def melange(length):
    tab = Etat(None)
    tab.config([0,1,2,3,4,5,6,7,8])
    choice = ['N','S','E','O']
    # boucle qui va melanger
    for i in range(length):
        # on choisit une action possible
        action = random.choice(choice)
        k = tab.pl.index(8)
        #on deplace la case vide en fonction de l'action quand cela est possible
        if action == 'N' and k-3>0:
            tab.pl[k-3], tab.pl[k] = tab.pl[k], tab.pl[k-3]
        elif action == "S" and k+3<len(tab.pl): 
            tab.pl[k+3], tab.pl[k] = tab.pl[k], tab.pl[k+3]
        elif action == "E" and k+1<len(tab.pl):
            tab.pl[k+1], tab.pl[k] = tab.pl[k], tab.pl[k+1]
        elif action == "O" and k-1>0:
            tab.pl[k-1], tab.pl[k] = tab.pl[k], tab.pl[k-1]
    # retourne un taquin qui a subi un melange aleatoire
    return tab
    
#===============================#
#               A*              #
#===============================#
def graphSearch (etat_initial, k =6):
    
    doc = time.time()
    frontiere.append(etat_initial)
    
    #on verifie si on a besoin de rentrer dans la boucle de recherche
    if not(valid(frontiere[0])):
        marty = time.time() - doc
        #print(marty)
        return []
    
    #========================================================#
    #                   Boucle de recherche                  #
    #========================================================# 

    while len(frontiere) != 0:
        
        #on verifie si on est arrive a la l'etat du but
        if but(frontiere[0]) :
            marty = time.time() - doc
            #print(marty)
            return frontiere[0]
        
        # on enleve e la frontiere la premiere valeur que l'on mets dans explorer et dans une variable temporaire
        test = frontiere.pop(0)
        explorer.append(test)
        
        
        # on recupere les etats expanser du taquin actuel
        expanser = expansion(test, moveP(test))
        # pour chaque nouvels etats on va regarder s'il n'a pas deja ete expanser
        for i in range(len(expanser)):
            if not doublon(expanser[i]):
                # si c'est un nouvel etat alors on calcul son f et on l'insere a la bonne place dans la frontiere
                
                expanser[i].f = expanser[i].g + manathan(expanser[i], k)
                #expanser[i].f = expanser[i].g + hamming(test)
                insertion(expanser[i])
        if doc < 1800:
            print("on est au dessus de 30min, je m'arrête")
            return frontiere[0]


# definition de la fonction retraçant le chemin 
def chemin(s):
    deplacement = s.g
    
    Phrase = f""
    Parent = s.get_parent()
    while Parent != None: 
        Phrase = f"{deplacement}.\n _ _ _ \n|{s.pl[0]}|{s.pl[1]}|{s.pl[2]}|\n _ _ _ \n|{s.pl[3]}|{s.pl[4]}|{s.pl[5]}|\n _ _ _ \n|{s.pl[6]}|{s.pl[7]}|{s.pl[8]}|\n _ _ _ \n" + Phrase
        s = Parent
        Parent = s.get_parent()
        deplacement = deplacement -1
    if Parent == None: 
        debut = f"0. \n _ _ _ \n|{s.pl[0]}|{s.pl[1]}|{s.pl[2]}|\n _ _ _ \n|{s.pl[3]}|{s.pl[4]}|{s.pl[5]}|\n _ _ _ \n|{s.pl[6]}|{s.pl[7]}|{s.pl[8]}|\n _ _ _ \n "
        print(debut)
    print(Phrase)
    
    
def test ():
    s = graphSearch(etat_initial, 6 )
    print("le nombre de coup qui a ete joue :",s.g)
    print("le chemin de la case vide depuis l'etat initial :",s.chemin)
    print("c'est la taille de explorer :", len(explorer))
    print("c'est la taille de la frontiere :", len(frontiere))

    chemin(s)

test()

it = 10000
m=0
nbF = nbE = tmptot = longG = 0 
for i in range(it):
    deb = time.time()
    #etat_initial = melange(100))
    shuffle(etat_initial.pl)
    s = graphSearch(etat_initial, 2)
    end = time.time() - deb
    if s == []:
        m+=1
    else :
        nbF = (nbF + len(frontiere))/2
        nbE =+ (nbE + len(explorer))/2
        longG = (longG + s.g)
    tmptot += end
    frontiere=[]
    explorer=[]


print("nombre d'état invalide :",m)
print("nombre moyen d'état dans la frontière :",nbF)
print("nombre moyen d'état dans l'explorer :",nbE)
print("Temps total d'éxécution",tmptot)
print("Temps moyen d'éxécution :", tmptot/abs(it-m))
print("longueur moyen de la solution :",longG/abs(it-m))