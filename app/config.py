from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional
import yaml

class _EnvSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEVICE_ID: int = 0
    RTSP_URL: Optional[str] = None
    STREAM_FPS: int = 15
    ENABLE_SSL: bool = False
    SSL_KEYFILE: Optional[str] = None
    SSL_CERTFILE: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def _load_yaml_config():
    config_file = Path("config.yaml")
    if not config_file.exists():
        return {}
    
    with open(config_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    return data or {}

_env = _EnvSettings()
_yaml_config = _load_yaml_config()

# Cargar configuración de cámara
if 'camera' in _yaml_config:
    camera_config = _yaml_config['camera']
    if 'device_id' in camera_config:
        _env.DEVICE_ID = int(camera_config['device_id'])
    if 'rtsp_url' in camera_config and camera_config['rtsp_url']:
        _env.RTSP_URL = str(camera_config['rtsp_url'])
    if 'fps' in camera_config:
        _env.STREAM_FPS = int(camera_config['fps'])

# Cargar configuración del servidor
if 'server' in _yaml_config:
    server_config = _yaml_config['server']
    if 'host' in server_config:
        _env.HOST = str(server_config['host'])
    if 'port' in server_config:
        _env.PORT = int(server_config['port'])

# Cargar configuración SSL
if 'ssl' in _yaml_config:
    ssl_config = _yaml_config['ssl']
    if 'enable' in ssl_config:
        _env.ENABLE_SSL = bool(ssl_config['enable'])
    
    # Solo cargar certificados si SSL está habilitado
    if _env.ENABLE_SSL:
        if 'keyfile' in ssl_config and ssl_config['keyfile']:
            _env.SSL_KEYFILE = str(ssl_config['keyfile'])
        if 'certfile' in ssl_config and ssl_config['certfile']:
            _env.SSL_CERTFILE = str(ssl_config['certfile'])

settings = _env 