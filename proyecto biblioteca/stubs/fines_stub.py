class FinesStub:
    def __init__(self, usuarios_bloqueados=None):
        self.block = set(usuarios_bloqueados or [])

    def bloqueado(self, usuario_id):
        return usuario_id in self.block
