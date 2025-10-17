"""
Flask Dashboard for Traffic Management System
Shows real-time vehicle count, density, and signal status
"""

from flask import Flask, render_template, Response, jsonify
import cv2
import json
import time
from threading import Thread
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from vehicle_detector import VehicleDetector
from traffic_density_analyzer import TrafficDensityAnalyzer

app = Flask(__name__)

# Global variables to store system state
system_state = {
    'vehicle_count': 0,
    'density': 'LOW',
    'signal_state': 'RED',
    'green_time': 10,
    'last_update': time.time()
}

# Initialize components
detector = VehicleDetector()
analyzer = TrafficDensityAnalyzer()
video_capture = None

def init_video(video_path):
    """Initialize video capture"""
    global video_capture
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video {video_path}")
        return False
    return True

def generate_frames():
    """Generate frames for video streaming"""
    global system_state, video_capture
    
    while True:
        if video_capture is None or not video_capture.isOpened():
            break
            
        ret, frame = video_capture.read()
        if not ret:
            # Loop video
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        # Detect vehicles
        count, annotated_frame = detector.detect_vehicles(frame)
        
        # Update system state
        system_state['vehicle_count'] = count
        system_state['density'] = analyzer.classify_density(count)
        system_state['green_time'] = analyzer.calculate_green_time(system_state['density'])
        system_state['last_update'] = time.time()
        
        # Add overlay text
        cv2.putText(annotated_frame, f"Vehicles: {count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        time.sleep(0.03)  # ~30 FPS

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status')
def get_status():
    """API endpoint for system status"""
    return jsonify(system_state)

if __name__ == '__main__':
    # Initialize with default video
    video_path = '../videos/traffic_video.mp4'
    
    if init_video(video_path):
        print("Dashboard starting at http://localhost:5000")
        app.run(debug=True, threaded=True)
    else:
        print("Please place a video file at:", video_path)
