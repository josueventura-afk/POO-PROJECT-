from datetime import date
from services.evaluador_nutricional import EvaluadorNutricional

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