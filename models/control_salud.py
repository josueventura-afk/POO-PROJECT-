from interfaces.evaluable import Evaluable
from datetime import date
from models.medida import Peso, Talla

class ControlSalud(Evaluable):

    def __init__(self, fecha: date, peso: Peso, talla: Talla, observaciones: str = ""):
        self.fecha = fecha
        self.peso = peso
        self.talla = talla
        self.observaciones = observaciones
        self.imc = self.calcular_imc()

    def calcular_imc(self) -> float:
        return self.peso.get_valor() / (self.talla.get_valor() ** 2)

    def get_imc(self) -> float:
        return self.imc

    def get_fecha(self) -> str:
        return str(self.fecha)