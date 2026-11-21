# Este módulo define el modelo de cliente y las reglas de validación de sus datos.
import re
# La clase base centraliza la normalización del identificador y el nombre.
from modelos.entidad_base import EntidadBase
# Estas excepciones distinguen datos inválidos de campos obligatorios ausentes.
from excepciones.excepciones_personalizadas import (
    DatosInvalidosError,
    ParametroFaltanteError,
)


class Cliente(EntidadBase):
    """Representa a una persona registrada con identificación y contacto validados."""

    def __init__(self, cedula: str, nombre: str, email: str, telefono: str):
        """Valida los datos personales y almacena el contacto normalizado."""
        # Una cédula vacía se reporta como parámetro obligatorio faltante.
        if cedula is None or str(cedula).strip() == "":
            raise ParametroFaltanteError("La cedula es obligatoria.")
        # Comprueba que la cédula cumpla el formato numérico admitido.
        if not self._validar_cedula(cedula):
            raise DatosInvalidosError(f"Cedula invalida: '{cedula}'.")
        # Comprueba el formato del correo antes de guardar el cliente.
        if not self._validar_email(email):
            raise DatosInvalidosError(f"Email invalido: '{email}'.")
        # Comprueba el formato del teléfono antes de guardar el cliente.
        if not self._validar_telefono(telefono):
            raise DatosInvalidosError(f"Telefono invalido: '{telefono}'.")
        # Delega la validación y normalización de cédula y nombre a la clase base.
        super().__init__(identificador=str(cedula), nombre=nombre)
        # Normaliza el correo para facilitar comparaciones posteriores.
        self._email = email.strip().lower()
        # Conserva el teléfono sin espacios externos.
        self._telefono = telefono.strip()

    @staticmethod
    def _validar_cedula(cedula: str) -> bool:
        """Acepta entre 6 y 12 dígitos, ignorando espacios externos."""
        return bool(re.fullmatch(r"\d{6,12}", str(cedula).strip()))

    @staticmethod
    def _validar_email(email: str) -> bool:
        """Comprueba que el correo tenga usuario, dominio y extensión."""
        # El correo debe ser texto y no puede estar vacío.
        if not email or not isinstance(email, str):
            return False
        # La expresión regular valida el formato completo, no solo una subcadena.
        return bool(re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email.strip()))

    @staticmethod
    def _validar_telefono(telefono: str) -> bool:
        """Acepta de 7 a 15 dígitos y un signo más inicial opcional."""
        return bool(re.fullmatch(r"\+?\d{7,15}", str(telefono).strip()))

    @property
    def cedula(self) -> str:
        """Expone la cédula, almacenada como identificador de la clase base."""
        return self._identificador

    @property
    def email(self) -> str:
        """Devuelve el correo normalizado del cliente."""
        return self._email

    @property
    def telefono(self) -> str:
        """Devuelve el teléfono normalizado del cliente."""
        return self._telefono

    def describir(self) -> str:
        """Compone una ficha de texto con identificación y datos de contacto."""
        return (f"Cliente[{self.cedula}] {self.nombre} | "
                f"email={self.email} | tel={self.telefono}")

    def __str__(self) -> str:
        """Usa la ficha descriptiva como representación textual del cliente."""
        return self.describir()