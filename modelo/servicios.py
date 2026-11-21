# Importo abstractmethod para obligar a las clases hijas a implementar sus propios metodos
from abc import abstractmethod
# Importo la clase base Entidad
from modelo.entidad import Entidad
# Importo las excepciones personalizadas necesarias para validar servicios y calculos
from modelo.excepciones import (
    CalculoInconsistenteError,
    DatoInvalidoError,
    ServicioNoDisponibleError,
)
# Importo la funcion para dejar registro en el log cuando se crea un servicio
from modelo.registro import guardar_evento


class Servicio(Entidad):
    # Clase abstracta que representa cualquier servicio ofrecido por Software FJ
    def __init__(self, codigo, nombre, tarifa_hora, disponible=True):
        # Valido el codigo usando el constructor de Entidad
        super().__init__(codigo)
        # Verifico que el nombre del servicio tenga al menos 3 letras
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise DatoInvalidoError("nombre_servicio", nombre, "El nombre debe tener minimo 3 caracteres")
        # Verifico que la tarifa por hora sea un numero mayor a cero
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise DatoInvalidoError("tarifa_hora", tarifa_hora, "La tarifa debe ser mayor a cero")

        # Guardo los atributos base del servicio
        self.nombre = nombre.strip()
        self.tarifa_hora = float(tarifa_hora)
        self.disponible = bool(disponible)

    def verificar_disponibilidad(self):
        # Si el servicio no esta habilitado lanzo la excepcion correspondiente
        if not self.disponible:
            raise ServicioNoDisponibleError(self.nombre, "El servicio se encuentra inactivo o ocupado")

    def aplicar_ajustes_financieros(self, subtotal, impuesto=0.19, descuento=0.0, cargo_extra=0.0):
        # Metodo que implementa la sobrecarga mediante parametros opcionales (IVA, descuento, extras)
        if impuesto < 0 or descuento < 0 or cargo_extra < 0:
            raise CalculoInconsistenteError("Los porcentajes o cargos extra no pueden ser negativos")
        if descuento >= 1:
            raise CalculoInconsistenteError("El descuento no puede ser del 100% o superior")

        # Calculo el valor con descuento, sumo cargos extra y aplico el impuesto
        base_con_descuento = subtotal * (1 - descuento) + cargo_extra
        total = base_con_descuento * (1 + impuesto)

        # Verifico que el resultado final sea coherente y positivo
        if total <= 0:
            raise CalculoInconsistenteError("El total calculado dio cero o negativo")
        return round(total, 2)

    @abstractmethod
    def validar_parametros(self, horas, **kwargs):
        # Metodo abstracto para validar las reglas especificas de cada tipo de servicio
        pass

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0.19, descuento=0.0, **kwargs):
        # Metodo abstracto sobrecargado para calcular el precio total segun el servicio
        pass


class ReservaSala(Servicio):
    # Servicio especializado para el alquiler de salas de reuniones o estudio
    def __init__(self, codigo, nombre, tarifa_hora, capacidad_maxima, disponible=True):
        # Llamo al constructor padre de Servicio
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        # Valido que la capacidad de personas sea un entero positivo
        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise DatoInvalidoError("capacidad_maxima", capacidad_maxima, "La capacidad debe ser mayor a 0")
        self.capacidad_maxima = capacidad_maxima
        guardar_evento(f"Servicio de sala creado: {self.nombre} (Capacidad: {self.capacidad_maxima})")

    def validar_parametros(self, horas, **kwargs):
        # Reviso disponibilidad, horas minimas y que los asistentes no superen el aforo
        self.verificar_disponibilidad()
        asistentes = kwargs.get("asistentes", 1)
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatoInvalidoError("horas", horas, "Las horas de reserva deben ser mayores a 0")
        if asistentes <= 0 or asistentes > self.capacidad_maxima:
            raise DatoInvalidoError(
                "asistentes",
                asistentes,
                f"La sala permite entre 1 y {self.capacidad_maxima} personas",
            )

    def calcular_costo(self, horas, impuesto=0.19, descuento=0.0, **kwargs):
        # Valido primero los parametros antes de liquidar
        self.validar_parametros(horas, **kwargs)
        # Si piden servicio de cafeteria (refrigerio=True) sumo un recargo fijo de 15000
        refrigerio = kwargs.get("refrigerio", False)
        extra = 15000.0 if refrigerio else 0.0
        subtotal = self.tarifa_hora * horas
        return self.aplicar_ajustes_financieros(subtotal, impuesto, descuento, extra)

    def describir(self):
        # Descripcion especifica de la sala
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Sala [{self.identificador}] {self.nombre} | ${self.tarifa_hora}/h | Aforo: {self.capacidad_maxima} | {estado}"


class AlquilerEquipo(Servicio):
    # Servicio especializado para prestamo de portatiles, proyectores o equipos tecnicos
    def __init__(self, codigo, nombre, tarifa_hora, serial_equipo, disponible=True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        # Verifico que el serial del equipo no este vacio
        if not isinstance(serial_equipo, str) or len(serial_equipo.strip()) < 3:
            raise DatoInvalidoError("serial_equipo", serial_equipo, "Serial de equipo invalido")
        self.serial_equipo = serial_equipo.strip()
        guardar_evento(f"Servicio de equipo creado: {self.nombre} (Serial: {self.serial_equipo})")

    def validar_parametros(self, horas, **kwargs):
        # Verifico que el equipo este libre y se alquile minimo por 1 hora
        self.verificar_disponibilidad()
        if not isinstance(horas, (int, float)) or horas < 1:
            raise DatoInvalidoError("horas", horas, "El alquiler de equipo requiere minimo 1 hora")

    def calcular_costo(self, horas, impuesto=0.19, descuento=0.0, **kwargs):
        self.validar_parametros(horas, **kwargs)
        # Si incluye seguro contra danos (seguro=True) cobro 10000 adicionales
        con_seguro = kwargs.get("seguro", False)
        extra = 10000.0 if con_seguro else 0.0
        subtotal = self.tarifa_hora * horas
        return self.aplicar_ajustes_financieros(subtotal, impuesto, descuento, extra)

    def describir(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Equipo [{self.identificador}] {self.nombre} (SN: {self.serial_equipo}) | ${self.tarifa_hora}/h | {estado}"


class Asesoria(Servicio):
    # Servicio especializado para consultorias tecnicas o desarrollo a medida
    def __init__(self, codigo, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_hora, disponible)
        # Valido que la especialidad tenga al menos 3 letras
        if not isinstance(especialidad, str) or len(especialidad.strip()) < 3:
            raise DatoInvalidoError("especialidad", especialidad, "La especialidad debe tener minimo 3 caracteres")
        self.especialidad = especialidad.strip()
        guardar_evento(f"Servicio de asesoria creado: {self.nombre} ({self.especialidad})")

    def validar_parametros(self, horas, **kwargs):
        # Verifico disponibilidad y limite maximo de 8 horas por sesion de asesoria
        self.verificar_disponibilidad()
        if not isinstance(horas, (int, float)) or horas <= 0 or horas > 8:
            raise DatoInvalidoError("horas", horas, "La asesoria debe durar entre 0.5 y 8 horas")

    def calcular_costo(self, horas, impuesto=0.19, descuento=0.0, **kwargs):
        self.validar_parametros(horas, **kwargs)
        # Si es asesoria urgente (urgente=True) tiene un recargo del 20% sobre el subtotal
        urgente = kwargs.get("urgente", False)
        subtotal = self.tarifa_hora * horas
        extra = subtotal * 0.20 if urgente else 0.0
        return self.aplicar_ajustes_financieros(subtotal, impuesto, descuento, extra)

    def describir(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Asesoria [{self.identificador}] {self.nombre} ({self.especialidad}) | ${self.tarifa_hora}/h | {estado}"