from services.evaluador_nutricional import EvaluadorNutricional

class SistemaSaludEscolar:

    def __init__(self):
        self.estudiantes = []

    # ===== RF01 / RF02 =====
    def registrar_estudiante(self, estudiante):
        # Evitar duplicados por código
        if self.buscar_estudiante(estudiante.codigo):
            raise ValueError("El estudiante ya existe")
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
        for k, v in kwargs.items():
            if hasattr(e, k):
                setattr(e, k, v)

    def eliminar_estudiante(self, codigo: str):
        self.estudiantes = [e for e in self.estudiantes if e.codigo != codigo]

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