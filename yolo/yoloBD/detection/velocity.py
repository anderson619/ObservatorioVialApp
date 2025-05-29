# utils/velocity.py
import math
import time

track_history = {}

def calcular_velocidad(track_id, cx, cy):
    current_time = time.time()
    if track_id in track_history:
        prev_x, prev_y, prev_time = track_history[track_id]
        dist = math.hypot(cx - prev_x, cy - prev_y)
        time_diff = current_time - prev_time
        velocidad = dist / time_diff if time_diff > 0 else 0
    else:
        velocidad = 0

    # Actualizar historial
    track_history[track_id] = (cx, cy, current_time)
    return velocidad
