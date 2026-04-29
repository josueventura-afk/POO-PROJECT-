from abc import ABC, abstractmethod

class Persona(ABC):

    def __init__(self, codigo: str, nombre_completo: str, edad: int, sexo: str):
        self.codigo = codigo
        self.nombre_completo = nombre_completo
        self.edad = edad
        self.sexo = sexo

    @abstractmethod
    def mostrar_info(self) -> str:
        pass