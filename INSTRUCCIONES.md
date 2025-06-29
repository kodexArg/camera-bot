# Configuración de Certificados SSL con Let's Encrypt

Instrucciones para configurar HTTPS en el streaming de cámara.

## Prerrequisitos

- Dominio público apuntando a tu Raspberry Pi
- Puerto 80 y 443 abiertos en router/firewall
- Acceso root/sudo

## Instalación de Certbot

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Certbot
sudo apt install certbot -y
```

## Obtener Certificados

### Método 1: Standalone (recomendado si no tienes otro servidor web)

```bash
# Detener cualquier servicio en puerto 80
sudo systemctl stop apache2 nginx 2>/dev/null || true

# Obtener certificado
sudo certbot certonly --standalone -d tu-dominio.com

# Los certificados se guardan en:
# /etc/letsencrypt/live/tu-dominio.com/privkey.pem
# /etc/letsencrypt/live/tu-dominio.com/fullchain.pem
```

### Método 2: Webroot (si ya tienes servidor web)

```bash
sudo certbot certonly --webroot -w /var/www/html -d tu-dominio.com
```

## Configurar la Aplicación

Edita `config.yaml` y habilita SSL:

```yaml
ssl:
  enable: true
  keyfile: "/etc/letsencrypt/live/tu-dominio.com/privkey.pem"
  certfile: "/etc/letsencrypt/live/tu-dominio.com/fullchain.pem"
```

**Nota**: `enable: false` por defecto. Debes cambiarlo a `true` para usar HTTPS.

## Permisos

```bash
# Opción 1: Ejecutar como root (simple pero menos seguro)
sudo python app/main.py

# Opción 2: Agregar usuario al grupo ssl-cert (más seguro)
sudo usermod -a -G ssl-cert $USER
sudo chgrp ssl-cert /etc/letsencrypt/live/tu-dominio.com/privkey.pem
sudo chmod 640 /etc/letsencrypt/live/tu-dominio.com/privkey.pem
# Reiniciar sesión después de esto
```

## Renovación Automática

```bash
# Configurar cron para renovación automática
sudo crontab -e

# Agregar línea (revisa a las 2:30 AM todos los días):
30 2 * * * /usr/bin/certbot renew --quiet && systemctl restart tu-servicio-camara
```

## Verificación

```bash
# Verificar certificados
sudo certbot certificates

# Probar renovación
sudo certbot renew --dry-run
```

## Firewall

```bash
# Si usas ufw
sudo ufw allow 443/tcp
sudo ufw allow 80/tcp  # para renovación de certificados

# Si usas iptables
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
```

## Troubleshooting

### Error de permisos
```bash
# Verificar propietario y permisos
ls -la /etc/letsencrypt/live/tu-dominio.com/
```

### Puerto 443 ocupado
```bash
# Verificar qué usa el puerto
sudo netstat -tulpn | grep :443
sudo systemctl stop apache2 nginx
```

### Dominio no resuelve
```bash
# Verificar DNS
nslookup tu-dominio.com
dig tu-dominio.com
``` 