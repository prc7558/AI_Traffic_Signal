"""
Shared State Manager
Synchronizes state between web dashboard and Arduino controller
"""

import json
import os
import time
from threading import Lock
from pathlib import Path

class SharedStateManager:
    def __init__(self, state_file="traffic_state.json"):
        """Initialize shared state manager"""
        self.state_file = Path(__file__).parent / state_file
        self.lock = Lock()
        
        # Initialize default state
        self.default_state = {
            'vehicle_count': 0,
            'density': 'LOW',
            'signal_state': 'RED',
            'green_time': 10,
            'last_update': time.time(),
            'time_remaining': 2,
            'cycle_count': 0,
            'total_runtime': 0
        }
        
        # Create state file if it doesn't exist
        if not self.state_file.exists():
            self._write_state(self.default_state)
    
    def _read_state(self):
        """Read state from file"""
        try:
            with self.lock:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading state: {e}")
            return self.default_state.copy()
    
    def _write_state(self, state):
        """Write state to file"""
        try:
            with self.lock:
                with open(self.state_file, 'w') as f:
                    json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error writing state: {e}")
    
    def get_state(self):
        """Get current state"""
        return self._read_state()
    
    def update_state(self, **kwargs):
        """Update specific state fields"""
        state = self._read_state()
        state.update(kwargs)
        state['last_update'] = time.time()
        self._write_state(state)
        return state
    
    def reset_state(self):
        """Reset to default state"""
        self._write_state(self.default_state.copy())
    
    def is_stale(self, max_age_seconds=5):
        """Check if state is stale (not updated recently)"""
        state = self._read_state()
        age = time.time() - state.get('last_update', 0)
        return age > max_age_seconds

# Singleton instance
_state_manager = None

def get_state_manager():
    """Get or create shared state manager instance"""
    global _state_manager
    if _state_manager is None:
        _state_manager = SharedStateManager()
    return _state_manager
