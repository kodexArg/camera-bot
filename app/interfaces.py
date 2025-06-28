from abc import ABC, abstractmethod
from typing import Generator


class CameraInterface(ABC):
    """Abstracción de cualquier fuente de imágenes."""

    @abstractmethod
    def frames(self) -> Generator[bytes, None, None]:
        """Devuelve un generador de imágenes JPEG en bytes."""

    @abstractmethod
    def close(self) -> None:
        """Libera recursos asociados a la cámara."""


class NotifierInterface(ABC):
    """Abstracción para notificaciones (futuro: Telegram, email, etc.)."""

    @abstractmethod
    def send_alert(self, message: str) -> None:
        """Envía una alerta con el mensaje especificado.""" 