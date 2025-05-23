import mysql.connector
import cv2
from ultralytics import YOLO

# Configuración de conexión a MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "r00t123",
    "database": "ovial"
}

# Conectar a MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("✅ Conexión exitosa a la base de datos")
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")

# Habilitar optimización en OpenCV
cv2.setUseOptimized(True)
cv2.setNumThreads(4)  # Ajusta el número de hilos según tu procesador

# Modelo YOLO optimizado
model = YOLO("yolov8s.pt")  # YOLOv8s es más rápido que YOLOv8n
video_path = "trafico.mp4"

# Procesar video
cap = cv2.VideoCapture(video_path)
frame_skip = 3  # Procesar cada 3 frames para mejorar velocidad
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  
    
    frame_count += 1
    if frame_count % frame_skip != 0:
        continue  # Saltar frames
    
    # Reducir resolución para mejorar velocidad
    frame = cv2.resize(frame, (640, 360))
    
    results = model(frame)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas del bounding box
            obj = model.names[int(box.cls)]  # Nombre del objeto detectado
            conf = float(box.conf[0])  # Confianza de detección
            
            if obj in ["car", "truck", "bus", "motorbike"]:  # Solo guardar vehículos
                
                # Insertar en tabla Vehiculo (si no existe)
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

                # Insertar en SeguimientoVehiculo
                coordenadas = f"{x1},{y1},{x2},{y2}"
                cursor.execute("""
                    INSERT INTO SeguimientoVehiculo (Vehiculo_id_vehiculo, coordenadas, velocidad, fecha_seguimiento, hora_seguimiento)
                    VALUES (%s, %s, '0 km/h', NOW(), NOW())
                """, (vehiculo_id, coordenadas))
                conn.commit()

                # Dibujar bounding box en el frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{obj} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Mostrar el video con las detecciones
    cv2.imshow('Detección de Vehículos', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()
print("Detecciones guardadas en MySQL")
