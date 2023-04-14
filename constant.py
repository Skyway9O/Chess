# coding : utf-8

'''constantes JEU D'ECHECS
La communauté de la truelle, mai 2022.'''

import tkinter 
from os import path


Width, Height = 1000, 1000
NB_Col, NB_Row = 8, 8
CELL_Size = 100
Square = 100



file = path.dirname(__file__) + "/images/"

#pieces blanches
pion_blanc = "{}wp.gif".format(file)
cavalier_blanc = "{}wc.gif".format(file)
fou_blanc = "{}wb.gif".format(file)
tour_blanc = "{}wr.gif".format(file)
roi_blanc = "{}wk.gif".format(file)
reine_blanc = "{}wq.gif".format(file)



#pieces noires
pion_noir = "{}bp.gif".format(file)
cavalier_noir = "{}bc.gif".format(file)
fou_noir = "{}bb.gif".format(file)
tour_noir = "{}br.gif".format(file)
roi_noir = "{}bk.gif".format(file)
reine_noir = "{}bq.gif".format(file)

echiquier = "{}echiquier.gif".format(file)
