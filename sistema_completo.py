from abc import ABC, abstractmethod
import logging

#Modulo de logging para registrar errores en un archivo de log. 
logging.basicConfig(
    filename='Error.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(lineno)d - %(filename)s',
    encoding='utf-8'
)
#Clases de excepciones personalizadas para manejar errores específicos del sistema. Luego registramos los errores en el archivo de log con las excepciones personalizadas.
class SistemaError(Exception):
    pass

class ClienteError(SistemaError):
    pass

class ProductoError(SistemaError):
    pass

class ReservaError(SistemaError):
    pass

#Primer requerimiento: Crear una clase abstracta que represente los requerimientos basicos que surjan dentro del sistema, como la clase SuperEntidad que tiene un atributo id_entidad y un método abstracto DetallesEntidad, este ultimo para mostrar los detalles de cada elemento del sistema.
class SuperEntidad(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad 
        
    @property
    def id_entidad(self) -> str:
        return self._id_entidad
        
    @abstractmethod
    def DetallesEntidad(self) -> str:
        pass
        
#Segundo requerimiento: Crear una clase Cliente que herede de SuperEntidad y tenga atributos como nombre, correo y telefono. Aun no tiene el registro de errores en al archivo de log, pero se implementará en la clase Reserva, más adelante, junto con las cadenas de try/except para capturar y registrar los errores personalizados.
class Cliente(SuperEntidad):
    def __init__(self, id_entidad: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_entidad)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono 
    #Si creen conveniente añadir algun otro atributo me lo hacen saber, por ejmplo, direccion, ciudad, etc. Pero por ahora me parece que con estos atributos es suficiente para representar a un cliente. Adicionalmente si los van a agregar, recuerden añadir la validacion de errores en el setter correspondiente, como se hizo con los atributos actuales.  
    @property
    def nombre(self) -> str:
        return self._nombre
    #Cada property tiene su respectivo setter para validar los datos ingresados y lanzar excepciones personalizadas en caso de que los datos no cumplan con los requisitos establecidos. Además de que encapsula los datos y los vuelve más seguros, evitando que se modifiquen directamente desde fuera de la clase, y no se vean afectados si algo cambia dentro de la logica de la clase.    
    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ClienteError("El nombre del cliente debe ser una cadena de al menos 2 caracteres.")
        self._nombre = valor.strip()
        
    @property
    def correo(self) -> str:
        return self._correo 
        
    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteError("El correo del cliente debe ser una cadena válida que contenga '@'.")
        self._correo = valor.strip()
            
    @property
    def telefono(self) -> str:
        return self._telefono 
        
    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not str(valor).isdigit() or len(str(valor)) < 10:
            raise ClienteError("El teléfono del cliente debe tener al menos 10 caracteres.")
        self._telefono = valor.strip()
    #Este metodo DetallesEntidad es el que se implementa de la clase abstracta SuperEntidad, y retorna una cadena con los detalles del cliente. Se uso en el resto del codigo para la misma finalidad en cada caso. Retornar una cadena con los detalles de la entidad (Requerimiento) correspondiente.
    def DetallesEntidad(self) -> str:
        return f"Cliente[ID: {self.id_entidad}, Nombre: {self.nombre}, Correo: {self.correo}, Teléfono: {self.telefono}]"

#Tercer requerimiento: Crear una clase abstracta Servicio que permita definir los servicios que se ofrecen en el sistema, con atributos como nombre_servicio y precio_base, y métodos abstractos calcular_costos y descripcion_servicio. Esta clase también hereda de SuperEntidad para mantener la consistencia en la estructura del sistema. Mas adelante servira para gestionar con herencia, polimorfismo, argumentos sobre escritos los servicios que se ofrecen en el sistema, como la reserva de salas, alquiler de equipos y asesorías especializadas.
class Servicio(SuperEntidad, ABC):
    def __init__(self, id_entidad: str, nombre_servicio: str, precio_base: float):
        super().__init__(id_entidad)
        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base
    #Nuevamente el metodo constructor con los atributos que me parecen necesarios para representar un servicio, y los property con sus respectivos setter para validar los datos ingresados y lanzar excepciones personalizadas en caso de que los datos no cumplan con los requisitos establecidos.
        
    @property
    def precio_base(self) -> float:
        return self._precio_base
        
    @precio_base.setter
    def precio_base(self, valor: float):
        if valor is None or valor <= 0:
            raise ProductoError("El precio base del servicio debe ser un número positivo.")
        self._precio_base = valor
        
    @abstractmethod
    def calcular_costos(self, duracion_horas: float, **kwargs) -> float:
        pass    
        
    @abstractmethod
    def descripcion_servicio(self, **kwargs) -> bool:
        pass 
        
    @abstractmethod
    def DetallesEntidad(self) -> str:
        pass 
        
#Requerimiento 3.1: Crear el primer servicio prestado, bajo la clase Reserva_Salas, que hereda de la clase abstracta Servicio, y tiene atributos como capacidad_maxima, y métodos como calcular_costos y descripcion_servicio. Este servicio permite reservar salas para eventos o reuniones, con un precio base por hora y una capacidad máxima de asistentes. Se implementan validaciones para asegurar que los datos ingresados sean correctos y se lanzan excepciones personalizadas en caso de errores.
class Reserva_Salas(Servicio): 
    def __init__(self, id_entidad: str, nombre_servicio: str, precio_base: float, capacidad_maxima: int):
        super().__init__(id_entidad, nombre_servicio, precio_base)
        self.capacidad_maxima = capacidad_maxima
        #El atributo capacidad_maxima es un entero positivo que representa la cantidad máxima de personas que pueden asistir a la sala reservada. Se valida que sea un número entero positivo en el setter correspondiente, y se lanza una excepción personalizada ProductoError en caso de que no cumpla con los requisitos establecidos.
        #Los property y setter permiten encapsular el atributo y evitar que se modifique directamente desde fuera de la clase, asegurando que siempre se cumplan las validaciones establecidas, siguiendo la misma logica de las clases anteriores. Adicionalmente, se implementan los métodos calcular_costos y descripcion_servicio para calcular el costo total de la reserva y verificar que el número de asistentes no exceda la capacidad máxima de la sala, respectivamente.
    @property
    def capacidad_maxima(self) -> int:
        return self._capacidad_maxima
    #El argumento valor es el que se valida para asegurarse de que sea un número entero positivo, y se lanza una excepción personalizada ProductoError en caso de que no cumpla con los requisitos establecidos. Cómo en todos los casos de los setters, de esa manera se realizan las validaciones de manera centralizada y se evita que se modifique directamente el atributo desde fuera de la clase, asegurando que siempre se cumplan las validaciones establecidas.   
    @capacidad_maxima.setter
    def capacidad_maxima(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ProductoError("La capacidad máxima debe ser un número entero positivo.")
        self._capacidad_maxima = valor 
    #El **kwargs permite pasar argumentos adicionales a la función, como el número de asistentes, que se valida para asegurarse de que no exceda la capacidad máxima de la sala. Si el número de asistentes es mayor que la capacidad máxima, se lanza una excepción personalizada ProductoError con un mensaje descriptivo del error.  
    def descripcion_servicio(self, **kwargs) -> bool:
        asistentes = kwargs.get('asistentes', 1)
        if asistentes > self._capacidad_maxima:
            raise ProductoError(f"El número de asistentes ({asistentes}) excede la capacidad máxima de la sala ({self._capacidad_maxima}).")
        return True 
    #La logica de los calculos se maneja con el estandar de porcentaje 100% = 1.0, 50% = 0.5, 25% = 0.25, etc. Para el descuento y el impuesto, de esta manera se puede calcular el costo total de la reserva de manera más sencilla y flexible, permitiendo aplicar descuentos e impuestos de manera proporcional al subtotal calculado.
    def calcular_costos(self, duracion_horas: float, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        if duracion_horas <= 0:
            raise ProductoError("La duración en horas debe ser un número positivo.")
        if not (0.0 <= descuento <= 1.0):
            raise ProductoError("El porcentaje de descuento es inválido. Debe estar entre 0.0 y 1.0")
        
        subtotal = self.precio_base * duracion_horas 
        total = (subtotal * (1.0 - descuento)) * (1.0 + impuesto)
        return total
        
    def DetallesEntidad(self) -> str:
        return f"Reserva de sala {self.nombre_servicio} | Capacidad: {self.capacidad_maxima} personas, Precio Base: ${self.precio_base:,.2f}/h"
        
#Requerimiento 3.2: Crear el segundo servicio prestado, bajo la clase Alquiler_Equipos, que hereda de la clase abstracta Servicio, y tiene atributos como stock_disponible, y métodos como calcular_costos y descripcion_servicio. Este servicio permite alquilar equipos para eventos o reuniones, con un precio base por hora y un stock disponible de equipos. Se implementan validaciones para asegurar que los datos ingresados sean correctos y se lanzan excepciones personalizadas en caso de errores.
class Alquiler_Equipos(Servicio):
    def __init__(self, id_entidad: str, nombre_servicio: str, precio_base: float, stock_disponible: int):
        super().__init__(id_entidad, nombre_servicio, precio_base)
        self.stock_disponible = stock_disponible
    #Mismo criterio para los atributos y el desarrollo de sus metodos, solo que aquí ya no habrá un metodo que use un argumento de porcentaje de impuesto, ya que el alquiler de equipos no tiene impuestos asociados, pero si se puede aplicar un seguro opcional para cubrir posibles daños o pérdidas del equipo alquilado. El seguro se calcula como un valor fijo que se suma al subtotal calculado, y se puede ajustar según las necesidades del cliente. Adicionalmente, manejaremos el stock disponible de los equipos alquilados, para asegurarnos de que no se alquilen más equipos de los que están disponibles en el inventario. Si la cantidad solicitada excede el stock disponible, se lanzará una excepción personalizada ProductoError con un mensaje descriptivo del error.   
    @property
    def stock_disponible(self) -> int:
        return self._stock_disponible
        
    @stock_disponible.setter
    def stock_disponible(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ProductoError("El stock disponible debe ser un número entero no negativo.")
        self._stock_disponible = valor
        
    def descripcion_servicio(self, **kwargs) -> bool:
        cantidad = kwargs.get('cantidad', 1)
        if cantidad > self._stock_disponible:
            raise ProductoError(f"La cantidad solicitada ({cantidad}) excede el stock disponible ({self._stock_disponible}).")
        return True 
        
    def calcular_costos(self, duracion_horas: float, seguro: float = 0.0, descuento: float = 0.0) -> float:
        if duracion_horas <= 0:
            raise ProductoError("La duración en horas debe ser un número positivo.")
        subtotal = (self.precio_base * duracion_horas) + seguro
        if descuento > 0:
            subtotal *= (1.0 - descuento)
        return subtotal
        
    def DetallesEntidad(self) -> str:
        return f"Alquiler de equipo {self.nombre_servicio} | Stock disponible: {self.stock_disponible}, Precio Base: ${self.precio_base:,.2f}/h"
        
#Requerimiento 3.3: Crear el tercer servicio prestado, bajo la clase Asesorias_Especializadas, que hereda de la clase abstracta Servicio, y tiene atributos como especialidad, y métodos como calcular_costos y descripcion_servicio. Este servicio permite ofrecer asesorías especializadas en diferentes áreas, con un precio base por hora y una especialidad determinada. Se implementan validaciones para asegurar que los datos ingresados sean correctos y se lanzan excepciones personalizadas en caso de errores.
class Asesorias_Especializadas(Servicio):
    def __init__(self, id_entidad: str, nombre_servicio: str, precio_base: float, especialidad: str):
        super().__init__(id_entidad, nombre_servicio, precio_base)
        self.especialidad = especialidad 
    #Aquí ya no habrá ni stock disponible ni capacidad máxima, ya que las asesorías especializadas no requieren de estos atributos. En cambio, se implementará un atributo especialidad que permitirá definir el nivel de especialización del servicio ofrecido, y se validará que sea uno de los niveles válidos establecidos en la lista niveles_validos. Si el valor ingresado no es válido, se lanzará una excepción personalizada ProductoError con un mensaje descriptivo del error. Adicional a eso, habrá un multiplicador o duplicador de complejidad que permitirá ajustar el costo del servicio según el nivel de especialización, y se aplicará en el método calcular_costos para calcular el costo total del servicio ofrecido.
    @property 
    def especialidad(self) -> str:
        return self._especialidad
        
    @especialidad.setter
    def especialidad(self, valor: str):
        niveles_validos = ["Básico", "Intermedio", "Avanzado"]
        if valor not in niveles_validos:
            raise ProductoError(f"La especialidad debe ser uno de los siguientes niveles: ({niveles_validos}).")
        self._especialidad = valor
        
    def descripcion_servicio(self, **kwargs) -> bool:
        return True
        
    def calcular_costos(self, duracion_horas: float, complejidad: float = 1.0) -> float:
        if duracion_horas <= 0:
            raise ProductoError("La duración en horas debe ser un número positivo.")
        duplicador_complejidad = {"Básico": 1.0, "Intermedio": 1.5, "Avanzado": 2.0}.get(self.especialidad, 1.0)
        return self.precio_base * duracion_horas * duplicador_complejidad * complejidad 
        
    def DetallesEntidad(self) -> str:
        return f"Asesoría especializada {self.nombre_servicio} | Especialidad: {self.especialidad}, Precio Base: ${self.precio_base:,.2f}/h"
   
   
#Breve resumen de funcionalidad, instanciando los objetos y mostrando los detalles de cada entidad, así como el cálculo de costos para cada servicio ofrecido. Se implementan validaciones y manejo de errores para asegurar que los datos ingresados sean correctos y se lancen excepciones personalizadas en caso de errores.
    
Reserva = Reserva_Salas("A001", "Reserva de Sala de Conferencias", 300.0, 50)
print(Reserva.calcular_costos(8,0.15))
print(Reserva.DetallesEntidad()) 
    
Asesoria = Asesorias_Especializadas("A001", "Asesoría en Marketing Digital", 150.0, "Avanzado")
print(Asesoria.calcular_costos(3,1.2))
print(Asesoria.DetallesEntidad())    
    
Alquiler = Alquiler_Equipos("A001", "Alquiler de Proyectores", 100.0, 5)
print(Alquiler.DetallesEntidad())
print(Alquiler.calcular_costos(5,300,0.3))
print(Alquiler.DetallesEntidad())
import logging



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
