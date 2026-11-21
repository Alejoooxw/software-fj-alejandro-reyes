class ErrorSistema(Exception):
    # Clase base para los errores propios del sistema Software FJ
    def __init__(self, mensaje="Error general en el sistema"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class DatoInvalidoError(ErrorSistema):
    # Se lanza cuando un dato viene vacio, negativo o con mal formato
    def __init__(self, campo, valor, detalle="Dato incorrecto"):
        self.campo = campo
        self.valor = valor
        texto = f"Error en '{campo}' con valor '{valor}': {detalle}"
        super().__init__(texto)


class ServicioNoDisponibleError(ErrorSistema):
    # Se lanza si el servicio esta inactivo o no se puede usar
    def __init__(self, servicio, detalle="Servicio no disponible"):
        self.servicio = servicio
        texto = f"El servicio '{servicio}' no esta disponible: {detalle}"
        super().__init__(texto)


class ReservaInvalidaError(ErrorSistema):
    # Se lanza cuando se intenta cambiar el estado de una reserva de forma no permitida
    def __init__(self, id_reserva, estado, accion):
        self.id_reserva = id_reserva
        self.estado = estado
        texto = f"No se puede {accion} la reserva {id_reserva} porque esta en estado '{estado}'"
        super().__init__(texto)


class CalculoInconsistenteError(ErrorSistema):
    # Se lanza cuando un calculo de precio, impuesto o descuento da un valor invalido
    def __init__(self, detalle="Resultado de calculo invalido"):
        super().__init__(f"Error en el calculo: {detalle}")