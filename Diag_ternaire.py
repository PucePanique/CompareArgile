import matplotlib.pyplot as plt
import mpltern

# Données pour le diagramme ternaire
# Les données doivent être dans le format : (A, B, C) où A + B + C = 100
data = [
    (70, 20, 10),  # Point 1
    (40, 40, 20),  # Point 2
    (20, 30, 50),  # Point 3
    (10, 80, 10),  # Point 4
]

# Séparer les données en trois listes
A, B, C = zip(*data)

# Création de la figure avec mpltern
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='ternary')

# Ajouter les points
ax.scatter(A, B, C, c='blue', marker='o', label='Points de données')

# Configurer les étiquettes des axes
ax.set_tlabel('AL2OH')
ax.set_llabel('FE2OH')
ax.set_rlabel('MG3OH')

# Ajouter un titre et une légende
ax.set_title('Exemple de diagramme ternaire')
ax.legend()

# Afficher le diagramme
plt.show()
