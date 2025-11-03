#!/bin/bash
# Automated Setup Script for Traffic Signal AI Project
# Run this file to automatically set up everything

echo "============================================================"
echo "   AI-BASED TRAFFIC SIGNAL CONTROLLER"
echo "   Automated Setup Script"
echo "============================================================"
echo ""

echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi
python3 --version
echo "Python found!"
echo ""

echo "[2/5] Creating virtual environment (recommended)..."
python3 -m venv traffic_env
echo "Virtual environment created!"
echo ""

echo "[3/5] Activating virtual environment..."
source traffic_env/bin/activate
echo "Virtual environment activated!"
echo ""

echo "[4/5] Installing required packages..."
echo "This may take 2-5 minutes..."
pip install --upgrade pip
pip install -r requirements.txt
echo ""

echo "[5/5] Testing installation..."
cd src
python test_installation.py
cd ..
echo ""

echo "============================================================"
echo "   SETUP COMPLETE!"
echo "============================================================"
echo ""
echo "Next Steps:"
echo "1. Place a traffic video in the 'videos' folder"
echo "2. Connect Arduino and upload 'arduino/traffic_light.ino'"
echo "3. Update port in src/main.py if needed (e.g., /dev/ttyUSB0)"
echo "4. Run: python src/main.py"
echo ""
echo "For detailed instructions, read: docs/QUICK_START_GUIDE.md"
echo ""
echo "To activate virtual environment later, run:"
echo "   source traffic_env/bin/activate"
echo ""
