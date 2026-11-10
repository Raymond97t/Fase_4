
 import logging

from FASE4 import SuperEntidad, Cliente, Servicio, ReservaError


class Reserva(SuperEntidad):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"

    def __init__(self, id_entidad: str, cliente: Cliente, servicio: Servicio, duracion: float):
        super().__init__(id_entidad)
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            self._fallar("El id de la reserva debe ser un texto no vacío.")
        if not isinstance(cliente, Cliente):
            self._fallar("La reserva necesita un cliente válido.")
        if not isinstance(servicio, Servicio):
            self._fallar("La reserva necesita un servicio válido.")
        self._cliente = cliente
        self._servicio = servicio
        self.duracion = duracion  # pasa por el setter con validación
        self._estado = Reserva.PENDIENTE
        logging.info("Reserva %s creada (cliente %s, servicio %s).",
                     self.id_entidad, cliente.id_entidad, servicio.nombre_servicio)

    
    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def duracion(self) -> float:
        return self._duracion

    @duracion.setter
    def duracion(self, valor: float):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor <= 0:
            self._fallar("La duración debe ser un número mayor que 0.")
        self._duracion = valor

    
    def _fallar(self, mensaje: str, causa: Exception = None):
        """Registra el error en el log y lanza ReservaError (encadenado si hay causa)."""
        logging.error("Reserva %s: %s", self.id_entidad, mensaje)
        raise ReservaError(mensaje) from causa

    
    def confirmar(self) -> None:
        """Pasa la reserva a 'confirmada'. Lanza ReservaError si no se puede."""
        if self._estado == Reserva.CANCELADA:
            self._fallar("No se puede confirmar una reserva cancelada.")
        if self._estado == Reserva.CONFIRMADA:
            self._fallar("La reserva ya está confirmada.")
        self._estado = Reserva.CONFIRMADA
        logging.info("Reserva %s confirmada.", self.id_entidad)

    def cancelar(self) -> None:
        """Pasa la reserva a 'cancelada'. Lanza ReservaError si ya estaba cancelada."""
        if self._estado == Reserva.CANCELADA:
            self._fallar("La reserva ya estaba cancelada.")
        self._estado = Reserva.CANCELADA
        logging.info("Reserva %s cancelada.", self.id_entidad)

    
    def DetallesEntidad(self) -> str:
        return (f"Reserva[ID:{self.id_entidad}, Cliente:{self._cliente.nombre}, "
                f"Servicio:{self._servicio.nombre_servicio}, Duración:{self._duracion}, "
                f"Estado:{self._estado}]")

    def __str__(self) -> str:
        return self.DetallesEntidad()
