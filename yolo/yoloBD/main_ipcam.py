import cv2
import datetime
import time
import math
from detection.yolo_detector import YoloDetector
from detection.tracker import Tracker
from database.db_manager import DatabaseManager
from detection.color_utils import detectar_color_principal  
from detection.velocity import calcular_velocidad

# Inicializar YOLO, DeepSORT y la base de datos
detector = YoloDetector("yolov8n.pt")
tracker = Tracker()
db = DatabaseManager(
    host="localhost",
    user="root",
    password="r00t123",
    database="ovial"
)

# Dirección IP de la cámara del celular
url = "http://192.168.0.3:8080/video"
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

frame_id = 0
track_history = {}
CLASES_VEHICULOS = ["car", "motorcycle", "bus", "truck", "bicycle"]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1
    frame = cv2.resize(frame, (640, 360))

    # Detección
    detections = detector.detect(frame, conf_threshold=0.3)

    # Seguimiento
    tracked_objects = tracker.update_tracks(detections, frame)
    print(f"[Frame {frame_id}] Detecciones: {len(tracked_objects)}")

    for track in tracked_objects:
        if not track.is_confirmed():
            continue

        clase_detectada = track.det_class
        if clase_detectada not in CLASES_VEHICULOS:
            continue

        track_id = track.track_id
        l, t, r, b = map(int, track.to_ltrb())
        cx = (l + r) // 2
        cy = (t + b) // 2
        current_time = time.time()

        # Calcular velocidad aproximada en px/s
        velocidad = calcular_velocidad(track_id, cx, cy)

        # ➕ Detectar color usando el recorte del bbox
        bbox = [l, t, r, b]
        color = detectar_color_principal(frame, bbox)

        # Datos simulados
        modelo = "generico"
        marca = "generica"
        tipo_servicio = "particular"
        camara_id = 1
        zona_id = 1
        identificador = f"track_{track_id}"

        vehiculo_id = db.get_or_create_vehicle(
            clase_detectada, color, modelo, marca, tipo_servicio, camara_id, zona_id, identificador
        )

        # Insertar seguimiento con velocidad estimada
        coordenadas = f"({l}, {t}, {r}, {b})"
        now = datetime.datetime.now()
        fecha = now.date()
        hora = now.time().strftime("%H:%M:%S")

        db.insert_tracking(vehiculo_id, coordenadas, "", f"{velocidad:.2f} km/h", fecha, hora)

        # Dibujar
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {track_id} {velocidad:.1f} km/h", (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"{color}", (l, b + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Cámara IP - Detección de Vehículos", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
db.close()
cv2.destroyAllWindows()
