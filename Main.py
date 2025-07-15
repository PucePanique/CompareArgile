# main.py

import tkinter as tk
from ui_launcher import ApplicationLauncher

if __name__ == "__main__":
    root = tk.Tk()
    launcher = ApplicationLauncher(root)
    root.mainloop()
