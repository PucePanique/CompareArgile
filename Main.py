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
    # Créer le graphique et définir sa largeur
    if comment is None:
        comment = []
    plt.figure().set_figwidth(50)  # Ajuster la taille du graphique
    plt.subplots_adjust(left=0.05, right=0.990)
    plt.xticks(np.arange(400, 4000, step=100))  # Définir les ticks de l'axe des x
    plt.margins(x=0)  # Réduire les marges sur l'axe des x

    # Tracer les deux courbes avec les données x1, y1 et x2, y2
    plt.plot(x1, y1, label=file_name[0])
    plt.plot(x2, y2, label=file_name[1])

    decalage_texte = 0
    # Ajouter des commentaires pour chaque intervalle
    for com in comment:
        debut, fin = com["intervalle"]  # Intervalle sur l'axe des x
        commentaire = com["commentaire"]  # Texte du commentaire

        # Mettre en évidence l'intervalle sur le graphique avec une zone colorée
        plt.axvspan(debut, fin, color="orange", alpha=0.3)

        # Ajouter le texte au centre de l'intervalle
        milieu = (debut + fin) / 2  # Calculer le centre de l'intervalle
        plt.text(
            milieu,
            (max(max(y1), max(y2)) * 0.7) + decalage_texte,  # Positionner le texte au-dessus de la courbe
            commentaire,
            color="red",
            fontsize=10,
            ha="center",  # Alignement horizontal du texte
            bbox=dict(facecolor="white", alpha=0.3, edgecolor="red")  # Boîte autour du texte
        )
        decalage_texte += 0.115  # Décaler le texte pour éviter qu'ils ne se superposent

    # Ajouter des labels et une légende
    cmMathFormat = r"$\mathrm{cm}^{-1}$"
    plt.xlabel(f'Nombre d\'onde ({cmMathFormat})')  # Label de l'axe des x
    plt.ylabel('Absorbance')  # Label de l'axe des y
    plt.title(f'Graphique {folder_name}')  # Titre du graphique
    plt.legend()  # Ajouter la légende pour les courbes
    plt.gca().invert_xaxis()  # Inverser l'axe des x (pour les spectres)

    # Si 'save' est vrai, enregistrer le graphique dans un fichier
    if save:
        plt.savefig(folder_name)
    plt.show()  # Afficher le graphique, avec ou sans blocage de l'exécution


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
