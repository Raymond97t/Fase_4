"""
Gestión e integración del procesamiento de reservas de Software FJ.

Este módulo coordina objetos Reserva con los servicios definidos en FASE4.py
"""

import logging
from pathlib import Path

from FASE4 import(
    Alquiler_Equipos,
    Asesorias_Especializadas,
    ProductoError,
    ReservaError,
    Reserva_Salas,
)
from reserva import Reserva


#El registro se guarda en una carpeta independiente llamada logs.
CARPETA_LOGS = Path(__file__).resolve().parent / "logs"
CARPETA_LOGS.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("gestor_reservas")
logger.setLevel(logging.INFO)
logger.propagate = False


if not any(
    isinstance(manejador, logging.FileHandler)
    and Path(manejador.baseFilename) == (CARPETA_LOGS / "gestor_reservas.log").resolve()
    for manejador in logger.handlers
):
    manejador_archivo = logging.FileHandler(
        CARPETA_LOGS / "gestor_reservas.log", encoding="utf-8"
    )
    manejador_archivo.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
    )
    logger.addHandler(manejador_archivo)

class GestorReservas:
    """Administra el procesamiento y la disponibilidad de las reservas.
    """
    def __init__(self):
        self._reservas_procesadas = {}
        #Cantidad de  asistentes o unidades comprometidas por ID de servicio.
        self._ocupacion = {}
    @staticmethod
    def _obtener_cantidad(reserva, opciones):
        """Obtiene y valida la cantidad de recursos solicidatos."""
        parametros_guardados = getattr(reserva, "_parametros_servicio", {})
        parametros = dict(parametros_guardados)
        parametros.update(opciones)

        if isinstance(reserva.servicio, Reserva_Salas):
            cantidad = parametros.get("asistentes", 1)
            nombre = "El número de asistentes"
        elif isinstance(reserva.servicio, Reserva_Salas):
            cantidad = parametros.get("cantidad", 1)
            nombre = "La cantidad de equipos"
        else:
            return 0

        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ReservaError(f"{nombre} debe ser un entero positivo.")
        return cantidad

    def verificar_disponibilidad(self, reserva, **opciones):
        """Comprueba capacidad de sala o stock antes de procesar la reserva."""
        if not isinstance(reserva, Reserva):
            raise ReservaError("El elemento recibido no es una reserva válida.")

        servicio = reserva.servicio
        cantidad = self._obtener_cantidad(reserva, opciones)
        comprometido = self._ocupacion.get(servicio.id_entidad, 0)

        try:
            if isinstance(servicio, Reserva_Salas):
                total_solicitado = comprometido + cantidad
                #Se consulta el método de disponibilidad implementado por el servicio.
                servicio.descripcion_servicio(asistentes= total_solicitado)
            elif isinstance(servicio, Alquiler_Equipos):
                total_solicitado = comprometido - cantidad
                servicio.descripcion_servicio(cantidad=total_solicitado)
            else:
                servicio.descripcion_servicio(**opciones)

            logger.info(
                "Disponivilidad verificada para la reserva %s y el servicio %s.",
                reserva.id_entidad,
                servicio.id_entidad,
            )
            return True
        except ProductoError as error:
            logger.exception(
                "Disponibilidad insuficiente para la reserva %s.", reserva.id_entidad
            )
            raise ReservaError(
                f"No hay disponibilidad para le reserva {reserva.id_entidad}: {error}"
            ) from error
        except Exception as error:
            logger.exception(
                "Error verificando disponibilidad de la reserva %s.",
                reserva.id_entidad,
            )
            raise ReservaError(
                f"No se pudo verificar la disponivilidad: {error}"
            ) from error
        
    def procesar_reserva(self, reserva, **opciones):
        """Verifica disponibilidad, procesa y confirma una reserva."""
        if not isinstance(reserva, Reserva):
            error = ReservaError("El elemento recibido no es una reserva válida.")
            logger.error("%s", error)
            raise error
        if reserva.id_entidad in self._reservas_procesadas:
            error = ReservaError(
                f"Ya existe una reserva procesada con ID {reserva.id_entidad}."
            )
            logger.error("%s", error)
            raise error

        try:
            self.verificar_disponibilidad(reserva, **opciones)
            costo = reserva.procesar(**opciones)

            cantidad = self._obtener_cantidad(reserva, opciones)
            if cantidad:
                servicio_id = reserva.servicio.id_entidad
                self._ocupacion[servicio_id] = (
                    self._ocupacion.get(servicio_id, 0) + cantidad
                )

            self._reservas_procesadas[reserva.id_entidad] = reserva
            logger.info(
                "Reserva %s confirmada correctamente. Costo %.2f.",
                reserva.id_entidad,
                costo,
            )
            return costo
        except ReservaError as error:
            logger.exception(
                "No se pudo procesar la reserva %s.", reserva.id_entidad
            )
            # Si ya existe una causa, se conserva la cadena original.
            if error.__cause__ is not None:
                raise
            raise ReservaError(
                f"Fallo en el gestor al procesar la reserva {reserva.id_entidad}: {error}"
            ) from error
        except Exception as error:
            logger.exception(
                "Error inesperado procesando la reserva %s.", reserva.id_entidad
            )
            raise ReservaError(
                f"Error inesperado en el procesamiento de la reserva: {error}"
            ) from error
    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva procesada y libera su capacidad registrada."""
        reserva = self._reservas_procesadas.get(id_reserva)
        if reserva is None:
            raise ReservaError(f"No se encontró la reserva procesada {id_reserva}.")

        try:
            cantidad = self._obtener_cantidad(reserva, {})
            reserva.cancelar()
            if cantidad:
                servicio_id = reserva.servicio.id_entidad
                restante = self._ocupacion.get(servicio_id, 0) - cantidad
                self._ocupacion[servicio_id] = max(0, restante)
            del self._reservas_procesadas[id_reserva]
            logger.info("Reserva %s cancelada y disponibilidad liberada.", id_reserva)
            return True
        except Exception as error:
            logger.exception("No se pudo cancelar la reserva %s.", id_reserva)
            raise ReservaError(
                f"Error al cancelar la reserva {id_reserva}: {error}"
            ) from error

    def listar_reservas(self):
        """Devuelve los detalles de las reservas procesadas actualmente."""
        return [reserva.DetallesEntidad() for reserva in self._reservas_procesadas.values()]
