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
