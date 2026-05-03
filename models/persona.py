from abc import ABC, abstractmethod
from datetime import datetime, date

class Persona(ABC):

    def __init__(self, codigo: str, nombre_completo: str, fecha_nacimiento: date, sexo: str):
        self.codigo = codigo
        self.nombre_completo = nombre_completo
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo

    def calcular_edad(self):
        hoy = datetime.today()
        nacimiento = datetime.strptime(self.fecha_nacimiento, "%Y-%m-%d")
        return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))

    @abstractmethod
    def mostrar_info(self) -> str:
        pass