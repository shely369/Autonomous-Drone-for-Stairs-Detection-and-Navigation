import serial
import threading
import json
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

class ArduinoCommunication:
    def __init__(self, port='COM3', baudrate=9600):
        self.serial = serial.Serial(port, baudrate, timeout=1)
        self.data_callback = None
        self.stop_thread = threading.Event()
        self.thread = threading.Thread(target=self.read_from_serial, daemon=True)
        self.thread.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def read_from_serial(self):
        while not self.stop_thread.is_set():
            try:
                line = self.serial.readline().decode('utf-8').strip()
                if line:
                    data = json.loads(line)
                    if self.data_callback:
                        self.data_callback(data)
            except json.JSONDecodeError:
                print("Invalid JSON:", line)
            except Exception as e:
                print("Error:", e)

    def close(self):
        self.stop_thread.set()
        self.thread.join()
        self.serial.close()

class SensorDataPlot:
    def __init__(self, maxlen=300):
        self.time_data = deque(maxlen=maxlen)
        self.sensor1_data = deque(maxlen=maxlen)
        self.sensor2_data = deque(maxlen=maxlen)
        self.x_position_data = deque(maxlen=maxlen)
        self.y_position_data = deque(maxlen=maxlen)

        self.start_time = time.time()
        self.last_time = self.start_time
        self.x_position = 0  # cm
        self.y_position = 0  # cm

        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 10))
        self.line1, = self.ax1.plot([], [], 'r-', label='Front Sensor')
        self.line2, = self.ax1.plot([], [], 'b-', label='Bottom Sensor')
        self.xy_line, = self.ax2.plot([], [], 'go-', label='Sensor1 vs Sensor2')
        self.xpos_line, = self.ax3.plot([], [], 'k-', label='X Position')
        self.ypos_line, = self.ax3.plot([], [], 'm-', label='Y Position')

        # Set axis limits to prevent flickering
        self.ax1.set_xlim(0, 50)
        self.ax1.set_ylim(0, 60)
        self.ax2.set_xlim(0, 60)
        self.ax2.set_ylim(0, 60)
        self.ax3.set_xlim(0, 50)
        self.ax3.set_ylim(0, 200)  # adjust if needed

        # Titles and labels
        self.ax1.set_title("Sensor Distances Over Time")
        self.ax1.set_xlabel("Time [s]")
        self.ax1.set_ylabel("Distance [cm]")
        self.ax1.legend(loc='upper right')
        self.ax1.grid()

        self.ax2.set_title("Sensor1 vs Sensor2")
        self.ax2.set_xlabel("Sensor1 (Front) [cm]")
        self.ax2.set_ylabel("Sensor2 (Bottom) [cm]")
        self.ax2.legend(loc='upper right')
        self.ax2.grid()

        self.ax3.set_title("Position Over Time")
        self.ax3.set_xlabel("Time [s]")
        self.ax3.set_ylabel("Position [cm]")
        self.ax3.legend(loc='upper left')
        self.ax3.grid()

        self.ani = None

    def handle_data(self, data):
        current_time = time.time()
        t = current_time - self.start_time
        delta_t = current_time - self.last_time
        self.last_time = current_time

        s1 = data.get('sensor1', 0)  # front
        s2 = data.get('sensor2', 0)  # bottom

        if not (0 < s1 <= 60) or not (0 < s2 <= 60):
            print(f"[{t:.2f}s] ❌ Skipping invalid reading: s1={s1}, s2={s2}")
            return

        # Update positions
        if s1 > 10:
            self.x_position += 3 * delta_t  # cm
        if s2 > 10:
            self.y_position += 3 * delta_t  # cm

        # Store data
        self.time_data.append(t)
        self.sensor1_data.append(s1)
        self.sensor2_data.append(s2)
        self.x_position_data.append(self.x_position)
        self.y_position_data.append(self.y_position)

        print(f"[{t:.2f}s] ✅ Front: {s1:.1f} cm | Bottom: {s2:.1f} cm | X = {self.x_position:.1f} cm | Y = {self.y_position:.1f} cm")

    def update_plot(self, frame):
        self.line1.set_data(self.time_data, self.sensor1_data)
        self.line2.set_data(self.time_data, self.sensor2_data)
        self.xy_line.set_data(self.sensor1_data, self.sensor2_data)
        self.xpos_line.set_data(self.time_data, self.x_position_data)
        self.ypos_line.set_data(self.time_data, self.y_position_data)

        return self.line1, self.line2, self.xy_line, self.xpos_line, self.ypos_line

    def plot(self):
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=200, blit=False)
        plt.tight_layout()
        plt.show()

def main():
    plotter = SensorDataPlot()
    try:
        with ArduinoCommunication(port='COM3') as arduino:
            arduino.data_callback = plotter.handle_data
            plotter.plot()
    except Exception as e:
        print("Failed to run:", e)

if __name__ == '__main__':
    main()
