# Objectifs

## Détecter la chute d'une personne à l'aide des canaux CSI avec un ESP-32

Pour ce faire nous découpons la tâche en plusieurs étapes:

* Capturer le signal wifi avec un ESP-32
* Récupérer les CSI en C 
* Le programme en C sort un fichier .csv qui est annalysé en python
* On va récupérer le fichier .csv pour réécrire un programme python adapté à notre projet


## Tests de la solution

En se connectant à un routeur, l'optimalité des résultats est garantie si l'ESP-32 est le seul appareil connecté au routeur. Pour tester notre solution dans des condition sréelles, nous allons effectuer des tests en connectant d'autre appareils et un comparant les performances de la solution en fonction du nombre d'appareils connectés.

# Guide pratique

## Avant de démarrer:

* Brancher l'ESP-32 à l'ordinateur via le port UART et non USB


## Comment régler certains problèmes courants ?

### Core dump

    Warning: Ignoring XDG_SESSION_TYPE=wayland on Gnome. Use QT_QPA_PLATFORM=wayland to run on Wayland anyway.
    qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
    This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

    Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.

    open serial port:  /dev/ttyUSB0
    Abandon (core dumped)

Cela peut arriver lorsqu'il y a une incompatibilité entre 2 applications, pour y remédier on repète la commande précédée de:

    QT_QPA_PLATFORM=wayland !!

