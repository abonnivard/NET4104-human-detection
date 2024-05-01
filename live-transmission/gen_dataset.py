import pandas as pd
import warnings
warnings.filterwarnings('ignore')

'''
Ce fichier permet de générer un jeu de données à partir de plusieurs fichiers CSV présents dans les dossier "enregistrement" et "new_enregistrement".
'''


d = pd.read_csv("../python/enregistrement/allonge_0.csv")
d2 = pd.read_csv("../python/enregistrement/debout_0.csv")
d3 = pd.read_csv("../python/enregistrement/rien_1.csv")

for i in range(1, 11):
    bis = pd.read_csv("../python/enregistrement/allonge_" + str(i) + ".csv")
    pd.concat([d, bis])
    
for i in range(1, 14) : 
    bis = pd.read_csv("../python/enregistrement/debout_" + str(i) + ".csv")
    pd.concat([d2, bis])

for i in range(2, 6) : 
    bis = pd.read_csv("../python/enregistrement/rien_" + str(i) + ".csv")
    pd.concat([d3, bis])


d['State'] = 0
d2['State'] = 1
d3['State'] = -1
