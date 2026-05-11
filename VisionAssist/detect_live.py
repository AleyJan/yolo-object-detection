import cv2
import time
import subprocess
import threading
import queue
from picamera2 import Picamera2
from ultralytics import YOLO

model = YOLO('yolo11n.onnx', task='detect')

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
))
picam2.start()

ANNOUNCE_COOLDOWN = 5
FRAME_WIDTH = 640
last_announced = {}
speech_queue = queue.Queue()

PIPER_MODEL = '/home/raspberrypi/piper-voices/en_US-lessac-medium.onnx'
AIRPODS_DEVICE = 'bluez_output.41_42_BE_BD_9C_4B.1'

def speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        try:
            piper = subprocess.Popen(
                ['/home/raspberrypi/piper/piper', '--model', PIPER_MODEL, '--output-raw'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            paplay = subprocess.Popen(
                ['paplay', '--raw', '--rate=22050', '--format=s16le',
                 '--channels=1', f'--device={AIRPODS_DEVICE}'],
                stdin=piper.stdout,
                stderr=subprocess.DEVNULL
            )
            piper.stdin.write(text.encode())
            piper.stdin.close()
            paplay.wait()
        except Exception as e:
            print(f"Speech error: {e}")
        speech_queue.task_done()

threading.Thread(target=speech_worker, daemon=True).start()

def speak(text):
    while not speech_queue.empty():
        try:
            speech_queue.get_nowait()
            speech_queue.task_done()
        except:
            pass
    speech_queue.put(text)

def get_direction(box_center_x, frame_width):
    left_zone = frame_width * 0.33
    right_zone = frame_width * 0.66
    if box_center_x < left_zone:
        return "on your left"
    elif box_center_x > right_zone:
        return "on your right"
    else:
        return "in front of you"

def get_urgency(box_area, frame_area):
    ratio = box_area / frame_area
    if ratio > 0.4:
        return "warning", True   # very close
    elif ratio > 0.15:
        return "ahead", False    # medium distance
    else:
        return "nearby", False   # far

print("Starting detection... Press 'q' to quit")
speak("Assistive glasses started. Object detection is active.")

prev_time = time.time()
frame_area = 640 * 480

while True:
    frame = picam2.capture_array()
    results = model(frame, verbose=False, conf=0.75)
    annotated = results[0].plot()

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(annotated, f'FPS: {fps:.1f}', (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    now = time.time()
    urgent_objects = []
    normal_objects = []

    for box in results[0].boxes:
        label = results[0].names[int(box.cls)]

        # Get box info
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        center_x = (x1 + x2) / 2
        box_area = (x2 - x1) * (y2 - y1)

        direction = get_direction(center_x, FRAME_WIDTH)
        urgency_word, is_urgent = get_urgency(box_area, frame_area)

        if now - last_announced.get(label, 0) > ANNOUNCE_COOLDOWN:
            last_announced[label] = now
            if is_urgent:
                urgent_objects.append(f"warning! {label} very close {direction}")
            else:
                normal_objects.append(f"{label} {urgency_word} {direction}")

    # Speak urgent first, then normal
    for msg in urgent_objects:
        speak(msg)
        print(f"\nSpeaking: {msg}")

    if not urgent_objects and normal_objects:
        # Combine normal objects into one sentence
        combined = ", ".join(normal_objects)
        speak(combined)
        print(f"\nSpeaking: {combined}")

    print(f"FPS: {fps:.1f} | Detected: {[results[0].names[int(b.cls)] for b in results[0].boxes]}", end='\r')

    cv2.imshow('Assistive Glasses', annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
