# # Seguimiento con DeepSORT

# # YOLOBD/detection/tracker.py

# from deep_sort_realtime.deepsort_tracker import DeepSort

# class Tracker:
#     def __init__(self):
#         self.tracker = DeepSort(max_age=60)

#     def update_tracks(self, detections, frame=None):
#         #formatted_detections = [
#         #    (
#         #        det["bbox"],        # [x, y, w, h]
#         #        det["confidence"], 
#         #        None,
#         #        det["class"],        # Este es el class_name
#         #        None
#         #    )
#         #    for det in detections
#         #]
#         #tracks = self.tracker.update_tracks(formatted_detections, frame=frame)

#         formatted_detections = []
#         class_map = {}  # Mapear track_id -> class_name

#         for det in detections:
#             bbox = det["bbox"]
#             conf = det["confidence"]
#             class_name = det["class"]

#             formatted_detections.append((
#                 bbox,
#                 conf,
#                 None,
#                 class_name,  # → esto se guarda como metadata
#                 None
#             ))

#         tracks = self.tracker.update_tracks(formatted_detections, frame=frame)

#         # Asignar clase detectada a cada track usando metadata
#         for track in tracks:
#             if hasattr(track, 'detections') and len(track.detections) > 0:
#                 track.det_class = track.detections[-1].metadata
#             else:
#                 track.det_class = None
#         return tracks

#     def update(self, detections, frame=None):
#         return self.update_tracks(detections, frame)


# ---------

# detection/tracker.py - Seguimiento con DeepSORT

from deep_sort_realtime.deepsort_tracker import DeepSort

class Tracker:
    def __init__(self):
        self.tracker = DeepSort(max_age=30)

    def update_tracks(self, detections, frame):
        converted = []
        for det in detections:
            x, y, w, h = det["bbox"]
            class_name = det["class"]
            conf = det["confidence"]
            converted.append(([x, y, w, h], conf, class_name))

        tracks = self.tracker.update_tracks(converted, frame=frame)

        resultados = []
        for track in tracks:
            if not track.is_confirmed():
                continue
            track.det_class = track.det_class if hasattr(track, 'det_class') else track.get_det_class()
            resultados.append(track)

        return resultados
