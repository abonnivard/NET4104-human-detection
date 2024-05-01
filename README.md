## NET4104-human-detection

Projet du cours NET4104 - Internet sans fil : concepts, technologies et architectures

# Objectifs

## Détecter la chute d'une personne à l'aide des canaux CSI avec un ESP-32

Pour ce faire nous découpons la tâche en plusieurs étapes:

* Connecter un esp-32 à un ordinateur via le port UART
* Connecter un esp-32 à un routeur wifi
* Récupérer les CSI à l'aide d'un programme
* Le programme enregistre les données capturés dans des fichier .csv qui sont ensuite analysés en python.
* Entraîner un modèle de machine learning pour détecter la chute d'une personne à partir des fichier .csv enregistrés.
* Écrire un programme python capable de récupérer les données en temps réel et d'en faire une prédiction instantanée.



# Guide de démarrage

```bash
git submodule update --init --recursive
```

* Brancher l'ESP-32 à l'ordinateur via le port UART et non USB
* Ouvrir le terminal et se placer dans le dossier `esp-idf` et exécuter les commandes suivantes:

```bash
cd esp-idf
git checkout v5.0.2
git submodule update --init --recursive
./install.sh
. ./export.sh
```

* Se placer dans le dossier `esp-csi` et exécuter les commandes suivantes:

Attention à bien vérifier que le port UART est le bon

Sur linux le port UART est généralement `/dev/ttyUSB0` ou `/dev/ttyUSB1`
```bash
ls /dev/ttyUSB*
```

Sur MacOS le port UART est généralement `/dev/cu.SLAB_USBtoUART`
```bash
ls /dev/cu.*
```

```bash
cd esp-csi/examples/console_test
idf.py set-target esp32s3
idf.py flash -b 921600 -p /dev/ttyUSB1
```

* Pour accèder à l'interface du projet esp-csi, exécuter la commande suivante:

```bash
cd esp-csi/examples/console_test/tools
# Install python related dependencies
pip install -r requirements.txt
# Graphical display
python esp_csi_tool.py -p /dev/ttyUSB1
```

* Lacement de la transmission des données.

1. Remplacer les valeurs de `SSID` et `PASSWORD` dans le fichier `live-transmission.py` par les valeurs de votre réseau wifi

2. Exécuter les commandes suivantes:

```bash
cd live-transmission/
make setup
make install
make start-transmission
```

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



