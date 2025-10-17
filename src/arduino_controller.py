"""
Arduino Communication Module
Sends signal commands to Arduino to control LED lights
"""

import serial
import time

class ArduinoController:
    def __init__(self, port='COM3', baud_rate=9600):
        """
        Initialize Arduino connection
        port: COM port where Arduino is connected (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
        """
        try:
            self.arduino = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f"✓ Connected to Arduino on {port}")
        except Exception as e:
            print(f"✗ Could not connect to Arduino: {e}")
            print("  Make sure Arduino is connected and port is correct")
            self.arduino = None
    
    def send_signal(self, state):
        """
        Send signal state to Arduino
        state: 'R' for RED, 'Y' for YELLOW, 'G' for GREEN
        """
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write(state.encode())
                print(f"Sent '{state}' to Arduino")
                return True
            except Exception as e:
                print(f"Error sending to Arduino: {e}")
                return False
        else:
            print("Arduino not connected")
            return False
    
    def close(self):
        """Close Arduino connection"""
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print("Arduino connection closed")

# Test Arduino connection
if __name__ == "__main__":
    # Change COM3 to your Arduino port
    # On Windows: COM3, COM4, etc.
    # On Linux/Mac: /dev/ttyUSB0, /dev/ttyACM0, etc.
    
    controller = ArduinoController(port='COM3')
    
    if controller.arduino:
        print("\nTesting LED signals...")
        signals = ['R', 'Y', 'G']
        
        for signal in signals * 2:  # Cycle twice
            controller.send_signal(signal)
            time.sleep(2)
        
        controller.close()
    else:
        print("\nCould not test - Arduino not connected")
        print("Please check:")
        print("  1. Arduino is plugged in via USB")
        print("  2. Correct COM port in code")
        print("  3. Arduino has the traffic_light.ino sketch uploaded")
