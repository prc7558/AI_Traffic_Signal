"""
Traffic Density Classification
Classifies traffic as LOW, MEDIUM, or HIGH based on vehicle count
"""

class TrafficDensityAnalyzer:
    def __init__(self):
        # Define thresholds (adjust based on your needs)
        self.low_threshold = 5      # 0-5 vehicles = LOW
        self.medium_threshold = 15  # 6-15 vehicles = MEDIUM
                                    # 16+ vehicles = HIGH
    
    def classify_density(self, vehicle_count):
        """
        Classify traffic density based on vehicle count
        Returns: density level (LOW, MEDIUM, HIGH)
        """
        if vehicle_count <= self.low_threshold:
            return "LOW"
        elif vehicle_count <= self.medium_threshold:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def get_density_color(self, density):
        """
        Get color code for density visualization
        Returns: BGR color tuple for OpenCV
        """
        colors = {
            "LOW": (0, 255, 0),      # Green
            "MEDIUM": (0, 165, 255),  # Orange
            "HIGH": (0, 0, 255)       # Red
        }
        return colors.get(density, (255, 255, 255))
    
    def calculate_green_time(self, density):
        """
        Calculate green light duration based on traffic density
        Returns: time in seconds
        """
        # Base timings (adjust as needed)
        timings = {
            "LOW": 10,      # 10 seconds for low traffic
            "MEDIUM": 20,   # 20 seconds for medium traffic
            "HIGH": 30      # 30 seconds for high traffic
        }
        return timings.get(density, 15)

# Example usage
if __name__ == "__main__":
    analyzer = TrafficDensityAnalyzer()
    
    # Test different vehicle counts
    test_counts = [3, 8, 20]
    
    for count in test_counts:
        density = analyzer.classify_density(count)
        green_time = analyzer.calculate_green_time(density)
        color = analyzer.get_density_color(density)
        
        print(f"\nVehicle Count: {count}")
        print(f"Density: {density}")
        print(f"Green Light Time: {green_time} seconds")
        print(f"Color (BGR): {color}")
