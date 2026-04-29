from models.persona import Persona
from typing import List

class Estudiante(Persona):

    def __init__(self, codigo: str, nombre_completo: str, edad: int, sexo: str, curso: str):
        super().__init__(codigo, nombre_completo, edad, sexo)
        self.curso = curso
        self.controles: List = []

    def agregar_control(self, control):
        self.controles.append(control)

    def obtener_historial(self):
        return self.controles

    def calcular_imc_promedio(self) -> float:
        if not self.controles:
            return 0
        return sum(c.get_imc() for c in self.controles) / len(self.controles)

    def obtener_ultimo_control(self):
        return self.controles[-1] if self.controles else None

    def mostrar_info(self) -> str:
        return f"{self.nombre_completo} - {self.curso}"