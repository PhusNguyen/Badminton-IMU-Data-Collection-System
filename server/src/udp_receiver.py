"""
UDP data receiver for ESP32 IMU sensor data
"""

import socket
import struct
from typing import Dict, List, Optional, Callable
import threading
import time

class UDPDataReceiver:
    """UDP receiver for real-time IMU data from ESP32"""

    def __init__(self, host: str = '0.0.0.0', port: int = 44444, buffer_size: int = 1024):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.socket = None
        self.is_running = False

        # Thread safety
        self.data_lock = threading.Lock()
        self.collection_thread = None

        # Data storage
        self.collected_data = {
            "Ax": [],
            "Ay": [],
            "Az": [],
            "Gx": [],
            "Gy": [],
            "Gz": [],
            "frame": []
        }

        self.frame_counter = 0

    def setup_socket(self):
        """Initialize UDP socket"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"UDP server listening on {self.host}:{self.port}")

    def parse_udp_packet(self, message: bytes) -> List[Dict]:
        """Parse UDP packet containing IMU data"""
        # Conver from ASCII to HEX
        message_hex = message.hex()
        parsed_data = []

        b = 0 # byte position counter

        for i in range(10):
            # Each packet is 48 hex characters (24 bytes)
            if b + 48 > len(message_hex):
                break
        
            # Extract 8-byte hex values for each sensor reading
            Ax_hex = message_hex[b:b+8]; b += 8
            Ay_hex = message_hex[b:b+8]; b += 8
            Az_hex = message_hex[b:b+8]; b += 8
            Gx_hex = message_hex[b:b+8]; b += 8
            Gy_hex = message_hex[b:b+8]; b += 8
            Gz_hex = message_hex[b:b+8]; b += 8

            try:
                # Convert hex to float
                Ax = struct.unpack('!f', bytes.fromhex(Ax_hex))[0]
                Ay = struct.unpack('!f', bytes.fromhex(Ay_hex))[0]
                Az = struct.unpack('!f', bytes.fromhex(Az_hex))[0]
                Gx = struct.unpack('!f', bytes.fromhex(Gx_hex))[0]
                Gy = struct.unpack('!f', bytes.fromhex(Gy_hex))[0]
                Gz = struct.unpack('!f', bytes.fromhex(Gz_hex))[0]

                parsed_data.append({
                    "Ax": Ax,
                    "Ay": Ay,
                    "Az": Az,
                    "Gx": Gx,
                    "Gy": Gy,
                    "Gz": Gz,
                    "frame": self.frame_counter
                })

                self.frame_counter += 1

            except (ValueError, struct.error) as e:
                print(f"Error parsing data packet {i}: {e}")
                continue

        return parsed_data
    
    def _collection_worker(self):
        """Worker method that runs in a separate thread for data collection"""
        if not self.socket:
            self.setup_socket()

        print("Starting data collection thread...")

        while self.is_running:
            try:
                # Receive UDP message
                message, address = self.socket.recvfrom(self.buffer_size)
                
                # Parse the message
                parsed_packets = self.parse_udp_packet(message)
                
                # Store data (thread-safe)
                with self.data_lock:
                    for packet in parsed_packets:
                        self.collected_data['Ax'].append(packet['Ax'])
                        self.collected_data['Ay'].append(packet['Ay'])
                        self.collected_data['Az'].append(packet['Az'])
                        self.collected_data['Gx'].append(packet['Gx'])
                        self.collected_data['Gy'].append(packet['Gy'])
                        self.collected_data['Gz'].append(packet['Gz'])
                        self.collected_data['frame'].append(packet['frame'])
                        
            except socket.error as e:
                if self.is_running:  # Only print error if we're supposed to be running
                    print(f"Socket error: {e}")
                break
            except Exception as e:
                print(f"Unexpected error in collection thread: {e}")
                break
    
    def start_collection(self, visualizer=None, storage=None):
        """Start collecting data with optional real-time visualization"""
        self.is_running = True

        # Start UDP collection in separate thread
        self.collection_thread = threading.Thread(target=self._collection_worker, daemon=True)
        self.collection_thread.start()
        
        # Start visualization in main thread (if provided)
        if visualizer:
            # Pass the data callback to visualizer
            visualizer.start_visualization(self.get_collected_data)
        else:
            # If no visualizer, just keep the main thread alive
            # try:
            while self.is_running:
                time.sleep(0.1)
    
    def get_collected_data(self) -> Dict:
        """Get all collected data (thread-safe)"""
        with self.data_lock:
            return {
                'Ax': self.collected_data['Ax'].copy(),
                'Ay': self.collected_data['Ay'].copy(),
                'Az': self.collected_data['Az'].copy(),
                'Gx': self.collected_data['Gx'].copy(),
                'Gy': self.collected_data['Gy'].copy(),
                'Gz': self.collected_data['Gz'].copy(),
                'frame': self.collected_data['frame'].copy()
            }
    
    def get_data_length(self) -> int:
        """Get current number of data points (thread-safe)"""
        with self.data_lock:
            return len(self.collected_data['frame'])
    
    def stop_collection(self):
        """Stop data collection"""
        self.is_running = False
        
        # Wait for thread to finish
        if self.collection_thread and self.collection_thread.is_alive():
            self.collection_thread.join(timeout=2.0)
    
    def close(self):
        """Close the socket"""
        if self.socket:
            self.socket.close()
            print("UDP socket closed")
                