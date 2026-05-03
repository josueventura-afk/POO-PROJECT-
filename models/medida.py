from abc import ABC, abstractmethod

class Medida(ABC):

    def __init__(self, valor: float, unidad: str) -> None:
        self._valor = float(valor)
        self._unidad = unidad

    def get_valor(self) -> float:
        return self._valor

    def set_valor(self, v: float) -> None:
        valor = float(v)
        self._valor = valor
        if not self.validar_rango():
            raise ValueError(f"Valor fuera de rango para {self.__class__.__name__}: {valor}")

    def get_unidad(self) -> str:
        return self._unidad

    @abstractmethod
    def validar_rango(self) -> bool:
        pass

    def __str__(self) -> str:
        return f"{self._valor} {self._unidad}"


class Peso(Medida):

    def __init__(self, valor: float, unidad: str = "kg") -> None:
        super().__init__(valor, unidad)
        if not self.validar_rango():
            raise ValueError("Peso fuera de rango")

    def validar_rango(self) -> bool:
        return 1.0 <= self._valor <= 300.0


class Talla(Medida):

    def __init__(self, valor: float, unidad: str = "m") -> None:
        super().__init__(valor, unidad)
        if not self.validar_rango():
            raise ValueError("Talla fuera de rango")

    def validar_rango(self) -> bool:
        return 0.3 <= self._valor <= 2.5

    def a_centimetros(self) -> float:
        return self._valor * 100.0
