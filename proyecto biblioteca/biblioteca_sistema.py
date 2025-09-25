class NullPolicy:
    def permite_prestamo(self, usuario_id, libro_id): return True
    def permite_reserva(self, usuario_id, libro_id): return False
    def dias_prestamo(self, usuario_id, libro_id): return 7

class NullNotifier:
    def enviar(self, usuario_id, mensaje): return True

class NullCalendar:
    def fecha_devolucion(self, hoy, dias): return hoy

class NullFines:
    def bloqueado(self, usuario_id): return False

class NullTx:
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): return False  # no suprime excepciones

class NullReservations:
    def crear_reserva(self, usuario_id, libro_id): return False

class BibliotecaSistema:
    def __init__(self, db, auth,
                 policy=None, notifier=None, calendar=None,
                 fines=None, tx=None, reservations=None):
        self.db = db
        self.auth = auth
        self.policy = policy or NullPolicy()
        self.notifier = notifier or NullNotifier()
        self.calendar = calendar or NullCalendar()
        self.fines = fines or NullFines()
        self.tx = tx or NullTx()
        self.reservations = reservations or NullReservations()

    def prestar_libro(self, usuario_id, libro_id, hoy=None):
        if not self.auth.verificar_usuario(usuario_id):
            return "Usuario no autorizado"
        if self.fines.bloqueado(usuario_id):
            return "Usuario bloqueado por deuda"
        if not self.policy.permite_prestamo(usuario_id, libro_id):
            return "Préstamo denegado por política"
        if not self.db.libro_disponible(libro_id):
            if self.policy.permite_reserva(usuario_id, libro_id):
                self.reservations.crear_reserva(usuario_id, libro_id)
                return "Libro no disponible: reserva creada"
            return "Libro no disponible"

        with self.tx:
            self.db.registrar_prestamo(usuario_id, libro_id)
            if hoy is not None:
                due = self.calendar.fecha_devolucion(
                    hoy, self.policy.dias_prestamo(usuario_id, libro_id)
                )
            else:
                due = None
            self.notifier.enviar(
                usuario_id,
                f"Préstamo confirmado para libro {libro_id}"
                + (f". Devuelve el {due}" if due else "")
            )
        return "Préstamo exitoso"