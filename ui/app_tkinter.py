from models.estudiante import Estudiante
from models.control_salud import ControlSalud
from models.medida import Peso, Talla
from services.evaluador_nutricional import EvaluadorNutricional
from utils.id_generator import generar_codigo

import customtkinter as ctk

from tkinter import ttk, messagebox, scrolledtext, Scrollbar
import tkinter as tk

from datetime import datetime, date

# ===============================
# INTERFAZ (CLASE PRINCIPAL)
# ===============================

class AppSaludEscolar:

    def __init__(self, root, sistema, reporte):
        self.root = root
        self.root.title("Sistema de Salud Escolar")
        self.root.geometry("1200x550")
        self.root.configure(fg_color="#f0eee8")

        self.sistema = sistema
        self.reporte = reporte
        self.codigo_actual = None

        # Contenedor principal
        self.crear_navbar()

        self.frame_principal = ctk.CTkFrame(
            self.root,
            fg_color="#f0eee8",
            corner_radius=0
        )

        self.frame_principal.pack(
            fill="both",
            expand=True
        )

        self.vista_registrar_estudiante()

    def limpiar_frame(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    def obtener_estudiantes_combobox(self):
        return [f"{e.codigo} - {e.nombre_completo}" for e in self.sistema.estudiantes]

    def actualizar_combo_estudiantes(self, combo):
        combo['values'] = self.obtener_estudiantes_combobox()
        if combo['values']:
            combo.current(0)

    def actualizar_lista_estudiantes(self):
        self.vista_lista_estudiantes()

    def crear_navbar(self):

        navbar = ctk.CTkFrame(
            self.root,
            height=90,
            fg_color="#1a7a5e",
            corner_radius=0
        )

        navbar.pack(fill="x")

    # Lado izquierdo
        frame_titulo = ctk.CTkFrame(
            navbar,
            fg_color="transparent"
        )

        frame_titulo.pack(
            side="left",
            padx=25,
            pady=15
        )

        ctk.CTkLabel(
            frame_titulo,
            text="Salud Escolar",
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_titulo,
            text="Sistema de seguimiento",
            font=("Segoe UI", 12),
            text_color="white"
        ).pack(anchor="w")

    # Lado derecho
        frame_botones = ctk.CTkFrame(
            navbar,
            fg_color="transparent"
        )

        frame_botones.pack(
            side="right",
            padx=25
        )

        ctk.CTkButton(
            frame_botones,
            text="Registrar",
            width=120,
            height=40,
            corner_radius=15,
            fg_color="#48957e",
            hover_color="#3c7c68",
            command=self.vista_registrar_estudiante
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            frame_botones,
            text="Control",
            width=120,
            height=40,
            corner_radius=15,
            fg_color="#48957e",
            hover_color="#3c7c68",
            command=self.vista_registrar_control
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            frame_botones,
            text="Estudiantes",
            width=120,
            height=40,
            corner_radius=15,
            fg_color="#48957e",
            hover_color="#3c7c68",
            command=self.vista_lista_estudiantes
        ).pack(side="left", padx=5)

    # ================ REGISTRAR ESTUDIANTE ================
    def vista_registrar_estudiante(self):
      
        self.limpiar_frame()
        self.entries_est = {}

    # Tarjeta principal
        card = ctk.CTkFrame(
            self.frame_principal,
            fg_color="white",
            corner_radius=20
        )

        card.pack(
            pady=40,
            padx=40,
            fill="both",
            expand=False
        )

    # Título
        titulo = ctk.CTkLabel(
            card,
            text="Registrar Estudiante",
            font=("Segoe UI", 24, "bold"),
            text_color="#1a7a5e"
        )

        titulo.pack(pady=(25, 20))

    # ===== Nombre =====
        ctk.CTkLabel(
            card,
            text="Nombre",
            font=("Segoe UI", 14)
        ).pack(anchor="w", padx=50)

        entry_nombre = ctk.CTkEntry(
            card,
            width=500,
            height=40,
            corner_radius=10,
            placeholder_text="Ingrese el nombre del estudiante"
        )

        entry_nombre.pack(pady=(5, 15))

        self.entries_est["Nombre"] = entry_nombre

    # ===== Fecha =====
        ctk.CTkLabel(
            card,
            text="Fecha de Nacimiento",
            font=("Segoe UI", 14)
        ).pack(anchor="w", padx=50)

        entry_fecha = ctk.CTkEntry(
            card,
            width=500,
            height=40,
            corner_radius=10,
            placeholder_text="YYYY-MM-DD"
        )

        entry_fecha.pack(pady=(5, 15))

        self.entries_est["Fecha de Nacimiento"] = entry_fecha

    # ===== Sexo =====
        ctk.CTkLabel(
            card,
            text="Sexo",
            font=("Segoe UI", 14)
        ).pack(anchor="w", padx=50)

        combo_sexo = ctk.CTkComboBox(
            card,
            values=["M", "F"],
            width=500,
            height=40
        )

        combo_sexo.set("M")

        combo_sexo.pack(pady=(5, 15))

        self.entries_est["Sexo"] = combo_sexo

    # ===== Curso =====
        ctk.CTkLabel(
            card,
            text="Curso",
            font=("Segoe UI", 14)
        ).pack(anchor="w", padx=50)

        combo_curso = ctk.CTkComboBox(
            card,
            values=[
                "1ro Primaria",
                "2do Primaria",
                "3ro Primaria",
                "4to Primaria",
                "5to Primaria",
                "6to Primaria"
            ],
            width=500,
            height=40
        )

        combo_curso.set("1ro Primaria")

        combo_curso.pack(pady=(5, 25))

        self.entries_est["Curso"] = combo_curso

    # ===== Botón =====
        btn_guardar = ctk.CTkButton(
            card,
            text="Guardar",
            width=200,
            height=45,
            corner_radius=12,
            fg_color="#1a7a5e",
            hover_color="#48957e",
            command=self.guardar_estudiante
        )

        btn_guardar.pack(pady=(0, 30))

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
            self.entries_est["Nombre"].delete(0, "end")
            self.entries_est["Fecha de Nacimiento"].delete(0, "end")

            # Reiniciar los ComboBox de CustomTkinter
            self.entries_est["Sexo"].set("M")
            self.entries_est["Curso"].set("1ro Primaria")

            messagebox.showinfo("Éxito", f"Estudiante registrado con código: {codigo}")
           # if hasattr(self, "combo"):
           #    self.actualizar_combo_estudiantes(self.combo)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")

    # ================ REGISTRAR CONTROL ================
    def vista_registrar_control(self):
            self.limpiar_frame()

            self.entries_ctrl = {}

            # Tarjeta principal
            card = ctk.CTkFrame(
                self.frame_principal,
                fg_color="white",
                corner_radius=20
            )

            card.pack(
                pady=40,
                padx=40,
                fill="both",
                expand=False
            )

            # Título
            ctk.CTkLabel(
                card,
                text="Registrar Control",
                font=("Segoe UI", 24, "bold"),
                text_color="#1a7a5e"
            ).pack(pady=(25, 20))

            # ===== Estudiante =====
            ctk.CTkLabel(
                card,
                text="Estudiante",
                font=("Segoe UI", 14)
            ).pack(anchor="w", padx=50)

            self.combo = ctk.CTkComboBox(
                card,
                width=500,
                height=40,
                values=["Sin estudiantes"]
            )

            estudiantes = self.obtener_estudiantes_combobox()

            if estudiantes:
                self.combo.configure(values=estudiantes)
                self.combo.set(estudiantes[0])

            self.combo.pack(pady=(5, 15))

            # ===== Peso =====
            ctk.CTkLabel(
                card,
                text="Peso (kg)",
                font=("Segoe UI", 14)
            ).pack(anchor="w", padx=50)

            peso_entry = ctk.CTkEntry(
                card,
                width=500,
                height=40,
                placeholder_text="Ej: 35.5"
            )

            peso_entry.pack(pady=(5, 15))

            self.entries_ctrl["Peso (kg)"] = peso_entry

            # ===== Talla =====
            ctk.CTkLabel(
                card,
                text="Talla (m)",
                font=("Segoe UI", 14)
            ).pack(anchor="w", padx=50)

            talla_entry = ctk.CTkEntry(
                card,
                width=500,
                height=40,
                placeholder_text="Ej: 1.42"
            )

            talla_entry.pack(pady=(5, 15))

            self.entries_ctrl["Talla (m)"] = talla_entry

            # ===== Observación =====
            ctk.CTkLabel(
                card,
                text="Observación",
                font=("Segoe UI", 14)
            ).pack(anchor="w", padx=50)

            obs_entry = ctk.CTkEntry(
                card,
                width=500,
                height=40,
                placeholder_text="Observaciones del control"
            )

            obs_entry.pack(pady=(5, 20))

            self.entries_ctrl["Observación"] = obs_entry

            # Resultado IMC
            self.resultado_label = ctk.CTkLabel(
                card,
                text="",
                font=("Segoe UI", 14, "bold"),
                text_color="#1a7a5e"
            )

            self.resultado_label.pack(pady=10)

            # Botones
            frame_botones = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            frame_botones.pack(pady=(10, 25))

            ctk.CTkButton(
                frame_botones,
                text="Calcular IMC",
                width=180,
                height=45,
                corner_radius=12,
                fg_color="#f39c12",
                hover_color="#d68910",
                command=self.calcular_resultado
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                frame_botones,
                text="Guardar",
                width=180,
                height=45,
                corner_radius=12,
                fg_color="#1a7a5e",
                hover_color="#48957e",
                command=self.guardar_control
            ).pack(side="left", padx=10)

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

                self.resultado_label.configure(text=f"IMC: {imc} | Estado: {estado}")
            except ValueError:
                self.resultado_label.configure(text="Datos inválidos")
            except Exception as e:
                self.resultado_label.configure(text=f"Error: {str(e)}")

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

                self.sistema.registrar_control(codigo, control)

                # Limpiar campos
                for e in self.entries_ctrl.values():
                    e.delete(0, "end")
                self.combo.set("")

                messagebox.showinfo("Éxito", "Control registrado correctamente")

            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar: {str(e)}")

    # ================ LISTA ================
    def vista_lista_estudiantes(self):
            self.limpiar_frame()
            self.codigo_actual = None

            # Tarjeta principal
            card = ctk.CTkFrame(
                self.frame_principal,
                fg_color="white",
                corner_radius=20
            )

            card.pack(
                fill="both",
                expand=True,
                padx=40,
                pady=30
            )

            # Título
            ctk.CTkLabel(
                card,
                text="Lista de Estudiantes",
                font=("Segoe UI", 24, "bold"),
                text_color="#1a7a5e"
            ).pack(pady=(20, 15))

            # Contenedor tabla
            frame_tabla = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            frame_tabla.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=10
            )

            # Scroll
            scroll = tk.Scrollbar(frame_tabla)
            scroll.pack(side="right", fill="y")

            # Tabla
            tabla = ttk.Treeview(
                frame_tabla,
                columns=(
                    "Codigo",
                    "Nombre",
                    "Edad",
                    "Curso",
                    "IMC",
                    "Estado"
                ),
                show="headings",
                yscrollcommand=scroll.set
            )

            scroll.config(command=tabla.yview)

            columnas = (
                "Codigo",
                "Nombre",
                "Edad",
                "Curso",
                "IMC",
                "Estado"
            )

            for col in columnas:
                tabla.heading(col, text=col)
                tabla.column(col, width=140, anchor="center")

            tabla.pack(
                fill="both",
                expand=True
            )

            def seleccionar_estudiante(event):
                seleccion = tabla.selection()

                if seleccion:
                    self.codigo_actual = tabla.item(
                        seleccion[0]
                    )["values"][0]

            tabla.bind(
                "<<TreeviewSelect>>",
                seleccionar_estudiante
            )

            # Cargar estudiantes
            for est in self.sistema.estudiantes:

                ultimo_control = est.obtener_ultimo_control()

                imc = (
                    round(ultimo_control.get_imc(), 2)
                    if ultimo_control
                    else "N/A"
                )

                estado = (
                    EvaluadorNutricional.clasificar_estado(imc)
                    if ultimo_control
                    else "N/A"
                )

                tabla.insert(
                    "",
                    "end",
                    values=(
                        est.codigo,
                        est.nombre_completo,
                        est.edad,
                        est.curso,
                        imc,
                        estado
                    )
                )

            # Botón reporte
            ctk.CTkButton(
                card,
                text="Generar Reporte",
                width=220,
                height=45,
                corner_radius=12,
                fg_color="#1a7a5e",
                hover_color="#48957e",
                command=self.abrir_reporte
            ).pack(
                pady=(15, 25)
            )
    
    def abrir_reporte(self):

      try:

        # Reporte individual
          if self.codigo_actual:

              estudiante = self.sistema.buscar_estudiante(
                  self.codigo_actual
              )

              archivo = self.reporte.exportar_pdf_individual(
                  estudiante
              )

              messagebox.showinfo(
                  "Reporte individual generado",
                  f"PDF guardado en:\n{archivo}"
              )

          # Reporte general
          else:

              archivo = self.reporte.exportar_pdf_general(
                  self.sistema.estudiantes
              )

              messagebox.showinfo(
                  "Reporte general generado",
                  f"PDF guardado en:\n{archivo}"
              )

      except Exception as e:
          messagebox.showerror(
              "Error",
              str(e)
          )

            