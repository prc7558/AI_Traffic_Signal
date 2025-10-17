# AI-Based Traffic Signal Controller

An intelligent traffic management system that uses YOLOv8 for vehicle detection and dynamically adjusts traffic signal timing based on real-time traffic density.

## 🚀 Features

- **Real-time Vehicle Detection** using YOLOv8
- **Dynamic Signal Timing** based on traffic density
- **Arduino LED Control** for physical traffic lights
- **Live Dashboard** showing traffic statistics
- **Density Classification** (LOW, MEDIUM, HIGH)

## 📁 Project Structure

```
traffic_signal_ai/
├── src/                          # Python source code
│   ├── test_installation.py      # Test if setup is correct
│   ├── vehicle_detector.py       # YOLOv8 vehicle detection
│   ├── traffic_density_analyzer.py  # Density classification
│   ├── traffic_signal_controller.py # Signal timing logic
│   ├── arduino_controller.py     # Arduino communication
│   └── main.py                   # Main integration script
├── arduino/                      # Arduino code
│   └── traffic_light.ino         # LED control sketch
├── dashboard/                    # Web dashboard
│   ├── app.py                    # Flask server
│   └── templates/
│       └── index.html            # Dashboard UI
├── videos/                       # Place your traffic videos here
├── docs/                         # Documentation
└── requirements.txt              # Python dependencies
```

## 🛠️ Installation

### Step 1: Install Python Packages

```bash
pip install -r requirements.txt
```

### Step 2: Test Installation

```bash
cd src
python test_installation.py
```

### Step 3: Setup Arduino

1. Open `arduino/traffic_light.ino` in Arduino IDE
2. Connect LEDs:
   - Red LED → Pin 13 → 220Ω resistor → Ground
   - Yellow LED → Pin 12 → 220Ω resistor → Ground
   - Green LED → Pin 11 → 220Ω resistor → Ground
3. Upload the sketch to Arduino
4. Note the COM port (e.g., COM3)

## 🎯 Usage

### Option 1: Run Complete System

```bash
cd src
python main.py
```

This runs vehicle detection + signal control + Arduino LEDs together.

### Option 2: Run Dashboard

```bash
cd dashboard
python app.py
```

Then open http://localhost:5000 in your browser.

### Option 3: Test Individual Components

**Test Vehicle Detection:**
```bash
cd src
python vehicle_detector.py
```

**Test Density Analyzer:**
```bash
python traffic_density_analyzer.py
```

**Test Arduino Connection:**
```bash
python arduino_controller.py
```

## 📹 Adding Your Video

1. Place your traffic video in the `videos/` folder
2. Name it `traffic_video.mp4` OR
3. Update the video path in the scripts

## ⚙️ Configuration

### Adjust Density Thresholds

Edit `traffic_density_analyzer.py`:
```python
self.low_threshold = 5      # Vehicles for LOW density
self.medium_threshold = 15  # Vehicles for MEDIUM density
```

### Adjust Signal Timings

Edit `traffic_signal_controller.py`:
```python
timings = {
    "LOW": 10,      # 10 seconds green for low traffic
    "MEDIUM": 20,   # 20 seconds for medium
    "HIGH": 30      # 30 seconds for high
}
```

### Change Arduino Port

Edit the port in scripts:
```python
ARDUINO_PORT = "COM3"  # Windows
# OR
ARDUINO_PORT = "/dev/ttyUSB0"  # Linux
```

## 🔧 Troubleshooting

### Video not opening?
- Check video path is correct
- Try different video formats (MP4, AVI)
- Place video in `videos/` folder

### Arduino not connecting?
- Check USB cable connection
- Verify correct COM port
- Install Arduino drivers if needed
- Make sure Arduino IDE can connect first

### YOLOv8 slow?
- Use `yolov8n.pt` (nano) for speed
- Reduce video resolution
- Skip frames if needed

### Import errors?
- Make sure you're in the correct directory
- Check all packages installed: `pip list`
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

## 📊 How It Works

1. **Video Input** → Reads traffic video frame by frame
2. **Vehicle Detection** → YOLOv8 detects cars, buses, trucks, motorcycles
3. **Count Vehicles** → Counts detected vehicles in each frame
4. **Classify Density** → LOW (0-5), MEDIUM (6-15), HIGH (16+)
5. **Calculate Timing** → Longer green time for higher density
6. **Control Signal** → Updates Arduino LED lights
7. **Display Dashboard** → Shows real-time statistics

## 🎓 For Beginners

This project is designed to be beginner-friendly:
- Comments explain each section
- Modular code structure
- Step-by-step testing
- Easy to modify and extend

## 📝 Next Steps

- Add multiple lane support
- Implement emergency vehicle detection
- Save statistics to database
- Add SMS/email alerts
- Create mobile app

## 🤝 Contributing

Feel free to modify and improve this project!


## 👨‍💻 Author

Created as a learning project for AI-based traffic management
