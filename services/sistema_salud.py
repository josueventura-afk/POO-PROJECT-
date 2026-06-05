from services.evaluador_nutricional import EvaluadorNutricional
from services.repository import EstudianteRepository

class SistemaSaludEscolar:

    def __init__(self, repo=None):
        self.repo = repo or EstudianteRepository()
        self.estudiantes = self.repo.cargar_estudiantes()

    # ===== RF01 / RF02 =====
    def registrar_estudiante(self, estudiante):
        if self.buscar_estudiante(estudiante.codigo):
            raise ValueError("El estudiante ya existe")
        self.repo.guardar_estudiante(estudiante)
        self.estudiantes.append(estudiante)

    def buscar_estudiante(self, codigo: str):
        for e in self.estudiantes:
            if e.codigo == codigo:
                return e
        return None

    def modificar_estudiante(self, codigo: str, **kwargs):
        e = self.buscar_estudiante(codigo)
        if not e:
            raise ValueError("No encontrado")
        self.repo.actualizar_estudiante(codigo, **kwargs)
        for k, v in kwargs.items():
            if hasattr(e, k):
                setattr(e, k, v)

    def eliminar_estudiante(self, codigo: str):
        if not self.buscar_estudiante(codigo):
            raise ValueError("No encontrado")
        self.repo.eliminar_estudiante(codigo)
        self.estudiantes = [e for e in self.estudiantes if e.codigo != codigo]

    def registrar_control(self, codigo: str, control):
        estudiante = self.buscar_estudiante(codigo)
        if not estudiante:
            raise ValueError("Estudiante no encontrado")
        self.repo.guardar_control(codigo, control)
        estudiante.agregar_control(control)

    # ===== RF05: Alertas =====
    def generar_alerta_estudiante(self, codigo: str) -> str:
        e = self.buscar_estudiante(codigo)
        if not e:
            return "No encontrado"
        controles = e.obtener_historial()
        if not controles:
            return "Sin controles"

        alertas = []

        if EvaluadorNutricional.detectar_bajo_peso_consecutivo(controles):
            alertas.append("Bajo peso consecutivo")

        if EvaluadorNutricional.detectar_var_bruscas(controles):
            alertas.append("Variación brusca de peso")

        if EvaluadorNutricional.detectar_falta_crecimiento(controles):
            alertas.append("Falta de crecimiento en talla")

        if EvaluadorNutricional.detectar_obs_repetidas(controles):
            alertas.append("Observaciones repetidas")

        return " | ".join(alertas) if alertas else "Sin alerta"