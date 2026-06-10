from datetime import date
from services.evaluador_nutricional import EvaluadorNutricional

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

class Reporte:

    def __init__(self, formato: str = "PDF"):
        self.formato = formato
        self.fecha_generacion = date.today()

    # ===== RF07 =====
    def generar_reporte_individual(self, estudiante) -> str:
        lineas = [
            f"Reporte Individual ({self.formato})",
            f"Fecha de generación: {self.fecha_generacion}",
            "",
            f"Código: {estudiante.codigo}",
            f"Nombre: {estudiante.nombre_completo}",
            f"Fecha de nacimiento: {estudiante.fecha_nacimiento}",
            f"Edad: {estudiante.edad}",
            f"Sexo: {estudiante.sexo}",
            f"Curso: {estudiante.curso}",
            "",
            "Controles de salud:",
        ]

        historial = estudiante.obtener_historial()
        if not historial:
            lineas.append("- Sin controles registrados")
        else:
            for c in historial:
                estado = EvaluadorNutricional.clasificar_estado(c.get_imc())
                lineas.append(
                    f"- Fecha: {c.fecha} | Fecha de nacimiento: {estudiante.fecha_nacimiento} | "
                    f"Edad: {estudiante.edad} | Peso: {c.peso.get_valor():.2f} {c.peso.get_unidad()} | "
                    f"Talla: {c.talla.get_valor():.2f} {c.talla.get_unidad()} | "
                    f"IMC: {c.get_imc():.2f} | Estado: {estado}"
                )

        if historial:
            ultimo = historial[-1]
            lineas.extend([
                "",
                "Resumen del último control:",
                f"- IMC: {ultimo.get_imc():.2f}",
                f"- Peso: {ultimo.peso.get_valor():.2f} {ultimo.peso.get_unidad()}",
                f"- Talla: {ultimo.talla.get_valor():.2f} {ultimo.talla.get_unidad()}",
                f"- Estado: {EvaluadorNutricional.clasificar_estado(ultimo.get_imc())}",
            ])

        return "\n".join(lineas)

    def generar_reporte_general(self, estudiantes) -> str:
        lineas = [
            f"Reporte General ({self.formato})",
            f"Fecha de generación: {self.fecha_generacion}",
            "",
        ]

        for e in estudiantes:
            ultimo = e.obtener_ultimo_control()
            if ultimo:
                estado = EvaluadorNutricional.clasificar_estado(ultimo.get_imc())
                lineas.append(
                    f"{e.nombre_completo} ({e.curso}) -> IMC: {ultimo.get_imc():.2f} | Estado: {estado}"
                )
            else:
                lineas.append(f"{e.nombre_completo} ({e.curso}) -> Sin controles")

        return "\n".join(lineas)
    
    def exportar_pdf_individual(self, estudiante):

        texto = self.generar_reporte_individual(estudiante)

        os.makedirs("reportes", exist_ok=True)

        archivo = f"reportes/Reporte_{estudiante.codigo}.pdf"

        pdf = SimpleDocTemplate(archivo)

        estilos = getSampleStyleSheet()

        contenido = [
            Paragraph("Reporte Individual de Salud Escolar", estilos["Title"]),
            Spacer(1, 12),
            Paragraph(texto.replace("\n", "<br/>"), estilos["Normal"])
        ]

        pdf.build(contenido)

        return archivo


    def exportar_pdf_general(self, estudiantes):

        texto = self.generar_reporte_general(estudiantes)

        os.makedirs("reportes", exist_ok=True)

        archivo = "reportes/Reporte_General.pdf"

        pdf = SimpleDocTemplate(archivo)

        estilos = getSampleStyleSheet()

        contenido = [
            Paragraph("Reporte General de Salud Escolar", estilos["Title"]),
            Spacer(1, 12),
            Paragraph(texto.replace("\n", "<br/>"), estilos["Normal"])
        ]

        pdf.build(contenido)

        return archivo