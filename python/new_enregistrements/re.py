import os

dossier = "rien"
i = 0
for filename in os.listdir(dossier):
    # Chemin complet du fichier
    chemin_complet = os.path.join(dossier, filename)

    # Vérification si l'élément est un fichier
    if os.path.isfile(chemin_complet):
        # Obtention du nouveau nom de fichier en ajoutant le préfixe

        # Renommer le fichier
        os.rename(chemin_complet, f'rien/rien_{i}.csv')
        i+=1