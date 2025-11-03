"""
Traffic Signal Controller
Manages traffic light timing based on vehicle density
"""

import time

class TrafficSignalController:
    def __init__(self):
        # Signal states
        self.states = ["RED", "YELLOW", "GREEN"]
        self.current_state = "RED"
        self.current_index = 0
        
        # Fixed timings (NEW: 10-30-3 cycle)
        self.yellow_time = 3   # Yellow always 3 seconds
        self.red_time = 10     # Red is now 10 seconds
        self.green_time = 30   # Green is now 30 seconds (constant)
        
    def get_signal_timing(self, density, has_vehicles=True):
        """
        Calculate timing for each signal phase
        NEW: Fixed 10-30-3 cycle, stays RED if no vehicles
        Returns: dictionary with timing for each state
        """
        # If no vehicles detected, stay RED indefinitely
        if not has_vehicles:
            return {
                "RED": 999999,  # Stay red indefinitely
                "GREEN": 0,
                "YELLOW": 0
            }
        
        # Fixed timing: 10 RED -> 30 GREEN -> 3 YELLOW
        return {
            "RED": self.red_time,      # 10 seconds
            "GREEN": self.green_time,  # 30 seconds
            "YELLOW": self.yellow_time # 3 seconds
        }
    
    def get_next_state(self):
        """
        Get the next signal state in cycle
        RED -> GREEN -> YELLOW -> RED
        """
        cycle = ["RED", "GREEN", "YELLOW"]
        self.current_index = (self.current_index + 1) % len(cycle)
        self.current_state = cycle[self.current_index]
        return self.current_state
    
    def get_led_pins(self, state):
        """
        Map signal state to LED pin states
        Returns: (red_state, yellow_state, green_state) as 0 or 1
        """
        led_mapping = {
            "RED": (1, 0, 0),
            "YELLOW": (0, 1, 0),
            "GREEN": (0, 0, 1)
        }
        return led_mapping.get(state, (0, 0, 0))

# Example usage
if __name__ == "__main__":
    controller = TrafficSignalController()
    
    # Test with different densities
    densities = ["LOW", "MEDIUM", "HIGH"]
    
    for density in densities:
        timing = controller.get_signal_timing(density)
        print(f"\n{density} Density Traffic:")
        print(f"  Green Time: {timing['GREEN']} seconds")
        print(f"  Yellow Time: {timing['YELLOW']} seconds")
        print(f"  Red Time: {timing['RED']} seconds")
    
    # Test signal cycle
    print("\n\nSignal Cycle Test:")
    for i in range(6):
        state = controller.get_next_state()
        leds = controller.get_led_pins(state)
        print(f"State {i+1}: {state} -> LEDs (R,Y,G): {leds}")
