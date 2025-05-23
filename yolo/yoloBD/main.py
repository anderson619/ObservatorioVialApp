# YOLOBD/main.py

import os
import cv2
from database.db_manager import DatabaseManager
from detection.yolo_detector import YoloDetector
from detection.tracker import Tracker
from detection.frame_saver import save_vehicle_frame
from datetime import datetime


# --- Crear carpeta para debug visual ---
os.makedirs("debug_frames", exist_ok=True)

# --- Configuración base de datos ---
db = DatabaseManager(
    host='localhost',
    user='root',
    password='r00t123',
    database='yolo_db'
)

# --- Inicializar modelos ---
detector = YoloDetector("yolov8s.pt")  # Usa yolov8s para mayor precisión
tracker = Tracker()

# --- Abrir video ---
video_path = "trafico.mp4"
cap = cv2.VideoCapture(video_path)

frame_count = 0
frame_skip = 3

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    # Redimensionar para mayor precisión
    frame = cv2.resize(frame, (1280, 720))

    # Detectar vehículos
    detections = detector.detect(frame, conf_threshold=0.3)
    print(f"[Frame {frame_count}] Detecciones: {len(detections)}")

    # Actualizar tracker
    tracked = tracker.update_tracks(detections, frame=frame)

    for track in tracked:
        if not track.is_confirmed() or track.time_since_update > 0:
            continue

        track_id = track.track_id
        x1, y1, x2, y2 = map(int, track.to_ltrb())
        clase = track.get_det_class()
        conf = track.get_det_conf()

        if clase not in ["car", "truck", "bus", "motorcycle"]:
            continue

        # Insertar en base de datos
        # vehiculo_id = db.get_or_create_vehicle(clase)
        import uuid

        # Datos genéricos por defecto
        color = "desconocido"
        modelo = "desconocido"
        marca = "desconocido"
        tipo_servicio = "particular"
        camara_id = 1  # puedes cambiarlo luego por una cámara real
        zona_id = 1    # puedes cambiarlo por zona crítica si hay lógica
        identificador = str(uuid.uuid4())  # identificador único interno

        vehiculo_id = db.get_or_create_vehicle(
            clase, color, modelo, marca, tipo_servicio, camara_id, zona_id, identificador
        )

        frame_path = save_vehicle_frame(frame, x1, y1, x2, y2, clase, vehiculo_id, frame_count)

        coordenadas = f"{x1},{y1},{x2},{y2}"


        # Simulación o cálculo real de velocidad
        velocidad = 0  # puedes calcularla luego con el tiempo y coordenadas

        # Fecha y hora actuales
        ahora = datetime.now()
        fecha = ahora.date()
        hora = ahora.time()

        # Insertar el seguimiento en la BD
        db.insert_tracking(vehiculo_id, coordenadas, frame_path, velocidad, fecha, hora)

        # Dibujar cuadro en frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'{clase} {conf:.2f}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Guardar frame con resultados
    cv2.imwrite(f"debug_frames/frame_{frame_count}.jpg", frame)

# --- Finalización ---
cap.release()
db.close()
print("✅ Proceso finalizado correctamente.")
