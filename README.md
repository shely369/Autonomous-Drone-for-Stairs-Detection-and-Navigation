# Drone Obstacle Avoidance System

## Project Overview

This project implements an obstacle avoidance system for DJI drones using Arduino-based ultrasonic sensors. The system detects obstacles in front of and below the drone, and automatically adjusts the drone's flight path to avoid collisions. The project integrates hardware components (Arduino with ultrasonic sensors) with software components (Python scripts) to create a complete obstacle detection and avoidance solution.

## Components

### Hardware
- Arduino board
- 2 Ultrasonic distance sensors (HC-SR04 or similar)
- 2 LEDs (blue and green) for visual feedback
- DJI drone compatible with the DJI Mobile SDK
- Android device for connecting to the drone

### Software
- Arduino code for sensor data collection
- Python scripts for data processing and drone control
- DJI-MSDK-to-PC library for drone communication

## File Structure

### Arduino Files
- `checkconnect.ino`: Tests BLE communication with the drone
- `Sensors.ino`: Main Arduino code for ultrasonic sensors and data transmission

### Python Files
- `SensorDataCollect.py`: Collects and visualizes sensor data from Arduino
- `ExampleControl.py`: Demonstrates basic keyboard control of the drone
- `drone_avoidance.py`: Main obstacle avoidance implementation
- `defultvals.py`: Configures drone default settings

## Setup Instructions

1. **Arduino Setup**
   - Connect the ultrasonic sensors to the Arduino:
     - Bottom sensor: Trigger pin 8, Echo pin 3
     - Front sensor: Trigger pin 11, Echo pin 6
   - Connect the LEDs:
     - Blue LED (bottom sensor indicator): Pin 4
     - Green LED (front sensor indicator): Pin 5
   - Upload the `Sensors.ino` sketch to the Arduino

2. **Python Environment Setup**
   - Install required Python packages:
     ```
     pip install pyserial matplotlib keyboard socket
     ```
   - Install the DJI-MSDK-to-PC library

3. **Drone Connection**
   - Connect the Android device to the drone using the DJI app
   - Note the IP address of the Android device (needed for the Python scripts)
   - Update the IP address in the Python scripts as needed

## Usage

### Data Collection and Visualization
Run `SensorDataCollect.py` to collect and visualize sensor data:
```
python SensorDataCollect.py
```
This will display real-time graphs of sensor readings and estimated position.

### Basic Drone Control
Run `ExampleControl.py` to control the drone using keyboard:
```
python ExampleControl.py
```
- Press F - to takeoff
- Press R - to land
- Press E - to enable keyboard control
- Press Q - to disable keyboard control
- Press X - to exit
- Use W/S, A/D, and arrow keys for movement

### Obstacle Avoidance
Run `drone_avoidance.py` to enable automatic obstacle avoidance:
```
python drone_avoidance.py
```
The drone will automatically:
- Ascend when detecting obstacles below (within 30cm)
- Move backward when detecting obstacles in front (within 30cm)

### Configuring Drone Settings
Run `defultvals.py` to modify drone default settings:
```
python defultvals.py
```
This will set the takeoff altitude to 5 meters and return-to-home altitude to 0.1 meters.

## System Workflow

1. Arduino continuously measures distances using ultrasonic sensors
2. Distance data is sent to the computer via serial communication in JSON format
3. Python scripts process the incoming data and make flight decisions
4. Commands are sent to the drone via the DJI-MSDK-to-PC interface
5. The drone responds to commands, avoiding obstacles as detected

## Notes

- The system requires a stable connection between all components
- Ensure the drone has sufficient battery before testing
- Always have manual override controls ready for safety
- The obstacle avoidance system has a 5-second stabilization period after takeoff
- Sensor readings beyond 60cm are considered invalid and ignored

## Troubleshooting

- If Arduino connection fails, check the COM port in `SensorDataCollect.py`
- If drone connection fails, verify the IP address in the Python scripts
- If sensors give erratic readings, check wiring and power supply
- For BLE connection issues, run `checkconnect.ino` to diagnose
