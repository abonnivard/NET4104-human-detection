import pandas as pd
import warnings
warnings.filterwarnings('ignore')


d = pd.read_csv("enregistrement/allonge_0.csv")
d2 = pd.read_csv("enregistrement/debout_0.csv")
d3 = pd.read_csv("enregistrement/rien_1.csv")

for i in range(1, 11):
    bis = pd.read_csv("enregistrement/allonge_" + str(i) + ".csv")
    pd.concat([d, bis])
    
for i in range(1, 14) : 
    bis = pd.read_csv("enregistrement/debout_" + str(i) + ".csv")
    pd.concat([d2, bis])

for i in range(2, 6) : 
    bis = pd.read_csv("enregistrement/rien_" + str(i) + ".csv")
    pd.concat([d3, bis])


d['State'] = 0
d2['State'] = 1
d3['State'] = -1
