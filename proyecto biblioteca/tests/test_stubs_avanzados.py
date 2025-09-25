from datetime import date
from unittest.mock import MagicMock
import pytest
from biblioteca_sistema import BibliotecaSistema
from stubs.policy_stub import PolicyStub
from stubs.notifier_stub import NotifierStub
from stubs.calendar_stub import CalendarStub
from stubs.fines_stub import FinesStub
from stubs.tx_stub import TxStub
from stubs.reservations_stub import ReservationsStub

def test_principal_con_notificacion_y_fecha_limite():
    db = MagicMock()
    db.libro_disponible.return_value = True
    auth = MagicMock(); auth.verificar_usuario.return_value = True
    notifier = NotifierStub()
    calendar = CalendarStub()
    policy = PolicyStub(dias=5)

    sistema = BibliotecaSistema(db, auth, policy=policy,
                                notifier=notifier, calendar=calendar)

    r = sistema.prestar_libro(1, 2, hoy=date(2025, 9, 24))
    assert r == "Préstamo exitoso"
    assert notifier.enviados and "Devuelve el" in notifier.enviados[0][1]


def test_bloqueado_por_deuda_con_finesstub():
    db = MagicMock()
    auth = MagicMock(); auth.verificar_usuario.return_value = True
    fines = FinesStub(usuarios_bloqueados=[99])
    sistema = BibliotecaSistema(db, auth, fines=fines)
    assert sistema.prestar_libro(99, 2) == "Usuario bloqueado por deuda"
    db.libro_disponible.assert_not_called()


def test_reserva_cuando_no_disponible_y_politica_lo_permita():
    db = MagicMock()
    db.libro_disponible.return_value = False
    auth = MagicMock(); auth.verificar_usuario.return_value = True
    policy = PolicyStub(permitir_reserva=True)
    reservations = ReservationsStub()

    sistema = BibliotecaSistema(db, auth, policy=policy, reservations=reservations)
    assert sistema.prestar_libro(1, 2) == "Libro no disponible: reserva creada"
    assert reservations.reservas == [(1, 2)]


def test_rollback_si_falla_notificador():
    db = MagicMock()
    db.libro_disponible.return_value = True
    auth = MagicMock(); auth.verificar_usuario.return_value = True
    notifier = NotifierStub(falla=True)
    txlog = []
    tx = TxStub(log=txlog)

    sistema = BibliotecaSistema(db, auth, notifier=notifier, tx=tx)
    with pytest.raises(RuntimeError):
        sistema.prestar_libro(1, 2)

    # Asegura que se intentó registrar pero se hizo rollback
    db.registrar_prestamo.assert_called_once_with(1, 2)
    assert txlog == ["BEGIN", "ROLLBACK"]
