from services.sistema_salud import SistemaSaludEscolar
from services.reporte import Reporte

from ui.app_tkinter import AppSaludEscolar

import tkinter as tk

def main():
    sistema = SistemaSaludEscolar()

    reporte = Reporte()

    root = tk.Tk()
    app = AppSaludEscolar(root, sistema, reporte)
    root.mainloop()

if __name__ == "__main__":
    main()