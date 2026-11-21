# Importo las clases del modelo para ejecutar las simulaciones completas del sistema
from modelo.cliente import Cliente
from modelo.excepciones import ErrorSistema
from modelo.registro import guardar_error, guardar_evento
from modelo.reserva import Reserva
from modelo.servicios import AlquilerEquipo, Asesoria, ReservaSala


def ejecutar_simulaciones():
    # Listas en memoria para guardar los registros validos sin usar bases de datos
    clientes = []
    servicios = []
    reservas = []
    exitos = 0
    fallos_controlados = 0

    guardar_evento("=== INICIO DE SIMULACIONES DE SOFTWARE FJ ===")
    print("Ejecutando 12 simulaciones del sistema Software FJ...\n")

    # Lista de 12 escenarios: 6 operaciones validas y 6 errores forzados para probar estabilidad
    def op_1_cliente_valido():
        c = Cliente("1023456789", "Carlos Mendoza", "carlos.mendoza@correo.com", "3104567890")
        clientes.append(c)
        return f"Cliente registrado: {c.describir()}"

    def op_2_cliente_correo_invalido():
        # Debe fallar porque el correo no tiene arroba ni dominio valido
        Cliente("1098765432", "Laura Gomez", "lauragomez.com", "3209876543")

    def op_3_cliente_telefono_invalido():
        # Debe fallar porque el telefono tiene letras y es muy corto
        Cliente("1055443322", "Andres Ruiz", "andres@correo.com", "123abc")

    def op_4_sala_valida():
        s = ReservaSala("SALA-01", "Sala de Juntas Norte", 60000, capacidad_maxima=10, disponible=True)
        servicios.append(s)
        return f"Servicio creado: {s.describir()}"

    def op_5_equipo_valido():
        e = AlquilerEquipo("EQ-01", "Portatil Dell Precision", 25000, serial_equipo="DELL-9988", disponible=True)
        servicios.append(e)
        return f"Servicio creado: {e.describir()}"

    def op_6_asesoria_valida():
        a = Asesoria("ASE-01", "Consultoria Arquitectura Cloud", 95000, especialidad="AWS y Python", disponible=True)
        servicios.append(a)
        return f"Servicio creado: {a.describir()}"

    def op_7_servicio_tarifa_negativa():
        # Debe fallar por tarifa negativa
        ReservaSala("SALA-ERR", "Sala Fantasma", -15000, capacidad_maxima=5)

    def op_8_reserva_sala_exitosa():
        # Reserva valida con sobrecarga: incluye refrigerio=True y 10% de descuento
        r = Reserva("RES-001", clientes[0], servicios[0], horas=3, descuento=0.10, asistentes=6, refrigerio=True)
        r.confirmar()
        r.procesar()
        reservas.append(r)
        return f"Reserva completada: {r.resumen()}"

    def op_9_reserva_aforo_excedido():
        # Debe fallar porque la sala tiene capacidad para 10 y se piden 18 asistentes
        Reserva("RES-002", clientes[0], servicios[0], horas=2, asistentes=18)

    def op_10_reserva_servicio_inactivo():
        # Creo un equipo inactivo e intento reservarlo para disparar ServicioNoDisponibleError
        equipo_danado = AlquilerEquipo("EQ-02", "Proyector Epson", 20000, serial_equipo="EP-001", disponible=False)
        Reserva("RES-003", clientes[0], equipo_danado, horas=2)

    def op_11_cancelar_reserva_procesada():
        # Intento cancelar RES-001 que ya fue procesada en la operacion 8
        reservas[0].cancelar()

    def op_12_reserva_asesoria_urgente():
        # Reserva valida de asesoria urgente con seguro/recargo del 20%
        r2 = Reserva("RES-004", clientes[0], servicios[2], horas=2, urgente=True)
        r2.confirmar()
        reservas.append(r2)
        return f"Reserva confirmada: {r2.resumen()}"

    operaciones = [
        ("1. Registro cliente valido", op_1_cliente_valido),
        ("2. Registro cliente con correo invalido", op_2_cliente_correo_invalido),
        ("3. Registro cliente con telefono invalido", op_3_cliente_telefono_invalido),
        ("4. Creacion servicio ReservaSala", op_4_sala_valida),
        ("5. Creacion servicio AlquilerEquipo", op_5_equipo_valido),
        ("6. Creacion servicio Asesoria", op_6_asesoria_valida),
        ("7. Creacion servicio con tarifa negativa", op_7_servicio_tarifa_negativa),
        ("8. Reserva completa con descuento y refrigerio", op_8_reserva_sala_exitosa),
        ("9. Reserva superando aforo maximo de sala", op_9_reserva_aforo_excedido),
        ("10. Reserva de equipo no disponible", op_10_reserva_servicio_inactivo),
        ("11. Cancelar una reserva ya procesada", op_11_cancelar_reserva_procesada),
        ("12. Reserva de asesoria urgente confirmada", op_12_reserva_asesoria_urgente),
    ]

    print("=" * 75)
    print("  SISTEMA INTEGRAL SOFTWARE FJ - PRUEBAS DE SIMULACION Y EXCEPCIONES")
    print("=" * 75)

    # Recorro cada operacion usando try/except/else/finally con espacios para lectura clara
    for titulo, funcion in operaciones:
        print(f"\n--- {titulo} ---")
        try:
            resultado = funcion()
        except ErrorSistema as err:
            # Capturo mis excepciones personalizadas y las mando al log
            fallos_controlados += 1
            guardar_error(err, origen=titulo)
            print(f"  [ERROR CONTROLADO] -> {err}")
        except Exception as err_inesperado:
            # Capturo cualquier otro error inesperado de Python
            fallos_controlados += 1
            guardar_error(err_inesperado, origen=titulo)
            print(f"  [ERROR INESPERADO] -> {err_inesperado}")
        else:
            # Si la operacion salio bien incremento el contador de exitos
            exitos += 1
            print(f"  [OK] -> {resultado}")
        finally:
            # Bloque finally que se ejecuta siempre tras evaluar cada caso
            pass

    resumen_final = (
        f"FIN DE SIMULACIONES | Exitosas: {exitos} | "
        f"Errores controlados en log: {fallos_controlados}"
    )
    guardar_evento(f"=== {resumen_final} ===")

    print("\n" + "=" * 75)
    print(f"  {resumen_final}")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    ejecutar_simulaciones()