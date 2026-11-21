# Este módulo modela el ciclo de vida de una reserva y su cálculo de costo.
# datetime registra el momento local en que se crea cada reserva.
from datetime import datetime
# Los tipos importados permiten validar los objetos asociados a la reserva.
from modelos.cliente import Cliente
from modelos.servicio import Servicio
# Las excepciones expresan errores de estado, datos y disponibilidad.
from excepciones.excepciones_personalizadas import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    DatosInvalidosError,
)


class Reserva:
    """Vincula un cliente con un servicio y controla el estado de la operación."""

    # Estados posibles del ciclo de vida de una reserva.
    ESTADOS_VALIDOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"}

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: float):
        """Verifica las referencias y la duración, y establece valores iniciales."""
        # Una reserva solo puede asociarse a una instancia Cliente válida.
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Cliente invalido.")
        # Una reserva solo puede asociarse a un servicio del dominio.
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Servicio invalido.")
        # La duración debe ser numérica y positiva.
        if duracion is None or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError(f"Duracion invalida: {duracion}.")
        # Conserva las referencias al cliente y al servicio reservados.
        self._cliente = cliente
        self._servicio = servicio
        # Estandariza la duración como número decimal.
        self._duracion = float(duracion)
        # Toda reserva comienza pendiente de confirmación.
        self._estado = "PENDIENTE"
        # Registra el instante de creación para consulta posterior.
        self._fecha_creacion = datetime.now()
        # Aún no se ha calculado ningún importe.
        self._costo_total = 0.0

    @property
    def cliente(self) -> Cliente:
        """Devuelve el cliente relacionado con la reserva."""
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        """Devuelve el servicio relacionado con la reserva."""
        return self._servicio

    @property
    def duracion(self) -> float:
        """Devuelve la duración contratada."""
        return self._duracion

    @property
    def estado(self) -> str:
        """Devuelve el estado actual del ciclo de vida."""
        return self._estado

    @property
    def costo_total(self) -> float:
        """Devuelve el costo calculado, o cero si aún no se procesa."""
        return self._costo_total

    def confirmar(self) -> None:
        """Confirma una reserva pendiente si el servicio está disponible."""
        # Solo una reserva recién creada puede pasar a confirmada.
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar en estado '{self._estado}'.")
        # La disponibilidad se comprueba al confirmar, no al crear.
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"Servicio '{self._servicio.nombre}' no disponible.")
        # Actualiza el estado tras superar las verificaciones.
        self._estado = "CONFIRMADA"

    def cancelar(self) -> None:
        """Cancela la reserva salvo que ya esté cancelada o procesada."""
        # Una reserva procesada no puede deshacerse con esta operación.
        if self._estado in ("CANCELADA", "PROCESADA"):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar en estado '{self._estado}'.")
        # Marca la reserva como cancelada.
        self._estado = "CANCELADA"

    def procesar(self, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo de una reserva confirmada y registra el resultado."""
        try:
            # Impide procesar reservas pendientes, canceladas o ya procesadas.
            if self._estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"Solo se procesa CONFIRMADA. Estado: {self._estado}.")
            # Aplica las validaciones de duración específicas del servicio.
            self._servicio.validar_parametros(self._duracion)
            # Delega al servicio su fórmula de costo y almacena el total.
            self._costo_total = self._servicio.calcular_costo(
                self._duracion, impuesto=impuesto, descuento=descuento)
        # Convierte los errores de dominio en un error uniforme de reserva.
        except (OperacionNoPermitidaError, ServicioNoDisponibleError,
                DatosInvalidosError) as error:
            raise ReservaInvalidaError(
                f"Fallo al procesar reserva: {error}") from error
        else:
            # Solo cambia a procesada si no hubo excepciones.
            self._estado = "PROCESADA"
            return self._costo_total
        finally:
            # Informa del estado final incluso si el procesamiento falla.
            print(f"[Reserva] Fin procesamiento. Estado: {self._estado}")

    def describir(self) -> str:
        """Genera un resumen textual de los datos y el estado de la reserva."""
        return (f"Reserva(cliente={self._cliente.cedula}, "
                f"servicio={self._servicio.identificador}, "
                f"duracion={self._duracion}, estado={self._estado}, "
                f"costo=${self._costo_total})")

    def __str__(self) -> str:
        """Usa el resumen de la reserva como representación textual."""
        return self.describir()