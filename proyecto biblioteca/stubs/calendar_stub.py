from datetime import timedelta

class CalendarStub:
    def __init__(self, feriados=None):
        self.feriados = set(feriados or [])

    def fecha_devolucion(self, hoy, dias):
        fecha = hoy
        pendientes = dias
        while pendientes > 0:
            fecha += timedelta(days=1)
            if fecha.weekday() < 5 and fecha not in self.feriados:  # L-V hábil
                pendientes -= 1
        return fecha
