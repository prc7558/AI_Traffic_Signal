"""
Comprehensive System Test Suite
Tests all components of the Traffic Signal AI system
Run this to verify everything is working correctly
"""

import sys
import os
import time

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def print_section(title):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_imports():
    """Test if all required packages are installed"""
    print_section("TEST 1: Package Installation")
    
    packages = {
        'cv2': 'opencv-python',
        'ultralytics': 'ultralytics',
        'serial': 'pyserial',
        'flask': 'flask',
        'numpy': 'numpy'
    }
    
    passed = 0
    failed = 0
    
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✓ {package:20s} - INSTALLED")
            passed += 1
        except ImportError:
            print(f"✗ {package:20s} - NOT FOUND")
            print(f"  Install with: pip install {package}")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0

def test_yolo_model():
    """Test YOLOv8 model loading"""
    print_section("TEST 2: YOLOv8 Model")
    
    try:
        from ultralytics import YOLO
        print("Loading YOLOv8 model...")
        model = YOLO('yolov8n.pt')
        print("✓ Model loaded successfully")
        print(f"  Model type: {type(model)}")
        return True
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        return False

def test_vehicle_detector():
    """Test vehicle detection module"""
    print_section("TEST 3: Vehicle Detector Module")
    
    try:
        from vehicle_detector import VehicleDetector
        import numpy as np
        
        detector = VehicleDetector()
        print("✓ Vehicle detector initialized")
        
        # Create a dummy frame
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        count, annotated = detector.detect_vehicles(dummy_frame)
        
        print(f"✓ Detection test passed")
        print(f"  Detected {count} vehicles in test frame")
        return True
    except Exception as e:
        print(f"✗ Vehicle detector test failed: {e}")
        return False

def test_density_analyzer():
    """Test density analyzer module"""
    print_section("TEST 4: Density Analyzer Module")
    
    try:
        from traffic_density_analyzer import TrafficDensityAnalyzer
        
        analyzer = TrafficDensityAnalyzer()
        print("✓ Density analyzer initialized")
        
        # Test different densities
        test_cases = [
            (3, "LOW"),
            (10, "MEDIUM"),
            (20, "HIGH")
        ]
        
        all_passed = True
        for count, expected in test_cases:
            result = analyzer.classify_density(count)
            if result == expected:
                print(f"✓ Count {count:2d} → {result:6s} (correct)")
            else:
                print(f"✗ Count {count:2d} → {result:6s} (expected {expected})")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"✗ Density analyzer test failed: {e}")
        return False

def test_signal_controller():
    """Test signal controller module"""
    print_section("TEST 5: Signal Controller Module")
    
    try:
        from traffic_signal_controller import TrafficSignalController
        
        controller = TrafficSignalController()
        print("✓ Signal controller initialized")
        
        # Test timing calculation
        densities = ["LOW", "MEDIUM", "HIGH"]
        for density in densities:
            timing = controller.get_signal_timing(density)
            print(f"✓ {density:6s} density → Green time: {timing['GREEN']}s")
        
        # Test state transitions
        print("\nTesting state transitions:")
        for i in range(3):
            state = controller.get_next_state()
            leds = controller.get_led_pins(state)
            print(f"  State {i+1}: {state:6s} → LEDs (R,Y,G): {leds}")
        
        return True
    except Exception as e:
        print(f"✗ Signal controller test failed: {e}")
        return False

def test_arduino_port():
    """Test Arduino connectivity (without actually connecting)"""
    print_section("TEST 6: Arduino Port Check")
    
    try:
        import serial.tools.list_ports
        
        ports = list(serial.tools.list_ports.comports())
        
        if ports:
            print("Available COM ports:")
            for port in ports:
                print(f"  - {port.device}: {port.description}")
            print("\n✓ COM ports found (Arduino may be connected)")
            print("  Update ARDUINO_PORT in code if needed")
            return True
        else:
            print("⚠ No COM ports found")
            print("  Arduino may not be connected")
            print("  This is okay if you don't have Arduino yet")
            return True
    except Exception as e:
        print(f"✗ Port check failed: {e}")
        return False

def test_video_path():
    """Test if video file exists"""
    print_section("TEST 7: Video File Check")
    
    video_dir = os.path.join(os.path.dirname(__file__), '..', 'videos')
    video_path = os.path.join(video_dir, 'traffic_video.mp4')
    
    if os.path.exists(video_path):
        print(f"✓ Video file found: {video_path}")
        
        # Try to open it
        try:
            import cv2
            cap = cv2.VideoCapture(video_path)
            if cap.isOpened():
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                print(f"  Resolution: {width}x{height}")
                print(f"  FPS: {fps}")
                print(f"  Total frames: {frames}")
                cap.release()
                return True
            else:
                print("✗ Could not open video file")
                return False
        except Exception as e:
            print(f"✗ Error opening video: {e}")
            return False
    else:
        print("⚠ Video file not found")
        print(f"  Expected location: {video_path}")
        print("  Please place a traffic video in the 'videos' folder")
        print("  This is okay for testing other components")
        return True

def test_dashboard_files():
    """Test if dashboard files exist"""
    print_section("TEST 8: Dashboard Files Check")
    
    dashboard_dir = os.path.join(os.path.dirname(__file__), '..', 'dashboard')
    app_file = os.path.join(dashboard_dir, 'app.py')
    template_file = os.path.join(dashboard_dir, 'templates', 'index.html')
    
    files_ok = True
    
    if os.path.exists(app_file):
        print("✓ dashboard/app.py found")
    else:
        print("✗ dashboard/app.py not found")
        files_ok = False
    
    if os.path.exists(template_file):
        print("✓ dashboard/templates/index.html found")
    else:
        print("✗ dashboard/templates/index.html not found")
        files_ok = False
    
    return files_ok

def test_project_structure():
    """Test if project structure is correct"""
    print_section("TEST 9: Project Structure")
    
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    required_dirs = [
        'src',
        'arduino',
        'dashboard',
        'videos',
        'docs'
    ]
    
    required_files = [
        'src/vehicle_detector.py',
        'src/traffic_density_analyzer.py',
        'src/traffic_signal_controller.py',
        'src/arduino_controller.py',
        'src/main.py',
        'arduino/traffic_light.ino',
        'README.md',
        'requirements.txt'
    ]
    
    all_ok = True
    
    print("Checking directories:")
    for dir_name in required_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.isdir(dir_path):
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - MISSING")
            all_ok = False
    
    print("\nChecking files:")
    for file_name in required_files:
        file_path = os.path.join(base_dir, file_name)
        if os.path.isfile(file_path):
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} - MISSING")
            all_ok = False
    
    return all_ok

def run_all_tests():
    """Run all tests and provide summary"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  TRAFFIC SIGNAL AI - SYSTEM TEST SUITE".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    tests = [
        ("Package Installation", test_imports),
        ("YOLOv8 Model", test_yolo_model),
        ("Vehicle Detector", test_vehicle_detector),
        ("Density Analyzer", test_density_analyzer),
        ("Signal Controller", test_signal_controller),
        ("Arduino Ports", test_arduino_port),
        ("Video File", test_video_path),
        ("Dashboard Files", test_dashboard_files),
        ("Project Structure", test_project_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test crashed: {e}")
            results.append((test_name, False))
        
        time.sleep(0.5)  # Small delay between tests
    
    # Print summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Tests Run: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"\nSuccess Rate: {(passed/total)*100:.1f}%\n")
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {test_name}")
    
    # Final verdict
    print("\n" + "="*60)
    if passed == total:
        print("  🎉 ALL TESTS PASSED! System is ready to use.")
    elif passed >= total * 0.8:
        print("  ⚠️  MOSTLY WORKING - Some optional components missing")
    else:
        print("  ❌ SETUP INCOMPLETE - Please fix the failed tests")
    print("="*60 + "\n")
    
    # Provide next steps
    if passed < total:
        print("Next Steps:")
        print("1. Fix failed tests by following error messages")
        print("2. Check QUICK_START_GUIDE.md for detailed instructions")
        print("3. Run this test again after fixing issues")
    else:
        print("Next Steps:")
        print("1. Place a traffic video in 'videos/' folder")
        print("2. Connect Arduino and upload traffic_light.ino")
        print("3. Run: python src/main.py")
        print("4. Or run dashboard: python dashboard/app.py")
    
    print("\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        print("Please report this issue")
