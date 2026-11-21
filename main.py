# Este módulo contiene una demostración ejecutable de las operaciones del sistema.
# SistemaFJ coordina el registro, la reserva y el procesamiento de servicios.
from sistema_fj import SistemaFJ
# Logger conserva los eventos generados por la demostración.
from utilidades.logger import Logger
# Se importan los tipos concretos para ilustrar cada categoría de servicio.
from modelos.servicio_sala import ServicioReservaSala
from modelos.servicio_equipo import ServicioAlquilerEquipo
from modelos.servicio_asesoria import ServicioAsesoria
# La demostración captura errores previstos del dominio y los muestra al usuario.
from excepciones.excepciones_personalizadas import SoftwareFJError


def sep(t):
    """Imprime un título entre líneas para separar las operaciones de ejemplo."""
    print("\n" + "=" * 60)
    print("  " + t)
    print("=" * 60)


def main():
    """Ejecuta ejemplos de uso, validaciones y procesamiento de reservas."""
    # Configura el archivo en el que se registrarán las operaciones.
    logger = Logger("logs/sistema_fj.log")
    # Construye el coordinador del sistema usando el logger configurado.
    s = SistemaFJ(logger=logger)
    # Registra el comienzo de esta ejecución de demostración.
    logger.info("=== INICIO SISTEMA SOFTWARE FJ ===")

    # Ejemplo positivo: registrar un cliente con datos que cumplen las validaciones.
    sep("OP 1: Cliente valido")
    try:
        c1 = s.registrar_cliente("1001234567", "Ana Gomez", "ana@mail.com", "3001234567")
        print("OK:", c1.describir())
    except SoftwareFJError as e:
        print("ERROR:", e)

    # Ejemplo negativo: el correo no contiene el formato esperado.
    sep("OP 2: Cliente invalido (email)")
    try:
        s.registrar_cliente("1009876543", "Pedro", "mal-email", "3115556666")
    except SoftwareFJError as e:
        print("ERROR capturado:", e)

    # Ejemplo negativo: la cédula tiene menos dígitos que los permitidos.
    sep("OP 3: Cliente invalido (cedula)")
    try:
        s.registrar_cliente("123", "Luis", "luis@mail.com", "3009998877")
    except SoftwareFJError as e:
        print("ERROR capturado:", e)

    # Ejemplo positivo: crear y registrar una sala con capacidad válida.
    sep("OP 4: Servicio sala valido")
    try:
        sala = ServicioReservaSala("S001", "Sala A", 50000, capacidad=12)
        s.registrar_servicio(sala)
        print("OK:", sala.describir())
    except SoftwareFJError as e:
        print("ERROR:", e)

    # Ejemplo positivo: registrar un equipo cuya categoría incluye su gama.
    sep("OP 5: Servicio equipo valido")
    try:
        equipo = ServicioAlquilerEquipo("E001", "Dell XPS", 120000, "Alta gama")
        s.registrar_servicio(equipo)
        print("OK:", equipo.describir())
    except SoftwareFJError as e:
        print("ERROR:", e)

    # Ejemplo positivo: registrar una asesoría asociada a un área profesional.
    sep("OP 6: Servicio asesoria valido")
    try:
        asesoria = ServicioAsesoria("A001", "Python", 80000, "Programacion")
        s.registrar_servicio(asesoria)
        print("OK:", asesoria.describir())
    except SoftwareFJError as e:
        print("ERROR:", e)

    # Ejemplo negativo: la tarifa base no puede ser cero ni negativa.
    sep("OP 7: Servicio invalido (tarifa negativa)")
    try:
        ServicioReservaSala("S002", "Mala", -1000, capacidad=5)
    except SoftwareFJError as e:
        print("ERROR capturado:", e)

    # Ejemplo negativo: la capacidad de una sala debe ser mayor que cero.
    sep("OP 8: Servicio invalido (capacidad cero)")
    try:
        ServicioReservaSala("S003", "Vacia", 30000, capacidad=0)
    except SoftwareFJError as e:
        print("ERROR capturado:", e)

    # Ejemplo positivo: crear, confirmar y calcular el costo de una sala.
    sep("OP 9: Reserva exitosa (sala)")
    try:
        r = s.crear_reserva("1001234567", "S001", 3)
        s.confirmar_reserva(r)
        costo = s.procesar_reserva(r, impuesto=19, descuento=5)
        print("OK costo:", costo)
    except SoftwareFJError as e:
        print("ERROR:", e)

    # Ejemplo negativo: no se puede reservar en nombre de un cliente inexistente.
    sep("OP 10: Reserva fallida (cliente inexistente)")
    try:
        s.crear_reserva("999999", "S001", 2)
    except SoftwareFJError as e:
        print("ERROR capturado:", e)

    # Ejemplo negativo: el equipo está registrado, pero marcado como no disponible.
    sep("OP 11: Reserva fallida (servicio no disponible)")
    try:
        equipo.disponible = False
        r = s.crear_reserva("1001234567", "E001", 5)
        s.confirmar_reserva(r)
        s.procesar_reserva(r)
    except SoftwareFJError as e:
        print("ERROR capturado:", e)

    # Ejemplo positivo: procesar una asesoría y aplicar el descuento indicado.
    sep("OP 12: Reserva exitosa (asesoria descuento)")
    try:
        r2 = s.crear_reserva("1001234567", "A001", 6)
        s.confirmar_reserva(r2)
        costo = s.procesar_reserva(r2, impuesto=19, descuento=10)
        print("OK costo:", costo)
    except SoftwareFJError as e:
        print("ERROR:", e)

    # Muestra el conteo final de clientes, servicios y reservas.
    sep("RESUMEN")
    print(s.resumen())
    # Registra el cierre normal de la demostración.
    logger.info("=== FIN SISTEMA SOFTWARE FJ ===")


# Ejecuta la demostración solo cuando este archivo es el programa principal.
if __name__ == "__main__":
    main()