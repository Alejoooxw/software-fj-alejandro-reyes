# Importo ABC y abstractmethod para definir clases abstractas en Python
from abc import ABC, abstractmethod
# Importo mi excepcion personalizada para validar el identificador
from modelo.excepciones import DatoInvalidoError


class Entidad(ABC):
    # Clase abstracta base que obliga a todas las entidades del sistema a tener ID y descripcion
    def __init__(self, identificador):
        # Valido que el identificador no llegue vacio ni con solo espacios
        if not identificador or not str(identificador).strip():
            raise DatoInvalidoError("identificador", identificador, "El ID no puede estar vacio")
        # Guardo el identificador limpio como atributo protegido
        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        # Propiedad de solo lectura para consultar el ID desde afuera sin modificarlo directo
        return self._identificador

    @abstractmethod
    def describir(self):
        # Metodo abstracto que cada clase hija (Cliente, Servicio, etc.) debe implementar a su manera
        pass