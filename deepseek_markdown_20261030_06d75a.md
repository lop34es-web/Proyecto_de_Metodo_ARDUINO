# 🛡️ Cámara de Seguridad IA (Arduino UNO Q)

Sistema de videovigilancia con Inteligencia Artificial (Edge Impulse) para la detección de armas blancas en tiempo real.

## 🏗️ Arquitectura
- **Captura:** Celular con la app IP Webcam (envía video MJPEG por Wi-Fi).
- **Procesamiento:** Arduino UNO Q (corre un modelo FOMO de Edge Impulse y un servidor Flask).
- **Visualización:** Navegador web local.

## 🚀 Cómo ejecutar
1. Asegurarse de tener el archivo `modelo.eim` en la raíz de la carpeta del proyecto.
2. Modificar la variable `CAMERA_URL` en `python/main.py` con la IP de tu celular.
3. Iniciar el servidor en la terminal de la placa:
   ```bash
   arduino-app-cli app start ~/ArduinoApps/servidor_web