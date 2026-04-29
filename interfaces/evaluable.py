from abc import ABC, abstractmethod

class Evaluable(ABC):
    """
    Interfaz que define el contrato para clases que
    pueden calcular el IMC.
    """

    @abstractmethod
    def calcular_imc(self) -> float:
        """
        Debe retornar el índice de masa corporal.
        """
        pass