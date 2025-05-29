# utils/velocity.py

import math
import time

# Historial global de posiciones por track_id
track_history = {}

# Parámetros ajustables
FPS = 30  # Cuadros por segundo del video
METROS_POR_PIXEL = 0.05  # Aproximación: 1 px = 5 cm

def calcular_velocidad(track_id, cx, cy):
    current_time = time.time()

    if track_id in track_history:
        prev_x, prev_y, prev_time = track_history[track_id]
        dist_px = math.hypot(cx - prev_x, cy - prev_y)
        tiempo_transcurrido = current_time - prev_time

        # Conversión de píxeles a metros
        dist_metros = dist_px * METROS_POR_PIXEL

        # Velocidad en m/s
        velocidad_m_s = dist_metros / tiempo_transcurrido if tiempo_transcurrido > 0 else 0

        # Convertir a km/h
        velocidad_kmh = velocidad_m_s * 3.6

    else:
        velocidad_kmh = 0

    # Actualizar historial
    track_history[track_id] = (cx, cy, current_time)

    return velocidad_kmh
