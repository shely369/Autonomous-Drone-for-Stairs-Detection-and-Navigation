#include <ArduinoBLE.h>

BLEDevice droneDevice;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!BLE.begin()) {
    Serial.println("Failed to start BLE!");
    while (1);
  }

  Serial.println("Scanning for DJI Drone...");
  BLE.scanForName("DJI-NEO-163A");

  while (!(droneDevice = BLE.available())) {
    Serial.println("Waiting for connection...");
    delay(500);
  }

  Serial.println("Drone found! Connecting...");
  BLE.stopScan();

  if (droneDevice.connect()) {
    Serial.println("Connected to drone!");
    Serial.println("Attempting forced service scan...");

    for (int i = 0; i < 10; i++) { 
      BLEService service = droneDevice.service(i);
      if (!service) break;

      Serial.print("Found Service UUID: ");
      Serial.println(service.uuid());

      // Now scan for characteristics inside each service
      for (int j = 0; j < 10; j++) {
        BLECharacteristic characteristic = service.characteristic(j);
        if (!characteristic) break;

        Serial.print("Found Characteristic UUID: ");
        Serial.println(characteristic.uuid());
      }
    }

  } else {
    Serial.println("Failed to connect.");
    while (1);
  }
}

void loop() {}
