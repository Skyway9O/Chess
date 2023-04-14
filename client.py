# coding : utf-8

"""JEU D'ECHECS programme serveur
La communauté de la truelle, mai 2022."""


from socket import *
couleur_joueur2 = None
connected = False


play = True
IP = None #Ip du serveur (c'est à vous de na noter ici)


def connect():
    """Cette fonction permet de se connecter au serveur et de le lui dire."""
    global maConx, couleur_joueur2, connected
    IP_serv = IP
    port_serv = 50000 
    maConx = socket() 

    maConx.connect((IP_serv, port_serv))
    envoie("connected")
    connected = True
    reponse = attente()
    couleur_joueur2 = reponse.decode()



def attente():
    """Cette fonction permet d'attendre que le serveur joue."""

    donnees = maConx.recv(1000)
    return donnees


def envoie(donnees):
    """Cette fonction permet d'envoyer les données au serveur."""
    maConx.send(donnees.encode())


def quitter():
    """Cette fonction permet de quitter le programme."""
    envoie("quitter")
    maConx.close()