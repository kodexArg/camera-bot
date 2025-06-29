import time
from typing import Generator
import cv2

from config import settings
from interfaces import CameraInterface


class OpenCVCamera(CameraInterface):
    """Implementación usando OpenCV para capturar fotogramas de cámara local o RTSP."""

    def __init__(self) -> None:
        # Priorizar RTSP si está configurado, sino usar device_id local
        if settings.RTSP_URL:
            self.source = settings.RTSP_URL
            print(f"Using RTSP camera: {settings.RTSP_URL}")
        else:
            self.source = settings.DEVICE_ID
            print(f"Using local camera device: {settings.DEVICE_ID}")
        
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Unable to open camera source: {self.source}")
        
        # Configuraciones adicionales para RTSP
        if settings.RTSP_URL:
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer para menor latencia
            
        self.interval = 1.0 / settings.STREAM_FPS

    def frames(self) -> Generator[bytes, None, None]:
        while True:
            ok, frame = self.cap.read()
            if not ok:
                continue
            _, jpeg = cv2.imencode(".jpg", frame)
            time.sleep(self.interval)
            yield jpeg.tobytes()

    def close(self) -> None:
        self.cap.release()


class StreamService:
    """Construye el flujo MJPEG a partir de la cámara."""

    def __init__(self, camera: CameraInterface):
        self._camera = camera

    def mjpeg_stream(self) -> Generator[bytes, None, None]:
        boundary = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
        for chunk in self._camera.frames():
            yield boundary + chunk + b"\r\n"


# Instancia global para DI simple
_camera_instance = None

def get_camera() -> OpenCVCamera:
    global _camera_instance
    if _camera_instance is None:
        _camera_instance = OpenCVCamera()
    return _camera_instance

def get_stream_service() -> StreamService:
    return StreamService(get_camera()) 