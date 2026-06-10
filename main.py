from services.sistema_salud import SistemaSaludEscolar
from services.reporte import Reporte

from ui.app_tkinter import AppSaludEscolar

import customtkinter as ctk


def main():
    sistema = SistemaSaludEscolar()
    
    reporte = Reporte()

    # Configuración visual de CustomTkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()

    app = AppSaludEscolar(root, sistema, reporte)

    root.mainloop()


if __name__ == "__main__":
    main()