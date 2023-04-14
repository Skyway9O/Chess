# coding : utf-8

"""JEU D'ECHECS interface graphique
La communauté de la truelle, mai 2022."""

import main, constant
from tkinter import *

bleu = None # variable pour les carrés bleus
img_piece = None # variables des images des pièces
couleur_tour = None
coup_joue = None #variable pour les carrés jaunes du coup joué
gris = None

def dessine_tout():
    """Cette fonction permet d'apperler toutes les fonctions de dessin"""
    global bleu, img_piece, couleur_tour, coup_joue, gris
    
    canvas.delete(bleu, img_piece, couleur_tour, coup_joue, gris)
    echiquier = canvas.create_image(0, 0, image=image_echiquier, anchor=NW)
    couleur_tour = dessine_tour()

    if main.tourJ != 0:
        coup_joue = dessine_coup_joue()

    bleu = dessine_coups_possibles()

    if main.case_selection != None:
        gris = dessine_case_selectionnee()
    if main.echec == True:
        img_piece = dessine_echec()
        label_info.configure(text="⚠ Échec ⚠")
    elif main.echec == False:
        label_info.configure(text="")
    if main.utilisateur_a_quitte == True:
        adversaire_a_quitter()

    img_piece = dessine_element()

    if main.case_piece_demandee != None:
        pop_up_choix_piece(main.case_piece_demandee)
    
    fenetre.update()


def dessine_element():
    """dessine les éléments de l'échiquier"""
    global image
    image = None
    for y in range(constant.NB_Row):
        for x in range(constant.NB_Col):
            num_case_piece = main.cases[y*8+x][0]
            if num_case_piece == constant.pion_blanc: 
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_pion_blanc, anchor=NW)
            elif num_case_piece == constant.pion_noir:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_pion_noir, anchor=NW)
            elif num_case_piece == constant.cavalier_blanc:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_cavalier_blanc, anchor=NW)
            elif num_case_piece == constant.cavalier_noir:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_cavalier_noir, anchor=NW)
            elif num_case_piece == constant.fou_blanc:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_fou_blanc, anchor=NW)
            elif num_case_piece == constant.fou_noir:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_fou_noir, anchor=NW)
            elif num_case_piece == constant.tour_blanc:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_tour_blanc, anchor=NW)
            elif num_case_piece == constant.tour_noir:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_tour_noir, anchor=NW)
            elif num_case_piece == constant.roi_blanc:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_roi_blanc, anchor=NW)
            elif num_case_piece == constant.roi_noir:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_roi_noir, anchor=NW)
            elif num_case_piece == constant.reine_blanc:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_reine_blanc, anchor=NW)
            elif num_case_piece == constant.reine_noir:
                image = canvas.create_image(x*constant.CELL_Size, y*constant.CELL_Size, image=image_reine_noir, anchor=NW)
            


def dessine_coups_possibles():
    """dessine avec des carrés bleus les cases où il y a des coups possibles"""
    
    for i in main.cases_possibles:
        x = i[2] % 8
        y = i[2] // 8
        carre_possible = canvas.create_rectangle(x*constant.CELL_Size, y*constant.CELL_Size, x*constant.CELL_Size+constant.CELL_Size, y*constant.CELL_Size+constant.CELL_Size, fill="#009eff")


def dessine_case_selectionnee():
    """Cette fonction permet de dessiner un carré de couleur qui montre la case selectionnée"""
    carre_selectionnee = canvas.create_rectangle(main.case_selection%8*constant.CELL_Size, main.case_selection//8*constant.CELL_Size, main.case_selection%8*constant.CELL_Size+constant.CELL_Size, main.case_selection//8*constant.CELL_Size+constant.CELL_Size, fill="#cfcfcf")


def dessine_coup_joue():
    """dessine une case jaune pâle sur la dernière case jouée"""
    carre_coup_joue = canvas.create_rectangle(main.new_case%8*constant.CELL_Size, main.new_case//8*constant.CELL_Size, main.new_case%8*constant.CELL_Size+constant.CELL_Size, main.new_case//8*constant.CELL_Size+constant.CELL_Size, fill="#ffeb6d")


def dessine_echec():
    """dessine une case rouge sous le roi quand celui-ci est en échec"""
    for i in main.cases:
        if i[0] == (main.roi_blanc if main.couleur_joueur1 == "blanc" else main.roi_noir):
            x = i[2] % 8
            y = i[2] // 8
            echec = canvas.create_rectangle(x*constant.CELL_Size, y*constant.CELL_Size, x*constant.CELL_Size+constant.CELL_Size, y*constant.CELL_Size+constant.CELL_Size, fill="#f85959")


def dessine_tour():
    """Cette fonction permet de dessiner un carré de couleur qui montre le tour de jeu"""
    if main.tour_de_jeu == "blanc":
        canvas_couleur.configure(bg="white")
    elif main.tour_de_jeu == "noir":
        canvas_couleur.configure(bg="black")


def pop_up_choix_piece(case : int):
    """Cette fonction permet au joueur de choisir la piece voulu quand un pion arrive jusqu'à la ligne 1"""

    popup_choix_piece = Toplevel() # on crée une fenêtre pop-up
    popup_choix_piece.title("Choix de la nouvelle piece") # on donne un titre à la fenêtre pop-up
    popup_choix_piece.geometry("800x300") # on donne une taille à la fenêtre pop-up
    popup_choix_piece.grab_set() # on empêche le joueur de cliquer dans la fenêtre principale

    #on crée une frame
    frame_choix_piece = Frame(popup_choix_piece)

    #on crée un label
    label_choix_piece = Label(frame_choix_piece, text="Choisissez la piece qui va remplacer votre pion :", font=("Helvetica, 16"))
    label_choix_piece.grid(row=0, column=0, columnspan=10, pady=20)

    #on crée les radios boutons
    piece_voulu = StringVar()

    radio_choix_piece_pion = Radiobutton(frame_choix_piece, image=(image_pion_blanc if main.couleur_joueur1 == "blanc" else image_pion_noir), variable=piece_voulu, value=(constant.pion_blanc if main.couleur_joueur1 == "blanc" else constant.pion_noir))
    radio_choix_piece_pion.grid(row=1, column=0, columnspan=2)
    radio_choix_piece_pion.select()

    radio_choix_piece_tour = Radiobutton(frame_choix_piece, image=(image_tour_blanc if main.couleur_joueur1 == "blanc" else image_tour_noir), variable=piece_voulu, value=(constant.tour_blanc if main.couleur_joueur1 == "blanc" else constant.tour_noir))
    radio_choix_piece_tour.grid(row=1, column=2, columnspan=2)

    radio_choix_piece_cavalier = Radiobutton(frame_choix_piece, image=(image_cavalier_blanc if main.couleur_joueur1 == "blanc" else image_cavalier_noir), variable=piece_voulu, value=(constant.cavalier_blanc if main.couleur_joueur1 == "blanc" else constant.cavalier_noir))
    radio_choix_piece_cavalier.grid(row=1, column=4, columnspan=2)

    radio_choix_piece_fou = Radiobutton(frame_choix_piece, image=(image_fou_blanc if main.couleur_joueur1 == "blanc" else image_fou_noir), variable=piece_voulu, value=(constant.fou_blanc if main.couleur_joueur1 == "blanc" else constant.fou_noir))
    radio_choix_piece_fou.grid(row=1, column=6, columnspan=2)

    radio_choix_piece_reine = Radiobutton(frame_choix_piece, image=(image_reine_blanc if main.couleur_joueur1 == "blanc" else image_reine_noir), variable=piece_voulu, value=(constant.reine_blanc if main.couleur_joueur1 == "blanc" else constant.reine_noir))
    radio_choix_piece_reine.grid(row=1, column=8, columnspan=2)

    #on crée un bouton pour valider
    bouton_valider = Button(frame_choix_piece, text="Valider", command=lambda:[confirme_modif(case, piece_voulu.get(), popup_choix_piece)])
    bouton_valider.grid(row=2, column=0, columnspan=10, pady=20)

    #on affiche la frame
    frame_choix_piece.pack()


def confirme_modif(case, piece_voulu, pop_up):
    """Cette fonction permet de confirmer et de fermer la pop-up de choix de piece"""
    main.demande_piece(case, piece_voulu) #on lance la fonction du programme principale qui modifie la piece sur l'échiquier
    pop_up.destroy() #on ferme la pop-up
    main.serveur.envoie(str(main.case_selection)+","+str(case)+","+str(main.cases[case][0])) #on envoie à l'autre joueur le déplacment effectué ainsi que la pièce qu'il a choisi
    main.case_selection = None #on réinitialise la case selectionnée
    dessine_tout()
    main.lance_attente() #on lance l'attente de l'autre joueur
    dessine_tout()


def clique(event):
    if main.tour_de_jeu == main.couleur_joueur1: # si c'est au tour du joueur 1
        ligne = event.y // constant.CELL_Size # on récupère la ligne
        colonne = event.x // constant.CELL_Size # on récupère la colonne
        main.selection_case(colonne, ligne) # on selectionne la case
        dessine_tout() # on dessine les éléments de sélection
        if main.tour_de_jeu == main.couleur_joueur2 and main.case_piece_demandee == None: # si c'est au tour du joueur 2
            main.lance_attente() # on lance l'attente
            dessine_tout()



def cherche():
    """Cette fonction permet de chercher un adversaire"""
    bouton_cherche.configure(text="Recherche en cours...")
    fenetre.update()
    main.lance() # on lance le serveur
    bouton_cherche.configure(state=DISABLED, text="Connecté") # désactive le bouton de recherche
    canvas.bind("<Button-1>", clique) #bind le canvas
    dessine_tout() # on dessine les éléments



def quitte():
    """Cette fonction permet de quitter le jeu"""
    if main.serveur.connect == True: # si on est connecté à un adversaire
        main.serveur.quitter() # on quitte le serveur
    fenetre.destroy() # on ferme la fenêtre
    exit() # on quitte le programme


def sur():
    """Cette fonction permet de demander la confirmation pour quitter le jeu"""
    pop_up = Toplevel()
    pop_up.title("demande de confirmation")
    pop_up.geometry("400x120")
    pop_up.grab_set() #bloc les intéraction avec la fenêtre principale

    # on crée une frame
    frame_pop_up = Frame(pop_up)

    # on crée un label
    label_confirmation = Label(frame_pop_up, text="Voulez-vous vraiment quitter le jeu ?", font=("Helvetica, 15"))
    label_confirmation.grid(row=0, column=0, columnspan=2, pady=20)

    # on crée un bouton pour quitter
    bouton_confirmer = Button(frame_pop_up, text="Quitter", command=quitte, bg="#fc6767")
    bouton_confirmer.grid(row=1, column=1, padx=20)

    bouton_annuler = Button(frame_pop_up, text="Annuler", command=pop_up.destroy, bg="#b6d585")
    bouton_annuler.grid(row=1, column=0, padx=20)

    #on pack la frame de la pop up
    frame_pop_up.pack()


def adversaire_a_quitter():
    """Cette fonction permet de demander la confirmation pour quitter le jeu quand l'adversaire quitte"""
    pop_up = Toplevel()
    pop_up.title("demande de confirmation")
    pop_up.geometry("400x150")
    pop_up.grab_set() #bloc les intéraction avec la fenêtre principale

    # on crée une frame
    frame_pop_up = Frame(pop_up)

    # on crée un label
    label_confirmation = Label(frame_pop_up, text="Votre adversaire a quitté le jeu.\r Voulez-vous quitter à votre tour ?",  font=("Helvetica, 15"))
    label_confirmation.grid(row=0, column=0, columnspan=2, pady=20)

    # on crée un bouton pour quitter
    bouton_confirmer = Button(frame_pop_up, text="Quitter", command=quitte, bg="#fc6767")
    bouton_confirmer.grid(row=1, column=1, padx=20)

    bouton_annuler = Button(frame_pop_up, text="Annuler", command=pop_up.destroy, bg="#b6d585")
    bouton_annuler.grid(row=1, column=0, padx=20)

    #on pack la frame de la pop up
    frame_pop_up.pack()




#création de la fenêtre
fenetre = Tk()
fenetre.title("jeu d'échec (serveur)")
fenetre.geometry("1000x1000")
fenetre.minsize(850, 850)

#création de toutes les images
image_pion_blanc = PhotoImage(file=constant.pion_blanc)
image_pion_noir = PhotoImage(file=constant.pion_noir)
image_cavalier_blanc = PhotoImage(file=constant.cavalier_blanc)
image_cavalier_noir = PhotoImage(file=constant.cavalier_noir)
image_fou_blanc = PhotoImage(file=constant.fou_blanc)
image_fou_noir = PhotoImage(file=constant.fou_noir)
image_tour_blanc = PhotoImage(file=constant.tour_blanc)
image_tour_noir = PhotoImage(file=constant.tour_noir)
image_roi_blanc = PhotoImage(file=constant.roi_blanc)
image_roi_noir = PhotoImage(file=constant.roi_noir)
image_reine_blanc = PhotoImage(file=constant.reine_blanc)
image_reine_noir = PhotoImage(file=constant.reine_noir)
image_echiquier = PhotoImage(file=constant.echiquier)

#cree une frame
frame = Frame(fenetre)

#cree un canvas qui va contenir l'échiquier
canvas = Canvas(frame, highlightthickness = 1, highlightbackground="Black", width=8*constant.CELL_Size, height=8*constant.CELL_Size, bg="white")
canvas.grid(row=5, column=5, columnspan=8, rowspan=8, padx=20, pady=20)

canvas_couleur = Canvas(frame, highlightthickness=1, highlightbackground="Black", width=100, height=50)
canvas_couleur.grid(row=1, column=8, columnspan=2, rowspan=2)


#cree des labels
"""label_TDJ = Label(frame, text="Au tour des :", font=("Helvetica, 13"))
label_TDJ.grid(row=1, column=7, sticky=E)"""

label_info = Label(frame, text="", font=("Helvetica, 16"))
label_info.grid(row=1, column=11)


dessine_tout()


#cree un bouton
bouton_cherche = Button(frame, text="chercher un adversaire", command=cherche)
bouton_cherche.grid(row=13, column=5, columnspan=2)

bouton_quitter = Button(frame, text="quitter", command=sur, font=("Helvetica, 13"), bg="#fc6767")
bouton_quitter.grid(row=13, column=12, columnspan=2)

#pack la fenêtre
frame.pack(expand=YES)



fenetre.mainloop()







