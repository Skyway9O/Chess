# Chess
Mon jeu d'échec en *Python*.

## Gestion des fichiers

Les fichiers `main.py`, `serveur.py` et `constant` et `JeuEchec_graphique_serveur.py` sont des fichiers à posséder sur le même ordinateur (l'odinateur servant de "serveur") et dans le même répertoire. Ensuite, le seul fichier à executer est `JeuEchec_graphique_serveur.py` sur l'ordinateur étant le "serveur".

Les fichiers `main_client.py`, `client.py` et `constant` et `JeuEchec_graphique_client.py` sont des fichiers à posséder sur le même ordinateur (l'ordinateur "client") et dans le même répertoire. Ensuite, le seul fichier à executer est `JeuEchec_graphique_client.py` sur l'ordinateur étant le "client".

## Partie réseau

Il est nécessaire que les deux ordinateurs soient connectés sur le même réseau local.
Pour assurer le fonctionnement de la connexion réseau entre les deux ordinateurs, il faut inscrire l'adresse IP de l'odinateur client à la ligne indiquée dans le programme `serveur.py`. De la même façon, il faut ajouter l'adresse IP du serveur dans le fichier `client.py` à l'emplacement indiqué.

#### Conseil :
Une fois le programme `JeuEchec_graphique_serveur.py` lancé sur l'ordinateur serveur et le fichier `JeuEchec_graphique_client.py` lancé sur l'ordinateur client, un bouton "*chercher un adversaire*" apparaît en bas à gauche de la fenêtre. Je vous conseille de d'abord appuier sur le bouton de l'ordinateur serveur puis sur celui de l'odinateur client. **Sans cela, le script risque de planter.**
