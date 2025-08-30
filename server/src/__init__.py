"""
Badminton IMU Data Collection Server

Main package for receiving and processing IMU data from ESP32 sensors.
"""

__version__ = "1.0.0"
__author__ = "Phu Nguyen"
__email__ = "phunguyen190101@gmail.com"

# Import main classes for easy access
from .udp_receiver import UDPDataReceiver
from .realtime_visualizer import RealtimeVisualizer  
from .json_storage import JSONStorage

# Define what gets imported with "from src import *"
__all__ = [
    'UDPDataReceiver',
    'RealtimeVisualizer', 
    'JSONStorage',
]