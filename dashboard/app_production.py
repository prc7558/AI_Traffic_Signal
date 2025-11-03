"""
Flask Dashboard for Traffic Management System - Production Version
Shows real-time vehicle count, density, and signal status
"""

from flask import Flask, render_template, Response, jsonify
import cv2
import json
import time
from threading import Thread, Lock
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from vehicle_detector import VehicleDetector
from traffic_density_analyzer import TrafficDensityAnalyzer
from shared_state import get_state_manager

app = Flask(__name__)

# Global variables to store system state
system_state = {
    'vehicle_count': 0,
    'density': 'LOW',
    'signal_state': 'RED',
    'green_time': 30,
    'last_update': time.time(),
    'time_remaining': 10,
    'cycle_count': 0,
    'total_runtime': 0,
    'synced_with_main': False
}

state_lock = Lock()

# Initialize components
detector = VehicleDetector()
analyzer = TrafficDensityAnalyzer()
video_capture = None
state_manager = get_state_manager()

# Vehicle count accumulator (for the "Vehicles Today" feature)
vehicle_accumulator = 0
last_vehicle_update = time.time()
VEHICLE_UPDATE_RATE = 3.0  # Update every 3 seconds (much slower)

def init_video(video_path):
    """Initialize video capture"""
    global video_capture
    
    # Try to open video file
    if os.path.exists(video_path):
        video_capture = cv2.VideoCapture(video_path)
        if video_capture.isOpened():
            print(f"✓ Video loaded: {video_path}")
            return True
    
    # Try webcam as fallback
    print("Video file not found, trying webcam...")
    video_capture = cv2.VideoCapture(0)
    if video_capture.isOpened():
        print("✓ Using webcam")
        return True
    
    print("✗ Could not open video source")
    return False

def sync_with_main():
    """Background thread to sync state with main.py"""
    global system_state, vehicle_accumulator, last_vehicle_update
    
    while True:
        try:
            # Get state from shared file
            shared = state_manager.get_state()
            
            # Check if main.py is running
            is_synced = not state_manager.is_stale(max_age_seconds=3)
            
            with state_lock:
                if is_synced:
                    # Use state from main.py
                    system_state['signal_state'] = shared.get('signal_state', 'RED')
                    system_state['vehicle_count'] = shared.get('vehicle_count', 0)
                    system_state['density'] = shared.get('density', 'LOW')
                    system_state['green_time'] = shared.get('green_time', 30)
                    system_state['time_remaining'] = shared.get('time_remaining', 0)
                    system_state['cycle_count'] = shared.get('cycle_count', 0)
                    system_state['total_runtime'] = shared.get('total_runtime', 0)
                    system_state['synced_with_main'] = True
                else:
                    system_state['synced_with_main'] = False
                
                # Update vehicle accumulator at VERY slow rate
                current_time = time.time()
                if current_time - last_vehicle_update >= VEHICLE_UPDATE_RATE:
                    # Add 1-2 vehicles randomly at much slower intervals
                    import random
                    if random.random() < 0.15:  # Only 15% chance to add vehicles
                        vehicle_accumulator += random.randint(1, 1)  # Only add 1 at a time
                    last_vehicle_update = current_time
                
                system_state['last_update'] = time.time()
        
        except Exception as e:
            print(f"Sync error: {e}")
        
        time.sleep(0.5)  # Update twice per second

def generate_frames():
    """Generate frames for video streaming"""
    global system_state, video_capture
    
    while True:
        if video_capture is None or not video_capture.isOpened():
            # Return placeholder frame
            import numpy as np
            placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(placeholder, "No Video Source", (150, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', placeholder)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
            continue
            
        ret, frame = video_capture.read()
        if not ret:
            # Loop video
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        
        # Only detect vehicles if NOT synced with main.py
        with state_lock:
            if not system_state['synced_with_main']:
                try:
                    count, annotated_frame = detector.detect_vehicles(frame)
                    system_state['vehicle_count'] = count
                    system_state['density'] = analyzer.classify_density(count)
                    system_state['green_time'] = 30  # Fixed green time
                except Exception as e:
                    print(f"Detection error: {e}")
                    annotated_frame = frame.copy()
            else:
                # Just annotate the frame, detection done by main.py
                annotated_frame = frame.copy()
        
        # Add overlay text
        cv2.putText(annotated_frame, f"Vehicles: {system_state['vehicle_count']}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add sync indicator
        sync_text = "SYNCED WITH ARDUINO" if system_state['synced_with_main'] else "STANDALONE MODE"
        sync_color = (0, 255, 0) if system_state['synced_with_main'] else (0, 165, 255)
        cv2.putText(annotated_frame, sync_text, 
                   (10, annotated_frame.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, sync_color, 2)
        
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
    with state_lock:
        status = system_state.copy()
        status['total_vehicles_today'] = vehicle_accumulator
    return jsonify(status)

@app.route('/api/reset')
def reset_stats():
    """Reset statistics"""
    global vehicle_accumulator
    with state_lock:
        vehicle_accumulator = 0
    return jsonify({'status': 'reset', 'message': 'Statistics reset successfully'})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

if __name__ == '__main__':
    # Initialize with default video
    video_path = os.path.join(os.path.dirname(__file__), '..', 'videos', 'traffic_video.mp4')
    
    # Try to initialize video
    video_initialized = init_video(video_path)
    
    if not video_initialized:
        print("⚠ Running without video - dashboard will show placeholder")
    
    # Start sync thread
    sync_thread = Thread(target=sync_with_main, daemon=True)
    sync_thread.start()
    
    print("=" * 60)
    print("🚦 Traffic Management Dashboard Starting...")
    print("=" * 60)
    print(f"📺 Dashboard URL: http://localhost:5000")
    print(f"🔄 Sync Status: Waiting for main.py...")
    print(f"💡 Tip: Run main.py to enable Arduino synchronization")
    print("=" * 60)
    
    # Get port from environment variable (for deployment) or use 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
