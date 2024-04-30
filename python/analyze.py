import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import ast
warnings.filterwarnings('ignore')

from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.model_selection import train_test_split

from gen_dataset import d, d2, d3


#isolation du vecteur "data" de taille 109
X = pd.concat([d, d2, d3])['data'].apply(ast.literal_eval)
X_data = np.array([np.array(x) for x in X])
X_data = np.vstack(X_data)


#version avec le rssi
X_rssi = pd.concat([d, d2, d3])[['rssi']]

#creation des étiquettes
y = pd.concat([d, d2, d3])['State']


#split des données de tests, 70% pour l'entrainement, 30% pour les tests
X_train, X_test, y_train, y_test = train_test_split(X_data, y, train_size=0.7, random_state=0)

#on force l'arbre à n'avoie qu'une profondeur de 15 pour éviter que l'IA apprenne le jeu par coeur
clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=15)
clf.fit(X_train, y_train)


# Afficher l'arbre
plt.figure(figsize=(10,10)) 
tree.plot_tree(clf, class_names=['1', '0', '-1'], filled=True)
plt.show()

# prédiction test et affichage du score de réussite
y_pred = clf.predict(X_test)

print("Train data accuracy:",round(100*accuracy_score(y_true = y_train, y_pred=clf.predict(X_train)),3),"%")
print("Test data accuracy:","%.3f" %(100*accuracy_score(y_true = y_test, y_pred=y_pred)),"%")


#test avec une donnée ne faisant pas partie du jeu de test
data = pd.read_csv("enregistrement/allonge_5.csv")
data['State'] = 0

data_nv_2 = data[['rssi']]

data_nv = data['data'].apply(ast.literal_eval)
data_nv = np.array([np.array(x) for x in data_nv])
data_nv = np.vstack(data_nv)

print("Test data accuracy:","%.3f" %(100*accuracy_score(y_true = data['State'], y_pred=clf.predict(data_nv))),"%")
plt.plot((data)['seq'].tolist(), clf.predict(data_nv))
plt.show()