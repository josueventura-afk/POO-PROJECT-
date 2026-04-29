from datetime import date
from services.evaluador_nutricional import EvaluadorNutricional

class Reporte:

    def __init__(self, formato: str = "PDF"):
        self.formato = formato
        self.fecha_generacion = date.today()

    # ===== RF07 =====
    def generar_reporte_individual(self, estudiante):
        print(f"\n=== Reporte Individual ({self.formato}) ===")
        print(f"Fecha: {self.fecha_generacion}")
        print(f"Estudiante: {estudiante.nombre_completo} | Curso: {estudiante.curso}")

        for c in estudiante.obtener_historial():
            estado = EvaluadorNutricional.clasificar_estado(c.get_imc())
            print(f"- {c.fecha} | Peso: {c.peso} | Talla: {c.talla} | IMC: {c.get_imc():.2f} | Estado: {estado}")

    def generar_reporte_general(self, estudiantes):
        print(f"\n=== Reporte General ({self.formato}) ===")
        print(f"Fecha: {self.fecha_generacion}")

        for e in estudiantes:
            ultimo = e.obtener_ultimo_control()
            if ultimo:
                estado = EvaluadorNutricional.clasificar_estado(ultimo.get_imc())
                print(f"{e.nombre_completo} ({e.curso}) -> IMC: {ultimo.get_imc():.2f} | Estado: {estado}")
            else:
                print(f"{e.nombre_completo} ({e.curso}) -> Sin controles")