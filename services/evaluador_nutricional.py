class EvaluadorNutricional:
    # Atributos de clase (compartidos)
    UMBRAL_BAJO_PESO = 18.5
    UMBRAL_SOBREPESO = 25
    UMBRAL_OBESIDAD = 30

    @classmethod
    def clasificar_estado(cls, imc: float) -> str:
        if imc < cls.UMBRAL_BAJO_PESO:
            return "Bajo peso"
        elif imc < cls.UMBRAL_SOBREPESO:
            return "Normal"
        elif imc < cls.UMBRAL_OBESIDAD:
            return "Sobrepeso"
        else:
            return "Obesidad"

    # ---- Reglas simples de alertas (RF05) ----
    @staticmethod
    def detectar_bajo_peso_consecutivo(controles) -> bool:
        if len(controles) < 2:
            return False
        estados = [EvaluadorNutricional.clasificar_estado(c.get_imc()) for c in controles[-2:]]
        return all(e == "Bajo peso" for e in estados)

    @staticmethod
    def detectar_var_bruscas(controles) -> bool:
        if len(controles) < 2:
            return False
        c1, c2 = controles[-2], controles[-1]
        return abs(c2.peso.get_valor() - c1.peso.get_valor()) >= 5  # umbral simple

    @staticmethod
    def detectar_falta_crecimiento(controles) -> bool:
        if len(controles) < 2:
            return False
        c1, c2 = controles[-2], controles[-1]
        return c2.talla.get_valor() <= c1.talla.get_valor()  # no crece

    @staticmethod
    def detectar_obs_repetidas(controles) -> bool:
        if len(controles) < 2:
            return False
        c1, c2 = controles[-2], controles[-1]
        return bool(c1.observaciones and c1.observaciones == c2.observaciones)