# Implementa las reglas específicas para reservar espacios físicos.
# La clase base aporta identificación, tarifa y control de disponibilidad.
from modelos.servicio import Servicio
# Las excepciones permiten reportar parámetros incorrectos y salas no disponibles.
from excepciones.excepciones_personalizadas import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
)


class ServicioReservaSala(Servicio):
    """Servicio de alquiler por hora de una sala con capacidad definida."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float,
                 capacidad: int, disponible: bool = True):
        """Inicializa el servicio y valida la capacidad de la sala."""
        # Inicializa y valida los campos comunes de todo servicio.
        super().__init__(codigo, nombre, tarifa_base, disponible)
        # La capacidad debe ser un entero positivo.
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError(f"Capacidad invalida: {capacidad}.")
        # Guarda la cantidad máxima de personas admitidas.
        self._capacidad = capacidad

    @property
    def capacidad(self) -> int:
        """Devuelve el aforo máximo de la sala."""
        return self._capacidad

    def validar_parametros(self, duracion: float) -> None:
        """Comprueba disponibilidad y que la duración no supere 12 horas."""
        # No se debe contratar una sala marcada como no disponible.
        if not self.disponible:
            raise ServicioNoDisponibleError(f"Sala '{self.nombre}' no disponible.")
        # La reserva debe tener una cantidad de horas positiva.
        if duracion is None or duracion <= 0:
            raise DatosInvalidosError("Duracion debe ser > 0.")
        # Limita una reserva de sala a un máximo de doce horas.
        if duracion > 12:
            raise DatosInvalidosError("Sala no puede exceder 12 horas.")

    def calcular_costo(self, duracion: float, impuesto: float = 0.0,
                       descuento: float = 0.0) -> float:
        """Calcula el costo por hora y aplica los porcentajes indicados."""
        # Valida de nuevo los parámetros para proteger llamadas directas al cálculo.
        self.validar_parametros(duracion)
        # Multiplica la tarifa por las horas reservadas.
        subtotal = self.tarifa_base * duracion
        # Aplica la lógica común de impuesto, descuento y redondeo.
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self) -> str:
        """Describe el código, el nombre, la capacidad y la tarifa por hora."""
        return (f"ReservaSala[{self.identificador}] {self.nombre} | "
                f"capacidad={self.capacidad} | tarifa/h=${self.tarifa_base}")