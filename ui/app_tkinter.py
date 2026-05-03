from models.estudiante import Estudiante
from models.control_salud import ControlSalud
from models.medida import Peso, Talla
from services.evaluador_nutricional import EvaluadorNutricional

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import re

# =========================
# VALIDACIONES
# =========================
def validar_nombre(nombre):
    return re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúñÑ ]+", nombre)


# =========================
class AppSaludEscolar:

    def __init__(self, root, sistema, reporte):
        self.root = root
        self.root.title("Gestión de Salud Escolar")
        self.root.geometry("520x750")

        self.sistema = sistema
        self.reporte = reporte

        self.codigo_actual = None
        self.entries = {}

        self.crear_widgets()

    # =========================
    def crear_widgets(self):

        # ===== REGISTRO =====
        frame_est = ttk.LabelFrame(self.root, text="Registro de Estudiante", padding=10)
        frame_est.pack(fill="x", padx=20, pady=10)

        frame_est.columnconfigure(1, weight=1)

        # Nombre
        ttk.Label(frame_est, text="Nombre").grid(row=0, column=0, sticky="w")
        self.entries["nombre"] = ttk.Entry(frame_est)
        self.entries["nombre"].grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        # Fecha de Nacimiento
        ttk.Label(frame_est, text="Fecha de Nacimiento (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
        self.entries["fecha_nacimiento"] = ttk.Entry(frame_est)
        self.entries["fecha_nacimiento"].grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        # Sexo (RadioButtons)
        ttk.Label(frame_est, text="Sexo").grid(row=2, column=0, sticky="w")

        self.sexo_var = tk.StringVar(value="M")

        frame_radio = ttk.Frame(frame_est)
        frame_radio.grid(row=2, column=1, sticky="w")

        ttk.Radiobutton(frame_radio, text="Masculino", variable=self.sexo_var, value="M").pack(side="left")
        ttk.Radiobutton(frame_radio, text="Femenino", variable=self.sexo_var, value="F").pack(side="left")

        # Curso (Combobox)
        ttk.Label(frame_est, text="Curso").grid(row=3, column=0, sticky="w")

        self.entries["curso"] = ttk.Combobox(
            frame_est,
            values=[
                "1ro Primaria",
                "2do Primaria",
                "3ro Primaria",
                "4to Primaria",
                "5to Primaria",
                "6to Primaria"
            ],
            state="readonly"
        )
        self.entries["curso"].grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        self.entries["curso"].current(0)

        # Botones
        ttk.Button(frame_est, text="Registrar Estudiante",
                   command=self.registrar_estudiante).grid(row=4, columnspan=2, pady=10)

        # ===== CONTROL =====
        frame_salud = ttk.LabelFrame(self.root, text="Control de Salud", padding=10)
        frame_salud.pack(fill="x", padx=20, pady=10)

        frame_salud.columnconfigure(1, weight=1)

        ttk.Label(frame_salud, text="Peso").grid(row=0, column=0, sticky="w")
        self.entry_peso = ttk.Entry(frame_salud)
        self.entry_peso.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_salud, text="Talla").grid(row=1, column=0, sticky="w")
        self.entry_talla = ttk.Entry(frame_salud)
        self.entry_talla.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Button(frame_salud, text="Registrar Control",
                   command=self.registrar_control).grid(row=2, columnspan=2, pady=10)

        # ===== REPORTE =====
        frame_rep = ttk.LabelFrame(self.root, text="Reporte", padding=10)
        frame_rep.pack(fill="both", expand=True, padx=20, pady=10)

        self.txt_reporte = scrolledtext.ScrolledText(frame_rep)
        self.txt_reporte.pack(fill="both", expand=True)

        ttk.Button(frame_rep, text="Mostrar Reporte",
                   command=self.generar_reporte).pack(pady=5)

        ttk.Button(frame_rep, text="Abrir en Nueva Ventana",
                   command=self.abrir_reporte).pack()

    # =========================
    # FUNCIONES
    # =========================

    def registrar_estudiante(self):
        try:
            from utils.id_generator import generar_codigo

            nombre = self.entries["nombre"].get()
            fecha_nacimiento = self.entries["fecha_nacimiento"].get().strip()
            sexo = self.sexo_var.get()

            if not validar_nombre(nombre):
                raise ValueError("Nombre inválido (solo letras)")

            try:
                datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")

            codigo = generar_codigo()
            self.codigo_actual = codigo

            est = Estudiante(
                codigo,
                nombre,
                fecha_nacimiento,
                sexo,
                self.entries["curso"].get()
            )

            self.sistema.registrar_estudiante(est)

            messagebox.showinfo("OK", f"Registrado con código: {codigo}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def registrar_control(self):
        try:
            from datetime import date

            if not self.codigo_actual:
                raise ValueError("Primero registra un estudiante")

            peso = Peso(float(self.entry_peso.get()))
            talla = Talla(float(self.entry_talla.get()))

            control = ControlSalud(
                str(date.today()),
                peso,
                talla
            )

            estudiante = self.sistema.buscar_estudiante(self.codigo_actual)
            if not estudiante:
                raise ValueError("Estudiante no encontrado")
            estudiante.agregar_control(control)

            registro = (
                f"- Fecha: {control.fecha} | Fecha de nacimiento: {estudiante.fecha_nacimiento} | "
                f"Edad: {estudiante.edad} | Peso: {control.peso.get_valor():.2f} {control.peso.get_unidad()} | "
                f"Talla: {control.talla.get_valor():.2f} {control.talla.get_unidad()} | "
                f"IMC: {control.get_imc():.2f} | Estado: {EvaluadorNutricional.clasificar_estado(control.get_imc())}"
            )
            self.txt_reporte.delete(1.0, tk.END)
            self.txt_reporte.insert(tk.END, registro)

            messagebox.showinfo("OK", "Control registrado")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generar_reporte(self):
        try:
            if not self.codigo_actual:
                raise ValueError("No hay estudiante seleccionado")

            estudiante = self.sistema.buscar_estudiante(self.codigo_actual)
            if not estudiante:
                raise ValueError("Estudiante no encontrado")

            reporte_texto = self.reporte.generar_reporte_individual(estudiante)
            self.txt_reporte.delete(1.0, tk.END)
            self.txt_reporte.insert(tk.END, reporte_texto)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_reporte(self):
        try:
            if not self.codigo_actual:
                raise ValueError("No hay estudiante seleccionado")

            estudiante = self.sistema.buscar_estudiante(self.codigo_actual)
            if not estudiante:
                raise ValueError("Estudiante no encontrado")

            reporte_texto = self.reporte.generar_reporte_individual(estudiante)

            ventana = tk.Toplevel(self.root)
            ventana.title("Reporte")
            ventana.geometry("400x400")

            txt = scrolledtext.ScrolledText(ventana)
            txt.pack(fill="both", expand=True)

            txt.insert(tk.END, reporte_texto)

        except Exception as e:
            messagebox.showerror("Error", str(e))

