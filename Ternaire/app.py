# app.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import gettext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mpltern
import ttkbootstrap as tb
import csv
import sys

from config_manager import CONFIG_FILE
from .validators import validate_abc, validate_color, validate_legend
from .tooltips import CreateToolTip

_ = gettext.gettext

class TernaryDiagramApp:
    def __init__(self, master):
        self.master = master
        self.master.title(_("Ternary Diagram Generator"))
        self.data_list = []
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.style = tb.Style(CONFIG_FILE['style_theme'])
        self.master.geometry(CONFIG_FILE['window_size'])
        self.create_widgets()

    def create_widgets(self):
        # Section titre du graphique
        self.chart_title_frame = ttk.Frame(self.master)
        self.chart_title_frame.pack(pady=5)
        ttk.Label(self.chart_title_frame, text=_("Chart Title:")).grid(row=0, column=0, padx=5)
        self.chart_title_entry = ttk.Entry(self.chart_title_frame, width=30)
        self.chart_title_entry.grid(row=0, column=1, padx=5)

        # Section titres des axes
        self.axis_frame = ttk.Frame(self.master)
        self.axis_frame.pack(pady=5)
        ttk.Label(self.axis_frame, text=_("Axis 1 Title:")).grid(row=0, column=0, padx=5)
        self.axis1_entry = ttk.Entry(self.axis_frame, width=15)
        self.axis1_entry.grid(row=0, column=1, padx=5)
        ttk.Label(self.axis_frame, text=_("Axis 2 Title:")).grid(row=0, column=2, padx=5)
        self.axis2_entry = ttk.Entry(self.axis_frame, width=15)
        self.axis2_entry.grid(row=0, column=3, padx=5)
        ttk.Label(self.axis_frame, text=_("Axis 3 Title:")).grid(row=0, column=4, padx=5)
        self.axis3_entry = ttk.Entry(self.axis_frame, width=15)
        self.axis3_entry.grid(row=0, column=5, padx=5)

         # Section pour la sélection de police et les dimensions
        self.font_frame = ttk.Frame(self.master)
        self.font_frame.pack(pady=10)

        ttk.Label(self.font_frame, text=_("Select Font:")).grid(row=0, column=0, padx=5)
        self.font_var = tk.StringVar(value=CONFIG_FILE['default_font'])
        self.font_dropdown = ttk.Combobox(
            self.font_frame, textvariable=self.font_var,
            values=CONFIG_FILE['font_choices']
        )
        self.font_dropdown.grid(row=0, column=1, padx=5)
        self.font_dropdown.state(["readonly"])

        ttk.Label(self.font_frame, text=_("Width (cm):")).grid(row=0, column=2, padx=5)
        self.width_var = tk.DoubleVar(value=CONFIG_FILE['default_width_cm'])
        self.width_entry = ttk.Entry(self.font_frame, textvariable=self.width_var, width=10)
        self.width_entry.grid(row=0, column=3, padx=5)

        ttk.Label(self.font_frame, text=_("Height (cm):")).grid(row=0, column=4, padx=5)
        self.height_var = tk.DoubleVar(value=CONFIG_FILE['default_height_cm'])
        self.height_entry = ttk.Entry(self.font_frame, textvariable=self.height_var, width=10)
        self.height_entry.grid(row=0, column=5, padx=5)

        # Section entrées A, B, C, Couleur, Légende
        self.input_frame = ttk.Frame(self.master)
        self.input_frame.pack(pady=10, padx=10)

        ttk.Label(self.input_frame, text="A:").grid(row=0, column=0, padx=5)
        self.entry_a = ttk.Entry(self.input_frame, width=10)
        self.entry_a.grid(row=1, column=0, padx=5)
        self.entry_a.bind("<Return>", lambda e: self.entry_b.focus_set())

        ttk.Label(self.input_frame, text="B:").grid(row=0, column=1, padx=5)
        self.entry_b = ttk.Entry(self.input_frame, width=10)
        self.entry_b.grid(row=1, column=1, padx=5)
        self.entry_b.bind("<Return>", lambda e: self.entry_c.focus_set())

        ttk.Label(self.input_frame, text="C:").grid(row=0, column=2, padx=5)
        self.entry_c = ttk.Entry(self.input_frame, width=10)
        self.entry_c.grid(row=1, column=2, padx=5)
        self.entry_c.bind("<Return>", lambda e: self.color_button.focus_set())

        ttk.Label(self.input_frame, text=_("Color:")).grid(row=0, column=3, padx=5)
        self.color_button = ttk.Button(self.input_frame, text=_("Select Color"), command=self.open_color_picker)
        self.color_button.grid(row=1, column=3, padx=5)
        self.color_button.tooltip = CreateToolTip(self.color_button, _("Choose a color for the point"))
        self.color_label = ttk.Label(self.input_frame, text=CONFIG_FILE['color_default'], background=CONFIG_FILE['color_bg'], relief="sunken", width=20)
        self.color_label.grid(row=1, column=4, padx=5)

        ttk.Label(self.input_frame, text=_("Legend:")).grid(row=0, column=5, padx=5)
        self.entry_legend = ttk.Entry(self.input_frame, width=15)
        self.entry_legend.grid(row=1, column=5, padx=5)
        self.entry_legend.bind("<Return>", lambda e: self.submit_button.focus_set())

        #Bouton d'enregistrement
        self.submit_button = ttk.Button(self.input_frame, text=_("Submit"), command=self.save_values)
        self.submit_button.grid(row=1, column=6, padx=5)
        self.submit_button.tooltip = CreateToolTip(self.submit_button, _("Add the data to the table"))
        self.master.bind('<Control-Return>', lambda e: self.save_values())

        # Tableau pour afficher les données enregistrées
        self.data_table = ttk.Treeview(self.master, columns=("A", "B", "C", "Color", "Legend"), show="headings", height=10)
        self.data_table.pack(pady=10, padx=10)
        for col in ("A", "B", "C", "Color", "Legend"):
            self.data_table.heading(col, text=_(col))

        # Boutons pour les actions        
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=10)
        
        self.delete_button = ttk.Button(self.button_frame, text=_("Delete Selected Row"), command=self.delete_selected_row)
        self.delete_button.grid(row=0, column=1, padx=5)
        self.delete_button.tooltip = CreateToolTip(self.delete_button, _("Delete the selected row from the table"))

        self.generate_button = ttk.Button(self.button_frame, text=_("Generate Ternary Plot"), command=self.generate_ternary_plot)
        self.generate_button.grid(row=0, column=2, padx=5)
        self.generate_button.tooltip = CreateToolTip(self.generate_button, _("Generate the ternary plot from the data"))

        self.save_plot_button = ttk.Button(self.button_frame, text=_("Save Plot"), command=self.save_plot)
        self.save_plot_button.grid(row=0, column=3, padx=5)
        self.save_plot_button.tooltip = CreateToolTip(self.save_plot_button, _("Save the current plot as an image"))

        self.import_button = ttk.Button(self.button_frame, text=_("Import CSV"), command=self.import_csv)
        self.import_button.grid(row=0, column=4, padx=5)
        self.import_button.tooltip = CreateToolTip(self.import_button, _("Import data from a CSV file"))

        self.export_button = ttk.Button(self.button_frame, text=_("Export CSV"), command=self.export_csv)
        self.export_button.grid(row=0, column=5, padx=5)
        self.export_button.tooltip = CreateToolTip(self.export_button, _("Export table data to a CSV file"))

        # Cadre pour le graphique généré
        self.plot_frame = ttk.Frame(self.master)
        self.plot_frame.pack(pady=10, expand=True, fill='both')

    # --- 2. Gestion de la fermeture ---
    def on_close(self):
        self.master.destroy()
        if hasattr(sys, 'exit'):
            sys.exit(0)

    def open_color_picker(self):
        color_code = colorchooser.askcolor(title=_("Choose a Color"))[1]
        if color_code:
            self.color_label.config(text=color_code, background=color_code)

    def save_values(self):
        a = self.entry_a.get()
        b = self.entry_b.get()
        c = self.entry_c.get()
        legend = self.entry_legend.get()
        color = self.color_label.cget("text")

        # --- 5. Utilisation de la logique métier testable ---
        valid, msg = validate_abc(a, b, c)
        if not valid:
            messagebox.showerror(_("Input Error"), msg)
            return

        valid, msg = validate_color(color)
        if not valid:
            messagebox.showerror(_("Input Error"), msg)
            return

        valid, msg = validate_legend(legend)
        if not valid:
            messagebox.showerror(_("Input Error"), msg)
            return


        data = {"A": float(a), "B": float(b), "C": float(c), "Color": color, "Legend": legend}
        self.data_list.append(data)
        self.data_table.insert("", tk.END, values=(a, b, c, color, legend))

        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.entry_c.delete(0, tk.END)
        self.entry_legend.delete(0, tk.END)
        self.color_label.config(text=CONFIG_FILE['color_default'], background=CONFIG_FILE['color_bg'])

    def delete_selected_row(self):
        selected_item = self.data_table.selection()
        if not selected_item:
            messagebox.showerror(_("Selection Error"), _("Please select a row to delete."))
            return

        for item in selected_item:
            index = self.data_table.index(item)
            self.data_table.delete(item)
            del self.data_list[index]

    def generate_ternary_plot(self):
        if not self.data_list:
            messagebox.showerror(_("Error"), _("No data available to generate the ternary plot."))
            return

        axis1 = self.axis1_entry.get().strip()
        axis2 = self.axis2_entry.get().strip()
        axis3 = self.axis3_entry.get().strip()

        if not axis1 or not axis2 or not axis3:
            messagebox.showerror(_("Input Error"), _("All axis titles must be specified."))
            return

        selected_font = self.font_var.get()
        fig = plt.Figure(figsize=CONFIG_FILE['plot_figsize'])
        ax = fig.add_subplot(111, projection="ternary")

        ax.set_tlabel(axis1, fontsize=CONFIG_FILE['axis_fontsize'], fontname=selected_font, labelpad=15)
        ax.set_llabel(axis2, fontsize=CONFIG_FILE['axis_fontsize'], fontname=selected_font, labelpad=15)
        ax.set_rlabel(axis3, fontsize=CONFIG_FILE['axis_fontsize'], fontname=selected_font, labelpad=15)

        chart_title = self.chart_title_entry.get().strip()
        if chart_title:
            ax.set_title(chart_title, fontsize=CONFIG_FILE['title_fontsize'], fontname=selected_font, pad=30)

        ax.grid(True, which="both", color="grey", linestyle="--", linewidth=0.3)

        # --- Group points by (color, legend) ---
        grouped = {}
        for data in self.data_list:
            legend = data["Legend"].strip() or _("")
            key = (data["Color"], legend)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append((data["A"] / 100, data["B"] / 100, data["C"] / 100))

        # Plot each group, one legend entry per group
        for (color, legend), points in grouped.items():
            a_vals = [p[0] for p in points]
            b_vals = [p[1] for p in points]
            c_vals = [p[2] for p in points]
            if legend != "No Legend":
                ax.scatter(
                    a_vals, b_vals, c_vals,
                    color=color, marker="x", label=legend, s=25
                )

        ax.legend(
            loc=CONFIG_FILE['legend_loc'],
            bbox_to_anchor=CONFIG_FILE['legend_bbox'],
            ncol=CONFIG_FILE['legend_ncol'],
            prop={"family": selected_font, "size": CONFIG_FILE['legend_fontsize']}
        )

        fig.tight_layout(rect=[0.05, 0.05, 0.95, 0.9])

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.get_tk_widget().pack(expand=True, fill="both")
        canvas.draw()

        self.current_plot = fig

    def save_plot(self):
        if not self.data_list:
            messagebox.showerror(_("Error"), _("No data available to save."))
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[(_("PNG files"), "*.png"), (_("JPEG files"), "*.jpg"), (_("All files"), "*.*")]
        )
        if not file_path:
            return

        try:
            width_cm = self.width_var.get()
            height_cm = self.height_var.get()
            width_inch = width_cm * 0.393701
            height_inch = height_cm * 0.393701
        except tk.TclError:
            messagebox.showerror(_("Input Error"), _("Width and Height must be valid numbers."))
            return

        if width_inch <= 0 or height_inch <= 0:
            messagebox.showerror(_("Input Error"), _("Width and Height must be greater than 0."))
            return

        try:
            self.current_plot.set_size_inches(width_inch, height_inch)
            self.current_plot.savefig(file_path, bbox_inches="tight")
            messagebox.showinfo(_("Success"), _("Plot saved to {0}").format(file_path))
        except Exception as e:
            messagebox.showerror(_("Save Error"), _("Failed to save the plot: {0}").format(str(e)))

    def export_csv(self):
        # Ouvre une boîte de dialogue pour choisir où sauvegarder le fichier CSV
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[(_("CSV files"), "*.csv"), (_("All files"), "*.*")]
        )
        if not file_path:
            return  # L'utilisateur a annulé la sauvegarde

        try:
            # Ouvre le fichier en écriture avec encodage UTF-8 et séparateur point-virgule
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["A", "B", "C", "Color", "Legend"],  # Entêtes du CSV
                    delimiter=';'  # Séparateur compatible Excel français
                )
                writer.writeheader()       # Écrit la ligne d'en-tête
                writer.writerows(self.data_list)  # Écrit toutes les données enregistrées
            messagebox.showinfo(_("Success"), _("Data exported successfully."))
        except Exception as e:
            # Affiche une erreur si quelque chose s'est mal passé pendant l'écriture
            messagebox.showerror(_("Error"), str(e))

    def import_csv(self):
        # Ouvre une boîte de dialogue pour choisir un fichier CSV à importer
        file_path = filedialog.askopenfilename(
            filetypes=[(_("CSV files"), "*.csv"), (_("All files"), "*.*")]
        )
        if not file_path:
            return  # L'utilisateur a annulé l'import

        try:
            # Ouvre le fichier en lecture avec le bon séparateur et l'encodage UTF-8
            with open(file_path, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')  # Utilise le point-virgule comme séparateur

                # Nettoie les anciennes données de la table et de la liste
                self.data_list.clear()
                for row in self.data_table.get_children():
                    self.data_table.delete(row)

                # Lit chaque ligne du fichier CSV
                for row in reader:
                    # Remplace la virgule par un point pour accepter les deux formats
                    a = float(row["A"].replace(',', '.'))
                    b = float(row["B"].replace(',', '.'))
                    c = float(row["C"].replace(',', '.'))
                    color = row["Color"]
                    legend = row["Legend"]

                    # Validation comme avant
                    valid, msg = validate_abc(a, b, c)
                    if not valid:
                        raise ValueError(msg)
                    valid, msg = validate_legend(legend)
                    if not valid:
                        raise ValueError(msg)

                    self.data_list.append({
                        "A": a, "B": b, "C": c, "Color": color, "Legend": legend
                    })
                    self.data_table.insert("", tk.END, values=(a, b, c, color, legend))


            # Si tout s'est bien passé, affiche un message de confirmation
            messagebox.showinfo(_("Success"), _("Data imported successfully."))
        except Exception as e:
            # En cas d'erreur (ex : mauvais format CSV), affiche une alerte
            messagebox.showerror(_("Import Error"), str(e))
