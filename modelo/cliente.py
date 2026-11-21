# Importo la clase abstracta padre Entidad
from modelo.entidad import Entidad
# Importo la excepcion personalizada para datos invalidos
from modelo.excepciones import DatoInvalidoError
# Importo la funcion para registrar en el log cuando se crea un cliente correctamente
from modelo.registro import guardar_evento


class Cliente(Entidad):
    # Clase que representa a un cliente de Software FJ con encapsulacion y validaciones
    def __init__(self, documento, nombre, correo, telefono):
        # Llamo al constructor de Entidad usando el documento como identificador unico
        super().__init__(documento)
        # Inicializo los atributos privados usando los setters para validar desde el inicio
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        # Dejo constancia en el archivo de log que el cliente quedo registrado
        guardar_evento(f"Cliente creado: {self.nombre} (Doc: {self.identificador})")

    @property
    def documento(self):
        # Devuelvo el identificador heredado como el documento del cliente
        return self._identificador

    @property
    def nombre(self):
        # Getter para leer el nombre privado del cliente
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Verifico que el nombre sea texto y tenga al menos 3 letras reales
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("nombre", valor, "El nombre debe tener minimo 3 caracteres")
        # Guardo el nombre limpio en el atributo privado
        self.__nombre = valor.strip()

    @property
    def correo(self):
        # Getter para leer el correo electronico privado
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Valido que sea texto y contenga arroba y punto en formato basico
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatoInvalidoError("correo", valor, "El formato del correo electronico no es valido")
        # Guardo el correo en minusculas y sin espacios
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        # Getter para leer el telefono privado
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Limpio espacios y verifico que sean solo numeros y tenga entre 7 y 15 digitos
        texto = str(valor).strip()
        if not texto.isdigit() or not (7 <= len(texto) <= 15):
            raise DatoInvalidoError("telefono", valor, "El telefono debe tener entre 7 y 15 digitos numericos")
        # Guardo el telefono validado
        self.__telefono = texto

    def describir(self):
        # Implemento el metodo abstracto obligado por Entidad con los datos del cliente
        return f"Cliente [{self.documento}] - {self.nombre} | Tel: {self.telefono} | Email: {self.correo}"