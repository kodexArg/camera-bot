from pathlib import Path
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, StreamingResponse

from camera import StreamService, get_stream_service

router = APIRouter()

# Rutas API
@router.get("/video_feed")
def video_feed(service: StreamService = Depends(get_stream_service)):
    """Devuelve el flujo MJPEG."""
    return StreamingResponse(
        service.mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Rutas Web
@router.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    """Devuelve la página que muestra el stream."""
    html_path = Path(__file__).parent / "templates" / "index.html"
    return HTMLResponse(html_path.read_text()) 