from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

class _EnvSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEVICE_ID: int = 0
    STREAM_FPS: int = 15
    ENABLE_SSL: bool = False
    SSL_KEYFILE: Optional[str] = None
    SSL_CERTFILE: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def _load_pyproject_config():
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        return {}
    data = tomllib.loads(pyproject.read_text())
    return data.get("tool", {}).get("pi-camera", {})

_env = _EnvSettings()
_toolcfg = _load_pyproject_config()

if "device_id" in _toolcfg:
    _env.DEVICE_ID = int(_toolcfg["device_id"])
if "fps" in _toolcfg:
    _env.STREAM_FPS = int(_toolcfg["fps"])
if "enable_ssl" in _toolcfg:
    _env.ENABLE_SSL = bool(_toolcfg["enable_ssl"])

# Solo cargar certificados si SSL está habilitado
if _env.ENABLE_SSL:
    if "ssl_keyfile" in _toolcfg and _toolcfg["ssl_keyfile"]:
        _env.SSL_KEYFILE = str(_toolcfg["ssl_keyfile"])
    if "ssl_certfile" in _toolcfg and _toolcfg["ssl_certfile"]:
        _env.SSL_CERTFILE = str(_toolcfg["ssl_certfile"])

settings = _env 