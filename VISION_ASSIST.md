# VisionAssist — AI Powered Glasses for the Visually Impaired

An open-source, offline, affordable assistive technology system built on
Raspberry Pi 5 that gives visually impaired people real-time awareness of
their surroundings through intelligent audio feedback.

---

## The Problem

Over 2.2 billion people worldwide have visual impairment. Most assistive
technologies are either too expensive, require internet connection, or provide
limited functionality. There is a need for an affordable, offline, intelligent
assistive system that works anywhere in the world.

---

## The Solution

VisionAssist is a wearable glasses system powered by Raspberry Pi 5 that uses
computer vision, depth sensing, speech recognition, and AI to give blind and
visually impaired users a complete picture of their surroundings through
natural audio feedback — completely offline, no internet required.

---

## Hardware

| Component | Purpose | Cost |
|---|---|---|
| Raspberry Pi 5 (4GB) | Main processing unit | ~$60 |
| Pi Camera Module 2 | Visual input | ~$25 |
| HC-SR04 Ultrasonic Sensor | Accurate distance measurement | ~$3 |
| Bluetooth Earphones | Audio output | varies |
| GPIO Button | Backup input trigger | ~$1 |
| MicroSD Card (32GB+) | Storage | ~$10 |
| Power Bank | Portable power | ~$15 |
| Glasses Frame | Wearable mount | ~$5 |
| **Total** | | **~$120** |

---

## System Architecture

### Core Concept

VisionAssist runs two parallel modes managed by a central Mode Manager.
Vosk voice recognition runs continuously in the background regardless of
which mode is active, always listening for voice commands.

---

### Mode Manager

The brain of the system. Decides which mode is active based on voice
commands. Only one mode runs at a time to avoid audio confusion.

---

### Navigation Mode (Default)

This is the primary mode that runs automatically on startup.

**Object Detection Pipeline:**

- **Layer 1 — yolo11n** runs every frame at 15 FPS
  - Detects large objects: people, cars, chairs, doors, stairs
  - Primary safety layer for obstacle avoidance

- **Layer 2 — yolo11s** runs every 5 frames (~3 FPS)
  - Detects small objects: cups, spoons, phones, bottles, books
  - More accurate than yolo11n for small everyday items

**Spatial Awareness:**

Each detected object is analysed for:
- Direction: left / center / right based on position in frame
- Urgency: nearby / ahead / warning based on object size in frame
- Distance: accurate measurement in cm from ultrasonic sensor

**Scene Description:**

- Moondream2 runs in background
- Describes full scene in natural language
- Triggers every 15 seconds when user is moving
- Triggers every 60 seconds when user is stationary
- Pauses automatically when reading mode activates
- Triggered instantly on "Hey Pi describe" command

---

### Reading Mode

Activated by voice command "Hey Pi read this".
Designed for stationary use — reading signs, books, menus, labels.

**What stops when reading mode activates:**
- YOLO object detection
- Moondream scene description
- All navigation audio announcements

**What runs during reading mode:**
- EasyOCR scans text in camera view
- Piper TTS reads extracted text aloud
- Vosk keeps listening for "Hey Pi stop reading"

**Returning to navigation:**
- User says "Hey Pi stop reading"
- Reading mode deactivates
- Navigation mode resumes automatically

---

### Always Running (Both Modes)

These components never stop regardless of active mode:

- **Vosk** — offline speech recognition, listens for all voice commands
- **Piper TTS** — converts text to human quality speech
- **Bluetooth Audio** — streams all audio to earphones
- **Ultrasonic Sensor** — continuously measures distance at 20Hz

---

## Voice Commands

| Command | Action |
|---|---|
| "Hey Pi read this" | Switch to reading mode |
| "Hey Pi stop reading" | Return to navigation mode |
| "Hey Pi describe" | Immediate scene description |
| "Hey Pi where am I" | Moondream describes current location |
| "Hey Pi help" | Lists all available commands |

---

## Urgency Levels

| Level | Condition | Audio Example |
|---|---|---|
| Nearby | Object far in frame | "Person nearby on your left" |
| Ahead | Object at medium distance | "Person ahead in front of you" |
| Warning | Object very close | "Warning! Person very close in front of you" |

---

## Direction Detection

| Position in Frame | Announced As |
|---|---|
| Left third of frame | "on your left" |
| Center third of frame | "in front of you" |
| Right third of frame | "on your right" |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Object Detection | Ultralytics YOLO11n + YOLO11s |
| Model Format | ONNX Runtime (ARM optimized) |
| Scene Description | Moondream2 |
| Text Reading | EasyOCR |
| Speech Recognition | Vosk (fully offline) |
| Text to Speech | Piper TTS (neural, human quality) |
| Camera Interface | Picamera2 + libcamera |
| Distance Sensing | HC-SR04 via RPi.GPIO |
| Audio Output | PulseAudio + Bluetooth |
| Language | Python 3.13 |
| OS | Raspberry Pi OS Bookworm 64-bit |

---

## Performance

| Component | Speed |
|---|---|
| yolo11n ONNX (320x320) | 15-16 FPS |
| yolo11s ONNX (320x320) | 8-10 FPS |
| Dual model pipeline | 12-13 FPS |
| Piper TTS response | under 200ms |
| Ultrasonic refresh rate | 20Hz |
| Moondream2 description | 3-5 seconds |

---

## Development Phases

### Phase 1 — Complete ✅
- YOLO11n object detection at 15-16 FPS
- ONNX runtime optimization
- Piper TTS human quality voice
- Direction detection (left / center / right)
- Urgency system (nearby / ahead / warning)
- Dual YOLO pipeline (yolo11n + yolo11s)
- Speech queue (no overlapping audio)
- 5 second cooldown per object

### Phase 2 — In Progress 🔄
- Vosk offline voice recognition
- Voice command system
- EasyOCR text reading
- Mode manager (navigation vs reading)

### Phase 3 — Planned 📋
- Moondream2 scene description
- Smart delay logic
- "Hey Pi describe" command
- "Hey Pi where am I" command

### Phase 4 — Hardware 🔧
- HC-SR04 ultrasonic sensor wiring guide
- GPIO button backup trigger
- Auto start on boot via systemd
- Glasses frame assembly guide

### Phase 5 — Polish 🎯
- Fine tune all cooldowns and thresholds
- Battery life optimization
- Complete documentation
- Final GitHub release

---

## Why VisionAssist?

| Feature | VisionAssist | Competitors |
|---|---|---|
| Cost | ~$120 | $2,000 - $5,000 |
| Internet required | No | Often yes |
| Works in darkness | Yes (ultrasonic) | Limited |
| Open source | Yes | No |
| Custom voice commands | Yes | Limited |
| Scene description | Yes | Rare |
| Text reading | Yes | Some |
| Wearable | Yes | Varies |
| Offline speech recognition | Yes | Rarely |

---

## Project Repository

GitHub: https://github.com/AleyJan/yolo-object-detection

---

## Developer

Built with love for visually impaired communities worldwide.
Especially designed for affordability in developing countries
where expensive assistive technology is out of reach.

---

> *VisionAssist — See the world through sound.*