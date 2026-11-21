# Define las reglas comunes que deben cumplir todos los servicios contratables.
from abc import abstractmethod
# Los servicios comparten identificador y nombre con el resto de entidades.
from modelos.entidad_base import EntidadBase
# Estas excepciones señalan datos inválidos y resultados de cálculo imposibles.
from excepciones.excepciones_personalizadas import (
    DatosInvalidosError,
    CalculoInconsistenteError,
)


class Servicio(EntidadBase):
    """Clase base abstracta para servicios con tarifa y disponibilidad."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float,
                 disponible: bool = True):
        """Valida la tarifa y configura el estado inicial del servicio."""
        # Valida el código y el nombre mediante la implementación compartida.
        super().__init__(identificador=codigo, nombre=nombre)
        # La tarifa debe haberse proporcionado explícitamente.
        if tarifa_base is None:
            raise DatosInvalidosError("La tarifa base es obligatoria.")
        # Solo se aceptan tarifas numéricas estrictamente positivas.
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError(f"Tarifa invalida: {tarifa_base}.")
        # Convierte la tarifa a un tipo uniforme para los cálculos.
        self._tarifa_base = float(tarifa_base)
        # Normaliza el valor inicial de disponibilidad a booleano.
        self._disponible = bool(disponible)

    @property
    def tarifa_base(self) -> float:
        """Devuelve el precio unitario base del servicio."""
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        """Indica si el servicio puede reservarse en este momento."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Actualiza el estado de disponibilidad del servicio."""
        self._disponible = bool(valor)

    @abstractmethod
    def calcular_costo(self, duracion: float, impuesto: float = 0.0,
                       descuento: float = 0.0) -> float:
        """Exige calcular el precio según las reglas del tipo de servicio."""
        raise NotImplementedError

    @abstractmethod
    def describir(self) -> str:
        """Exige una descripción adaptada al servicio concreto."""
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, duracion: float) -> None:
        """Exige validar disponibilidad y límites propios de cada servicio."""
        raise NotImplementedError

    def _aplicar_impuesto_y_descuento(self, subtotal: float,
                                      impuesto: float, descuento: float) -> float:
        """Aplica porcentajes al subtotal y devuelve el resultado a dos decimales."""
        # No se admiten porcentajes negativos.
        if impuesto < 0 or descuento < 0:
            raise DatosInvalidosError("Impuesto y descuento no negativos.")
        # El descuento no puede ser superior al total del subtotal.
        if descuento > 100:
            raise DatosInvalidosError("Descuento no puede superar 100%.")
        # Primero aumenta el subtotal por impuesto y luego reduce por descuento.
        total = subtotal * (1 + impuesto / 100.0) * (1 - descuento / 100.0)
        # Un total cero o negativo se considera inconsistente para una venta.
        if total <= 0:
            raise CalculoInconsistenteError(f"Total invalido: {total}")
        # Redondea el importe final a la precisión usual de moneda.
        return round(total, 2)

    def __str__(self) -> str:
        """Muestra el tipo, la identificación, la tarifa y la disponibilidad."""
        # Presenta el estado con etiquetas legibles para la salida de consola.
        estado = "DISPONIBLE" if self.disponible else "NO DISPONIBLE"
        return (f"{self.__class__.__name__}[{self.identificador}] "
                f"{self.nombre} | tarifa={self.tarifa_base} | {estado}")