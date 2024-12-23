import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style  # Pour un style moderne avec ttkbootstrap
from Ternaire import TernaryDiagramApp  # Importer la classe TernaryDiagramApp

class ApplicationLauncher:
    """
    Interface simple pour gérer plusieurs applications.
    Actuellement, un seul bouton permet de lancer TernaryDiagramApp.
    Deux autres boutons sont réservés pour des applications futures.
    """

    def __init__(self, master):
        """
        Initialise l'interface principale du lanceur d'applications.
        :param master: Fenêtre principale Tkinter (tk.Tk).
        """
        self.master = master
        self.master.title("Application Launcher")
        self.master.geometry("400x300")

        # Configuration du style avec ttkbootstrap
        self.style = Style("cosmo")  # Choisissez un thème esthétique

        # Titre de l'application
        self.title_label = ttk.Label(self.master, text="Application Launcher", font=("Helvetica", 16))
        self.title_label.pack(pady=20)

        # Cadre pour les boutons
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=20)

        # Bouton pour lancer TernaryDiagramApp
        self.ternary_button = ttk.Button(self.button_frame, text="Ternary Diagram App", command=self.launch_ternary_app)
        self.ternary_button.grid(row=0, column=0, padx=10, pady=10)

        # Bouton pour une application future 1 (désactivé pour le moment)
        self.future_button_1 = ttk.Button(self.button_frame, text="Future App 1", state="disabled")
        self.future_button_1.grid(row=1, column=0, padx=10, pady=10)

        # Bouton pour une application future 2 (désactivé pour le moment)
        self.future_button_2 = ttk.Button(self.button_frame, text="Future App 2", state="disabled")
        self.future_button_2.grid(row=2, column=0, padx=10, pady=10)

        # Bouton pour quitter l'application
        self.quit_button = ttk.Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.pack(pady=10)

    def launch_ternary_app(self):
        """
        Lance TernaryDiagramApp dans une nouvelle fenêtre.
        """
        new_window = tk.Toplevel(self.master)  # Crée une nouvelle fenêtre
        TernaryDiagramApp(new_window)  # Instancie TernaryDiagramApp dans la nouvelle fenêtre


if __name__ == "__main__":
    root = tk.Tk()
    launcher = ApplicationLauncher(root)
    root.mainloop()
