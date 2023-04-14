# coding : utf-8

"""JEU D'ECHECS, programme serveur
La communauté de la truelle, mai 2022."""

import random
from constant import *
import serveur



cases_possibles = []
cases_precalculees = [] 
case_selection = None #il s'agit de l'index de la case sélectionnée dans le tableau cases
piece_selection = False
new_case = None #à mettre dans la fonction quand on valide un coup
echec = False
p_roque = False
g_roque = False
deja_roque = p_roque and g_roque
utilisateur_a_quitte = False
case_piece_demandee = None

#tour de jeu et couleur des joueurs
tour_de_jeu = 'blanc'
couleur_joueur1 = random.choice(['blanc', 'noir'])
couleur_joueur2 = "blanc" if couleur_joueur1 == "noir" else "noir"
tourJ = 0



########-------fonctions utilisées pour le déroulement du jeu-------########

def aquiletour():
    """Cette fonction permet de savoir qui est le tour de jeu"""
    global tourJ, tour_de_jeu
    if tourJ % 2 == 0 and tour_de_jeu == 'noir':
        tour_de_jeu = 'blanc'
    elif tourJ % 2 != 0 and tour_de_jeu == 'blanc':
        tour_de_jeu = 'noir'


def selection_case(x : int, y : int):
    """Cette fonction permet de gérer les cliques des joueurs"""
    global piece_selection, cases_possibles, case_selection, deja_roque, p_roque, g_roque, case_piece_demandee
    deja_roque = p_roque and g_roque
    for i in range(len(cases)): #on parcourt le tableau de cases
        if i == y*8+x: #si la case cliquée correspond à une case du tableau
            case_clique = i #on récupère l'index de la case cliquée

    if piece_selection == True and cases[case_selection][0] == (roi_blanc if couleur_joueur1 == "blanc" else roi_noir) and cases[case_clique][0] == (tour_blanc if couleur_joueur1 == "blanc" else tour_noir) and deja_roque == False: #si la pièce sélectionnée est un roi et que le joueur clique sur une tour (roque)
        if ((cases[case_clique][2] == 63) if couleur_joueur1 == "blanc" else cases[case_clique][2] == 56) and p_roque == False:  #si le joueur clique sur la tour de droite
            if ((cases[61][0] == "vide" and cases[62][0] == "vide") if couleur_joueur1 == "blanc" else (cases[57][0] == "vide" and cases[58][0] == "vide")):
                petit_roque(couleur_joueur1)
                serveur.envoie("petit_roque")
        elif ((cases[case_clique][2] == 56) if couleur_joueur1 == "blanc" else cases[case_clique][2] == 63) and g_roque == False: #si le joueur clique sur la tour de gauche
            if ((cases[57][0] == "vide" and cases[57][0] == "vide" and cases[58][0] == "vide") if couleur_joueur1 == "blanc" else (cases[60][0] == "vide" and cases[61][0] == "vide" and cases[62][0] == "vide")):
                grand_roque(couleur_joueur1)
                serveur.envoie("grand_roque")
    
    elif cases[case_clique][1] == "blanc" and tour_de_jeu == "blanc" and couleur_joueur1 == "blanc": #si la piece est blanche et que c'est le tour des blancs
        piece_selection = True #la sélection d'une pièce est vraie
        cases_possibles = [] #on vide la liste des cases possibles pour ne pas avoir de problèmes avec les cases possibles d'autres pièces
        case_selection = case_clique #permet de garder en mémoire la case de la pièce sélectionnée 
        deplacement_possible(case_clique)

    elif cases[case_clique][1] == "noir" and tour_de_jeu == "noir" and couleur_joueur1 == "noir": #si la piece est noire et que c'est le tour des noirs
        piece_selection = True #la sélection d'une pièce est vraie
        cases_possibles = [] #on vide la liste des cases possibles pour ne pas avoir de problèmes avec les cases possibles d'autres pièces
        case_selection = case_clique #permet de garder en mémoire la case de la pièce sélectionnée 
        deplacement_possible(case_clique)

    elif cases[case_clique] in cases_possibles and piece_selection == True: #si la case est dans la liste des cases possibles et que la sélection d'une pièce est vraie (donc qu'on clique sur une case pour jouer)+
        joue(case_clique) #permet de déplacer la pièce sélectionnée à la case case_clique choisi par le joueur
        if echec == True: #si le roi est en échec
            serveur.envoie(str(case_selection)+","+str(case_clique)+","+"echec") #on envoie à l'autre joueur le déplacment effectué ainsi que le roi est en échec
            case_selection = None #on remet la case sélectionnée à "aucune"
        elif echec == False: #si le roi n'est pas en échec
            if cases[case_clique][0] == (pion_blanc if couleur_joueur1 == "blanc" else pion_noir) and case_clique // 8 == 0: #si le pion a atteint la ligne 1
                case_piece_demandee = case_clique #on garde en mémoire la case ou le joueur doit choisir une piece
            else:
                if cases[case_clique][0] == roi_noir or cases[case_clique][0] == roi_blanc:
                    p_roque = True
                    g_roque = True
                serveur.envoie(str(case_selection)+","+str(case_clique)) #on envoie à l'autre joueur le déplacment effectué
                case_selection = None #on remet la case sélectionnée à "aucune"
    else: #si la case n'est pas dans la liste des cases possibles ni une pièce que l'on peut déplacer
        piece_selection = False #la sélection d'une pièce est fausse
        case_selection = None #on remet la case sélectionnée à "aucune"
        cases_possibles = [] #on vide la liste des cases possibles pour ne pas avoir de problèmes avec les cases possibles d'autres pièces


def joue(case_clique):
    """Cette fonction permet de déplacer une pièce"""
    global new_case, cases_possibles, piece_selection, case_selection, tourJ
    #cases[case_selection][0], cases[case_clique][0] = cases[case_clique][0], cases[case_selection][0]
    #cases[case_selection][1], cases[case_clique][1] = cases[case_clique][1], cases[case_selection][1]
    cases[case_clique][0] = cases[case_selection][0]
    cases[case_clique][1] = cases[case_selection][1]
    cases[case_selection][0] = "vide"
    cases[case_selection][1] = ""
    
    new_case = case_clique #permet de garder en mémoire la case de la pièce déplacée
    cases_possibles = [] #on vide la liste des cases possibles car on a déplacé une pièce
    piece_selection = False #on désélectionne la pièce sélectionnée
    tourJ += 1
    aquiletour()
    #fnc_echec()
    



def deplacement_possible(case_select : int):
    """Cette fonction permet, de la case mise en paramètre, de connaitre la pièce qui lui est associée, et ainsi de connaitre les cases où elle peut aller"""
    global cases_possibles
    cases_possibles = [] #on vide la liste des cases possibles pour ne pas avoir de problèmes avec les cases possibles d'autres pièces
    piece = cases[case_select][0] #on récupère la pièce qui est sur la case

    if piece == (pion_blanc if couleur_joueur1 == "blanc" else pion_noir): #si c'est un pion
        pion(case_select, "joueur") #on appelle la fonction pion

    elif piece == (tour_blanc if couleur_joueur1 == "blanc" else tour_noir): #si c'est une tour
        #Deplacement haut
        deplacement_direction(case_select, 0, -1, "joueur")#on appelle la fonction deplacement_direction
        #Deplacement bas
        deplacement_direction(case_select, 0, 1, "joueur")  #on appelle la fonction deplacement_direction
        #Deplacement droite
        deplacement_direction(case_select, 1, 0, "joueur") #on appelle la fonction deplacement_direction
        #Deplacement gauche
        deplacement_direction(case_select, -1, 0, "joueur") #on appelle la fonction deplacement_direction

    elif piece == (cavalier_blanc if couleur_joueur1 == "blanc" else cavalier_noir): #si c'est un cavalier
        cavalier(case_select, -17, -1, "joueur") #on appelle la fonction cavalier
        cavalier(case_select, -15, 1, "joueur") #on appelle la fonction cavalier
        cavalier(case_select, -10, -2, "joueur") #on appelle la fonction cavalier
        cavalier(case_select, -6, 2, "joueur") #on appelle la fonction cavalier
        cavalier(case_select, 6, -2, "joueur") #on appelle la fonction cavalier
        cavalier(case_select, 10, 2, "joueur") #on appelle la fonction cavalier
        cavalier(case_select, 15, -1, "joueur") #on appelle la fonction cavalier
        cavalier(case_select, 17, 1, "joueur") #on appelle la fonction cavalier


    elif piece == (fou_blanc if couleur_joueur1 == "blanc" else fou_noir): #si c'est un fou
        # Direction N-E
        deplacement_direction(case_select, 1, -1, "joueur") #on appelle la fonction deplacement_direction
        # Direction N-O
        deplacement_direction(case_select, -1, -1, "joueur") #on appelle la fonction deplacement_direction
        # Direction S-E
        deplacement_direction(case_select, 1, 1, "joueur") #on appelle la fonction deplacement_direction
        # Direction S-O
        deplacement_direction(case_select, -1, 1, "joueur") #on appelle la fonction deplacement_direction

    elif piece == (roi_blanc if couleur_joueur1 == "blanc" else roi_noir): #si c'est un roi
        roi(case_select, -9, -1, "joueur") #on appelle la fonction roi
        roi(case_select, -8, 0, "joueur") #on appelle la fonction roi
        roi(case_select, -7, 1, "joueur") #on appelle la fonction roi
        roi(case_select, -1, -1, "joueur") #on appelle la fonction roi
        roi(case_select, 1, 1, "joueur") #on appelle la fonction roi
        roi(case_select, 7, -1, "joueur") #on appelle la fonction roi
        roi(case_select, 8, 0, "joueur") #on appelle la fonction roi
        roi(case_select, 9, 1, "joueur") #on appelle la fonction roi
        

    elif piece == (reine_blanc if couleur_joueur1 == "blanc" else reine_noir): #si c'est une reine
        ##deplacement comme un fou##
        # Direction N-E
        deplacement_direction(case_select, 1, -1, "joueur") #on appelle la fonction deplacement_direction
        # Direction N-O
        deplacement_direction(case_select, -1, -1, "joueur") #on appelle la fonction deplacement_direction
        # Direction S-E
        deplacement_direction(case_select, 1, 1, "joueur") #on appelle la fonction deplacement_direction
        # Direction S-O
        deplacement_direction(case_select, -1, 1, "joueur") #on appelle la fonction deplacement_direction
        
        ##deplacement comme une tour##
        #Deplacement haut
        deplacement_direction(case_select, 0, -1, "joueur")#on appelle la fonction deplacement_direction
        #Deplacement bas
        deplacement_direction(case_select, 0, 1, "joueur")  #on appelle la fonction deplacement_direction
        #Deplacement droite
        deplacement_direction(case_select, 1, 0, "joueur") #on appelle la fonction deplacement_direction
        #Deplacement gauche
        deplacement_direction(case_select, -1, 0, "joueur") #on appelle la fonction deplacement_direction


def pion(case_select : int, type_joueur : str):
    """Cette fonction permet de connaitre toutes les cases où le pion peut aller"""
    global cases_possibles
    if type_joueur == "joueur": #si c'est le joueur qui joue
        if cases[case_select-8][0] == "vide": #si la première case de déplacement du pion est vide
            cases_possibles.append(cases[case_select-8]) #on ajoute la case à la liste des cases possibles
        if case_select // 8 == 6 and cases[case_select-8][0] == "vide": #si le pion n'a toujours pas été bougé et que la première case de déplacement du pion est vide
            if cases[case_select-16][0] == "vide": #si la deuxième case de déplacement du pion est vide
                cases_possibles.append(cases[case_select-16]) #on ajoute la case à la liste des cases possibles
        if cases[case_select-7][0] != "vide" and cases[case_select-7][1] == couleur_joueur2:  #si la case de déplacement du pion est occupée par une pièce adverse
            if (case_select-7) % 8 == (case_select % 8) + 1: #si la case pour manger un adversaire est bien sur la colonne d'après
                cases_possibles.append(cases[case_select-7]) #on ajoute la case à la liste des cases possibles
        if cases[case_select-9][0] != "vide" and cases[case_select-9][1] == couleur_joueur2: #si la case de déplacement du pion est occupée par une pièce adverse
            if (case_select-9) % 8 == (case_select % 8) - 1: #si la case pour manger un adversaire est bien sur la colonne d'avant
                cases_possibles.append(cases[case_select-9]) #on ajoute la case à la liste des cases possibles

    elif type_joueur == "auto": #si c'est l'ordinateur qui calcule les coups possibles afin d'éviter de jouer des pièces alors qu'il y a échec
        if cases[case_select+7][2] <= 63:
            cases_precalculees.append(cases[case_select+7]) #on ajoute la case à la liste des cases echec
        if cases[case_select+9][2] <= 63: 
            cases_precalculees.append(cases[case_select+9]) #on ajoute la case à la liste des cases echec


    
def cavalier(case_select : int, index_diff_case_visee : int ,difference_colonne : int,  type_joueur : str):
    """Cette fonction permet d'ajouter aux cases possibles la case d'index de différence index_diff_case_visee avec case_select. difference_colonne est la différence de colonne entre la case_select et la case_visee"""
    global cases_possibles

    if (63 >= (case_select+index_diff_case_visee) >= 0) and ((case_select+index_diff_case_visee) % 8) == (case_select % 8) + difference_colonne: #si la case pour manger un adversaire est bien égale à la différence de colonne
        if cases[case_select+index_diff_case_visee][1] != (("blanc" if couleur_joueur1 == "blanc" else "noir") if type_joueur == "joueur" else ("noir" if couleur_joueur1 == "blanc" else "blanc") ): #si la case de déplacement du cavalier est occupée par une pièce adverse
            if type_joueur == "joueur": #si c'est un joueur
                cases_possibles.append(cases[case_select+index_diff_case_visee]) #on ajoute la case à la liste des cases possibles
            elif type_joueur == "auto": #si c'est l'ordinateur qui calcule les coups possibles afin d'éviter de jouer des pièces alors qu'il y a échec
                cases_precalculees.append(cases[case_select+index_diff_case_visee]) #on ajoute la case à la liste des cases echec



def roi(case_select : int, index_diff_case_visee : int, difference_colonne : int, type_joueur : str):
    """Cette fonction permet de connaitre toutes les cases où le roi peut aller"""
    global cases_possibles, cases_precalculees
    if 0 < (case_select+index_diff_case_visee) <= 63 and ((case_select+index_diff_case_visee) % 8) == (case_select % 8) + difference_colonne: #si la case de destination est bien dans le plateau
        if cases[case_select+index_diff_case_visee] not in cases_precalculees and type_joueur == "joueur": #si la case de destination n'est pas dans la liste des cases echec
            if cases[case_select+index_diff_case_visee][1] != couleur_joueur1: #si la case de destination n'est pas occupée par une pièce de la même couleur que le roi
                cases_possibles.append(cases[case_select+index_diff_case_visee]) #on ajoute la case à la liste des cases possibles

        elif type_joueur == "auto": #si c'est l'ordinateur qui calcule les coups possibles afin d'éviter de jouer des pièces alors qu'il y a échec
            cases_precalculees.append(cases[case_select+index_diff_case_visee]) #on ajoute la case à la liste des cases echec

def deplacement_direction(idx_case,x,y, type_joueur):
    """Cette fonction permet de déplacer une tour ou un fou à une index idx_case dans une direction donnée par x (-1 pour gauche, 1 pour droite) et y (-1 pour haut, 1 pour bas)"""
    idx_list_offset = x + 8*y
    #connaitre les limites en fonctions des colonnes
    modulo_offset = 0 if x > 0 else 1 #pour connaitre le modulo à appliquer
    index_deplacement = idx_case + idx_list_offset 
    case_possible = (index_deplacement >=0 and index_deplacement <=63 and (True if x == 0 else (index_deplacement+modulo_offset)%8 !=0))
    while (case_possible):
        case_possible = False
        if cases[index_deplacement][0] == "vide":
            if type_joueur == "joueur":
                cases_possibles.append(cases[index_deplacement])
            elif type_joueur == "auto":
                cases_precalculees.append(cases[index_deplacement])
            index_deplacement = index_deplacement + idx_list_offset
            case_possible = (index_deplacement >=0 and index_deplacement <=63 and (True if x == 0 else (index_deplacement+modulo_offset)%8 !=0))
        elif cases[index_deplacement][1] != couleur_joueur1:
            if type_joueur == "joueur":
                cases_possibles.append(cases[index_deplacement])
            elif type_joueur == "auto":
                cases_precalculees.append(cases[index_deplacement])
            case_possible = False


def demande_piece(case : int, piece_choisi):
    """Cette fonction permet, quand un pion arrive sur la ligne 1, de modifier le pion en la piece piece_choisi mise en paramètre."""
    global cases, case_piece_demandee
    cases[case][0] = piece_choisi #on change la piece de la case
    case_piece_demandee = None #on remet la variable à None
    #serveur.envoie(str(case_selection)+","+str(case)+","+str(cases[case][0])) #on envoie à l'autre joueur le déplacment effectué ainsi que la pièce qu'il a choisi


def petit_roque(couleur_joueur : str):
    """Cette fonction permet faire le coup appelé 'petit roque'"""
    global new_case, cases_possibles, piece_selection, tourJ, p_roque, cases
    if couleur_joueur == "blanc":
        cases[60][0:2], cases[62][0:2] = cases[62][0:2], cases[60][0:2]
        cases[63][0:2], cases[61][0:2] = cases[61][0:2], cases[63][0:2]
        new_case = 62 #permet de garder en mémoire la case de la pièce déplacée
    elif couleur_joueur == "noir":
        cases[59][0:2], cases[57][0:2] = cases[57][0:2], cases[59][0:2]
        cases[56][0:2], cases[58][0:2] = cases[58][0:2], cases[56][0:2]
        new_case = 57
    cases_possibles = [] #on vide la liste des cases possibles car on a déplacé une pièce
    piece_selection = False #on désélectionne la pièce sélectionnée
    tourJ += 1
    p_roque = True #on dit que le roque a déjà été effectué
    aquiletour()


def grand_roque(couleur_joueur : str):
    """Cette fonction permet faire le coup appelé 'grand roque'"""
    global new_case, cases_possibles, piece_selection, tourJ, g_roque, cases
    if couleur_joueur == "blanc":
        cases[60][0:2], cases[58][0:2] = cases[58][0:2], cases[60][0:2]
        cases[56], cases[59] = cases[59], cases[56][0:2]
        new_case = 58
    elif couleur_joueur == "noir":
        cases[59][0:2], cases[61][0:2] = cases[61][0:2], cases[59][0:2]
        cases[60][0:2], cases[63][0:2] = cases[63][0:2], cases[60][0:2]
        new_case = 61
    cases_possibles = [] #on vide la liste des cases possibles car on a déplacé une pièce
    piece_selection = False #on désélectionne la pièce sélectionnée
    tourJ += 1
    g_roque = True #on dit que le roque a déjà été effectué
    aquiletour()   





def interpretteur(donnees):
    """Cette fonction permet d'interpréter les données reçues par le client."""
    global new_case, tourJ, cases, utilisateur_a_quitte
    info = (donnees.decode()).split(",")

    if len(info) == 1: 
        if info[0] == "connected": #si le client est connecté
            serveur.connect = True
            serveur.envoie(couleur_joueur2) #on envoie au client sa couleur
            if couleur_joueur1 == "noir":
                donnee = serveur.attente()
                interpretteur(donnee)
        elif info[0] == "petit_roque":
            if couleur_joueur2 == "blanc":
                cases[0][0:2], cases[2][0:2] = cases[2][0:2], cases[0][0:2]
                cases[3][0:2], cases[1][0:2] = cases[1][0:2], cases[3][0:2]
                new_case = 1
            elif couleur_joueur2 == "noir":
                cases[7][0:2], cases[5][0:2] = cases[5][0:2], cases[7][0:2]
                cases[6][0:2], cases[4][0:2] = cases[4][0:2], cases[6][0:2]
                new_case = 6
            tourJ += 1
            aquiletour()
            test_echec()
            fnc_echec()
        elif info[0] == "grand_roque":
            if couleur_joueur2 == "blanc":
                cases[3][0:2], cases[5][0:2] = cases[5][0:2], cases[3][0:2]
                cases[7][0:2], cases[4][0:2] = cases[4][0:2], cases[7][0:2]
                new_case = 5
            elif couleur_joueur2 == "noir":
                cases[0][0:2], cases[3][0:2] = cases[3][0:2], cases[0][0:2]
                cases[4][0:2], cases[2][0:2] = cases[2][0:2], cases[4][0:2]
                new_case = 2
            tourJ += 1
            aquiletour()
            test_echec()
            fnc_echec()
        elif info[0] == "quitter":
            utilisateur_a_quitte = True
            serveur.quitter()
            serveur.connect = False


    elif len(info) == 2:
        case1 = 63 - int(info[0])
        case2 = 63 - int(info[1])
        cases[case2][0] = cases[case1][0]
        cases[case2][1] = cases[case1][1]
        cases[case1][0] = "vide"
        cases[case1][1] = ""
        new_case = case2 #permet de garder en mémoire la case de la pièce déplacée
        tourJ += 1 #permet de changer de tour
        aquiletour() #on change de tour
        test_echec()
        fnc_echec()
    elif len(info) == 3:
        if info[2] == "echec":
            case1 = 63 - int(info[0]) 
            case2 = 63 - int(info[1])
            cases[case2][0] = cases[case1][0]
            cases[case2][1] = cases[case1][1]
            cases[case1][0] = "vide"
            cases[case1][1] = ""
            new_case = case2 #permet de garder en mémoire la case de la pièce déplacée
            tourJ += 1
            aquiletour()
            test_echec()
            fnc_echec()
        else: #quand un pion adverse atteind la dernière ligne
            case1 = 63 - int(info[0])
            case2 = 63 - int(info[1])
            cases[case2][0] = info[2]
            cases[case2][1] = cases[case1][1]
            cases[case1][0] = "vide"
            cases[case1][1] = ""
            new_case = case2
            tourJ += 1
            aquiletour()
            test_echec()
            fnc_echec()
            print(cases)
    
    
def lance():
    """Cette fonction permet d'ouvrir le serveur."""
    serveur.open_server()
    donnees = serveur.attente()
    interpretteur(donnees)

def lance_attente():
    """Cette fonction permet d'attendre que le client joue et de récupérer son coup."""
    donnees = serveur.attente()
    interpretteur(donnees)



def test_echec():
    """Cette fonction permet de tester s'il y a échec."""
    global cases_precalculees
    cases_precalculees = []
    for i in cases: #on parcourt toutes les cases
        if i[0] == (pion_blanc if couleur_joueur1 == "noir" else pion_noir): #si la pièce est un pion
            pion(i[2], "auto")
        elif i[0] == (tour_blanc if couleur_joueur1 == "noir" else tour_noir): #si la pièce est une tour
            #Deplacement haut
            deplacement_direction(i[2], 0, -1, "auto")#on appelle la fonction deplacement_direction
            #Deplacement bas
            deplacement_direction(i[2], 0, 1, "auto")  #on appelle la fonction deplacement_direction
            #Deplacement droite
            deplacement_direction(i[2], 1, 0, "auto") #on appelle la fonction deplacement_direction
            #Deplacement gauche
            deplacement_direction(i[2], -1, 0, "auto") #on appelle la fonction deplacement_direction
        elif i[0] == (cavalier_blanc if couleur_joueur1 == "noir" else cavalier_noir): #si la pièce est un cavalier
            cavalier(i[2], -17, -1, "auto") #on appelle la fonction cavalier
            cavalier(i[2], -15, 1, "auto") #on appelle la fonction cavalier
            cavalier(i[2], -10, -2, "auto") #on appelle la fonction cavalier
            cavalier(i[2], -6, 2, "auto") #on appelle la fonction cavalier
            cavalier(i[2], 6, -2, "auto") #on appelle la fonction cavalier
            cavalier(i[2], 10, 2, "auto") #on appelle la fonction cavalier
            cavalier(i[2], 15, -1, "auto") #on appelle la fonction cavalier
            cavalier(i[2], 17, 1, "auto") #on appelle la fonction cavalier
        elif i[0] == (fou_blanc if couleur_joueur1 == "noir" else fou_noir): #si la pièce est un fou
            # Direction N-E
            deplacement_direction(i[2], 1, -1, "auto") #on appelle la fonction deplacement_direction
            # Direction N-O
            deplacement_direction(i[2], -1, -1, "auto") #on appelle la fonction deplacement_direction
            # Direction S-E
            deplacement_direction(i[2], 1, 1, "auto") #on appelle la fonction deplacement_direction
            # Direction S-O
            deplacement_direction(i[2], -1, 1, "auto") #on appelle la fonction deplacement_direction
        elif i[0] == (roi_blanc if couleur_joueur1 == "noir" else roi_noir): #si la pièce est un roi
            roi(i[2], -9, -1, "auto") #on appelle la fonction roi
            roi(i[2], -8, 0, "auto") #on appelle la fonction roi
            roi(i[2], -7, 1, "auto") #on appelle la fonction roi
            roi(i[2], -1, -1, "auto") #on appelle la fonction roi
            roi(i[2], 1, 1, "auto") #on appelle la fonction roi
            roi(i[2], 7, -1, "auto") #on appelle la fonction roi
            roi(i[2], 8, 0, "auto") #on appelle la fonction roi
            roi(i[2], 9, 1, "auto") #on appelle la fonction roi
            
        elif i[0] == (reine_blanc if couleur_joueur1 == "noir" else reine_noir): #si la pièce est une reine
            ##deplacement comme un fou##
            # Direction N-E
            deplacement_direction(i[2], 1, -1, "auto") #on appelle la fonction deplacement_direction
            # Direction N-O
            deplacement_direction(i[2], -1, -1, "auto") #on appelle la fonction deplacement_direction
            # Direction S-E
            deplacement_direction(i[2], 1, 1, "auto") #on appelle la fonction deplacement_direction
            # Direction S-O
            deplacement_direction(i[2], -1, 1, "auto") #on appelle la fonction deplacement_direction
            
            ##deplacement comme une tour##
            #Deplacement haut
            deplacement_direction(i[2], 0, -1, "auto")#on appelle la fonction deplacement_direction
            #Deplacement bas
            deplacement_direction(i[2], 0, 1, "auto")  #on appelle la fonction deplacement_direction
            #Deplacement droite
            deplacement_direction(i[2], 1, 0, "auto") #on appelle la fonction deplacement_direction
            #Deplacement gauche
            deplacement_direction(i[2], -1, 0, "auto") #on appelle la fonction deplacement_direction



def fnc_echec():
    """Cette fonction permet de savoir s'il y a échec"""
    global echec 
    for i in cases: #on parcourt toutes les cases
        if i[0] == (roi_blanc if couleur_joueur1 == "blanc" else roi_noir): #si la pièce est un roi
            if i in cases_precalculees: #si la case est dans la liste des cases précalculées
                echec = True
                return True
            else:
                echec = False
                return False
                
            


A1 = [tour_noir, "noir", None]
A2 = [cavalier_noir, "noir", None]
A3 = [fou_noir, "noir", None]
A4 = [reine_noir, "noir", None]
A5 = [roi_noir, "noir", None]
A6 = [fou_noir, "noir", None]
A7 = [cavalier_noir, "noir", None]
A8 = [tour_noir, "noir", None]

B1 = [pion_noir, "noir", None]
B2 = [pion_noir, "noir", None]
B3 = [pion_noir, "noir", None]
B4 = [pion_noir, "noir", None]
B5 = [pion_noir, "noir", None]
B6 = [pion_noir, "noir", None]
B7 = [pion_noir, "noir", None]
B8 = [pion_noir, "noir", None]

C1 = ["vide", "", None]
C2 = ["vide", "", None]
C3 = ["vide", "", None]
C4 = ["vide", "", None]
C5 = ["vide", "", None]
C6 = ["vide", "", None]
C7 = ["vide", "", None]
C8 = ["vide", "", None]

D1 = ["vide", "", None]
D2 = ["vide", "", None]
D3 = ["vide", "", None]
D4 = ["vide", "", None]
D5 = ["vide", "", None]
D6 = ["vide", "", None]
D7 = ["vide", "", None]
D8 = ["vide", "", None]

E1 = ["vide", "", None]
E2 = ["vide", "", None]
E3 = ["vide", "", None]
E4 = ["vide", "", None]
E5 = ["vide", "", None]
E6 = ["vide", "", None]
E7 = ["vide", "", None]
E8 = ["vide", "", None]

F1 = ["vide", "", None]
F2 = ["vide", "", None]
F3 = ["vide", "", None]
F4 = ["vide", "", None]
F5 = ["vide", "", None]
F6 = ["vide", "", None]
F7 = ["vide", "", None]
F8 = ["vide", "", None]

G1 = [pion_blanc, "blanc", None]
G2 = [pion_blanc, "blanc", None]
G3 = [pion_blanc, "blanc", None]
G4 = [pion_blanc, "blanc", None]
G5 = [pion_blanc, "blanc", None]
G6 = [pion_blanc, "blanc", None]
G7 = [pion_blanc, "blanc", None]
G8 = [pion_blanc, "blanc", None]

H1 = [tour_blanc, "blanc", None]
H2 = [cavalier_blanc, "blanc", None]
H3 = [fou_blanc, "blanc", None]
H4 = [reine_blanc, "blanc", None]
H5 = [roi_blanc, "blanc", None]
H6 = [fou_blanc, "blanc", None]
H7 = [cavalier_blanc, "blanc", None]
H8 = [tour_blanc, "blanc", None]

cases = [
    A1, A2, A3, A4, A5, A6, A7, A8,
    B1, B2, B3, B4, B5, B6, B7, B8, 
    C1, C2, C3, C4, C5, C6, C7, C8,
    D1, D2, D3, D4, D5, D6, D7, D8, 
    E1, E2, E3, E4, E5, E6, E7, E8, 
    F1, F2, F3, F4, F5, F6, F7, F8,
    G1, G2, G3, G4, G5, G6, G7, G8,
    H1, H2, H3, H4, H5, H6, H7, H8
    ]


if couleur_joueur1 == "noir":
    cases.reverse()

for i in range(len(cases)):
    cases[i][2] = i

