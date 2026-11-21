# Este módulo registra mensajes con fecha y nivel en un archivo de texto.
# os permite crear la carpeta de destino si todavía no existe.
import os
# datetime genera la marca temporal de cada entrada del registro.
from datetime import datetime


class Logger:
    """Escribe eventos del sistema en un archivo, uno por línea."""

    def __init__(self, ruta_archivo: str = "logs/sistema_fj.log"):
        """Configura la ruta y crea su carpeta contenedora cuando hace falta."""
        # Conserva la ubicación elegida para reutilizarla en cada escritura.
        self.ruta_archivo = ruta_archivo
        # Obtiene el directorio padre; una ruta sin directorio produce una cadena vacía.
        directorio = os.path.dirname(ruta_archivo)
        # Crea la carpeta solo si se indicó una y aún no existe.
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

    def _escribir(self, nivel: str, mensaje: str) -> None:
        """Añade una línea con fecha, nivel y mensaje al archivo de registro."""
        # Genera la fecha y hora local con un formato legible y uniforme.
        marca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Construye el texto completo que se almacenará.
        linea = f"[{marca}] [{nivel}] {mensaje}\n"
        try:
            # Abre el archivo en modo anexado para conservar registros anteriores.
            with open(self.ruta_archivo, "a", encoding="utf-8") as archivo:
                # Escribe la entrada usando codificación UTF-8.
                archivo.write(linea)
        except OSError as error:
            # Informa por consola si el registro no puede escribirse en disco.
            print(f"ADVERTENCIA: {error}")

    def info(self, mensaje: str) -> None:
        """Registra un mensaje informativo."""
        self._escribir("INFO", mensaje)

    def advertencia(self, mensaje: str) -> None:
        """Registra una advertencia."""
        self._escribir("ADVERTENCIA", mensaje)

    def error(self, mensaje: str) -> None:
        """Registra un error."""
        self._escribir("ERROR", mensaje)

    def critico(self, mensaje: str) -> None:
        """Registra un evento crítico."""
        self._escribir("CRITICO", mensaje)