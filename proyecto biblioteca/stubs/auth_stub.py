class AuthStub:
    """Stub que simula autenticación"""

    def verificar_usuario(self, usuario_id):
        # STUB: Usuarios con ID > 0 están autorizados
        return usuario_id > 0
