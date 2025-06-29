# Pi Camera Stream MVP

FastAPI + OpenCV para visualizar en LAN/WAN la cámara de una Raspberry Pi con soporte HTTPS.

**Soporta:**
- Cámaras locales USB/CSI (Raspberry Pi Camera)
- Cámaras IP con protocolo RTSP

## Instalación

```bash
python -m venv venv               # crea entorno virtual
source venv/bin/activate          # activa entorno (Linux/Mac)
# o en Windows: venv\Scripts\activate
pip install -r requirements.txt  # instala dependencias
```

## Configuración

Edita el archivo `config.yaml`:

```yaml
camera:
  # Para cámara local USB/CSI (usar device_id)
  device_id: 0         # ID del dispositivo de cámara (/dev/video0)
  
  # Para cámara IP RTSP (usar rtsp_url, tiene prioridad sobre device_id)
  rtsp_url: "rtsp://usuario:contraseña@192.168.1.100:554/stream"
  
  fps: 15              # Frames por segundo

server:
  host: "0.0.0.0"      # Host del servidor
  port: 8000           # Puerto del servidor

ssl:
  enable: false        # true para HTTPS, false para HTTP
  keyfile: ""          # Path a clave privada SSL (solo si enable = true)
  certfile: ""         # Path a certificado SSL (solo si enable = true)
```

**Nota:** Si `rtsp_url` está configurado, tiene prioridad sobre `device_id`.

## Ejecución

### HTTP (por defecto)
```bash
python app/main.py
```

### HTTPS (requiere configuración)
1. Configura certificados SSL (ver [INSTRUCCIONES.md](INSTRUCCIONES.md))
2. Actualiza `config.yaml`:
   ```yaml
   ssl:
     enable: true
     keyfile: "/etc/letsencrypt/live/tu-dominio.com/privkey.pem"
     certfile: "/etc/letsencrypt/live/tu-dominio.com/fullchain.pem"
   ```
3. Ejecuta con privilegios necesarios:
```bash
sudo python app/main.py    # puerto 443 requiere sudo
```

## Acceso

- HTTP: `http://192.168.10.40:8000`
- HTTPS: `https://tu-dominio.com:443`

Ver [INSTRUCCIONES.md](INSTRUCCIONES.md) para configuración detallada de certificados SSL. 