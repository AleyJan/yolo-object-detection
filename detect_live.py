import cv2
import numpy as np
import time
from picamera2 import Picamera2
from ultralytics import YOLO

# Use ONNX model instead of .pt
model = YOLO('yolo11n.onnx')

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
))
picam2.start()

print("Starting detection... Press 'q' to quit")

prev_time = time.time()

while True:
    frame = picam2.capture_array()

    # imgsz=320 = faster inference, conf=0.6 = stable detections
    results = model(frame, verbose=False, conf=0.6)
    annotated = results[0].plot()

    # FPS counter
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    cv2.putText(annotated, f'FPS: {fps:.1f}', (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    print(f"FPS: {fps:.1f}", end='\r')

    cv2.imshow('YOLO11n ONNX - Object Detection', annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
