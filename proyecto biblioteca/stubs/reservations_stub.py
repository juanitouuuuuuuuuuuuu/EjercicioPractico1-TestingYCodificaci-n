class ReservationsStub:
    def __init__(self):
        self.reservas = []  # [(usuario_id, libro_id), ...]

    def crear_reserva(self, usuario_id, libro_id):
        self.reservas.append((usuario_id, libro_id))
        return True
