from ultralytics import YOLO

# Load model
model = YOLO('yolo11n.pt')

# Run on a sample image (downloads automatically)
results = model('https://ultralytics.com/images/bus.jpg', save=True)

# Print what was detected
for r in results:
    for box in r.boxes:
        print(f"Detected: {r.names[int(box.cls)]}, confidence: {float(box.conf):.2f}")
