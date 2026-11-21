# Define errores de dominio para que las capas puedan distinguir fallos conocidos.


class SoftwareFJError(Exception):
    """Excepción raíz de la que derivan los errores propios del sistema."""
    pass


class DatosInvalidosError(SoftwareFJError):
    """Indica que un dato recibido no cumple las reglas de validación."""
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Indica que falta un parámetro obligatorio para una operación."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Indica que la operación solicitada no es válida en el estado actual."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Indica que el servicio no puede reservarse o utilizarse."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Indica que una reserva no puede crearse o procesarse correctamente."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Indica que una operación de cálculo produjo un total no válido."""
    pass


class ClienteNoEncontradoError(SoftwareFJError):
    """Indica que no existe un cliente con la identificación solicitada."""
    pass