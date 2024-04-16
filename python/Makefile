# Créer l'environnement virtuel
setup:
	python3 -m venv env

# Installer les dépendances
install:
	. env/bin/activate && pip install -r requirements.txt && pip install --upgrade pip

# Démarrer le site
start-data:
	. env/bin/activate && python3 human-detection-analyse.py

start-click:
	. env/bin/activate && python3 click_automatique.py

start-ML:
	. env/bin/activate && python3 ML.py

clean:
	rm -R env/

