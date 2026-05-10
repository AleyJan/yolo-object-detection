# YOLO11n Object Detection on Raspberry Pi 5

An real-time object detection system built for Raspberry Pi 5 using YOLO11n, designed as the foundation for an **AI-powered assistive glasses system for visually impaired people**.

## Hardware Used
- Raspberry Pi 5 (4GB RAM)
- Pi Camera Module 2
- MicroSD Card (32GB+)

## Features
- Real-time object detection using YOLO11n
- Optimized for Raspberry Pi 5 (CPU only, no GPU needed)
- ONNX runtime for faster inference
- Achieves 15-16 FPS on Pi 5

## Project Roadmap
- [x] Real-time object detection with YOLO11n
- [x] Optimized with ONNX export (320x320)
- [ ] Distance estimation using MiDaS depth model
- [ ] Audio feedback for visually impaired users
- [ ] Smart announcements (speak only when new object appears)
- [ ] Wearable glasses integration

## Setup Instructions

### 1. Clone the repo
git clone https://github.com/AleyJan/yolo-object-detection.git
cd yolo-object-detection

### 2. Create virtual environment
python3 -m venv yolo-env --system-site-packages
source yolo-env/bin/activate

### 3. Install PyTorch CPU only
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

### 4. Install dependencies
pip install ultralytics --no-deps
pip install opencv-python numpy pillow pyyaml tqdm scipy matplotlib psutil requests ultralytics-thop
pip install picamera2 --no-deps
pip install onnxruntime onnx onnxslim

### 5. Export YOLO11n to ONNX
python3 -c "
from ultralytics import YOLO
model = YOLO('yolo11n.pt')
model.export(format='onnx', imgsz=320)
"

### 6. Run detection
python3 detect_live.py

## Performance
| Model | Input Size | FPS |
|---|---|---|
| yolo11n.pt | 640x640 | ~3.7 |
| yolo11n.pt | 320x320 | ~9.9 |
| yolo11n.onnx | 320x320 | ~15-16 |

## Tech Stack
- Python 3.13
- Ultralytics YOLO11n
- ONNX Runtime
- OpenCV
- Picamera2
- Raspberry Pi OS Bookworm (64-bit)
