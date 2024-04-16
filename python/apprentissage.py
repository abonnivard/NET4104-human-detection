import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report

# Charger les données à partir des fichiers CSV
donnees_debout = pd.concat([pd.read_csv(f'enregistrement/debout_{i}.csv') for i in range(1, 9)])
donnees_allonge = pd.concat([pd.read_csv(f'enregistrement/allonge_{i}.csv') for i in range(1, 9)])

# Créer les étiquettes pour les données (1 pour debout, 0 pour allongé)
donnees_debout['label'] = 1
donnees_allonge['label'] = 0

# Concaténer les données debout et allongé
donnees_totales = pd.concat([donnees_debout, donnees_allonge])

# Fonction pour extraire les données CSI d'une chaîne de caractères
def extract_csi_data(csi_string):
    csi_values = csi_string.strip('[]').split(', ')
    csi_data = [int(value) for value in csi_values]
    return csi_data

# Extraire les données CSI de la colonne 'data'
donnees_totales['csi_data'] = donnees_totales['data'].apply(extract_csi_data)

# Supprimer la colonne 'data' si elle n'est plus nécessaire
donnees_totales.drop('data', axis=1, inplace=True)

# Séparer les fonctionnalités et les étiquettes
X = donnees_totales['csi_data']
y = donnees_totales['label']

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner un modèle SVM
model = SVC(kernel='linear')
model.fit(X_train.tolist(), y_train)

# Faire des prédictions sur l'ensemble de test
y_pred = model.predict(X_test.tolist())

# Évaluer le modèle
print(classification_report(y_test, y_pred))

# Utiliser le modèle pour prédire de nouvelles données
nouvelles_donnees = pd.read_csv('2024-04-09_12-37-33-975_104_1.csv')
nouvelles_donnees['csi_data'] = nouvelles_donnees['data'].apply(extract_csi_data)
nouvelles_predictions = model.predict(nouvelles_donnees['csi_data'].tolist())
print("Prédictions pour les nouvelles données :", nouvelles_predictions)
