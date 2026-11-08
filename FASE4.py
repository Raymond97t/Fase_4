from abc import ABC, abstractmethod
import logging 


logging.basicConfig(
    filename='Error.log',
    filemode= 'w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s - %(lineno)d - %(filename)s',
    encoding='utf-8'
)

class SistemaError(Exception):
    pass

class ClienteError(SistemaError):
    pass

class ProductoError(SistemaError):
    pass

class ReservaError(SistemaError):
    pass


class SuperEntidad(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad 
        
        @property
        def id_entidad(self) -> str:
            return self._id_entidad
        
        @abstractmethod
        def DetallesEntidad(self):
            pass
        
class Cliente(SuperEntidad):
        def __init__(self, id_entidad: str, nombre: str, correo: str, telefono: str):
            super().__init__(id_entidad)
            self.nombre = nombre
            self.correo = correo
            self.telefono = telefono 
            
            @property
            def nombre(self) -> str:
                return self._nombre
            
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
                
            @abstractmethod
            def DetallesEntidad(self) -> str:
                return f"Cliente[ID: {self.id_entidad}, Nombre: {self.nombre}, Correo: {self.correo}, Teléfono: {self.telefono}]"
            
