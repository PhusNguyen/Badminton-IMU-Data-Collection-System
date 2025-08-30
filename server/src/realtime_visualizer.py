"""
Real-time visualization for IMU sensor data
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for better threading support
from matplotlib.animation import FuncAnimation
import numpy as np
from typing import Dict, List, Callable, Optional

class RealtimeVisualizer:
    """Real-time matplotlib visualization for IMU data"""
    
    def __init__(self, window_size: int = 1000, update_interval: int = 10):
        self.window_size = window_size
        self.update_interval = update_interval  # milliseconds between updates
        self.data_callback: Optional[Callable] = None
        
        # Animation object
        self.animation = None
        
        self.setup_plot()
        
    def setup_plot(self):
        """Initialize the matplotlib figure and axes"""
        # Set up the plot with dark theme
        plt.style.use('dark_background')
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        self.fig.suptitle('Real-time IMU Data', fontsize=16)
        
        # Initialize empty line objects
        # Accelerometer plot
        self.line_ax, = self.ax1.plot([], [], label='Ax')
        self.line_ay, = self.ax1.plot([], [], label='Ay')
        self.line_az, = self.ax1.plot([], [], label='Az')
        
        self.ax1.set_title('Accelerometer Data (m/s²)')
        self.ax1.set_xlabel('Sample')
        self.ax1.set_ylabel('Acceleration')
        self.ax1.legend()
        
        # Gyroscope plot
        self.line_gx, = self.ax2.plot([], [], label='Gx')
        self.line_gy, = self.ax2.plot([], [], label='Gy')
        self.line_gz, = self.ax2.plot([], [], label='Gz')
        
        self.ax2.set_title('Gyroscope Data (rad/s)')
        self.ax2.set_xlabel('Sample')
        self.ax2.set_ylabel('Angular Velocity')
        self.ax2.legend()
        
        # Set initial axis limits
        # self.ax1.set_xlim(0, self.window_size)
        # self.ax2.set_xlim(0, self.window_size)
        
        plt.tight_layout()
    
    def animate(self):
        """Animation function called by FuncAnimation"""
        if not self.data_callback:
            return (self.line_ax, self.line_ay, self.line_az,
                    self.line_gx, self.line_gy, self.line_gz)
        
        try:
            # Get current data from callback
            data = self.data_callback()
            
            if not data or len(data['frame']) == 0:
                return (self.line_ax, self.line_ay, self.line_az,
                        self.line_gx, self.line_gy, self.line_gz)
            
            # Get the most recent data points (window_size worth)
            data_length = len(data['frame'])
            
            if data_length > self.window_size:
                # Take the most recent window_size points
                start_idx = data_length - self.window_size
                x_data = list(range(self.window_size))
                acc_x = data['Ax'][start_idx:]
                acc_y = data['Ay'][start_idx:]
                acc_z = data['Az'][start_idx:]
                gy_x = data['Gx'][start_idx:]
                gy_y = data['Gy'][start_idx:]
                gy_z = data['Gz'][start_idx:]
            else:
                # Use all available data
                x_data = list(range(data_length))
                acc_x = data['Ax']
                acc_y = data['Ay']
                acc_z = data['Az']
                gy_x = data['Gx']
                gy_y = data['Gy']
                gy_z = data['Gz']
            
            # Update line data
            self.line_ax.set_data(x_data, acc_x)
            self.line_ay.set_data(x_data, acc_y)
            self.line_az.set_data(x_data, acc_z)
            self.line_gx.set_data(x_data, gy_x)
            self.line_gy.set_data(x_data, gy_y)
            self.line_gz.set_data(x_data, gy_z)
            
            # Auto-scale y-axes based on current data
            if len(acc_x) > 0:
                acc_data = acc_x + acc_y + acc_z
                acc_min, acc_max = min(acc_data), max(acc_data)
                acc_range = acc_max - acc_min
                if acc_range > 0:
                    self.ax1.set_ylim(acc_min - 0.1 * acc_range, acc_max + 0.1 * acc_range)
                
                gy_data = gy_x + gy_y + gy_z
                gy_min, gy_max = min(gy_data), max(gy_data)
                gy_range = gy_max - gy_min
                if gy_range > 0:
                    self.ax2.set_ylim(gy_min - 0.1 * gy_range, gy_max + 0.1 * gy_range)
            
            # Update x-axis to show current window
            if data_length > self.window_size:
                self.ax1.set_xlim(0, self.window_size)
                self.ax2.set_xlim(0, self.window_size)
            else:
                self.ax1.set_xlim(0, max(50, data_length))
                self.ax2.set_xlim(0, max(50, data_length))
            
        except Exception as e:
            print(f"Error in animation update: {e}")
        
        return (self.line_ax, self.line_ay, self.line_az,
                self.line_gx, self.line_gy, self.line_gz)
    
    def start_visualization(self, data_callback: Callable[[], Dict]):
        """Start the real-time visualization (runs in main thread)"""
        self.data_callback = data_callback
        
        print("Starting real-time visualization...")
        print("Close the plot window or press Ctrl+C to stop")
        
        # Create animation - this runs in the main thread
        self.animation = FuncAnimation(
            self.fig, 
            self.animate, 
            interval=self.update_interval,
            blit=False,
            cache_frame_data=False
        )
        
        # Show the plot - this blocks until window is closed or Ctrl+C
        try:
            plt.show()
        finally:
            if self.animation:
                self.animation.event_source.stop()
    
    def stop_visualization(self):
        """Stop the visualization"""
        if self.animation:
            self.animation.event_source.stop()
        plt.close('all')
