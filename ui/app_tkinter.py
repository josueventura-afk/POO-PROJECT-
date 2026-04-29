import tkinter as tk
from tkinter import messagebox

from models.estudiante import Estudiante
from models.control_salud import ControlSalud

class AppSaludEscolar:

    def __init__(self, root, sistema, admin, reporte):
        self.root = root
        self.root.title("Sistema Salud Escolar")

        self.sistema = sistema
        self.admin = admin
        self.reporte = reporte

        # ===== FORMULARIO ESTUDIANTE =====
        tk.Label(root, text="Código").grid(row=0, column=0)
        self.codigo = tk.Entry(root)
        self.codigo.grid(row=0, column=1)

        tk.Label(root, text="Nombre").grid(row=1, column=0)
        self.nombre = tk.Entry(root)
        self.nombre.grid(row=1, column=1)

        tk.Label(root, text="Edad").grid(row=2, column=0)
        self.edad = tk.Entry(root)
        self.edad.grid(row=2, column=1)

        tk.Label(root, text="Sexo").grid(row=3, column=0)
        self.sexo = tk.Entry(root)
        self.sexo.grid(row=3, column=1)

        tk.Label(root, text="Curso").grid(row=4, column=0)
        self.curso = tk.Entry(root)
        self.curso.grid(row=4, column=1)

        tk.Button(root, text="Registrar Estudiante",
                  command=self.registrar_estudiante).grid(row=5, columnspan=2)

        # ===== CONTROL SALUD =====
        tk.Label(root, text="Peso").grid(row=6, column=0)
        self.peso = tk.Entry(root)
        self.peso.grid(row=6, column=1)

        tk.Label(root, text="Talla").grid(row=7, column=0)
        self.talla = tk.Entry(root)
        self.talla.grid(row=7, column=1)

        tk.Button(root, text="Registrar Control",
                  command=self.registrar_control).grid(row=8, columnspan=2)

        # ===== REPORTE =====
        tk.Button(root, text="Generar Reporte",
                  command=self.generar_reporte).grid(row=9, columnspan=2)

    # =========================
    # MÉTODOS UI
    # =========================
    def registrar_estudiante(self):
        try:
            est = Estudiante(
                self.codigo.get(),
                self.nombre.get(),
                int(self.edad.get()),
                self.sexo.get(),
                self.curso.get()
            )
            self.admin.registrar_estudiante(self.sistema, est)
            messagebox.showinfo("OK", "Estudiante registrado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def registrar_control(self):
        try:
            control = ControlSalud(
                "2026-04-01",
                float(self.peso.get()),
                float(self.talla.get())
            )
            self.admin.registrar_control(
                self.sistema,
                self.codigo.get(),
                control
            )
            messagebox.showinfo("OK", "Control registrado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generar_reporte(self):
        self.admin.generar_reporte_individual(
            self.sistema,
            self.codigo.get(),
            self.reporte
        )
        messagebox.showinfo("OK", "Reporte generado en consola")