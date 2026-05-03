import uuid

def generar_codigo():
    return str(uuid.uuid4())[:8]