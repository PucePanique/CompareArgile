import os
import csv
import matplotlib.pyplot as plt
import numpy as np


def cree_graph(x1, x2, y1, y2, folder_name="", save=False, comment=None):
    """
    Fonction pour créer un graphique avec les données passées en paramètres.

    :param x1, x2: Listes des valeurs sur l'axe des abscisses (nombre d'ondes)
    :param y1, y2: Listes des valeurs sur l'axe des ordonnées (absorbance)
    :param folder_name: Nom du dossier ou fichier pour enregistrer le graphique
    :param save: Booléen pour enregistrer le graphique ou non
    :param comment: Liste de commentaires à afficher sur le graphique
    """
    if comment is None:
        comment = []

    # Création de la figure et d'un subplot
    fig, ax = plt.subplots(figsize=(15, 8))  # Taille de la figure

    # Tracer les deux courbes avec les données x1, y1 et x2, y2
    ax.plot(x1, y1, label="Bulk", color="blue")
    ax.plot(x2, y2, label="Infra", color="green")

    # Configuration de l'axe des x
    ax.set_xticks(np.arange(400, 4000, step=100))
    ax.margins(x=0)  # Réduire les marges sur l'axe des x
    ax.invert_xaxis()  # Inverser l'axe des x pour les spectres

    # Ajouter des labels et un titre
    cmMathFormat = r"$\mathrm{cm}^{-1}$"
    ax.set_xlabel(f'Nombre d\'onde ({cmMathFormat})', fontsize=14)
    ax.set_ylabel('Absorbance', fontsize=14)
    ax.set_title(f'Graphique {folder_name}', fontsize=16)

    # Ajouter une légende
    ax.legend(loc="upper right")

    # Ajouter des annotations et zones sur le graphique
    used_positions = []  # Liste pour suivre les positions utilisées
    max_y = max(max(y1), max(y2)) * 0.7
    min_y = max(max(y1), max(y2)) * 0.1

    for com in comment:
        debut, fin = com["intervalle"]
        commentaire = com["commentaire"]

        # Mettre en évidence l'intervalle avec une zone colorée
        ax.axvspan(debut, fin, color="orange", alpha=0.3)

        # Ajouter le texte au centre de l'intervalle
        milieu = (debut + fin) / 2
        position_y = max_y

        # Assurer que les textes ne se superposent pas et restent dans la zone
        while position_y in used_positions or position_y > max_y:
            position_y -= 0.07

        # Réinitialiser à une position intermédiaire si trop bas
        if position_y < min_y:
            position_y = (max_y + min_y) / 2

        used_positions.append(position_y)

        ax.text(
            milieu,
            position_y,
            commentaire,
            color="red",
            fontsize=10,
            ha="center",
            bbox=dict(facecolor="white", alpha=0.3, edgecolor="red")
        )

    # Ajuster les marges de la figure
    plt.subplots_adjust(left=0.05, right=0.95)

    # Sauvegarder ou afficher le graphique
    if save and folder_name:
        plt.savefig(f"{folder_name}.png", dpi=300)
    else:
        plt.show()


# Demander le chemin du répertoire contenant les fichiers de données
clay_path = ""
clay_path_exist = False
while not clay_path_exist:
    clay_path = input("Entrer le chemin du répertoire: ")  # Demander à l'utilisateur le chemin du répertoire
    if os.path.exists(clay_path):
        clay_path_exist = True  # Vérifier que le chemin existe

folder_name = os.path.basename(clay_path)  # Extraire le nom du dossier

# Initialiser les listes pour stocker les données
bulk = []  # Données brutes
treat = []  # Données traitées
cur_file = 0  # Compteur pour suivre le fichier traité (0 ou 1)
file_name = []  # Liste pour stocker les noms de fichiers sans extension

# Parcourir les fichiers du répertoire
for file in os.listdir(clay_path):

    file_name.append(os.path.splitext(os.path.basename(file))[0])  # Extraire le nom sans extension
    full_path = os.path.join(clay_path, file)  # Obtenir le chemin complet du fichier

    with open(full_path, newline='') as csv_file:  # Ouvrir le fichier CSV
        reader = csv.reader(csv_file, delimiter=';', quotechar='"')  # Créer un lecteur CSV
        for line in reader:
            if cur_file == 0:  # Si c'est le premier fichier (données brutes)
                bulk.append((float(line[0].replace(',', '.')),
                             float(line[1].replace(',', '.'))))  # Ajouter les données dans la liste "bulk"
            if cur_file == 1:  # Si c'est le deuxième fichier (données traitées)
                treat.append((float(line[0].replace(',', '.')),
                              float(line[1].replace(',', '.'))))  # Ajouter les données dans la liste "treat"
        cur_file += 1  # Passer au fichier suivant

# Séparer les valeurs x et y pour chaque fichier
x1, y1 = zip(*bulk)
x2, y2 = zip(*treat)

# Afficher le graphique avec les données des deux fichiers
cree_graph(x1, x2, y1, y2, folder_name)


# Fonction pour demander des commentaires à l'utilisateur
def demander_commentaires():
    commentaires = []  # Liste pour stocker les commentaires
    print("\nAprès avoir vu le graphique, vous pouvez ajouter des commentaires sur des intervalles spécifiques.")
    print("Entrez 'stop' à tout moment pour terminer.")
    nbcomment = 0  # Compteur de commentaires
    while True:
        debut = input("Début de l'intervalle (ou 'stop' pour terminer) : ")  # Demander le début de l'intervalle
        if debut.lower() == 'stop':
            break  # Arrêter si l'utilisateur entre 'stop'
        fin = input("Fin de l'intervalle : ")  # Demander la fin de l'intervalle
        commentaire = input("Commentaire pour cet intervalle : ")  # Demander le commentaire

        try:
            debut = float(debut)  # Convertir le début en nombre
            fin = float(fin)  # Convertir la fin en nombre
            commentaires.append({"intervalle": (debut, fin), "commentaire": commentaire})  # Ajouter le commentaire

            # Réafficher le graphique avec les commentaires ajoutés
            cree_graph(x1, x2, y1, y2, folder_name, comment=commentaires)

            # Demander à l'utilisateur si le commentaire convient
            intervalok = input("Le commentaire convient-il ? (oui/non) : ")
            if intervalok == "non":
                commentaires.pop(nbcomment)  # Supprimer le commentaire si non validé
            else:
                nbcomment += 1  # Ajouter un nouveau commentaire si validé
        except ValueError:
            print("Veuillez entrer des nombres valides pour les intervalles.")  # Gestion des erreurs de saisie

    return commentaires


# Récupérer les commentaires de l'utilisateur
commentaires_utilisateur = demander_commentaires()

# Créer un graphique final avec les commentaires et sauvegarder l'image
cree_graph(x1, x2, y1, y2, folder_name, comment=commentaires_utilisateur, save=True)
