"""
Main Integration Script
Combines vehicle detection, density analysis, and signal control
Synchronized with web dashboard via shared state
"""

import cv2
import time
from vehicle_detector import VehicleDetector
from traffic_density_analyzer import TrafficDensityAnalyzer
from traffic_signal_controller import TrafficSignalController
from arduino_controller import ArduinoController
from shared_state import get_state_manager

class TrafficManagementSystem:
    def __init__(self, video_path, arduino_port='COM3', sync_with_dashboard=True):
        """
        Initialize the complete traffic management system
        """
        print("Initializing Traffic Management System...")
        
        # Initialize components
        self.detector = VehicleDetector()
        self.analyzer = TrafficDensityAnalyzer()
        self.signal_controller = TrafficSignalController()
        self.arduino = ArduinoController(port=arduino_port)
        
        # Initialize shared state manager for dashboard sync
        self.sync_with_dashboard = sync_with_dashboard
        if sync_with_dashboard:
            self.state_manager = get_state_manager()
            print("✓ Dashboard synchronization enabled")
        
        # Video capture
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise Exception(f"Could not open video: {video_path}")
        
        # System state
        self.current_density = "LOW"
        self.vehicle_count = 0
        self.signal_state = "RED"
        self.cycle_count = 0
        self.start_time = time.time()
        
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
        
        # Add sync indicator
        if self.sync_with_dashboard:
            cv2.putText(annotated_frame, "SYNCED", 
                       (annotated_frame.shape[1] - 120, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return annotated_frame
    
    def update_signal(self, state, time_remaining=0):
        """
        Update traffic signal state and send to Arduino
        Also updates shared state for dashboard
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
        
        # Update shared state for dashboard sync
        if self.sync_with_dashboard:
            total_runtime = int(time.time() - self.start_time)
            self.state_manager.update_state(
                signal_state=state,
                vehicle_count=self.vehicle_count,
                density=self.current_density,
                green_time=self.analyzer.calculate_green_time(self.current_density),
                time_remaining=time_remaining,
                cycle_count=self.cycle_count,
                total_runtime=total_runtime
            )
    
    def run_signal_cycle(self):
        """
        Run one complete signal cycle based on current density
        NEW: Stays RED if no vehicles detected
        """
        # Check if there are vehicles
        has_vehicles = self.vehicle_count > 0
        
        timing = self.signal_controller.get_signal_timing(
            self.current_density, 
            has_vehicles=has_vehicles
        )
        
        # If no vehicles, stay RED and wait
        if not has_vehicles:
            self.update_signal("RED", 10)
            if not self.run_for_duration(10):  # Check every 10 seconds
                return False
            return True  # Don't increment cycle, just loop
        
        # RED signal (10 seconds)
        self.update_signal("RED", timing["RED"])
        if not self.run_for_duration(timing["RED"]):
            return False
        
        # GREEN signal (30 seconds)
        self.update_signal("GREEN", timing["GREEN"])
        if not self.run_for_duration(timing["GREEN"]):
            return False
        
        # YELLOW signal (3 seconds)
        self.update_signal("YELLOW", timing["YELLOW"])
        if not self.run_for_duration(timing["YELLOW"]):
            return False
        
        # Increment cycle count
        self.cycle_count += 1
        
        return True
    
    def run_for_duration(self, duration):
        """
        Process frames for a specific duration (in seconds)
        Updates time remaining in shared state
        """
        start_time = time.time()
        while (time.time() - start_time) < duration:
            frame = self.process_frame()
            if frame is None:
                break
            
            # Calculate remaining time
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            
            # Update shared state with current time remaining
            if self.sync_with_dashboard:
                total_runtime = int(time.time() - self.start_time)
                self.state_manager.update_state(
                    signal_state=self.signal_state,
                    vehicle_count=self.vehicle_count,
                    density=self.current_density,
                    time_remaining=remaining,
                    cycle_count=self.cycle_count,
                    total_runtime=total_runtime
                )
            
            # Add timer to frame
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
        print("Press 'q' to quit")
        if self.sync_with_dashboard:
            print("Dashboard sync: ENABLED - Check http://localhost:5000\n")
        else:
            print()
        
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
    SYNC_WITH_DASHBOARD = True  # Enable dashboard synchronization
    
    try:
        system = TrafficManagementSystem(
            VIDEO_PATH, 
            ARDUINO_PORT,
            sync_with_dashboard=SYNC_WITH_DASHBOARD
        )
        system.run()
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease check:")
        print("  1. Video file exists in 'videos' folder")
        print("  2. Arduino is connected to correct port")
        print("  3. All dependencies are installed")
        print("  4. Dashboard is running (if sync enabled)")
