# Seguimiento con DeepSORT

# YOLOBD/detection/tracker.py

from deep_sort_realtime.deepsort_tracker import DeepSort

class Tracker:
    def __init__(self):
        self.tracker = DeepSort(max_age=60)

    def update_tracks(self, detections, frame=None):
        formatted_detections = [
            (
                det["bbox"],      # [x, y, w, h]
                det["confidence"], 
                det["class"]
            )
            for det in detections
        ]
        return self.tracker.update_tracks(formatted_detections, frame=frame)
