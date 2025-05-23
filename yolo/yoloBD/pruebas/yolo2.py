import cv2
import os
import mysql.connector
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

# Conexión a la base de datos
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "r00t123",
    "database": "ovial"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Crear carpeta para guardar los frames
frame_dir = "frames"
os.makedirs(frame_dir, exist_ok=True)

# Cargar modelo YOLO
model = YOLO("yolov8n.pt")

# Inicializar DeepSORT
tracker = DeepSort(max_age=30)

# Ruta del video
video_path = "trafico.mp4"
cap = cv2.VideoCapture(video_path)
frame_id = 0
frame_skip = 3
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    frame = cv2.resize(frame, (640, 360))
    results = model(frame)[0]

    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        label = model.names[cls]

        if label in ["car", "truck", "bus", "motorcycle"]:
            detections.append(([x1, y1, x2 - x1, y2 - y1], conf, label))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = track.to_ltrb()
        l, t, r, b = map(int, [l, t, r, b])
        w, h = r - l, b - t
        crop = frame[t:b, l:r]

        # Obtener clase del objeto desde detección original
        obj = track.get_det_class()
        if obj is None:
            obj = "vehiculo"

        # Verificar si el vehículo ya existe en la base de datos
        cursor.execute("SELECT id_vehiculo FROM Vehiculo WHERE Tipo = %s", (obj,))
        vehiculo = cursor.fetchone()

        if not vehiculo:
            cursor.execute("""
                INSERT INTO Vehiculo (Tipo, Color, Modelo, Marca, TipoServicio, CamaraSeguridad_id_CamaraSeguridad, CamaraSeguridad_ZonaCritica_id_ZonaCritica) 
                VALUES (%s, 'Desconocido', 'Desconocido', 'Desconocido', 'Privado', 1, 1)
            """, (obj,))
            conn.commit()
            vehiculo_id = cursor.lastrowid
        else:
            vehiculo_id = vehiculo[0]

        # Guardar el recorte del vehículo
        frame_filename = f"{frame_dir}/vehiculo_{vehiculo_id}_track{track_id}_frame{frame_count}.jpg"
        if crop.size > 0:
            cv2.imwrite(frame_filename, crop)

        # Insertar en la base de datos
        coordenadas = f"{l},{t},{r},{b}"
        cursor.execute("""
            INSERT INTO SeguimientoVehiculo (Vehiculo_id_vehiculo, coordenadas, velocidad, fecha_seguimiento, hora_seguimiento, frame_path)
            VALUES (%s, %s, '0 km/h', NOW(), NOW(), %s)
        """, (vehiculo_id, coordenadas, frame_filename))
        conn.commit()

        # Dibujar en el frame
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(frame, f'ID {track_id}', (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Seguimiento de Vehículos", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cierre
cap.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()
print("Seguimiento con DeepSORT y YOLO completado.")
