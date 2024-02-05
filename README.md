# ESP32-CAM and RFID-Based Attendance System with Door Access Control

This comprehensive guide details constructing an attendance system and access control mechanism using ESP32-CAM for face recognition and an RFID module for tag detection. Recognized faces or validated RFID tags activate a green LED and control a servo motor to simulate door opening. The system records attendance in a CSV file and uploads captured images to Google Drive. The Raspberry Pi Pico W, using MQTT for communication, displays the name or RFID tag ID of the authenticated individual on an I2C LCD and manages the access control hardware.

## Prerequisites

### Hardware
- ESP32-CAM module
- RFID reader module (e.g., MFRC522)
- Raspberry Pi Pico W
- I2C LCD display
- Servo motor
- Green LED
- Resistors for LED (typically 330Ω)

### Software
- [Mosquitto MQTT Broker](https://mosquitto.org/download/) on PC
- [Python 3](https://www.python.org/downloads/) on PC with `paho-mqtt` library (`pip install paho-mqtt`)
- [CircuitPython firmware](https://circuitpython.org/board/esp32cam/) for ESP32-CAM
- MicroPython firmware on Raspberry Pi Pico W
- Libraries for interfacing with the I2C LCD and RFID on Pico W

## Setup and Configuration

### ESP32-CAM Configuration
Follow [this detailed guide](https://how2electronics.com/face-recognition-based-attendance-system-using-esp32-cam/) to set up the ESP32-CAM for video capture, Wi-Fi connectivity, and face recognition data transmission to a PC.

### RFID Reader Integration
Connect your RFID reader to the Raspberry Pi Pico W, ensuring SPI communication compatibility. Install MicroPython libraries that facilitate reading from the RFID module. A useful starting point for RFID with MicroPython can be found [here](https://github.com/wendlers/micropython-mfrc522).

### Face Recognition and Attendance Recording
Process the video stream from the ESP32-CAM, identify individuals using a face database, and log attendance in a CSV file. This involves setting up a face recognition library on your PC, as outlined in the [how2electronics guide](https://how2electronics.com/face-recognition-based-attendance-system-using-esp32-cam/).

### Google Drive Integration
Automate captured image uploads to Google Drive through API authentication, as described in [this how2electronics tutorial](https://how2electronics.com/how-to-send-esp32-cam-captured-image-to-google-drive/).

### MQTT Communication Setup
Follow [Cedalo's guide](https://cedalo.com/blog/how-to-install-mosquitto-mqtt-broker-on-windows/) to install the Mosquitto MQTT Broker on a Windows PC. This broker facilitates message exchange between the main PC and the Raspberry Pi Pico W.

### Raspberry Pi Pico W and I2C LCD Setup
For setting up the I2C LCD with the Raspberry Pi Pico W, [this video tutorial](https://youtu.be/bXLgxEcT1QU?si=CtYzVgTlwoT3zRW1) provides an excellent overview. Ensure the Pico W is programmed to display recognized names or RFID tag IDs on the LCD.

### Door Access Control Mechanism
Design the access control system using a servo motor for door operation and a green LED as an access indicator. Program the Pico W to respond to MQTT messages or RFID validation, controlling these components accordingly.

## Running the System

1. **Install and run the Mosquitto MQTT Broker** on your PC.
2. **Power the ESP32-CAM** and ensure it's connected to the same network as your PC for seamless face recognition and data transmission.
3. **Power the Raspberry Pi Pico W**; it should automatically connect to Wi-Fi and the MQTT broker to receive commands and manage the access control mechanism.
4. **Execute the face recognition script** on your PC to analyze the ESP32-CAM video feeds, recognize faces and send appropriate commands to the Pico W for access control.

## Extending the System

### RFID-Based Access
Integrate RFID functionality to grant access through RFID tags alongside face recognition. Each valid tag swipe should trigger the door access mechanism similar to face recognition, indicating a versatile and secure entry system.

## Contributing


## License

