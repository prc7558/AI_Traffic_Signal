"""
Vehicle Detection using YOLOv8
This script detects vehicles in a video and counts them
"""

import cv2
from ultralytics import YOLO
import numpy as np

class VehicleDetector:
    def __init__(self):
        # Load pre-trained YOLOv8 model
        self.model = YOLO('yolov8n.pt')
        
        # Vehicle class IDs in COCO dataset
        # 2: car, 3: motorcycle, 5: bus, 7: truck
        self.vehicle_classes = [2, 3, 5, 7]
        
    def detect_vehicles(self, frame):
        """
        Detect vehicles in a single frame
        Returns: number of vehicles detected and annotated frame
        """
        # Run detection
        results = self.model(frame, verbose=False)
        
        vehicle_count = 0
        
        # Process detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get class ID
                cls_id = int(box.cls[0])
                
                # Check if it's a vehicle
                if cls_id in self.vehicle_classes:
                    vehicle_count += 1
                    
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Add label
                    label = f"{result.names[cls_id]}: {confidence:.2f}"
                    cv2.putText(frame, label, (x1, y1-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return vehicle_count, frame

# Test the detector
if __name__ == "__main__":
    detector = VehicleDetector()
    
    # Test with video file
    video_path = "../videos/traffic_video.mp4"  # Replace with your video path
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file")
        print("Please provide a valid video path or place video in 'videos' folder")
        exit()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect vehicles
        count, annotated_frame = detector.detect_vehicles(frame)
        
        # Display count on frame
        cv2.putText(annotated_frame, f"Vehicles: {count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Show frame
        cv2.imshow('Vehicle Detection', annotated_frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
