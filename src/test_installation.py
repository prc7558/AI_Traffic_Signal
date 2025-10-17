"""
Test script to verify YOLOv8 and OpenCV installation
Run this first to make sure everything is installed correctly
"""

import cv2
from ultralytics import YOLO

print("✓ OpenCV version:", cv2.__version__)
print("✓ YOLOv8 imported successfully")

# Download a pre-trained model (this will download on first run)
model = YOLO('yolov8n.pt')  # 'n' stands for nano - smallest and fastest
print("✓ YOLOv8 model loaded successfully")
print("\nAll installations working! You're ready to proceed.")
