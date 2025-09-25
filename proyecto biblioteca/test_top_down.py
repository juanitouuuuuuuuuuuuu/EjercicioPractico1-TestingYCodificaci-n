from unittest.mock import MagicMock
import pytest
from biblioteca_sistema import BibliotecaSistema
from stubs.auth_stub import AuthStub
from stubs.database_stub import DatabaseStub

def test_libro_no_disponible():
    db = MagicMock()
    db.libro_disponible.return_value = False
    auth = MagicMock()
    auth.verificar_usuario.return_value = True

    sistema = BibliotecaSistema(db, auth)
    r = sistema.prestar_libro(usuario_id=1, libro_id=123)

    assert r == "Libro no disponible"
    auth.verificar_usuario.assert_called_once_with(1)
    db.libro_disponible.assert_called_once_with(123)
    db.registrar_prestamo.assert_not_called()


def test_no_toca_bd_si_no_autorizado():
    db = MagicMock()
    auth = MagicMock()
    auth.verificar_usuario.return_value = False

    sistema = BibliotecaSistema(db, auth)
    r = sistema.prestar_libro(usuario_id=0, libro_id=2)

    assert r == "Usuario no autorizado"
    auth.verificar_usuario.assert_called_once_with(0)
    db.libro_disponible.assert_not_called()
    db.registrar_prestamo.assert_not_called()


def test_registra_prestamo_con_args_correctos():
    db = MagicMock()
    db.libro_disponible.return_value = True
    auth = MagicMock()
    auth.verificar_usuario.return_value = True

    sistema = BibliotecaSistema(db, auth)
    r = sistema.prestar_libro(usuario_id=7, libro_id=42)

    assert r == "Préstamo exitoso"
    db.registrar_prestamo.assert_called_once_with(7, 42)


def test_error_al_registrar_se_propagara():
    db = MagicMock()
    db.libro_disponible.return_value = True
    db.registrar_prestamo.side_effect = RuntimeError("Fallo en BD")
    auth = MagicMock()
    auth.verificar_usuario.return_value = True

    sistema = BibliotecaSistema(db, auth)
    with pytest.raises(RuntimeError):
        sistema.prestar_libro(usuario_id=1, libro_id=2)


@pytest.mark.parametrize("usuario_id,libro_id,esperado", [
    (1, 2, "Préstamo exitoso"),     # autorizado + disponible
    (1, 3, "Libro no disponible"),  # autorizado + no disponible
    (0, 2, "Usuario no autorizado"),# no autorizado
    (-5, 2, "Usuario no autorizado")# límite negativo (según tu AuthStub: >0 autoriza)
])
def test_parametrizado_con_stubs(usuario_id, libro_id, esperado):
    # Usa tus stubs reales para probar el contrato de alto nivel
    sistema = BibliotecaSistema(DatabaseStub(), AuthStub())
    assert sistema.prestar_libro(usuario_id, libro_id) == esperado


def test_orden_de_flujo_auth_antes_que_disponibilidad():
    # Asegura que si auth falla, ni siquiera preguntemos disponibilidad
    db = MagicMock()
    auth = MagicMock()
    auth.verificar_usuario.return_value = False

    sistema = BibliotecaSistema(db, auth)
    _ = sistema.prestar_libro(usuario_id=0, libro_id=999)

    auth.verificar_usuario.assert_called_once()
    db.libro_disponible.assert_not_called()
