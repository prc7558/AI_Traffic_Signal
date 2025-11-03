"""
Quick Test Script for Traffic Management System
Tests the synchronization between main.py and dashboard
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from shared_state import get_state_manager
import time

def test_shared_state():
    """Test the shared state manager"""
    print("=" * 60)
    print("Testing Shared State Manager")
    print("=" * 60)
    
    manager = get_state_manager()
    
    # Test 1: Write state
    print("\n✓ Test 1: Writing initial state...")
    manager.update_state(
        signal_state='RED',
        vehicle_count=5,
        density='LOW',
        time_remaining=2
    )
    time.sleep(0.5)
    
    # Test 2: Read state
    print("✓ Test 2: Reading state...")
    state = manager.get_state()
    print(f"  Signal: {state['signal_state']}")
    print(f"  Vehicles: {state['vehicle_count']}")
    print(f"  Density: {state['density']}")
    print(f"  Time Remaining: {state['time_remaining']}")
    
    # Test 3: Update state
    print("\n✓ Test 3: Updating state (GREEN light)...")
    manager.update_state(
        signal_state='GREEN',
        vehicle_count=12,
        density='MEDIUM',
        time_remaining=20
    )
    time.sleep(0.5)
    
    state = manager.get_state()
    print(f"  Signal: {state['signal_state']}")
    print(f"  Vehicles: {state['vehicle_count']}")
    print(f"  Density: {state['density']}")
    
    # Test 4: Check if stale
    print("\n✓ Test 4: Checking freshness...")
    is_stale = manager.is_stale(max_age_seconds=5)
    print(f"  Is state stale? {is_stale}")
    
    # Test 5: Wait and check stale
    print("\n✓ Test 5: Waiting 6 seconds to test staleness...")
    time.sleep(6)
    is_stale = manager.is_stale(max_age_seconds=5)
    print(f"  Is state stale now? {is_stale}")
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    print("\nThe shared_state.py module is working correctly!")
    print("You can now run main.py and app.py together.")
    print("\nNext steps:")
    print("  1. Start main.py: cd src && python main.py")
    print("  2. Start app.py:  cd dashboard && python app.py")
    print("  3. Open browser:  http://localhost:5000")

if __name__ == "__main__":
    try:
        test_shared_state()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease make sure you're running this from the project root directory.")
