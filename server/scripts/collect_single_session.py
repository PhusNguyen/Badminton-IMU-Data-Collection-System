"""
Single session data collection with real-time visualization
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from udp_receiver import UDPDataReceiver
from realtime_visualizer import RealtimeVisualizer
from json_storage import JSONStorage
import yaml

def main():
    """Main function for single session data collection"""
    
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'server_config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize components
    receiver = UDPDataReceiver(
        host=config['udp']['host'], 
        port=config['udp']['port'],
        buffer_size=config['udp']['buffer_size']
    )
    
    visualizer = RealtimeVisualizer(
        window_size=config['visualization']['window_size'],
        update_interval=config['visualization']['update_interval_ms']
    )
    
    storage = JSONStorage(
        output_dir=config['storage']['raw_sessions_dir']
    )
    
    try:
        print("Starting data collection...")
        print("Press Ctrl+C to stop and save data")
        
        # Start real-time collection and visualization
        receiver.start_collection(visualizer=visualizer)

    except (KeyboardInterrupt, Exception) as e:
        # Stop collection
        receiver.stop_collection()
        print("Stopping data collection...")
        
        # Save data
        file_name = input("Enter file name for this session: ")
        storage.save_session(file_name, receiver.get_collected_data())
        
        print(f"Data saved as {file_name}.json")

    finally:
        # Close socket
        receiver.close()
        

if __name__ == "__main__":
    main()