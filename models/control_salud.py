from interfaces.evaluable import Evaluable
from datetime import date

class ControlSalud(Evaluable):

    def __init__(self, fecha: date, peso: float, talla: float, observaciones: str = ""):
        self.fecha = fecha
        self.peso = peso
        self.talla = talla
        self.observaciones = observaciones
        self.imc = self.calcular_imc()

    def calcular_imc(self) -> float:
        return self.peso / (self.talla ** 2)

    def get_imc(self) -> float:
        return self.imc

    def get_fecha(self) -> str:
        return self.fecha