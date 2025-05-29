import socket
import time
import keyboard
from OpenDJI import OpenDJI

# === Settings ===
DRONE_IP = "192.168.1.35"
SERVER_IP = "0.0.0.0"
SERVER_PORT = 5000

MOVE_VALUE = 0.02
SAFE_DISTANCE_CM = 30
STABILIZATION_TIME = 5

# === Connect to Arduino ===
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

print("Waiting for Arduino connection...")
client_socket, client_address = server_socket.accept()
print(f"Connection established with: {client_address}")

client_file = client_socket.makefile('r')

# === Connect to Drone ===
with OpenDJI(DRONE_IP) as drone:
    print("Connecting to drone...")

    takeoff_time = None

    while True:
        try:
            # === Keyboard control ===

            if keyboard.is_pressed('e'):
                print("Enabling control...")
                drone.enableControl(True)
                time.sleep(1)

            if keyboard.is_pressed('q'):
                print("Disabling control...")
                drone.disableControl(True)
                time.sleep(1)

            if keyboard.is_pressed('f'):
                print("Takeoff...")
                drone.takeoff(True)
                takeoff_time = time.time()
                time.sleep(1)

            if keyboard.is_pressed('r'):
                print("Landing...")
                drone.land(True)
                takeoff_time = None
                time.sleep(1)

            # === Sensor reading from Arduino ===

            line = client_file.readline().strip()
            if line:
                print("Received:", line)
                if "S1=" in line and "S2=" in line:
                    parts = line.split("&")
                    bottom_distance = float(parts[0].replace("S1=", ""))
                    front_distance = float(parts[1].replace("S2=", ""))

                    print(f"Bottom: {bottom_distance:.2f} cm | Front: {front_distance:.2f} cm")

                    rcw, du, lr, bf = 0.0, 0.0, 0.0, 0.0

                    if takeoff_time is not None:
                        elapsed = time.time() - takeoff_time

                        if elapsed >= STABILIZATION_TIME:
                            if bottom_distance < SAFE_DISTANCE_CM:
                                du = MOVE_VALUE
                                print("Obstacle below - moving up")

                            if front_distance < SAFE_DISTANCE_CM:
                                bf = -MOVE_VALUE
                                print("Obstacle ahead - moving back")

                    drone.move(rcw, du, lr, bf, True)

            time.sleep(0.1)

        except KeyboardInterrupt:
            print("Emergency stop (Ctrl+C) - landing...")
            drone.land(True)
            break
