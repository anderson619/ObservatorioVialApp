# Guardar frames recortados

# YOLOBD/detection/frame_saver.py

import os
import cv2

def save_vehicle_frame(frame, x1, y1, x2, y2, clase, vehiculo_id, frame_count):
    base_dir = os.path.join("frames", clase)
    os.makedirs(base_dir, exist_ok=True)

    filename = f"vehiculo_{vehiculo_id}_{frame_count}.jpg"
    path = os.path.join(base_dir, filename)

    vehicle_crop = frame[y1:y2, x1:x2]
    cv2.imwrite(path, vehicle_crop)
    return path

