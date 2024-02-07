# ESP32-CAM and RFID-Based Attendance System with Door Access Control

This project integrates ESP32-CAM and RFID technology to create a versatile attendance system and access control solution. The system employs the ESP32-CAM for facial recognition and an RFID reader connected to a Raspberry Pi Pico W for tag scanning. Upon successful identification or tag validation, the Raspberry Pi Pico W activates a servo motor to simulate door opening and displays the user's name on an I2C LCD. Attendance records are maintained in a CSV file, and images of recognized individuals are uploaded to Google Drive for record-keeping. Communication between the main PC and the Raspberry Pi Pico W is facilitated through MQTT, exclusively used for transmitting recognition results and control commands for the access mechanism.
See [this video](https://youtu.be/rm8MsGPP1t8) for a live demonstration.

## Prerequisites

### Hardware
- ESP32-CAM module
- RFID reader module (MFRC522)
- Raspberry Pi Pico W
- I2C LCD display
- Servo motor

### Software
- [Mosquitto MQTT Broker](https://mosquitto.org/download/) on PC
- [Python 3](https://www.python.org/downloads/) on PC with `paho-mqtt` library (`pip install paho-mqtt`)
- [CircuitPython firmware for ESP32-CAM](https://circuitpython.org/board/esp32cam/)
- MicroPython firmware on Raspberry Pi Pico W
- Libraries for interfacing with I2C LCD and RFID on Pico W

## Setup and Configuration

### MQTT Broker Setup
Install and configure the Mosquitto MQTT Broker on your PC before initiating the system, as detailed in [Cedalo's installation guide](https://cedalo.com/blog/how-to-install-mosquitto-mqtt-broker-on-windows/). Manage the service with:
- **To start the broker**: `sc start mosquitto`
- **To stop the broker**: `sc stop mosquitto`
- **To check the broker status**: `sc query mosquitto`

### ESP32-CAM Configuration
Follow [this guide](https://how2electronics.com/face-recognition-based-attendance-system-using-esp32-cam/) to set up the ESP32-CAM for capturing video and connecting to Wi-Fi for facial recognition processing.

### RFID Reader Integration with Raspberry Pi Pico W
Set up the RFID reader with the Raspberry Pi Pico W, ensuring correct SPI communication. Library support and setup instructions are available in [this GitHub resource](https://github.com/wendlers/micropython-mfrc522).

### Google Drive Integration
Set up Google Drive to automatically receive uploaded images of recognized individuals by following [this tutorial](https://how2electronics.com/how-to-send-esp32-cam-captured-image-to-google-drive/).

### Raspberry Pi Pico W and I2C LCD Setup
Configure the Raspberry Pi Pico W to display authentication data on an I2C LCD with guidance from [this video tutorial](https://youtu.be/bXLgxEcT1QU?si=CtYzVgTlwoT3zRW1).

### Servo Motor Integration with Raspberry Pi Pico W
For connecting and controlling a servo motor with the Raspberry Pi Pico W, refer to [this MicroPython guide](https://www.hackster.io/raspberry-pi/projects).

## Running the System

1. **Ensure the Mosquitto MQTT Broker** is up and operational on your PC to manage communications.
2. **Power on the ESP32-CAM**, connecting it to the same Wi-Fi network as your PC.
3. **Activate the Raspberry Pi Pico W**, ready to receive MQTT messages and RFID inputs.
4. **Launch the facial recognition script** on your PC, which analyzes ESP32-CAM feeds and sends recognition results or commands to the Pico W for access control.

## Extending the System

The system's modular design allows for the integration of RFID technology alongside facial recognition for enhanced security and flexibility. Future expansions may explore complex access control algorithms, additional security measures, or the incorporation of a broader range of IoT devices for a fully integrated management system.

## Contributing
Contributions are encouraged and appreciated.

## License
