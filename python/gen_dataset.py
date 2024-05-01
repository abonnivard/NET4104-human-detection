import pandas as pd
import warnings
warnings.filterwarnings('ignore')

'''
Ce fichier permet de générer un jeu de données à partir de plusieurs fichiers CSV présents dans les dossier "enregistrement" et "new_enregistrement".
'''


d = pd.read_csv("enregistrement/allonge_2.csv")
d2 = pd.read_csv("new_enregistrements/debout/debout_1.csv")
d3 = pd.read_csv("new_enregistrements/rien/rien_1.csv")

for i in range(2, 3):
    bis = pd.read_csv("enregistrement/allonge_" + str(i) + ".csv")
    pd.concat([d, bis])
    
for i in range(1, 4) : 
    if i != 2 :
        bis = pd.read_csv("new_enregistrements/debout/debout_" + str(i) + ".csv")
        pd.concat([d2, bis])

for i in range(1, 4) : 
     bis = pd.read_csv("new_enregistrements/rien/rien_" + str(i) + ".csv")
     pd.concat([d3, bis])


d['State'] = 0
d2['State'] = 1
d3['State'] = -1
