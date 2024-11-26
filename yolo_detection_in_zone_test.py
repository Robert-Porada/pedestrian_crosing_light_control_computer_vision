import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np


def run_yolo_inference(video_path, model_path):
    model = YOLO(model_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video at {video_path}")
        return

    # PROPERTIES
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Video loaded: {width}x{height} at {fps} FPS")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video.")
            break

        # Run model inference
        results = model(frame, conf=0.5, vid_stride=2)

        # Process detections
        detections = sv.Detections.from_ultralytics(results[0])

        # Filter detections by category for each zone
        detections_category_0 = detections[detections.class_id == 0]
        detections_category_1 = detections[detections.class_id == 1]

        # Trigger zones with filtered detections
        zone_lewa_category_0_count = sum(
            zone_lewa.trigger(detections=detections_category_0)
        )
        zone_lewa_category_1_count = sum(
            zone_lewa.trigger(detections=detections_category_1)
        )
        zone_prawa_category_0_count = sum(
            zone_prawa.trigger(detections=detections_category_0)
        )
        zone_prawa_category_1_count = sum(
            zone_prawa.trigger(detections=detections_category_1)
        )

        # Annotate frame
        frame = box_annotator.annotate(scene=frame, detections=detections)
        frame = label_annotator.annotate(scene=frame, detections=detections)
        frame = zone_annotator_lewa.annotate(scene=frame)
        frame = zone_annotator_prawa.annotate(scene=frame)

        # Add text to show counts for each category in each zone
        cv2.putText(
            frame,
            f"Strona Lewa: Ograniczona mobilnosc={zone_lewa_category_0_count}, Regularna mobilnosc={zone_lewa_category_1_count}",
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (0, 0, 255),
            4,
        )
        cv2.putText(
            frame,
            f"Strona Prawa: Ograniczona mobilnosc={zone_prawa_category_0_count}, Regularna mobilnosc={zone_prawa_category_1_count}",
            (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.3,
            (0, 0, 255),
            4,
        )

        # Resize and display frame
        frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))
        cv2.imshow("YOLO Inference", frame)

        # Exit with q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# FRAME SIZE
TARGET_WIDTH = 960
TARGET_HEIGHT = 540


polygon_lewa = np.array([[479, 641], [979, 783], [608, 1008], [89, 819]])
polygon_prawa = np.array([[1196, 340], [1314, 278], [1690, 350], [1572, 414]])

zone_lewa = sv.PolygonZone(polygon=polygon_lewa)
zone_prawa = sv.PolygonZone(polygon=polygon_prawa)

box_annotator = sv.BoundingBoxAnnotator(thickness=1)
label_annotator = sv.LabelAnnotator(text_thickness=1, text_scale=1.5)
zone_annotator_lewa = sv.PolygonZoneAnnotator(
    zone=zone_lewa, color=sv.Color.WHITE, thickness=6, text_thickness=6, text_scale=4, display_in_zone_count=False
)
zone_annotator_prawa = sv.PolygonZoneAnnotator(
    zone=zone_prawa, color=sv.Color.BLUE, thickness=6, text_thickness=6, text_scale=4, display_in_zone_count=False
)

# laska i rower
video_path = "D:\\Nagrania praca inzynierska\\Obrobione\\30.mp4"

# wiele przechodniów
# video_path = "D:\\Nagrania praca inzynierska\\Obrobione\\16.mp4"

# wózek na zakupy
# video_path = "D:\\Nagrania praca inzynierska\\Obrobione\\49.mp4"
model_path = "models\\best.pt"

run_yolo_inference(video_path, model_path)
