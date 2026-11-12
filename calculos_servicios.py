
"""
Archivo: calculos_servicios.py
Métodos sobrecargados - Cálculos y polimorfismo.

Permite calcular los costos básicos de los servicios,
aplicar impuestos, descuentos y utilizar parámetros opcionales.
"""

import math

from FASE4 import (
    Servicio,
    Reserva_Salas,
    Alquiler_Equipos,
    Asesorias_Especializadas,
    ProductoError
)


class CalculadoraServicios:
    """Realiza los cálculos de costos de los servicios."""

    @staticmethod
    def validar_numero(valor, nombre, minimo=0, maximo=None):
        """Valida que los valores sean numéricos y correctos."""

        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ProductoError(f"{nombre} debe ser un número.")

        if not math.isfinite(valor):
            raise ProductoError(f"{nombre} debe ser un número finito.")

        if valor < minimo:
            raise ProductoError(f"{nombre} no puede ser negativo o inválido.")

        if maximo is not None and valor > maximo:
            raise ProductoError(f"{nombre} supera el límite permitido.")

        return float(valor)

    @staticmethod
    def calcular_basico(servicio: Servicio, duracion: float,
                        seguro: float = 0.0,
                        complejidad: float = 1.0) -> float:
        """
        Calcula el costo básico según el tipo de servicio.
        Incluye parámetros opcionales cuando son necesarios.
        """

        if not isinstance(servicio, Servicio):
            raise ProductoError("El servicio no es válido.")

        duracion = CalculadoraServicios.validar_numero(
            duracion, "La duración", minimo=0.000001
        )

        seguro = CalculadoraServicios.validar_numero(
            seguro, "El seguro"
        )

        complejidad = CalculadoraServicios.validar_numero(
            complejidad, "La complejidad", minimo=0.000001
        )

        if isinstance(servicio, Reserva_Salas):
            return servicio.calcular_costos(
                duracion, descuento=0.0, impuesto=0.0
            )

        elif isinstance(servicio, Alquiler_Equipos):
            return servicio.calcular_costos(
                duracion, seguro=seguro, descuento=0.0
            )

        elif isinstance(servicio, Asesorias_Especializadas):
            return servicio.calcular_costos(
                duracion, complejidad=complejidad
            )

        raise ProductoError("Tipo de servicio no reconocido.")

    @staticmethod
    def calcular_con_impuesto(servicio: Servicio, duracion: float,
                              impuesto: float = 0.19,
                              seguro: float = 0.0,
                              complejidad: float = 1.0) -> float:
        """
        Calcula el costo básico incluyendo impuestos.
        El impuesto se expresa en formato decimal.
        Ejemplo: 0.19 equivale al 19%.
        """

        impuesto = CalculadoraServicios.validar_numero(
            impuesto, "El impuesto", minimo=0, maximo=1
        )

        subtotal = CalculadoraServicios.calcular_basico(
            servicio, duracion, seguro, complejidad
        )

        return subtotal * (1 + impuesto)

    @staticmethod
    def calcular_con_descuento(servicio: Servicio, duracion: float,
                               descuento: float = 0.10,
                               seguro: float = 0.0,
                               complejidad: float = 1.0) -> float:
        """
        Calcula el costo básico aplicando un descuento.
        Ejemplo: 0.10 equivale al 10%.
        """

        descuento = CalculadoraServicios.validar_numero(
            descuento, "El descuento", minimo=0, maximo=1
        )

        subtotal = CalculadoraServicios.calcular_basico(
            servicio, duracion, seguro, complejidad
        )

        return subtotal * (1 - descuento)

    @staticmethod
    def calcular_personalizado(servicio: Servicio, duracion: float,
                               impuesto: float = 0.0,
                               descuento: float = 0.0,
                               seguro: float = 0.0,
                               complejidad: float = 1.0) -> float:
        """
        Permite combinar impuestos, descuentos y parámetros
        opcionales para obtener un costo personalizado.
        """

        impuesto = CalculadoraServicios.validar_numero(
            impuesto, "El impuesto", minimo=0, maximo=1
        )

        descuento = CalculadoraServicios.validar_numero(
            descuento, "El descuento", minimo=0, maximo=1
        )

        subtotal = CalculadoraServicios.calcular_basico(
            servicio, duracion, seguro, complejidad
        )

        total = subtotal * (1 - descuento)
        return total * (1 + impuesto)


# ---------------------------------------------------------
# PRUEBAS DE FUNCIONAMIENTO
# ---------------------------------------------------------

def ejecutar_pruebas():
    """Prueba los cálculos con los tres servicios disponibles."""

    sala = Reserva_Salas(
        "S001", "Sala de conferencias", 300.0, 50
    )

    equipo = Alquiler_Equipos(
        "E001", "Proyector", 100.0, 5
    )

    asesoria = Asesorias_Especializadas(
        "A001", "Marketing Digital", 150.0, "Avanzado"
    )

    servicios = [
        ("Reserva de salas", sala),
        ("Alquiler de equipos", equipo),
        ("Asesorías especializadas", asesoria)
    ]

    print("\n===== CÁLCULOS BÁSICOS =====")

    for nombre, servicio in servicios:
        try:
            costo = CalculadoraServicios.calcular_basico(
                servicio, 2
            )
            print(f"{nombre}: ${costo:,.2f}")
        except ProductoError as error:
            print(f"Error en {nombre}: {error}")

    print("\n===== CÁLCULOS CON IMPUESTOS =====")

    for nombre, servicio in servicios:
        try:
            costo = CalculadoraServicios.calcular_con_impuesto(
                servicio, 2, impuesto=0.19
            )
            print(f"{nombre}: ${costo:,.2f}")
        except ProductoError as error:
            print(f"Error en {nombre}: {error}")

    print("\n===== CÁLCULOS CON DESCUENTOS =====")

    for nombre, servicio in servicios:
        try:
            costo = CalculadoraServicios.calcular_con_descuento(
                servicio, 2, descuento=0.10
            )
            print(f"{nombre}: ${costo:,.2f}")
        except ProductoError as error:
            print(f"Error en {nombre}: {error}")

    print("\n===== CÁLCULO PERSONALIZADO =====")

    try:
        costo = CalculadoraServicios.calcular_personalizado(
            equipo, 3, impuesto=0.19,
            descuento=0.10, seguro=50
        )
        print(f"Equipo con seguro: ${costo:,.2f}")
    except ProductoError as error:
        print(f"Error: {error}")

    print("\n===== VALIDACIÓN DE ERRORES =====")

    pruebas_invalidas = [
        ("Duración negativa",
         lambda: CalculadoraServicios.calcular_basico(sala, -2)),
        ("Descuento inválido",
         lambda: CalculadoraServicios.calcular_con_descuento(
             sala, 2, descuento=1.5)),
        ("Impuesto negativo",
         lambda: CalculadoraServicios.calcular_con_impuesto(
             sala, 2, impuesto=-0.19))
    ]

    for nombre, prueba in pruebas_invalidas:
        try:
            prueba()
        except ProductoError as error:
            print(f"{nombre}: {error}")

    print("\n===== FIN DE LAS PRUEBAS =====")


if __name__ == "__main__":
    ejecutar_pruebas()
