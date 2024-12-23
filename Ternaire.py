import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mpltern
import matplotlib.pyplot as plt
import ttkbootstrap as tb


class TernaryDiagramApp:
    """
    Application pour créer et visualiser un diagramme ternaire interactif avec la bibliothèque mpltern.
    L'utilisateur peut saisir des données, ajouter des légendes, configurer les titres des axes et
    sauvegarder le graphique généré.
    """

    def __init__(self, master):
        """
        Initialise l'interface utilisateur et configure les composants de l'application.
        :param master: Fenêtre principale Tkinter (tk.Tk).
        """
        self.master = master
        self.master.title("Ternary Diagram Generator")
        self.data_list = []  # Liste pour stocker les données enregistrées

        # Configuration du style avec ttkbootstrap pour un look moderne
        self.style = tb.Style("litera")  # Choix d'un thème esthétique
        self.master.geometry("950x700")  # Dimensions initiales de la fenêtre

        # Créer les widgets principaux
        self.create_widgets()

    def create_widgets(self):
        """
        Crée les différents widgets de l'interface utilisateur :
        champs d'entrée, tableaux, boutons, et espace pour afficher le graphique.
        """
        # Section pour les entrées de données
        self.input_frame = ttk.Frame(self.master)
        self.input_frame.pack(pady=10, padx=10)

        # Champs A, B et C pour les proportions
        ttk.Label(self.input_frame, text="A:").grid(row=0, column=0, padx=5)
        self.entry_a = ttk.Entry(self.input_frame, width=10)
        self.entry_a.grid(row=1, column=0, padx=5)

        ttk.Label(self.input_frame, text="B:").grid(row=0, column=1, padx=5)
        self.entry_b = ttk.Entry(self.input_frame, width=10)
        self.entry_b.grid(row=1, column=1, padx=5)

        ttk.Label(self.input_frame, text="C:").grid(row=0, column=2, padx=5)
        self.entry_c = ttk.Entry(self.input_frame, width=10)
        self.entry_c.grid(row=1, column=2, padx=5)

        # Sélecteur de couleurs pour personnaliser les points
        ttk.Label(self.input_frame, text="Color:").grid(row=0, column=3, padx=5)
        self.color_button = ttk.Button(self.input_frame, text="Select Color", command=self.open_color_picker)
        self.color_button.grid(row=1, column=3, padx=5)
        self.color_label = ttk.Label(self.input_frame, text="No Color", background="white", relief="sunken", width=20)
        self.color_label.grid(row=1, column=4, padx=5)

        # Champ pour entrer une légende associée aux données
        ttk.Label(self.input_frame, text="Legend:").grid(row=0, column=5, padx=5)
        self.entry_legend = ttk.Entry(self.input_frame, width=15)
        self.entry_legend.grid(row=1, column=5, padx=5)

        # Section pour le titre du graphique
        self.chart_title_frame = ttk.Frame(self.master)
        self.chart_title_frame.pack(pady=10)

        ttk.Label(self.chart_title_frame, text="Chart Title:").grid(row=0, column=0, padx=5)
        self.chart_title_entry = ttk.Entry(self.chart_title_frame, width=30)
        self.chart_title_entry.grid(row=0, column=1, padx=5)

        # Section pour les titres des axes
        self.axis_frame = ttk.Frame(self.master)
        self.axis_frame.pack(pady=10)

        ttk.Label(self.axis_frame, text="Axis 1 Title:").grid(row=0, column=0, padx=5)
        self.axis1_entry = ttk.Entry(self.axis_frame, width=15)
        self.axis1_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.axis_frame, text="Axis 2 Title:").grid(row=0, column=2, padx=5)
        self.axis2_entry = ttk.Entry(self.axis_frame, width=15)
        self.axis2_entry.grid(row=0, column=3, padx=5)

        ttk.Label(self.axis_frame, text="Axis 3 Title:").grid(row=0, column=4, padx=5)
        self.axis3_entry = ttk.Entry(self.axis_frame, width=15)
        self.axis3_entry.grid(row=0, column=5, padx=5)

        # Tableau pour afficher les données enregistrées
        self.data_table = ttk.Treeview(self.master, columns=("A", "B", "C", "Color", "Legend"), show="headings", height=10)
        self.data_table.pack(pady=10, padx=10)
        self.data_table.heading("A", text="A")
        self.data_table.heading("B", text="B")
        self.data_table.heading("C", text="C")
        self.data_table.heading("Color", text="Color")
        self.data_table.heading("Legend", text="Legend")

        # Boutons pour les actions
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=10)

        self.submit_button = ttk.Button(self.button_frame, text="Submit", command=self.save_values)
        self.submit_button.grid(row=0, column=0, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Selected Row", command=self.delete_selected_row)
        self.delete_button.grid(row=0, column=1, padx=5)

        self.generate_button = ttk.Button(self.button_frame, text="Generate Ternary Plot", command=self.generate_ternary_plot)
        self.generate_button.grid(row=0, column=2, padx=5)

        self.save_plot_button = ttk.Button(self.button_frame, text="Save Plot", command=self.save_plot)
        self.save_plot_button.grid(row=0, column=3, padx=5)

        # Cadre pour le graphique généré
        self.plot_frame = ttk.Frame(self.master)
        self.plot_frame.pack(pady=10)

    def open_color_picker(self):
        """
        Ouvre un sélecteur de couleurs pour permettre à l'utilisateur de choisir une couleur.
        La couleur sélectionnée est affichée dans un label.
        """
        color_code = colorchooser.askcolor(title="Choose a Color")[1]
        if color_code:
            self.color_label.config(text=color_code, background=color_code)

    def save_values(self):
        """
        Enregistre les valeurs saisies (A, B, C, couleur, légende) après validation.
        Les données sont ajoutées à une liste et affichées dans un tableau.
        """
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            c = float(self.entry_c.get())
        except ValueError:
            messagebox.showerror("Input Error", "A, B, and C must be decimal numbers.")
            return

        if a + b + c != 100:
            messagebox.showerror("Input Error", "The sum of A, B, and C must be exactly 100.")
            return

        color = self.color_label.cget("text")
        if color == "No Color":
            messagebox.showerror("Input Error", "Please select a color.")
            return

        legend = self.entry_legend.get().strip()
        if not legend:
            messagebox.showerror("Input Error", "Legend cannot be empty.")
            return

        data = {"A": a, "B": b, "C": c, "Color": color, "Legend": legend}
        self.data_list.append(data)
        self.data_table.insert("", tk.END, values=(a, b, c, color, legend))

        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.entry_c.delete(0, tk.END)
        self.entry_legend.delete(0, tk.END)
        self.color_label.config(text="No Color", background="white")

    def delete_selected_row(self):
        """
        Supprime la ligne sélectionnée dans le tableau et dans la liste des données.
        """
        selected_item = self.data_table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a row to delete.")
            return

        for item in selected_item:
            index = self.data_table.index(item)
            self.data_table.delete(item)
            del self.data_list[index]

    def generate_ternary_plot(self):
        """
        Génère un diagramme ternaire avec les données enregistrées et l'affiche dans l'interface.
        """
        if not self.data_list:
            messagebox.showerror("Error", "No data available to generate the ternary plot.")
            return

        axis1 = self.axis1_entry.get().strip()
        axis2 = self.axis2_entry.get().strip()
        axis3 = self.axis3_entry.get().strip()

        if not axis1 or not axis2 or not axis3:
            messagebox.showerror("Input Error", "All axis titles must be specified.")
            return

        fig = plt.Figure(figsize=(10, 8))  # Augmentez la taille pour plus d'espace
        ax = fig.add_subplot(111, projection="ternary")

        ax.set_tlabel(axis1)
        ax.set_llabel(axis2)
        ax.set_rlabel(axis3)

        chart_title = self.chart_title_entry.get().strip()
        if chart_title:
            ax.set_title(chart_title, fontsize=16, pad=20)  # Ajoutez un espace supplémentaire avec `pad`

        for data in self.data_list:
            point = (data["A"] / 100, data["B"] / 100, data["C"] / 100)
            ax.scatter([point[0]], [point[1]], [point[2]], color=data["Color"], label=data["Legend"], s=100)

        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
        fig.tight_layout(rect=[0, 0, 1, 0.95])  # Réservez de l'espace pour le titre

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()

        self.current_plot = fig

    def save_plot(self):
        """
        Sauvegarde le diagramme ternaire généré sous forme d'image (PNG, JPEG, etc.).
        """
        if not self.data_list:
            messagebox.showerror("Error", "No data available to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.current_plot.savefig(file_path, bbox_inches="tight")
            messagebox.showinfo("Success", f"Plot saved to {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TernaryDiagramApp(root)
    root.mainloop()