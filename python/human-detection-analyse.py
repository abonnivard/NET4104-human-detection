import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Fonction pour détecter la présence d'humains
def rssi_method(data):
    # Supprimer les colonnes non pertinentes
    data = data[['seq', 'timestamp', 'mac', 'rssi', 'data']]
    sum = 0
    nb_under_seuil = 0
    # Parcourir les données pour détecter les humains
    for index, row in data.iterrows():
        # Analyser les données RSSI pour détecter les humains
        # Exemple simplifié : Si RSSI est supérieur à -60 dBm, on considère qu'un humain est présent
        sum +=row['rssi']
        if row['rssi'] > -60:
            nb_under_seuil += 1


    print(f"La moyenne des RSSI est {sum/len(data)} avec {nb_under_seuil} valeurs sous le seuil sur {len(data)}.")


# Fonction pour détecter la posture
def detect_posture(csi_data):
    # Définir des seuils adaptatifs pour la posture debout et allongée
    standing_threshold = 7  # Seuil pour la posture debout
    lying_threshold = 3     # Seuil pour la posture allongée

    # Calculer une métrique de mouvement basée sur les données CSI
    # Par exemple, la métrique pourrait être la moyenne des amplitudes des signaux sur toutes les sous-porteuses
    mean_amplitude = sum(abs(value) for value in csi_data) / len(csi_data)

    # Comparer la métrique de mouvement aux seuils de posture
    if mean_amplitude > standing_threshold:
        return "Debout"
    elif mean_amplitude < lying_threshold:
        return "Allongé"
    else:
        return "Indéterminé"

dossier = 'enregistrement'

# Liste pour stocker les données de tous les fichiers CSV ayant un "12" dans leur nom
donnees_debout = []

# Liste pour stocker les données de tous les autres fichiers CSV
donnes_allonge = []

# Parcourir tous les fichiers dans le dossier
for fichier in os.listdir(dossier):
    if fichier.endswith('.csv'):  # Vérifier si le fichier est un fichier CSV
        chemin_fichier = os.path.join(dossier, fichier)

        # Vérifier si le nom du fichier contient "12"
        if '12' in fichier:
            # Lire le fichier CSV et ajouter ses données à la liste des données ayant "12" dans le nom
            donnees = pd.read_csv(chemin_fichier)
            donnees_debout.append(donnees)
        else:
            # Lire le fichier CSV et ajouter ses données à la liste des autres données
            donnes_allonge.append(pd.read_csv(chemin_fichier))

# Concaténer les données ayant "12" dans le nom
donnees_debout_all = pd.concat(donnees_debout, ignore_index=True)

# Concaténer les autres données
donnes_allonge_all = pd.concat(donnes_allonge, ignore_index=True)


# Appeler la fonction pour détecter les humains avec les RSSI
rssi_method(donnees_debout_all)
rssi_method(donnes_allonge_all)

# Liste pour stocker les postures détectées
postures = []

# Parcourir les données pour détecter la posture avec les données CSI
for index, row in donnees_debout_all.iterrows():
    detect_posture(eval(row['data']))

for index, row in donnes_allonge_all.iterrows():
    detect_posture(eval(row['data']))



# Afficher un graphique du RSSI au fil du temps
plt.plot(donnees_debout_all['timestamp'], donnees_debout_all['rssi'])
plt.xlabel('Temps')
plt.ylabel('RSSI (dBm)')
plt.title('RSSI au fil du temps debout')
plt.show()


# Afficher un graphique du RSSI au fil du temps
plt.plot(donnes_allonge_all['timestamp'], donnes_allonge_all['rssi'])
plt.xlabel('Temps')
plt.ylabel('RSSI (dBm)')
plt.title('RSSI au fil du temps allongé')
plt.show()

