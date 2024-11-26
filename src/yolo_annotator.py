import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np



class yolo_model():
    def __init__(self):
        self.model = YOLO("models\\best.pt")

        self.polygon_lewa = np.array([[479, 641], [979, 783], [608, 1008], [89, 819]])
        self.polygon_prawa = np.array([[1196, 340], [1314, 278], [1690, 350], [1572, 414]])
        
        self.zone_lewa = sv.PolygonZone(polygon=self.polygon_lewa)
        self.zone_prawa = sv.PolygonZone(polygon=self.polygon_prawa)
        
        self.box_annotator = sv.BoundingBoxAnnotator(thickness=2)
        self.label_annotator = sv.LabelAnnotator(text_thickness=2, text_scale=2)
        self.zone_annotator_lewa = sv.PolygonZoneAnnotator(
            zone=self.zone_lewa, color=sv.Color.WHITE, thickness=6, text_thickness=6, text_scale=4, display_in_zone_count=False
        )
        self.zone_annotator_prawa = sv.PolygonZoneAnnotator(
            zone=self.zone_prawa, color=sv.Color.BLUE, thickness=6, text_thickness=6, text_scale=4, display_in_zone_count=False
        )
    

    def create_annotated_image(self, video_path, frame):
        cap = cv2.VideoCapture(video_path)
        totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if frame >= 0 and frame <= totalFrames:
            # set frame position
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, frame = cap.read()
        results = self.model(frame, conf=0.5, vid_stride=2)

        # Process detections
        detections = sv.Detections.from_ultralytics(results[0])

        # Filter detections by category for each zone
        detections_category_0 = detections[detections.class_id == 0]
        detections_category_1 = detections[detections.class_id == 1]

        # Trigger zones with filtered detections
        zone_lewa_category_0_count = sum(
            self.zone_lewa.trigger(detections=detections_category_0)
        )
        zone_lewa_category_1_count = sum(
            self.zone_lewa.trigger(detections=detections_category_1)
        )
        zone_prawa_category_0_count = sum(
            self.zone_prawa.trigger(detections=detections_category_0)
        )
        zone_prawa_category_1_count = sum(
            self.zone_prawa.trigger(detections=detections_category_1)
        )

        # Annotate frame
        frame = self.box_annotator.annotate(scene=frame, detections=detections)
        frame = self.label_annotator.annotate(scene=frame, detections=detections)
        frame = self.zone_annotator_lewa.annotate(scene=frame)
        frame = self.zone_annotator_prawa.annotate(scene=frame)

        # Add text to show counts for each category in each zone
        cv2.putText(
            frame,
            f"Strona Lewa: Ograniczona mobilnosc={zone_lewa_category_0_count}, Regularna mobilnosc={zone_lewa_category_1_count}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 255),
            4,
        )
        cv2.putText(
            frame,
            f"Strona Prawa: Ograniczona mobilnosc={zone_prawa_category_0_count}, Regularna mobilnosc={zone_prawa_category_1_count}",
            (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 255),
            4,
        )
        cv2.imwrite("results/inference.png", frame) 
        cap.release()
        pedestrian_count = [zone_lewa_category_1_count, zone_lewa_category_0_count, zone_prawa_category_1_count, zone_prawa_category_0_count]
        return pedestrian_count
