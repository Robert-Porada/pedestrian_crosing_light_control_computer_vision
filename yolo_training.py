from ultralytics import YOLO


def main():
    model = YOLO("yolov8m.pt")
    # model = YOLO("runs\\detect\\train3\\weights\\best.pt")

    results = model.train(
        data="data.yaml",
        epochs=70,
        imgsz=640,
        batch=4,
        workers=2,
        amp=False,
    )
    results = model.val(imgsz=640, batch=8, plots=True)


if __name__ == "__main__":
    main()
