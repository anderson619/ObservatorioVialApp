# Funciones utilitarias

# YOLOBD/detection/utils.py

def filter_vehicle_detections(detections):
    vehicle_classes = ["car", "truck", "bus", "motorcycle"]
    return [d for d in detections if d["class"] in vehicle_classes]
