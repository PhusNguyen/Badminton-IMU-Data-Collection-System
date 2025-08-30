"""
JSON storage ultilities for IMU data sensor
"""
import json
import os
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

class JSONStorage:
    """Handle JSON storage of IMU sensor data"""
    
    def __init__(self, output_dir: str = "data/raw_sessions"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_session(self, filename: str, data: Dict, metadata: Optional[Dict] = None):
        """Save a data collection session to JSON file"""
        
        # Add timestamp and metadata
        session_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_frame": len(data.get('Ax', [])),
                "duration_seconds": len(data.get('Ax', [])) / 100,  # Assuming 100Hz
                "sampling_rate": 100,
                "session_name": filename,
                **(metadata or {})
            },
            "data": data
        }
        
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(session_data, f, indent=4)
            print(f"Session data saved to: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"Error saving session data: {e}")
            return None
    
    def load_session(self, filename: str) -> Optional[Dict]:
        """Load a session from JSON file"""
        filepath = self.output_dir / filename
        
        if not filepath.exists():
            print(f"File not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading session data: {e}")
            return None