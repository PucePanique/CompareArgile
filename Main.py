import os
import csv
import matplotlib.pyplot as plt

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

    with open(full_path, newline='', mode='r') as csv_file:
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
plt.plot(x1, y1, label=file_name[0])
plt.plot(x2, y2, label=file_name[1])

# Ajouter des labels et une légende
plt.xlabel('Wave number (cm)')
plt.ylabel('Absorbance')
plt.title(f'Graphique {folder_name}')
plt.legend()
plt.gca().invert_xaxis()
# Afficher le graphique
plt.savefig(folder_name)