import os
import csv
import matplotlib.pyplot as plt
import numpy as np

clay_path = ""
clay_path_exist = False
while not clay_path_exist:
    clay_path = input("Entrer le chemin du répèrtoire: ")
    if os.path.exists(clay_path):
        clay_path_exist = True

folder_name = os.path.basename(clay_path)

bulk = []
treat = []
cur_file = 0
file_name=[]
for file in os.listdir(clay_path):

    file_name.append(os.path.splitext(os.path.basename(file))[0])
    full_path = os.path.join(clay_path,file)

    with open(full_path, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=';', quotechar='"')
        for line in reader:
            if cur_file==0:
                bulk.append((float(line[0].replace(',', '.')) , float(line[1].replace(',', '.'))))
            if cur_file == 1:
                treat.append((float(line[0].replace(',', '.')), float(line[1].replace(',', '.'))))
        cur_file += 1

x1, y1 = zip(*bulk)
x2, y2 = zip(*treat)

# Créer le graphique
plt.figure().set_figwidth(30)
plt.xticks(np.arange(400,4000,step=200))
plt. margins(x=0)

plt.plot(x1, y1, label=file_name[0])
plt.plot(x2, y2, label=file_name[1])

# Ajouter des labels et une légende
plt.xlabel('Wavenumber (cm^-1)')
plt.ylabel('Absorbance')
plt.title(f'Graphique {folder_name}')
plt.legend()
plt.gca().invert_xaxis()
#plt.show()
# Afficher le graphique
plt.savefig(folder_name)

# Fonction pour demander des commentaires
def demander_commentaires():
    commentaires = []
    print("\nAprès avoir vu le graphique, vous pouvez ajouter des commentaires sur des intervalles spécifiques.")
    print("Entrez 'stop' à tout moment pour terminer.")

    while True:
        debut = input("Début de l'intervalle (ou 'stop' pour terminer) : ")
        if debut.lower() == 'stop':
            break
        fin = input("Fin de l'intervalle : ")
        commentaire = input("Commentaire pour cet intervalle : ")

        try:
            debut = float(debut)
            fin = float(fin)
            commentaires.append({"intervalle": (debut, fin), "commentaire": commentaire})
        except ValueError:
            print("Veuillez entrer des nombres valides pour les intervalles.")

    return commentaires

# Récupérer les commentaires
commentaires_utilisateur = demander_commentaires()


# Créer le graphique
plt.figure().set_figwidth(30)
plt.xticks(np.arange(400, 4000, step=100))
plt.margins(x=0)

# Tracer les courbes
plt.plot(x1, y1, label=file_name[0])
plt.plot(x2, y2, label=file_name[1])


# Ajout des commentaires sur le graphique
decalage_texte = 0
for com in commentaires_utilisateur:
    debut, fin = com["intervalle"]
    commentaire = com["commentaire"]

    # Mettre en évidence l'intervalle
    plt.axvspan(debut, fin, color="orange", alpha=0.3)

    # Ajouter le texte au centre de l'intervalle
    milieu = (debut + fin) / 2
    plt.text(
        milieu,
        (max(max(y1), max(y2)) * 0.7)+decalage_texte,  # Placer le texte vers le haut du graphique
        commentaire,
        color="red",
        fontsize=10,
        ha="center",
        bbox=dict(facecolor="white", alpha=0.7, edgecolor="red")
    )
    decalage_texte += 0.15

# Ajouter des labels, une légende et inverser l'axe x
plt.xlabel('Wavenumber (cm^-1)')
plt.ylabel('Absorbance')
plt.title(f'Graphique {folder_name}')
plt.legend()
plt.gca().invert_xaxis()

# Afficher le graphique
#plt.show()
plt.savefig(folder_name)


