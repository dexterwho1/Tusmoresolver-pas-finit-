import os
from unidecode import unidecode

# ouvre le fichier lexique.txt en mode lecture avec l'encodage UTF-8
with open("lexique.txt", "r", encoding="utf-8") as f:
    # lit le contenu du fichier ligne par ligne
    lines = f.readlines()
    # boucle pour chaque ligne dans le fichier
    for line in lines:
        # enlever les espace en debut et fin de ligne
        word = line.strip()
        # déterminer la longueur du mot
        word_length = len(word)
        # créer un nom de dossier en utilisant la longueur du mot
        folder_name = str(word_length) + "letters"
        # vérifier si le dossier existe déjà, sinon le créer
        os.makedirs(folder_name, exist_ok=True)
        # supprimer les accents du mot
        unaccented_word = unidecode(word)
        # prendre la première lettre du mot sans accent
        first_letter = unaccented_word[0]
        # créer un nom de fichier en utilisant la longueur et la première lettre
        file_name = folder_name + "/" + first_letter + ".txt"
        # vérifier si le fichier existe déjà, sinon le créer
        if not os.path.exists(file_name):
            with open(file_name, "w", encoding="utf-8") as f:
                pass
        # ajouter le mot au fichier
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(word + "\n")