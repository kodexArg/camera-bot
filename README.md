# Pi Camera Stream MVP

FastAPI + OpenCV para visualizar en LAN/WAN la cámara de una Raspberry Pi con soporte HTTPS.

## Instalación

```bash
uv venv       # crea entorno virtual
uv sync       # instala dependencias según pyproject.toml / uv.lock
```

## Configuración

Edita la sección `[tool.pi-camera]` en `pyproject.toml`:

```toml
[tool.pi-camera]
device_id = 0                 # ID del dispositivo de cámara (/dev/video0)
fps = 15                      # Frames por segundo
enable_ssl = false            # true para HTTPS, false para HTTP (por defecto)
ssl_keyfile = ""              # Path a clave privada SSL (solo si enable_ssl = true)
ssl_certfile = ""             # Path a certificado SSL (solo si enable_ssl = true)
```

## Ejecución

### HTTP (por defecto)
```bash
uv run app
```

### HTTPS (requiere configuración)
1. Configura certificados SSL (ver [INSTRUCCIONES.md](INSTRUCCIONES.md))
2. Actualiza `pyproject.toml`:
   ```toml
   enable_ssl = true
   ssl_keyfile = "/etc/letsencrypt/live/tu-dominio.com/privkey.pem"
   ssl_certfile = "/etc/letsencrypt/live/tu-dominio.com/fullchain.pem"
   ```
3. Ejecuta con privilegios necesarios:
```bash
sudo uv run app    # puerto 443 requiere sudo
```

## Acceso

- HTTP: `http://192.168.10.40:8000`
- HTTPS: `https://tu-dominio.com:443`

Ver [INSTRUCCIONES.md](INSTRUCCIONES.md) para configuración detallada de certificados SSL. 