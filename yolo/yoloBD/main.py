# # main.py mejorado con seguimiento y control de duplicados

# import cv2
# import datetime
# from detection.yolo_detector import YoloDetector
# from detection.tracker import Tracker
# from detection.frame_saver import save_cropped_vehicle
# from database.db_manager import DatabaseManager

# # Inicializar modelos y base de datos
# detector = YoloDetector('yolov8n.pt')
# tracker = Tracker()
# db = DatabaseManager(
#     host='localhost',
#     user='root',
#     password='r00t123',
#     database='ovial'
# )

# # Video de entrada
# cap = cv2.VideoCapture('trafico.mp4')
# frame_id = 0
# track_ids_guardados = set()
# output_dir = "frames"  # Carpeta donde se guardan recortes

# CLASES_VEHICULOS = ['car', 'motorcycle', 'bus', 'truck', 'bicycle']

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     frame_id += 1
#     frame = cv2.resize(frame, (1280, 720))

#     # Detección con YOLO
#     detections = detector.detect(frame, conf_threshold=0.3)

#     # Seguimiento
#     tracked_objects = tracker.update_tracks(detections, frame)
#     print(f"[Frame {frame_id}] Detecciones: {len(tracked_objects)}")

#     for track in tracked_objects:
#         if not track.is_confirmed():
#             continue

#         clase_detectada = track.det_class  # ← esta es la clase original

#         if clase_detectada not in CLASES_VEHICULOS:
#             continue

#         track_id = track.track_id
#         l, t, r, b = map(int, track.to_ltrb())  # left, top, right, bottom

#         if track_id in track_ids_guardados:
#             continue

#         # Datos simulados
#         clase = clase_detectada  # ← ahora usamos la clase real detectada
#         color = "desconocido"
#         modelo = "generico"
#         marca = "generica"
#         tipo_servicio = "particular"
#         camara_id = 1
#         zona_id = 1
#         identificador = f"track_{track_id}"

#         vehiculo_id = db.get_or_create_vehicle(
#             clase, color, modelo, marca, tipo_servicio, camara_id, zona_id, identificador
#         )

#         # Guardar recorte de imagen
#         frame_path = save_cropped_vehicle(frame, [l, t, r, b], output_dir, track_id)

#         # Guardar seguimiento
#         coordenadas = f"({l}, {t}, {r}, {b})"
#         velocidad = 0
#         now = datetime.datetime.now()
#         fecha = now.date()
#         hora = now.time().strftime("%H:%M:%S")

#         db.insert_tracking(vehiculo_id, coordenadas, frame_path, velocidad, fecha, hora)
#         track_ids_guardados.add(track_id)

#         # Dibujar en pantalla
#         cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
#         cv2.putText(frame, f'ID {track_id}', (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#     cv2.imshow("Detección", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# db.close()
# cv2.destroyAllWindows()


# ------------

# main.py - Detección y seguimiento de vehículos con YOLOv8 y DeepSORT

import cv2
import datetime
from detection.yolo_detector import YoloDetector
from detection.tracker import Tracker
from detection.frame_saver import save_cropped_vehicle
from database.db_manager import DatabaseManager

# Inicializar modelos y base de datos
detector = YoloDetector('yolov8n.pt')  # Ruta a tu modelo YOLOv8
tracker = Tracker()
db = DatabaseManager(
    host='localhost',
    user='root',
    password='r00t123',
    database='ovial'
)

# Video de entrada
cap = cv2.VideoCapture('trafico.mp4')  # Asegúrate de que este archivo exista
frame_id = 0
track_ids_guardados = set()
output_dir = "frames"

# Clases que se consideran vehículos
CLASES_VEHICULOS = ['car', 'motorcycle', 'bus', 'truck', 'bicycle']

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1
    frame = cv2.resize(frame, (1280, 720))

    # Detección con YOLO
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

        if track_id in track_ids_guardados:
            continue

        # Datos simulados
        clase = clase_detectada
        color = "desconocido"
        modelo = "generico"
        marca = "generica"
        tipo_servicio = "particular"
        camara_id = 1
        zona_id = 1
        identificador = f"track_{track_id}"

        vehiculo_id = db.get_or_create_vehicle(
            clase, color, modelo, marca, tipo_servicio, camara_id, zona_id, identificador
        )

        # Guardar recorte
        frame_path = save_cropped_vehicle(frame, [l, t, r, b], output_dir, track_id)

        # Guardar seguimiento
        coordenadas = f"({l}, {t}, {r}, {b})"
        velocidad = 0  # Opcional: calcular velocidad en el futuro
        now = datetime.datetime.now()
        fecha = now.date()
        hora = now.time().strftime("%H:%M:%S")

        db.insert_tracking(vehiculo_id, coordenadas, frame_path, velocidad, fecha, hora)
        track_ids_guardados.add(track_id)

        # Mostrar en pantalla
        cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(frame, f'ID {track_id}', (l, t - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Detección", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
db.close()
cv2.destroyAllWindows()
