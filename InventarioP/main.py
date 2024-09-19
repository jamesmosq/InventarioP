import os
import sys
import tkinter as tk

# Añadir el directorio del proyecto al path de Python
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from gui.product_gui import ProductGUI

def main():
    root = tk.Tk()
    app = ProductGUI(root)
    app.run()

if __name__ == "__main__":
    main()