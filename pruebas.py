"""Pruebas de integración para el gestor de reservas."""

from pathlib import Path

from FASE4 import (
    Alquiler_Equipos,
    Asesorias_Especializadas,
    Cliente,
    ProductoError,
    ReservaError,
    Reserva_Salas,
)

from reserva import Reserva
from gestor_reservas import GestorReservas


def ejecutar_pruebas():

    gestor = GestorReservas()

    cliente = Cliente(
        "C100",
        "Ana Perez",
        "ana@example.com",
        "3001234567"
    )

    sala = Reserva_Salas(
        "S100",
        "Sala de reuniones",
        100000,
        20
    )

    equipo = Alquiler_Equipos(
        "E100",
        "Proyector",
        25000,
        3
    )

    asesoria = Asesorias_Especializadas(
        "A100",
        "Asesoria tecnologica",
        80000,
        "Avanzado"
    )

    print("\n===== PRUEBAS DE INTEGRACION =====")

    # 1. Reserva exitosa de una sala
    reserva_sala = Reserva(
        "R100",
        cliente,
        sala,
        2,
        asistentes=12
    )

    costo_sala = gestor.procesar_reserva(
        reserva_sala,
        impuesto=0.19,
        descuento=0.10
    )

    assert costo_sala > 0
    assert reserva_sala.estado == Reserva.CONFIRMADA

    print("OK - Reserva de sala confirmada")

    # 2. Intento de reserva sin capacidad disponible
    reserva_sala_sin_cupo = Reserva(
        "R101",
        cliente,
        sala,
        1,
        asistentes=10
    )

    try:
        gestor.procesar_reserva(reserva_sala_sin_cupo)

    except ReservaError as error:
        assert isinstance(error.__cause__, ProductoError)
        print("OK - Error de capacidad controlado")

    else:
        raise AssertionError(
            "Se debia rechazar la reserva por falta de capacidad."
        )

    # 3. Reserva exitosa de equipos
    reserva_equipo = Reserva(
        "R102",
        cliente,
        equipo,
        2,
        cantidad=2
    )

    costo_equipo = gestor.procesar_reserva(
        reserva_equipo,
        seguro=15000
    )

    assert costo_equipo > 0
    assert reserva_equipo.estado == Reserva.CONFIRMADA

    print("OK - Reserva de equipos confirmada")

    # 4. Intento de reserva sin stock
    reserva_equipo_sin_stock = Reserva(
        "R103",
        cliente,
        equipo,
        1,
        cantidad=2
    )

    try:
        gestor.procesar_reserva(reserva_equipo_sin_stock)

    except ReservaError as error:
        assert isinstance(error.__cause__, ProductoError)
        print("OK - Error de inventario controlado")

    else:
        raise AssertionError(
            "Se debia rechazar la reserva por falta de stock."
        )

    # 5. Reserva exitosa de asesoria
    reserva_asesoria = Reserva(
        "R104",
        cliente,
        asesoria,
        1.5
    )

    costo_asesoria = gestor.procesar_reserva(
        reserva_asesoria,
        complejidad=1.2
    )

    assert costo_asesoria > 0
    assert reserva_asesoria.estado == Reserva.CONFIRMADA

    print("OK - Reserva de asesoria confirmada")

    # 6. Intento de procesar una reserva cancelada
    reserva_cancelada = Reserva(
        "R105",
        cliente,
        sala,
        1,
        asistentes=1
    )

    reserva_cancelada.cancelar()

    try:
        gestor.procesar_reserva(reserva_cancelada)

    except ReservaError:
        print("OK - Reserva cancelada rechazada")

    else:
        raise AssertionError(
            "No se debia procesar una reserva cancelada."
        )

    # 7. Comprobar que el sistema sigue funcionando
    reserva_posterior = Reserva(
        "R106",
        cliente,
        sala,
        1,
        asistentes=2
    )

    costo_posterior = gestor.procesar_reserva(
        reserva_posterior
    )

    assert costo_posterior > 0
    assert reserva_posterior.estado == Reserva.CONFIRMADA

    print("OK - El sistema continuo funcionando despues de los errores")

    # 8. Comprobar liberacion de capacidad al cancelar
    assert gestor.cancelar_reserva("R100") is True

    reserva_con_cupo_liberado = Reserva(
        "R107",
        cliente,
        sala,
        1,
        asistentes=15
    )

    gestor.procesar_reserva(reserva_con_cupo_liberado)

    assert reserva_con_cupo_liberado.estado == Reserva.CONFIRMADA

    print("OK - La cancelacion libero la capacidad")

    # 9. Verificar archivo de registro de errores
    archivo_log = (
        Path(__file__).resolve().parent
        / "logs"
        / "gestor_reservas.log"
    )

    assert archivo_log.exists(), (
        "No se creo el archivo de registro."
    )

    assert archivo_log.stat().st_size > 0, (
        "El archivo de registro esta vacio."
    )

    contenido_log = archivo_log.read_text(
        encoding="utf-8"
    )

    assert "ERROR" in contenido_log, (
        "No se encontraron errores en el registro."
    )

    print("OK - Registro de errores verificado")

    print("\nTodas las pruebas finalizaron correctamente.")

    print(
        "Reservas activas:",
        len(gestor.listar_reservas())
    )
