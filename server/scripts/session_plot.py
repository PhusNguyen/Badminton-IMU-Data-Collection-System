import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from udp_receiver import UDPDataReceiver
from realtime_visualizer import RealtimeVisualizer
from json_storage import JSONStorage
import json
import matplotlib.pyplot as plt

def main():
    session_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_sessions')
    # List all JSON files in the directory
    json_files = [f for f in os.listdir(session_path) if f.endswith('.json')]
    
    # Choose the JSON file to plot
    input_file = input(f"Enter the JSON file to plot (available: {json_files}): ")
    if input_file not in json_files:
        print("File not found in the specified directory.")
        return
    
    # Access JSON file
    file_path = os.path.join(session_path, input_file)
    print(f"Loading session from: {file_path}")
    with open(file_path, 'r') as f:
        session_data = json.load(f)

    # Plot the data
    plt.subplot(3,2,1); plt.plot(session_data['data']['frame'], session_data['data']['Ax']); plt.title('Ax'); plt.grid()
    plt.subplot(3,2,2); plt.plot(session_data['data']['frame'], session_data['data']['Ay']); plt.title('Ay'); plt.grid()
    plt.subplot(3,2,3); plt.plot(session_data['data']['frame'], session_data['data']['Az']); plt.title('Az'); plt.grid()
    plt.subplot(3,2,4); plt.plot(session_data['data']['frame'], session_data['data']['Gx']); plt.title('Gx'); plt.grid()
    plt.subplot(3,2,5); plt.plot(session_data['data']['frame'], session_data['data']['Gy']); plt.title('Gy'); plt.grid()
    plt.subplot(3,2,6); plt.plot(session_data['data']['frame'], session_data['data']['Gz']); plt.title('Gz'); plt.grid()

    plt.tight_layout()
    plt.suptitle(input_file)

    plt.show()

if __name__ == "__main__":
    main()