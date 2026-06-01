from models.estudiante import Estudiante
from models.control_salud import ControlSalud
from models.medida import Peso, Talla
from services.evaluador_nutricional import EvaluadorNutricional
from utils.id_generator import generar_codigo

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

# ===============================
# INTERFAZ (CLASE PRINCIPAL)
# ===============================

class AppSaludEscolar:

    def __init__(self, root, sistema, reporte):
        self.root = root
        self.root.title("Sistema de Salud Escolar")
        self.root.geometry("800x550")
        self.root.configure(bg="#F5F7FA")

        self.sistema = sistema
        self.reporte = reporte

        self.frame_principal = tk.Frame(root, bg="#F5F7FA")
        self.frame_principal.pack(fill="both", expand=True)

        self.crear_menu()
        self.vista_registrar_estudiante()

    def limpiar_frame(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    # ================ MENU ================
    def crear_menu(self):
        menu = tk.Menu(self.root)

        menu.add_command(label="Registrar Estudiante", command=self.vista_registrar_estudiante)
        menu.add_command(label="Registrar Control", command=self.vista_registrar_control)
        menu.add_command(label="Lista de Estudiantes", command=self.vista_lista_estudiantes)

        self.root.config(menu=menu)

    # ================ REGISTRAR ESTUDIANTE ================
    def vista_registrar_estudiante(self):
        self.limpiar_frame()

        tk.Label(self.frame_principal, text="Registrar Estudiante",
                 font=("Arial", 16), bg="#F5F7FA").pack(pady=10)

        self.entries_est = {}
        campos = ["Nombre", "Fecha de Nacimiento (YYYY-MM-DD)", "Sexo", "Curso"]

        # Nombre
        tk.Label(self.frame_principal, text="Nombre", bg="#F5F7FA").pack()
        entry_nombre = tk.Entry(self.frame_principal)
        entry_nombre.pack()
        self.entries_est["Nombre"] = entry_nombre

        # Fecha de Nacimiento
        tk.Label(self.frame_principal, text="Fecha de Nacimiento (YYYY-MM-DD)", bg="#F5F7FA").pack()
        entry_fecha = tk.Entry(self.frame_principal)
        entry_fecha.pack()
        self.entries_est["Fecha de Nacimiento"] = entry_fecha

        # Sexo (Combobox)
        tk.Label(self.frame_principal, text="Sexo", bg="#F5F7FA").pack()
        combo_sexo = ttk.Combobox(self.frame_principal, values=["M", "F"], state="readonly")
        combo_sexo.pack()
        combo_sexo.current(0)
        self.entries_est["Sexo"] = combo_sexo

        # Curso (Combobox)
        tk.Label(self.frame_principal, text="Curso", bg="#F5F7FA").pack()
        combo_curso = ttk.Combobox(
            self.frame_principal,
            values=["1ro Primaria", "2do Primaria", "3ro Primaria", "4to Primaria", "5to Primaria", "6to Primaria"],
            state="readonly"
        )
        combo_curso.pack()
        combo_curso.current(0)
        self.entries_est["Curso"] = combo_curso

        tk.Button(self.frame_principal, text="Guardar",
                  bg="#4CAF50", fg="white",
                  command=self.guardar_estudiante).pack(pady=10)

    def guardar_estudiante(self):
        try:
            nombre = self.entries_est["Nombre"].get().strip()
            fecha_nacimiento = self.entries_est["Fecha de Nacimiento"].get().strip()
            sexo = self.entries_est["Sexo"].get()
            curso = self.entries_est["Curso"].get()

            if not nombre:
                raise ValueError("El nombre es requerido")

            # Validar formato de fecha
            datetime.strptime(fecha_nacimiento, "%Y-%m-%d")

            codigo = generar_codigo()

            est = Estudiante(
                codigo,
                nombre,
                fecha_nacimiento,
                sexo,
                curso
            )
            self.sistema.registrar_estudiante(est)

            # Limpiar campos
            self.entries_est["Nombre"].delete(0, tk.END)
            self.entries_est["Fecha de Nacimiento"].delete(0, tk.END)
            self.entries_est["Curso"].current(0)

            messagebox.showinfo("Éxito", f"Estudiante registrado con código: {codigo}")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")

    # ================ REGISTRAR CONTROL ================
    def vista_registrar_control(self):
        self.limpiar_frame()

        tk.Label(self.frame_principal, text="Registrar Control",
                 font=("Arial", 16), bg="#F5F7FA").pack(pady=10)

        tk.Label(self.frame_principal, text="Estudiante", bg="#F5F7FA").pack()

        self.combo = ttk.Combobox(self.frame_principal, state="readonly")
        self.combo['values'] = [f"{e.codigo} - {e.nombre_completo}" for e in self.sistema.estudiantes]
        self.combo.pack()

        self.entries_ctrl = {}
        campos = ["Peso (kg)", "Talla (m)", "Observación"]

        for campo in campos:
            tk.Label(self.frame_principal, text=campo, bg="#F5F7FA").pack()
            entry = tk.Entry(self.frame_principal)
            entry.pack()
            self.entries_ctrl[campo] = entry

        self.resultado_label = tk.Label(self.frame_principal, text="", bg="#F5F7FA", font=("Arial", 12))
        self.resultado_label.pack(pady=10)

        tk.Button(self.frame_principal, text="Resultado",
                  bg="#FF9800", fg="white",
                  command=self.calcular_resultado).pack(pady=5)

        tk.Button(self.frame_principal, text="Guardar",
                  bg="#2196F3", fg="white",
                  command=self.guardar_control).pack(pady=5)

    def calcular_resultado(self):
        try:
            peso_val = float(self.entries_ctrl["Peso (kg)"].get())
            talla_val = float(self.entries_ctrl["Talla (m)"].get())

            peso = Peso(peso_val)
            talla = Talla(talla_val)

            control = ControlSalud(
                date.today(),
                peso,
                talla,
                self.entries_ctrl["Observación"].get()
            )

            imc = round(control.calcular_imc(), 2)
            estado = EvaluadorNutricional.clasificar_estado(imc)

            self.resultado_label.config(text=f"IMC: {imc} | Estado: {estado}")
        except ValueError:
            self.resultado_label.config(text="Datos inválidos")
        except Exception as e:
            self.resultado_label.config(text=f"Error: {str(e)}")

    def guardar_control(self):
        try:
            if not self.combo.get():
                raise ValueError("Debe seleccionar un estudiante")

            codigo = self.combo.get().split(" - ")[0]
            peso_val = float(self.entries_ctrl["Peso (kg)"].get())
            talla_val = float(self.entries_ctrl["Talla (m)"].get())

            peso = Peso(peso_val)
            talla = Talla(talla_val)

            control = ControlSalud(
                date.today(),
                peso,
                talla,
                self.entries_ctrl["Observación"].get()
            )

            estudiante = self.sistema.buscar_estudiante(codigo)
            if not estudiante:
                raise ValueError("Estudiante no encontrado")

            estudiante.agregar_control(control)

            # Limpiar campos
            for e in self.entries_ctrl.values():
                e.delete(0, tk.END)
            self.combo.set("")

            messagebox.showinfo("Éxito", "Control registrado correctamente")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")

    # ================ LISTA ================
    def vista_lista_estudiantes(self):
        self.limpiar_frame()

        tk.Label(self.frame_principal, text="Lista de Estudiantes",
                 font=("Arial", 16), bg="#F5F7FA").pack(pady=10)

        frame_tabla = tk.Frame(self.frame_principal, bg="#F5F7FA")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        scroll = tk.Scrollbar(frame_tabla)
        scroll.pack(side="right", fill="y")

        tabla = ttk.Treeview(
            frame_tabla,
            columns=("Codigo", "Nombre", "Edad", "Curso", "IMC", "Estado"),
            show="headings",
            yscrollcommand=scroll.set
        )

        scroll.config(command=tabla.yview)

        columnas = ("Codigo", "Nombre", "Edad", "Curso", "IMC", "Estado")

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=100)

        tabla.pack(fill="both", expand=True)

        for est in self.sistema.estudiantes:
            ultimo_control = est.obtener_ultimo_control()
            imc = round(ultimo_control.get_imc(), 2) if ultimo_control else "N/A"
            estado = EvaluadorNutricional.clasificar_estado(imc) if ultimo_control else "N/A"

            tabla.insert("", "end", values=(
                est.codigo,
                est.nombre_completo,
                est.edad,
                est.curso,
                imc,
                estado
            ))

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

