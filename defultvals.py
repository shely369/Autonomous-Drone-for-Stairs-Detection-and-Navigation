from OpenDJI import OpenDJI

IP_ADDR = "172.20.10.6"

# Configuration parameters
NEW_TAKEOFF_ALTITUDE = 5  # meters
NEW_RTH_ALTITUDE = 0.1    # meters

with OpenDJI(IP_ADDR) as drone:
    # Retrieve all keys from the flight controller module
    list_keys = drone.getModuleKeys(OpenDJI.MODULE_FLIGHTCONTROLLER)[1:-1].replace('"', '').split(",")
    print("Flight Controller Keys:", sorted(list_keys))
    print()

    # Set automatic takeoff altitude
    if "TakeoffMaxAltitude" in list_keys:
        result = drone.setValue(OpenDJI.MODULE_FLIGHTCONTROLLER, "TakeoffMaxAltitude", NEW_TAKEOFF_ALTITUDE)
        print(f"Set TakeoffMaxAltitude to {NEW_TAKEOFF_ALTITUDE}m: {result}")
    else:
        print("Key 'TakeoffMaxAltitude' not found.")

    # Set return-to-home altitude
    if "GoHomeHeight" in list_keys:
        result = drone.setValue(OpenDJI.MODULE_FLIGHTCONTROLLER, "GoHomeHeight", NEW_RTH_ALTITUDE)
        print(f"Set GoHomeHeight to {NEW_RTH_ALTITUDE}m: {result}")
    elif "RTHHeight" in list_keys:
        result = drone.setValue(OpenDJI.MODULE_FLIGHTCONTROLLER, "RTHHeight", NEW_RTH_ALTITUDE)
        print(f"Set RTHHeight to {NEW_RTH_ALTITUDE}m: {result}")
    else:
        print("RTH height key not found.")

    print("Done.")
