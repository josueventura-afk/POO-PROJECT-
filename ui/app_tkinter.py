from models.estudiante import Estudiante
from models.control_salud import ControlSalud

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class AppSaludEscolar:
    def __init__(self, root, sistema, admin, reporte):
        self.root = root
        self.root.title("Gestión de Salud Escolar")
        self.root.geometry("500x700")

        self.sistema = sistema
        self.admin = admin
        self.reporte = reporte

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 10))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"))

        self.crear_widgets()

    def crear_widgets(self):
        # --- FRAME: DATOS DEL ESTUDIANTE ---
        frame_est = ttk.LabelFrame(self.root, text=" Registro de Estudiante ", padding=10)
        frame_est.pack(fill="x", padx=20, pady=10)
        frame_est.columnconfigure(1, weight=1) 

        fields = [("Código:", "codigo"), ("Nombre:", "nombre"), 
                  ("Edad:", "edad"), ("Sexo:", "sexo"), ("Curso:", "curso")]
        
        self.entries = {}
        for i, (label, var_name) in enumerate(fields):
            ttk.Label(frame_est, text=label).grid(row=i, column=0, sticky="w", pady=2)
            entry = ttk.Entry(frame_est)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2) 
            self.entries[var_name] = entry

        ttk.Button(frame_est, text="Registrar Estudiante", 
                   command=self.registrar_estudiante).grid(row=len(fields), columnspan=2, pady=10)

        # --- FRAME: CONTROL DE SALUD ---
        frame_salud = ttk.LabelFrame(self.root, text=" Control de Salud Mensual ", padding=10)
        frame_salud.pack(fill="x", padx=20, pady=10)
        frame_salud.columnconfigure(1, weight=1)

        ttk.Label(frame_salud, text="Peso (kg):").grid(row=0, column=0, sticky="w")
        self.entry_peso = ttk.Entry(frame_salud)
        self.entry_peso.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(frame_salud, text="Talla (m):").grid(row=1, column=0, sticky="w")
        self.entry_talla = ttk.Entry(frame_salud)
        self.entry_talla.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        ttk.Button(frame_salud, text="Registrar Signos Vitales", 
                   command=self.registrar_control).grid(row=2, columnspan=2, pady=10)

        # --- FRAME: REPORTE Y RESULTADOS ---
        frame_rep = ttk.LabelFrame(self.root, text=" Reporte Generado ", padding=10)
        frame_rep.pack(fill="both", expand=True, padx=20, pady=10)

        self.txt_reporte = scrolledtext.ScrolledText(frame_rep, height=12, font=("Consolas", 10))
        self.txt_reporte.pack(fill="both", expand=True)

        # El comando debe ser generar_reporte (el método de la UI)
        ttk.Button(frame_rep, text="Generar y Mostrar Reporte", 
                   command=self.generar_reporte).pack(pady=5)

    # =========================
    # MÉTODOS DE LA INTERFAZ
    # =========================

    def registrar_estudiante(self):
        try:
            est = Estudiante(
                self.entries["codigo"].get(),
                self.entries["nombre"].get(),
                int(self.entries["edad"].get()),
                self.entries["sexo"].get(),
                self.entries["curso"].get()
            )
            self.admin.registrar_estudiante(self.sistema, est)
            messagebox.showinfo("Éxito", f"Estudiante {est.nombre_completo} registrado.")
        except Exception as e:
            messagebox.showerror("Error de Datos", f"Verifica los campos: {e}")

    def registrar_control(self):
        try:
            from datetime import date
            control = ControlSalud(
                str(date.today()),
                float(self.entry_peso.get()),
                float(self.entry_talla.get())
            )
            codigo = self.entries["codigo"].get()
            self.admin.registrar_control(self.sistema, codigo, control)
            messagebox.showinfo("Éxito", "Control médico guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el control: {e}")

    def generar_reporte(self):
        """ Este es el método que llama el botón """
        try:
            codigo = self.entries["codigo"].get()
            if not codigo:
                raise ValueError("Debes ingresar el código del estudiante.")

            # Llamamos a la lógica del admin/docente
            # Nota: Este método DEBE estar definido en tu clase Docente/Admin
            resultado = self.admin.generar_reporte_individual(self.sistema, codigo, self.reporte)
            
            if resultado is None:
                resultado = "Aviso: El reporte no devolvió texto. Revisa el return en la clase Docente."

            self.txt_reporte.delete(1.0, tk.END)
            self.txt_reporte.insert(tk.END, str(resultado))
            
        except Exception as e:
            messagebox.showerror("Error de Reporte", str(e))