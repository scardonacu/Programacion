# Define asesorías con tarifas por hora y descuento para sesiones extensas.
# La clase Servicio aporta los datos y las reglas compartidas.
from modelos.servicio import Servicio
# Se emplean para validar el área y la disponibilidad de la asesoría.
from excepciones.excepciones_personalizadas import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
)


class ServicioAsesoria(Servicio):
    """Representa una asesoría profesional asociada a un área temática."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float,
                 area: str, disponible: bool = True):
        """Inicializa el servicio y verifica que se indique un área."""
        # Valida y almacena los atributos comunes definidos en Servicio.
        super().__init__(codigo, nombre, tarifa_base, disponible)
        # El área temática es obligatoria para identificar la asesoría.
        if not area or not str(area).strip():
            raise DatosInvalidosError("Area obligatoria.")
        # Guarda el área sin espacios externos.
        self._area = area.strip()

    @property
    def area(self) -> str:
        """Devuelve el área temática de la asesoría."""
        return self._area

    def validar_parametros(self, duracion: float) -> None:
        """Comprueba la disponibilidad y el límite de ocho horas por asesoría."""
        # No permite usar una asesoría marcada como no disponible.
        if not self.disponible:
            raise ServicioNoDisponibleError(f"Asesoria '{self.nombre}' no disponible.")
        # La duración debe ser mayor que cero.
        if duracion is None or duracion <= 0:
            raise DatosInvalidosError("Duracion debe ser > 0.")
        # Limita una sesión de asesoría a ocho horas.
        if duracion > 8:
            raise DatosInvalidosError("Asesoria no puede exceder 8 horas.")

    def calcular_costo(self, duracion: float, impuesto: float = 0.0,
                       descuento: float = 0.0) -> float:
        """Calcula el costo y aplica un descuento del 10 % si supera cuatro horas."""
        # Verifica duración y disponibilidad antes de calcular el importe.
        self.validar_parametros(duracion)
        # Calcula el subtotal con base en la tarifa por hora.
        subtotal = self.tarifa_base * duracion
        # Aplica un descuento comercial automático a sesiones largas.
        if duracion > 4:
            subtotal *= 0.90
        # Aplica los porcentajes adicionales comunes y redondea el resultado.
        return self._aplicar_impuesto_y_descuento(subtotal, impuesto, descuento)

    def describir(self) -> str:
        """Describe el código, el nombre, el área y la tarifa por hora."""
        return (f"Asesoria[{self.identificador}] {self.nombre} | "
                f"area={self.area} | tarifa/h=${self.tarifa_base}")