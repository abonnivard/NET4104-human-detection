import pandas as pd
import warnings
warnings.filterwarnings('ignore')

d = pd.read_csv("enregistrement/allonge_0.csv")
d2 = pd.read_csv("enregistrement/debout_0.csv")

for i in range(1, 12):
    bis = pd.read_csv("enregistrement/allonge_" + str(i) + ".csv")
    pd.concat([d, bis])
    
for i in range(1, 15) : 
    bis = pd.read_csv("enregistrement/debout_" + str(i) + ".csv")
    pd.concat([d2, bis])


d['State'] = 0
d2['State'] = 1
