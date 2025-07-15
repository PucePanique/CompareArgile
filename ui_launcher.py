# ui_launcher.py

import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Button, Combobox, Separator
from tkinter import messagebox
import gettext

from Ternaire import TernaryDiagramApp
from config_manager import load_config, save_config

# Charger configuration XML
config = load_config()

# Traduction dynamique depuis XML
localedir = 'locales'
lang = gettext.translation('messages', localedir=localedir, languages=[config.get("language", "fr")], fallback=True)
lang.install()
_ = lang.gettext


class ApplicationLauncher:
    def __init__(self, master):
        self.master = master
        self.config = config  # accès local à la config

        # Initialisation du style avec thème depuis config
        self.style = Style(self.config.get("theme", "cosmo"))

        self.master.title(_("Application Launcher"))
        self.master.geometry(f'{self.config.get("window_width", "500")}x{self.config.get("window_height", "400")}')
        self.master.resizable(False, False)

        # Liste des thèmes dynamiques depuis config
        self.available_themes = [t.strip() for t in self.config.get("themes", "").split(",") if t.strip()]

        # Frame principale
        self.container = Frame(self.master, padding=30)
        self.container.pack(fill="both", expand=True)

        # Titre principal
        self.title = Label(
            self.container,
            text=_("🚀 Application Launcher"),
            font=(self.config.get("font", "Segoe UI"), 22, "bold"),
            anchor="center"
        )
        self.title.pack(pady=(0, 20))

        # Séparateur
        Separator(self.container).pack(fill="x", pady=10)

        # Choix du thème
        theme_row = Frame(self.container)
        theme_row.pack(pady=10)

        Label(theme_row, text=_("🎨 Theme:"), font=(self.config["font"], 12)).pack(side="left", padx=(0, 10))

        self.theme_var = tk.StringVar(value=self.config["theme"])
        self.theme_combo = Combobox(
            theme_row,
            textvariable=self.theme_var,
            values=self.available_themes,
            state="readonly",
            width=20
        )
        self.theme_combo.pack(side="left")
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # Zone de boutons
        button_frame = Frame(self.container, padding=10)
        button_frame.pack(pady=20)

        Button(
            button_frame,
            text=_("📈 Ternary Diagram App"),
            style="primary.TButton",
            width=30,
            command=self.launch_ternary_app
        ).pack(pady=8)

        Button(
            button_frame,
            text=_("🛠 Future App 1"),
            state="disabled",
            style="secondary.TButton",
            width=30
        ).pack(pady=8)

        Button(
            button_frame,
            text=_("🧪 Future App 2"),
            state="disabled",
            style="secondary.TButton",
            width=30
        ).pack(pady=8)

        Button(
            self.container,
            text=_("❌ Quit"),
            style="danger.TButton",
            width=20,
            command=self.confirm_quit
        ).pack(pady=(20, 5))

    def launch_ternary_app(self):
        new_root = tk.Tk()
        TernaryDiagramApp(new_root)
        self.master.destroy()

    def change_theme(self, event):
        selected_theme = self.theme_var.get()
        self.style.theme_use(selected_theme)
        self.config["theme"] = selected_theme
        save_config(self.config)

    def confirm_quit(self):
        if messagebox.askokcancel(_("Quit"), _("Are you sure you want to quit?")):
            self.master.quit()
