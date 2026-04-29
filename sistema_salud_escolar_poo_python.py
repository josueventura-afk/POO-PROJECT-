# Sistema de Seguimiento de Salud Escolar
# Implementación completa con POO, herencia, abstracción, interfaces y polimorfismo

from abc import ABC, abstractmethod

# =========================
# CLASE ABSTRACTA
# =========================
class Persona(ABC):
    def __init__(self, codigo, nombre_completo, edad, sexo):
        self.codigo = codigo
        self.nombre_completo = nombre_completo
        self.edad = edad
        self.sexo = sexo

    @abstractmethod
    def mostrar_info(self):
        pass


# =========================
# INTERFAZ
# =========================
class Evaluable(ABC):
    @abstractmethod
    def calcular_imc(self):
        pass


# =========================
# CLASE CONTROL SALUD
# =========================
class ControlSalud(Evaluable):
    def __init__(self, fecha, peso, talla, observaciones=""):
        self.fecha = fecha
        self.peso = peso
        self.talla = talla
        self.observaciones = observaciones
        self.imc = self.calcular_imc()

    def calcular_imc(self):
        return self.peso / (self.talla ** 2)

    def get_imc(self):
        return self.imc

    def get_fecha(self):
        return self.fecha


# =========================
# CLASE ESTUDIANTE
# =========================
class Estudiante(Persona):
    def __init__(self, codigo, nombre_completo, edad, sexo, curso):
        super().__init__(codigo, nombre_completo, edad, sexo)
        self.curso = curso
        self.controles = []

    def agregar_control(self, control):
        self.controles.append(control)

    def obtener_historial(self):
        return self.controles

    def calcular_imc_promedio(self):
        if not self.controles:
            return 0
        return sum(c.get_imc() for c in self.controles) / len(self.controles)

    def obtener_ultimo_control(self):
        return self.controles[-1] if self.controles else None

    def mostrar_info(self):
        return f"{self.nombre_completo} - {self.curso}"


# =========================
# EVALUADOR NUTRICIONAL
# =========================
class EvaluadorNutricional:
    UMBRAL_BAJO_PESO = 18.5
    UMBRAL_SOBREPESO = 25
    UMBRAL_OBESIDAD = 30

    @classmethod
    def clasificar_estado(cls, imc):
        if imc < cls.UMBRAL_BAJO_PESO:
            return "Bajo peso"
        elif imc < cls.UMBRAL_SOBREPESO:
            return "Normal"
        elif imc < cls.UMBRAL_OBESIDAD:
            return "Sobrepeso"
        else:
            return "Obesidad"


# =========================
# SISTEMA PRINCIPAL
# =========================
class SistemaSaludEscolar:
    def __init__(self):
        self.estudiantes = []

    def registrar_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)

    def buscar_estudiante(self, codigo):
        for e in self.estudiantes:
            if e.codigo == codigo:
                return e
        return None

    def eliminar_estudiante(self, codigo):
        self.estudiantes = [e for e in self.estudiantes if e.codigo != codigo]

    def generar_alerta_estudiante(self, codigo):
        estudiante = self.buscar_estudiante(codigo)
        if not estudiante:
            return "No encontrado"

        ultimo = estudiante.obtener_ultimo_control()
        if not ultimo:
            return "Sin controles"

        estado = EvaluadorNutricional.clasificar_estado(ultimo.get_imc())

        if estado in ["Bajo peso", "Obesidad"]:
            return f"ALERTA: {estado}"
        return "Sin alerta"


# =========================
# REPORTE
# =========================
class Reporte:
    def __init__(self, formato="PDF"):
        self.formato = formato

    def generar_reporte_individual(self, estudiante):
        print(f"Reporte de {estudiante.nombre_completo}")
        for c in estudiante.obtener_historial():
            print(f"Fecha: {c.fecha} | IMC: {c.get_imc():.2f}")

    def generar_reporte_general(self, estudiantes):
        for e in estudiantes:
            self.generar_reporte_individual(e)


# =========================
# EJECUCIÓN DE PRUEBA
# =========================
if __name__ == "__main__":
    sistema = SistemaSaludEscolar()

    e1 = Estudiante("001", "Juan Perez", 15, "M", "5to")
    c1 = ControlSalud("2026-04-01", 50, 1.6)

    e1.agregar_control(c1)
    sistema.registrar_estudiante(e1)

    print(sistema.generar_alerta_estudiante("001"))

    reporte = Reporte()
    reporte.generar_reporte_general(sistema.estudiantes)
