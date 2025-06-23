import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style  # Pour un style moderne avec ttkbootstrap
from Ternaire import TernaryDiagramApp  # Importer la classe TernaryDiagramApp
import gettext

# Initialisation de gettext
localedir = 'locales'
lang = gettext.translation('messages', localedir=localedir, languages=['fr'], fallback=True)
lang.install()
_ = lang.gettext

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
        self.master.title(_("Application Launcher"))
        self.master.geometry("400x300")

        # Configuration du style avec ttkbootstrap
        self.style = Style("cosmo")  # Choisissez un thème esthétique

        # Définition des styles
        self.styles = {
            'title_font': ("Helvetica", 16),
            'button_font': ("Helvetica", 12),
            'padding': {'padx': 10, 'pady': 10}
        }

        # Titre de l'application
        self.title_label = ttk.Label(self.master, text=_("Application Launcher"), font=self.styles['title_font'])
        self.title_label.pack(pady=20)

        # Cadre pour les boutons
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=20)

        # Bouton pour lancer TernaryDiagramApp
        self.ternary_button = ttk.Button(
            self.button_frame, 
            text=_("Ternary Diagram App"), 
            command=self.launch_ternary_app, 
            style='TButton'
        )
        self.ternary_button.grid(row=0, column=0, **self.styles['padding'])

        # Bouton pour une application future 1 (désactivé pour le moment)
        self.future_button_1 = ttk.Button(self.button_frame, text=_("Future App 1"), state="disabled")
        self.future_button_1.grid(row=1, column=0, **self.styles['padding'])

        # Bouton pour une application future 2 (désactivé pour le moment)
        self.future_button_2 = ttk.Button(self.button_frame, text=_("Future App 2"), state="disabled")
        self.future_button_2.grid(row=2, column=0, **self.styles['padding'])

        # Bouton pour quitter l'application
        self.quit_button = ttk.Button(self.master, text=_("Quit"), command=self.master.quit)
        self.quit_button.pack(pady=10)

    def launch_ternary_app(self):
        """
        Lance TernaryDiagramApp dans une nouvelle fenêtre et ferme le menu principal.
        """
        # Crée une nouvelle fenêtre principale pour l'app ternaire
        new_root = tk.Tk()
        TernaryDiagramApp(new_root)
        self.master.destroy()  # Ferme le menu principal


if __name__ == "__main__":
    root = tk.Tk()
    launcher = ApplicationLauncher(root)
    root.mainloop()
