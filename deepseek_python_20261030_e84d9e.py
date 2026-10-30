from flask import Flask
import cv2
import time
import threading
from edge_impulse_linux.image import ImageImpulseRunner

app = Flask(__name__)

# --- CONFIGURACIÓN ---
# IP del celular con IP Webcam
CAMERA_URL = "http://192.168.1.50:8080/video" 
# Nombre del modelo de IA
MODEL_PATH = "/app/modelo.eim" 

# --- CARGAR MODELO ---
runner = None
try:
    print("Cargando modelo de IA...")
    runner = ImageImpulseRunner(MODEL_PATH)
    model_info = runner.init()
    print(f"✅ Modelo cargado: {model_info['model_parameters']['labels']}")
except Exception as e:
    print(f"❌ Error: {e}")

# --- HILO DE IA ---
def bucle_ia():
    if not runner: return
    cap = cv2.VideoCapture(CAMERA_URL)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    ultima_alerta = 0
    cooldown = 3 
    
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            time.sleep(0.5)
            continue
        try:
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            features, cropped = runner.get_features_from_image(img_rgb)
            res = runner.classify(features)
            
            if res and "result" in res and "bounding_boxes" in res["result"]:
                for bb in res["result"]["bounding_boxes"]:
                    label = bb['label']
                    confidence = bb['value']
                    
                    if confidence > 0.15: 
                        tiempo_actual = time.time()
                        if tiempo_actual - ultima_alerta > cooldown:
                            print(f"🚨 ¡ALERTA! Se detectó: {label.upper()} ({confidence*100:.1f}%)")
                            ultima_alerta = tiempo_actual
        except Exception:
            pass 
        time.sleep(0.1)

threading.Thread(target=bucle_ia, daemon=True).start()

# --- SERVIDOR WEB ---
@app.route('/')
def index():
    url_directa = CAMERA_URL
    return f"""
    <html>
        <head>
            <title>Camara de Seguridad IA</title>
            <style>
                body {{ text-align: center; background-color: #111; color: white; font-family: Arial; }}
                img {{ width: 100%; max-width: 800px; border: 3px solid #333; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <h1>Camara de Seguridad IA</h1>
            <p>La Inteligencia Artificial está analizando el video en la placa.</p>
            <img src="{url_directa}">
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)