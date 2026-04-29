from models.administrador import Administrador
from services.sistema_salud import SistemaSaludEscolar
from services.reporte import Reporte

from ui.app_tkinter import AppSaludEscolar

import tkinter as tk

def main():
    sistema = SistemaSaludEscolar()
    admin = Administrador("A01", "Docente", 40, "M", "Profesor")
    reporte = Reporte()

    root = tk.Tk()
    app = AppSaludEscolar(root, sistema, admin, reporte)
    root.mainloop()

if __name__ == "__main__":
    main()