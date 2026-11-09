import logging
from abc import abstractmethod

from FASE4 import SuperEntidad, Cliente, ProductoError, ReservaError


# =================================================================================================================
# CONTRATO DE Servicio (TEMPORAL)
# nesesitava crear esta clase para probar Reserva mientras el Participante 2 hace la parte de el, despues se borra
# =================================================================================================================
class Servicio(SuperEntidad):

    def __init__(self, id_entidad, nombre, costo_base, disponible=True):
        super().__init__(id_entidad)
        self.nombre = nombre            
        self.costo_base = costo_base    
        self.disponible = disponible    

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:

    @abstractmethod
    def describir(self) -> str:

    @abstractmethod
    def validar_parametros(self, duracion) -> None:
        
