# coding : utf-8

"""JEU D'ECHECS programme serveur
La communauté de la truelle, mai 2022."""

from socket import *



connect = False
IP = None #Ip du client (c'est à vous de na noter ici)


def envoie(donnees):
    """Cette fonction permet d'envoyer les données au client."""
    sclient.send(donnees.encode())



def attente():
    """Cette fonction permet d'attendre que le client joue."""
    global sclient
    if connect == False:
        (sclient, adclient) = serveur.accept()
    donnee = sclient.recv(1000)
    return donnee
    


def open_server():
    global serveur
    serveur = socket() 
    serveur.bind((IP, 50000)) 
    serveur.listen(5)


def quitter():
    """Cette fonction permet de quitter le programme."""
    envoie("quitter")
    serveur.close()

