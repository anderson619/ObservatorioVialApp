# Detección con Yolo

# YOLOBD/detection/yolo_detector.py

from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.names = self.model.model.names

    def detect(self, frame, conf_threshold=0.5):
        results = self.model(frame, verbose=False)
        detections = []

        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf < conf_threshold:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                class_name = self.names[cls_id]

                detections.append({
                    "bbox": [x1, y1, x2 - x1, y2 - y1],  # formato xywh
                    "confidence": conf,
                    "class": class_name
                })
        return detections

