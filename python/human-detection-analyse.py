import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Charger les données CSI depuis le fichier CSV
data = pd.read_csv('2024-04-09_12-37-33-975_104_1.csv')

#Detect mouvement with CSI data
def data_method(data, timestamp):
    # Récupérer les données CSI de la ligne
    csi_data = eval(data)  # Convertir la chaîne de caractères en liste

    # Définir un seuil de détection de mouvement
    threshold = 7  # Seuil arbitraire, à ajuster selon les données et le contexte

    # Calculer une métrique de mouvement basée sur les données CSI
    # Par exemple, la métrique pourrait être la moyenne des amplitudes des signaux sur toutes les sous-porteuses
    mean_amplitude = sum(abs(value) for value in csi_data) / len(csi_data)
    # Comparer la métrique de mouvement au seuil de détection
    if mean_amplitude < threshold:
        movement_detected = True
        print(f"Moyenne des amplitudes : {mean_amplitude}, time : {timestamp}")

    else:
        movement_detected = False

    return movement_detected

# Fonction pour détecter la présence d'humains
def rssi_method(data):
    # Supprimer les colonnes non pertinentes
    data = data[['seq', 'timestamp', 'mac', 'rssi', 'data']]

    # Parcourir les données pour détecter les humains
    for index, row in data.iterrows():
        # Analyser les données CSI pour détecter les humains
        # Remplacez cette partie du code par votre algorithme de détection

        # Exemple simplifié : Si RSSI est supérieur à -60 dBm, on considère qu'un humain est présent
        if row['rssi'] > -60:
            print(f"Humain détecté à la séquence {row['seq']} à {row['timestamp']}")



# Appeler la fonction pour détecter les humains avec les RSSI
rssi_method(data)

# Appeler la fonction pour détecter le mouvement humains avec les datas
for index, row in data.iterrows():
    data_method(row.data, row.timestamp)

# Afficher un graphique du RSSI au fil du temps
plt.plot(data['timestamp'], data['rssi'])
plt.xlabel('Temps')
plt.ylabel('RSSI (dBm)')
plt.title('RSSI au fil du temps')
plt.show()
