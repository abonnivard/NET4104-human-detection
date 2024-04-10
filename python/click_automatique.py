import pyautogui
import time
import random
from playsound import playsound

# Définir l'intervalle de temps entre chaque clic (en secondes)
interval_temps = 10


# Fonction pour effectuer un clic à l'emplacement actuel de la souris et jouer un son
def effectuer_clic_et_jouer_son():
    x_clic, y_clic = pyautogui.position()
    print(f"Effectuer un clic à la position ({x_clic}, {y_clic})")
    pyautogui.click(x_clic, y_clic)
    son ="son.mp3"
    playsound(son)

# Boucle principale
try:
    while True:
        effectuer_clic_et_jouer_son()
        time.sleep(interval_temps)
except KeyboardInterrupt:
    print("\nArrêt du script.")
