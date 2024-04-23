# Créer l'environnement virtuel
setup:
	python3 -m venv env

# Installer les dépendances
install:
	. env/bin/activate && pip install -r requirements.txt && pip install --upgrade pip

# Démarrer le site
start-transmission:
	. env/bin/activate && python3 live-transmission.py -p /dev/cu.usbserial-2130

clean:
	rm -R env/