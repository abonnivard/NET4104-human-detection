# Objectifs

## Détecter la chute d'une personne à l'aide des canaux CSI avec un ESP-32

Pour ce faire nous découpons la tâche en plusieurs étapes:

* Capturer le signal wifi avec un ESP-32
* Récupérer les CSI en C 
* Le programme en C sort un fichier .csv qui est annalysé en python
* On va récupérer le fichier .csv pour réécrire un programme python adapté à notre projet


## Tests de la solution

En se connectant à un routeur, l'optimalité des résultats est garantie si l'ESP-32 est le seul appareil connecté au routeur. Pour tester notre solution dans des condition sréelles, nous allons effectuer des tests en connectant d'autre appareils et un comparant les performances de la solution en fonction du nombre d'appareils connectés.

