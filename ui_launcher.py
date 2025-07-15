# ui_launcher.py

import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Button, Combobox, Notebook, Entry
from tkinter import messagebox
import gettext

from Ternaire import TernaryDiagramApp
from config_manager import load_config, save_config

# Charger configuration
config = load_config()

# Traduction
localedir = 'locales'
lang = gettext.translation('messages', localedir=localedir, languages=[config.get("language", "fr")], fallback=True)
lang.install()
_ = lang.gettext


class ApplicationLauncher:
    def __init__(self, master):
        self.master = master
        self.config = config

        self.style = Style(self.config.get("theme", "cosmo"))
        self.master.title(_("Application Launcher"))
        self.master.geometry(f'{self.config.get("window_width", "500")}x{self.config.get("window_height", "400")}')
        self.master.resizable(False, False)

        self.font_choices = ["Segoe UI", "Arial", "Courier", "Verdana"]
        self.language_choices = ["fr", "en"]
        self.theme_choices = [t.strip() for t in self.config.get("themes", "")]

        # Notebook (tabs)
        self.notebook = Notebook(self.master, padding=10)
        self.notebook.pack(fill="both", expand=True)

        # --- Onglet Accueil ---
        self.home_tab = Frame(self.notebook)
        self.notebook.add(self.home_tab, text=_("🏠 Home"))

        Label(self.home_tab, text=_("🚀 Application Launcher"), font=(self.config["font"], 20, "bold")).pack(pady=10)

        Button(
            self.home_tab, text=_("📈 Ternary Diagram App"),
            style="primary.TButton", width=30, command=self.launch_ternary_app
        ).pack(pady=10)

        Button(
            self.home_tab, text=_("❌ Quit"),
            style="danger.TButton", width=20, command=self.confirm_quit
        ).pack(pady=10)

        # --- Onglet Paramètres ---
        self.settings_tab = Frame(self.notebook)
        self.notebook.add(self.settings_tab, text=_("⚙️ Settings"))

        self.build_settings_tab()

    def build_settings_tab(self):
        padding = {"padx": 10, "pady": 5}

        # Langue
        Label(self.settings_tab, text=_("Language:"), font=(self.config["font"], 12)).grid(row=0, column=0, sticky="w", **padding)
        self.lang_var = tk.StringVar(value=self.config.get("language", "fr"))
        lang_combo = Combobox(self.settings_tab, textvariable=self.lang_var, values=self.language_choices, state="readonly")
        lang_combo.grid(row=0, column=1, **padding)

        # Thème
        Label(self.settings_tab, text=_("Theme:"), font=(self.config["font"], 12)).grid(row=1, column=0, sticky="w", **padding)
        self.theme_var = tk.StringVar(value=self.config.get("theme", "cosmo"))
        theme_combo = Combobox(self.settings_tab, textvariable=self.theme_var, values=self.theme_choices, state="readonly")
        theme_combo.grid(row=1, column=1, **padding)

        # Police
        Label(self.settings_tab, text=_("Font:"), font=(self.config["font"], 12)).grid(row=2, column=0, sticky="w", **padding)
        self.font_var = tk.StringVar(value=self.config.get("font", "Segoe UI"))
        font_combo = Combobox(self.settings_tab, textvariable=self.font_var, values=self.font_choices, state="readonly")
        font_combo.grid(row=2, column=1, **padding)

        # Taille fenêtre
        Label(self.settings_tab, text=_("Window Width:"), font=(self.config["font"], 12)).grid(row=3, column=0, sticky="w", **padding)
        self.width_var = tk.StringVar(value=self.config.get("window_width", "500"))
        Entry(self.settings_tab, textvariable=self.width_var, width=10).grid(row=3, column=1, **padding)

        Label(self.settings_tab, text=_("Window Height:"), font=(self.config["font"], 12)).grid(row=4, column=0, sticky="w", **padding)
        self.height_var = tk.StringVar(value=self.config.get("window_height", "400"))
        Entry(self.settings_tab, textvariable=self.height_var, width=10).grid(row=4, column=1, **padding)

        # Bouton appliquer
        Button(
            self.settings_tab,
            text=_("💾 Apply & Save"),
            style="success.TButton",
            command=self.save_settings
        ).grid(row=5, column=0, columnspan=2, pady=20)

    def launch_ternary_app(self):
        new_root = tk.Tk()
        TernaryDiagramApp(new_root)
        self.master.destroy()

    def save_settings(self):
        # Met à jour la config
        self.config["theme"] = self.theme_var.get()
        self.config["language"] = self.lang_var.get()
        self.config["font"] = self.font_var.get()
        self.config["window_width"] = self.width_var.get()
        self.config["window_height"] = self.height_var.get()

        save_config(self.config)
        messagebox.showinfo(_("Settings"), _("Settings saved. Please restart the application to apply language and size changes."))

    def confirm_quit(self):
        if messagebox.askokcancel(_("Quit"), _("Are you sure you want to quit?")):
            self.master.quit()

