import cv2
import numpy as np

def detectar_color_principal(image, bbox):
    x1, y1, x2, y2 = bbox
    roi = image[y1:y2, x1:x2]

    if roi.size == 0:
        return "desconocido"

    # Convertir a espacio de color HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    avg_color = np.mean(hsv.reshape(-1, 3), axis=0)
    h, s, v = avg_color

    # Clasificación básica por tonos
    if s < 40 and v > 150:
        return "blanco"
    elif v < 50:
        return "negro"
    elif 0 <= h <= 15 or 160 <= h <= 180:
        return "rojo"
    elif 15 < h <= 35:
        return "amarillo"
    elif 35 < h <= 85:
        return "verde"
    elif 85 < h <= 135:
        return "azul"
    elif 135 < h < 160:
        return "morado"
    else:
        return "gris"
