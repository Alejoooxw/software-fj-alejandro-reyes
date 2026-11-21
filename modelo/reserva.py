# Importo datetime para registrar la fecha y hora exacta de creacion de cada reserva
from datetime import datetime
# Importo Cliente y Servicio para validar que los objetos recibidos sean del tipo correcto
from modelo.cliente import Cliente
from modelo.servicios import Servicio
# Importo las excepciones personalizadas para controlar estados y datos invalidos
from modelo.excepciones import (
    DatoInvalidoError,
    ErrorSistema,
    ReservaInvalidaError,
)
# Importo las funciones del log para guardar cada cambio de estado o error
from modelo.registro import guardar_error, guardar_evento


class Reserva:
    # Clase que une un cliente con un servicio y controla el ciclo de vida de la reserva
    def __init__(self, id_reserva, cliente, servicio, horas, impuesto=0.19, descuento=0.0, **opciones):
        # Valido que el identificador de la reserva no llegue vacio
        if not id_reserva or not str(id_reserva).strip():
            raise DatoInvalidoError("id_reserva", id_reserva, "El codigo de reserva es obligatorio")
        # Verifico que el cliente sea realmente una instancia de la clase Cliente
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("cliente", cliente, "Se esperaba un objeto Cliente valido")
        # Verifico que el servicio sea realmente una instancia hija de Servicio
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("servicio", servicio, "Se esperaba un objeto Servicio valido")

        # Guardo los atributos principales de la reserva
        self.id_reserva = str(id_reserva).strip()
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.impuesto = impuesto
        self.descuento = descuento
        self.opciones = opciones
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Toda reserva arranca en estado Pendiente
        self.estado = "Pendiente"

        # Calculo el total desde la creacion para validar disponibilidad y parametros de una vez
        self.costo_total = self.servicio.calcular_costo(
            self.horas,
            impuesto=self.impuesto,
            descuento=self.descuento,
            **self.opciones,
        )
        guardar_evento(
            f"Reserva {self.id_reserva} creada ({self.estado}) | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Total: ${self.costo_total}"
        )

    def confirmar(self):
        # Solo se puede confirmar una reserva que este en estado Pendiente
        if self.estado != "Pendiente":
            raise ReservaInvalidaError(self.id_reserva, self.estado, "confirmar")
        # Verifico nuevamente que el servicio siga disponible antes de confirmar
        self.servicio.verificar_disponibilidad()
        self.estado = "Confirmada"
        guardar_evento(f"Reserva {self.id_reserva} cambiada a estado: Confirmada")

    def cancelar(self):
        # No permito cancelar una reserva que ya fue procesada o que ya estaba cancelada
        if self.estado in ("Procesada", "Cancelada"):
            raise ReservaInvalidaError(self.id_reserva, self.estado, "cancelar")
        self.estado = "Cancelada"
        guardar_evento(f"Reserva {self.id_reserva} cambiada a estado: Cancelada")

    def procesar(self):
        # Uso try/except/else para procesar el cobro y cierre solo si esta Confirmada
        try:
            if self.estado != "Confirmada":
                raise ReservaInvalidaError(self.id_reserva, self.estado, "procesar")
            # Recalculo el costo final para asegurar consistencia antes de cerrar
            self.costo_total = self.servicio.calcular_costo(
                self.horas,
                impuesto=self.impuesto,
                descuento=self.descuento,
                **self.opciones,
            )
        except ErrorSistema as err:
            # Registro el error en el log y lo relanzo para que la interfaz o prueba lo capture
            guardar_error(err, origen=f"Reserva.procesar({self.id_reserva})")
            raise
        else:
            # Si no hubo ninguna excepcion marco la reserva como Procesada exitosamente
            self.estado = "Procesada"
            guardar_evento(
                f"Reserva {self.id_reserva} PROCESADA con exito | Total cobrado: ${self.costo_total}"
            )

    def resumen(self):
        # Devuelvo una linea con toda la informacion resumida de la reserva
        return (
            f"[{self.id_reserva}] {self.cliente.nombre} -> {self.servicio.nombre} "
            f"({self.horas}h) | Total: ${self.costo_total} | Estado: {self.estado}"
        )