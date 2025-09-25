class PolicyStub:
    def __init__(self, bloqueados=None, permitir_reserva=False, dias=7):
        self._bloqueados = set(bloqueados or [])
        self._permitir_reserva = permitir_reserva
        self._dias = dias

    def permite_prestamo(self, usuario_id, libro_id):
        return usuario_id not in self._bloqueados

    def permite_reserva(self, usuario_id, libro_id):
        return self._permitir_reserva

    def dias_prestamo(self, usuario_id, libro_id):
        return self._dias
