from OpenDJI import OpenDJI

import keyboard
import time

"""
In this example you can fly the drone with your keyboard!
This example demonstrate how to control the drone using OpenDJI class.

    press F - to takeoff the drone.
    press R - to land the drone.
    press E - to enable control from keyboard (joystick disabled)
    press Q - to disable control from keyboard (joystick enabled)
    press X - to close the problam

    press W/S - to move up/down (ascent)
    press A/D - to rotate left/right (yaw control)
    press ↑/↓ - to move forward/backward (pitch)
    press ←/→ - to move left/right (roll)
"""

# IP address of the connected android device
IP_ADDR = "192.168.1.57"

# Movement factors
MOVE_VALUE = 0.03
ROTATE_VALUE = 0.15


# Connect to the drone
with OpenDJI(IP_ADDR) as drone:

    # Press 'x' to close the program
    print("Press 'x' to close the program")
    while not keyboard.is_pressed('x'):

        # A little delay to not spam the server
        time.sleep(0.1)

        # Core variables
        rcw = 0.0       # Rotate, left horizontal stick
        du = 0.0        # Ascent, left vertical stick
        lr = 0.0        # Side movement, right horizontal stick
        bf = 0.0        # Forward movement, right vertical stick

        # Set core variables based on key presses
        if keyboard.is_pressed('a'): rcw = -ROTATE_VALUE
        if keyboard.is_pressed('d'): rcw =  ROTATE_VALUE
        if keyboard.is_pressed('s'): du  = -MOVE_VALUE
        if keyboard.is_pressed('w'): du  =  MOVE_VALUE

        if keyboard.is_pressed('left'):  lr = -MOVE_VALUE
        if keyboard.is_pressed('right'): lr =  MOVE_VALUE
        if keyboard.is_pressed('down'):  bf = -MOVE_VALUE
        if keyboard.is_pressed('up'):    bf =  MOVE_VALUE

        # Send the movement command, and print the result
        print(drone.move(rcw, du, lr, bf, True))

        # Special commands
        if keyboard.is_pressed('f'): print(drone.takeoff(True))
        if keyboard.is_pressed('r'): print(drone.land(True))
        if keyboard.is_pressed('e'): print(drone.enableControl(True))
        if keyboard.is_pressed('q'): print(drone.disableControl(True))
