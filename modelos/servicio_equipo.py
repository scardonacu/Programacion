# Implementa el alquiler de equipos y su recargo para equipos de alta gama.
# Servicio proporciona la validación y los datos comunes del servicio.
from modelos.servicio import Servicio
# Se usan para rechazar datos incorrectos o equipos no disponibles.
from excepciones.excepciones_personalizadas import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
)


class ServicioAlquilerEquipo(Servicio):
    """Representa el alquiler de un equipo por día."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float,
                 tipo_equipo: str, disponible: bool = True):
        """Inicializa el servicio y exige una categoría de equipo no vacía."""
        # Configura código, nombre, tarifa y disponibilidad heredados.
        super().__init__(codigo, nombre, tarifa_base, disponible)
        # El tipo describe la categoría y es necesario para calcular recargos.
        if not tipo_equipo or not str(tipo_equipo).strip():
            raise DatosInvalidosError("Tipo de equipo obligatorio.")
        # Conserva la categoría sin espacios externos.
        self._tipo_equipo = tipo_equipo.strip()

    @property
    def tipo_equipo(self) -> str:
        """Devuelve la categoría del equipo alquilado."""
        return self._tipo_equipo

    def validar_parametros(self, duracion: float) -> None:
        """Comprueba que el equipo esté disponible y el alquiler dure hasta 30 días."""
        # Impide contratar equipos temporalmente no disponibles.
        if not self.disponible:
            raise ServicioNoDisponibleError(f"Equipo '{self.nombre}' no disponible.")
        # La cantidad de días de alquiler debe ser positiva.
        if duracion is None or duracion <= 0:
            raise DatosInvalidosError("Duracion debe ser > 0.")
        # Limita la duración del alquiler a treinta días.
        if duracion > 30:
            raise DatosInvalidosError("Alquiler no puede exceder 30 dias.")

    def calcular_costo(self, duracion: float, impuesto: float = 0.0,
                       descuento: float = 0.0) -> float:
        """Calcula el alquiler y agrega un 5 % para equipos de alta gama."""
        # Asegura que la duración y la disponibilidad sean válidas.
        self.validar_parametros(duracion)
        # Calcula el costo antes de impuestos y descuentos.
        subtotal = self.tarifa_base * duracion
        # Identifica la categoría sin distinguir mayúsculas y añade el recargo.
        if "alta" in self._tipo_equipo.lower():
            subtotal *= 1.05
        # Aplica impuesto, descuento y redondeo compartidos por los servicios.
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self) -> str:
        """Describe el código, el nombre, el tipo de equipo y la tarifa diaria."""
        return (f"AlquilerEquipo[{self.identificador}] {self.nombre} | "
                f"tipo={self.tipo_equipo} | tarifa/d=${self.tarifa_base}")