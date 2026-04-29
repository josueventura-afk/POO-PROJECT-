from models.persona import Persona

class Administrador(Persona):

    def __init__(self, codigo: str, nombre_completo: str, edad: int, sexo: str, rol: str):
        super().__init__(codigo, nombre_completo, edad, sexo)
        self.rol = rol

    def registrar_estudiante(self, sistema, estudiante):
        sistema.registrar_estudiante(estudiante)

    def eliminar_estudiante(self, sistema, codigo: str):
        sistema.eliminar_estudiante(codigo)

    def registrar_control(self, sistema, codigo: str, control):
        estudiante = sistema.buscar_estudiante(codigo)
        if estudiante:
            estudiante.agregar_control(control)

    def generar_reporte_individual(self, sistema, codigo: str, reporte):
        estudiante = sistema.buscar_estudiante(codigo)
        if estudiante:
            reporte.generar_reporte_individual(estudiante)

    def mostrar_info(self) -> str:
        return f"Administrador: {self.nombre_completo}"