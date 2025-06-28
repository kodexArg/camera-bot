from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import router

app = FastAPI(title="Pi Camera Stream MVP")

# Sirve templates como archivos estáticos
TEMPLATE_DIR = Path(__file__).parent / "templates"
app.mount("/static", StaticFiles(directory=TEMPLATE_DIR), name="static")

# Todas las rutas
app.include_router(router)


# CLI entry point
def cli() -> None:
    """Punto de entrada del comando `uv run app`."""
    import uvicorn
    from config import settings
    
    uvicorn_config = {
        "app": "main:app",
        "host": settings.HOST,
        "port": settings.PORT,
        "reload": False,
    }
    
    if settings.ENABLE_SSL and settings.SSL_KEYFILE and settings.SSL_CERTFILE:
        uvicorn_config.update({
            "ssl_keyfile": settings.SSL_KEYFILE,
            "ssl_certfile": settings.SSL_CERTFILE,
        })
        print(f"Starting HTTPS server on {settings.HOST}:{settings.PORT}")
    else:
        if settings.ENABLE_SSL:
            print("WARNING: SSL enabled but certificates not configured, falling back to HTTP")
        print(f"Starting HTTP server on {settings.HOST}:{settings.PORT}")
    
    uvicorn.run(**uvicorn_config)


if __name__ == "__main__":
    cli() 