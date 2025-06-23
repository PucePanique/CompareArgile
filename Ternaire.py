import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mpltern
assert mpltern.TernaryAxes is not None
import matplotlib.pyplot as plt
import ttkbootstrap as tb
import gettext
import sys
import csv

localedir = 'locales'
lang = gettext.translation('messages', localedir=localedir, languages=['fr'], fallback=True)
lang.install()
_ = lang.gettext

CONFIG = {
    'window_size': "950x700",
    'style_theme': "litera",
    'default_font': "Arial",
    'font_choices': ["Arial", "Courier", "Times New Roman", "Verdana"],
    'default_width_cm': 25,
    'default_height_cm': 20,
    'title_fontsize': 16,
    'axis_fontsize': 12,
    'legend_fontsize': 10,
    'legend_ncol': 2,
    'legend_loc': "upper center",
    'legend_bbox': (0.5, -0.2),
    'plot_figsize': (10, 8),
    'color_default': "No Color",
    'color_bg': "white"
}

def validate_abc(a, b, c):
    try:
        a, b, c = float(a), float(b), float(c)
    except ValueError:
        return False, _("A, B, and C must be decimal numbers.")
    if a + b + c != 100:
        return False, _("The sum of A, B, and C must be exactly 100.")
    return True, ""

def validate_legend(legend):
    if not legend.strip():
        return False, _("Legend cannot be empty.")
    return True, ""

def validate_color(color):
    if color == CONFIG['color_default']:
        return False, _("Please select a color.")
    return True, ""

class TernaryDiagramApp:
    def __init__(self, master):
        self.master = master
        self.master.title(_("Ternary Diagram Generator"))
        self.data_list = []
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.style = tb.Style(CONFIG['style_theme'])
        self.master.geometry(CONFIG['window_size'])
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
        self.font_var = tk.StringVar(value=CONFIG['default_font'])
        self.font_dropdown = ttk.Combobox(
            self.font_frame, textvariable=self.font_var,
            values=CONFIG['font_choices']
        )
        self.font_dropdown.grid(row=0, column=1, padx=5)
        self.font_dropdown.state(["readonly"])

        ttk.Label(self.font_frame, text=_("Width (cm):")).grid(row=0, column=2, padx=5)
        self.width_var = tk.DoubleVar(value=CONFIG['default_width_cm'])
        self.width_entry = ttk.Entry(self.font_frame, textvariable=self.width_var, width=10)
        self.width_entry.grid(row=0, column=3, padx=5)

        ttk.Label(self.font_frame, text=_("Height (cm):")).grid(row=0, column=4, padx=5)
        self.height_var = tk.DoubleVar(value=CONFIG['default_height_cm'])
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
        self.color_label = ttk.Label(self.input_frame, text=CONFIG['color_default'], background=CONFIG['color_bg'], relief="sunken", width=20)
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

        # --- 6. Gestion des doublons dans la légende ---
        if any(d["Legend"] == legend for d in self.data_list):
            messagebox.showerror(_("Input Error"), _("Legend must be unique."))
            return

        data = {"A": float(a), "B": float(b), "C": float(c), "Color": color, "Legend": legend}
        self.data_list.append(data)
        self.data_table.insert("", tk.END, values=(a, b, c, color, legend))

        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.entry_c.delete(0, tk.END)
        self.entry_legend.delete(0, tk.END)
        self.color_label.config(text=CONFIG['color_default'], background=CONFIG['color_bg'])

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
        fig = plt.Figure(figsize=CONFIG['plot_figsize'])
        ax = fig.add_subplot(111, projection="ternary")

        ax.set_tlabel(axis1, fontsize=CONFIG['axis_fontsize'], fontname=selected_font, labelpad=15)
        ax.set_llabel(axis2, fontsize=CONFIG['axis_fontsize'], fontname=selected_font, labelpad=15)
        ax.set_rlabel(axis3, fontsize=CONFIG['axis_fontsize'], fontname=selected_font, labelpad=15)

        chart_title = self.chart_title_entry.get().strip()
        if chart_title:
            ax.set_title(chart_title, fontsize=CONFIG['title_fontsize'], fontname=selected_font, pad=30)

        ax.grid(True, which="both", color="grey", linestyle="--", linewidth=0.3)

        for data in self.data_list:
            point = (data["A"] / 100, data["B"] / 100, data["C"] / 100)
            ax.scatter(
                [point[0]], [point[1]], [point[2]],
                color=data["Color"], marker="x", label=data["Legend"], s=25
            )

        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(),
                  loc=CONFIG['legend_loc'],
                  bbox_to_anchor=CONFIG['legend_bbox'],
                  ncol=CONFIG['legend_ncol'],
                  prop={"family": selected_font, "size": CONFIG['legend_fontsize']})

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


    


# --- 4. Accessibilité : Tooltips ---
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()
