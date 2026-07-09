import cv2
from ultralytics import YOLO
from collections import Counter

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Open Webcam
cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    # Object Detection + Tracking
    results = model.track(
        frame,
        persist=True,
        verbose=False
    )

    annotated_frame = results[0].plot()

    object_names = []

    if results[0].boxes is not None:

        for box in results[0].boxes:

            class_id = int(box.cls)

            object_name = model.names[class_id]

            object_names.append(object_name)

    counts = Counter(object_names)

    y_position = 30

    for obj, count in counts.items():

        cv2.putText(
            annotated_frame,
            f"{obj}: {count}",
            (10, y_position),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        y_position += 30

    cv2.imshow(
        "AI Object Detection & Tracking",
        annotated_frame
    )

    key = cv2.waitKey(1)

    results = model.track(
    frame,
    persist=True
    )
    print("Screenshot Saved")

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()