import pyautogui
import time
from playsound import playsound



'''
Script pour effectuer un clic à l'emplacement actuel de la souris et jouer un son à intervalles réguliers.
Ce programme a été utilisé pour pouvoir déclencher l'enregistrement des données de capteurs à intervalles réguliers à partir de l'interface graphique du projet esp-csi.
'''

# Définir l'intervalle de temps entre chaque clic (en secondes)
interval_temps = 15
compteur = 0
son_liste = ["stop.m4a", "go.m4a"]
# Fonction pour effectuer un clic à l'emplacement actuel de la souris et jouer un son
def effectuer_clic_et_jouer_son(i):
    x_clic, y_clic = pyautogui.position()
    print(f"Effectuer un clic à la position ({x_clic}, {y_clic})")
    if i==0:
        pyautogui.click(x_clic, y_clic)
    son =son_liste[i]
    playsound(son)

# Boucle principale
try:
    i=0
    time.sleep(15)
    while compteur<20:
        if i==2:
            i=0
        effectuer_clic_et_jouer_son(i)
        i+=1
        time.sleep(interval_temps)
        compteur+=1
except KeyboardInterrupt:
    print("\nArrêt du script.")
