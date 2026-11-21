"""Define la clase abstracta común a los objetos identificables del sistema."""
# ABC permite crear clases base que no se pueden instanciar directamente.
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Proporciona identificador, nombre y contrato de descripción a sus subclases."""

    def __init__(self, identificador: str, nombre: str):
        """Valida y normaliza los datos comunes al construir una entidad."""
        # Rechaza identificadores ausentes o que solo contengan espacios.
        if not identificador or not str(identificador).strip():
            # La importación local evita dependencias innecesarias al cargar el módulo.
            from excepciones.excepciones_personalizadas import DatosInvalidosError
            # Informa el problema usando la excepción común de validación.
            raise DatosInvalidosError("El identificador no puede estar vacio.")
        # Rechaza nombres ausentes o que solo contengan espacios.
        if not nombre or not str(nombre).strip():
            # Importa la excepción solo cuando ocurre esta validación.
            from excepciones.excepciones_personalizadas import DatosInvalidosError
            # Evita guardar entidades sin nombre.
            raise DatosInvalidosError("El nombre no puede estar vacio.")
        # Guarda el identificador como texto, sin espacios externos.
        self._identificador = str(identificador).strip()
        # Guarda el nombre sin espacios externos.
        self._nombre = str(nombre).strip()

    @property
    def identificador(self) -> str:
        """Devuelve el identificador de solo lectura de la entidad."""
        return self._identificador

    @property
    def nombre(self) -> str:
        """Devuelve el nombre de solo lectura de la entidad."""
        return self._nombre

    @abstractmethod
    def describir(self) -> str:
        """Exige a cada subclase definir una representación legible de sí misma."""
        # Mantiene explícito que este método debe implementarse en las subclases.
        raise NotImplementedError

    def __str__(self) -> str:
        """Devuelve una representación genérica con el tipo, el ID y el nombre."""
        return f"{self.__class__.__name__}(id={self._identificador}, nombre={self._nombre})"