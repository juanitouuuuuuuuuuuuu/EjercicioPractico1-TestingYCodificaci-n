class NotifierStub:
    def __init__(self, falla=False):
        self.enviados = []   # [(usuario_id, msg), ...]
        self.falla = falla

    def enviar(self, usuario_id, mensaje):
        if self.falla:
            raise RuntimeError("Fallo en notificador")
        self.enviados.append((usuario_id, mensaje))
        return True
