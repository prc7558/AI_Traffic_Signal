"""
Main Integration Script
Combines vehicle detection, density analysis, and signal control
"""

import cv2
import time
from vehicle_detector import VehicleDetector
from traffic_density_analyzer import TrafficDensityAnalyzer
from traffic_signal_controller import TrafficSignalController
from arduino_controller import ArduinoController

class TrafficManagementSystem:
    def __init__(self, video_path, arduino_port='COM3'):
        """
        Initialize the complete traffic management system
        """
        print("Initializing Traffic Management System...")
        
        # Initialize components
        self.detector = VehicleDetector()
        self.analyzer = TrafficDensityAnalyzer()
        self.signal_controller = TrafficSignalController()
        self.arduino = ArduinoController(port=arduino_port)
        
        # Video capture
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise Exception(f"Could not open video: {video_path}")
        
        # System state
        self.current_density = "LOW"
        self.vehicle_count = 0
        self.signal_state = "RED"
        
        print("✓ System initialized successfully!\n")
    
    def process_frame(self):
        """
        Process a single frame: detect vehicles and update display
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Detect vehicles
        self.vehicle_count, annotated_frame = self.detector.detect_vehicles(frame)
        
        # Classify density
        self.current_density = self.analyzer.classify_density(self.vehicle_count)
        density_color = self.analyzer.get_density_color(self.current_density)
        
        # Add information overlay
        cv2.putText(annotated_frame, f"Vehicles: {self.vehicle_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.putText(annotated_frame, f"Density: {self.current_density}", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, density_color, 2)
        
        cv2.putText(annotated_frame, f"Signal: {self.signal_state}", 
                   (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        green_time = self.analyzer.calculate_green_time(self.current_density)
        cv2.putText(annotated_frame, f"Green Time: {green_time}s", 
                   (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return annotated_frame
    
    def update_signal(self, state):
        """
        Update traffic signal state and send to Arduino
        """
        self.signal_state = state
        
        # Map state to Arduino command
        signal_map = {
            "RED": 'R',
            "YELLOW": 'Y',
            "GREEN": 'G'
        }
        
        if state in signal_map:
            self.arduino.send_signal(signal_map[state])
    
    def run_signal_cycle(self):
        """
        Run one complete signal cycle based on current density
        """
        timing = self.signal_controller.get_signal_timing(self.current_density)
        
        # RED signal
        self.update_signal("RED")
        self.run_for_duration(timing["RED"])
        
        # GREEN signal
        self.update_signal("GREEN")
        self.run_for_duration(timing["GREEN"])
        
        # YELLOW signal
        self.update_signal("YELLOW")
        self.run_for_duration(timing["YELLOW"])
    
    def run_for_duration(self, duration):
        """
        Process frames for a specific duration (in seconds)
        """
        start_time = time.time()
        while (time.time() - start_time) < duration:
            frame = self.process_frame()
            if frame is None:
                break
            
            # Add timer to frame
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            cv2.putText(frame, f"Time: {remaining}s", 
                       (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            cv2.imshow('Traffic Management System', frame)
            
            if cv2.waitKey(30) & 0xFF == ord('q'):
                return False
        
        return True
    
    def run(self):
        """
        Main system loop
        """
        print("Starting Traffic Management System...")
        print("Press 'q' to quit\n")
        
        try:
            while self.cap.isOpened():
                # Run one signal cycle
                if not self.run_signal_cycle():
                    break
                
                # Reset video if it ends
                if self.cap.get(cv2.CAP_PROP_POS_FRAMES) >= self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        except KeyboardInterrupt:
            print("\nSystem stopped by user")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """
        Clean up resources
        """
        print("\nCleaning up...")
        self.cap.release()
        cv2.destroyAllWindows()
        self.arduino.close()
        print("✓ Cleanup complete")

# Main execution
if __name__ == "__main__":
    # Configuration
    VIDEO_PATH = "../videos/traffic_video.mp4"
    ARDUINO_PORT = "COM3"  # Change to your Arduino port
    
    try:
        system = TrafficManagementSystem(VIDEO_PATH, ARDUINO_PORT)
        system.run()
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease check:")
        print("  1. Video file exists in 'videos' folder")
        print("  2. Arduino is connected to correct port")
        print("  3. All dependencies are installed")
