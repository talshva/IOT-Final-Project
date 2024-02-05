# ESP32-CAM and RFID-Based Attendance System with Door Access Control

This guide provides a step-by-step approach to building an advanced attendance system that leverages both ESP32-CAM for facial recognition and an RFID module for tag detection. When an individual is recognized or an RFID tag is validated, a green LED lights up and a servo motor operates to simulate door opening, granting access. The system also logs attendance in a CSV file and uploads images of recognized faces to Google Drive. Utilizing MQTT for communication, the Raspberry Pi Pico W displays the authenticated person's name or RFID tag ID on an I2C LCD and controls the access mechanism.

## Prerequisites

### Hardware
- ESP32-CAM module
- RFID reader module (MFRC522)
- Raspberry Pi Pico W
- I2C LCD display
- Servo motor
- Green LED
- 330Ω resistor for LED

### Software
- [Mosquitto MQTT Broker](https://mosquitto.org/download/) on PC
- [Python 3](https://www.python.org/downloads/) on PC with `paho-mqtt` library (`pip install paho-mqtt`)
- [CircuitPython firmware for ESP32-CAM](https://circuitpython.org/board/esp32cam/)
- MicroPython firmware on Raspberry Pi Pico W
- Libraries for interfacing with I2C LCD and RFID on Pico W

## Setup and Configuration

### MQTT Broker Setup
Before powering up your devices, ensure the Mosquitto MQTT Broker is installed and running on your PC. Follow [Cedalo's guide](https://cedalo.com/blog/how-to-install-mosquitto-mqtt-broker-on-windows/) for installation. Use the following commands to manage the Mosquitto service:
- **To start the broker**: `sc start mosquitto`
- **To stop the broker**: `sc stop mosquitto`
- **To check the broker status**: `sc query mosquitto`

### ESP32-CAM Configuration
Set up the ESP32-CAM for video capture and Wi-Fi connectivity following [this detailed guide](https://how2electronics.com/face-recognition-based-attendance-system-using-esp32-cam/).

### RFID Reader Integration
Connect the RFID reader to your Raspberry Pi Pico W, ensuring proper SPI communication. Use [this resource](https://github.com/wendlers/micropython-mfrc522) for library support and setup instructions.

### Google Drive Integration
Configure automatic upload of captured images to Google Drive by following [this tutorial](https://how2electronics.com/how-to-send-esp32-cam-captured-image-to-google-drive/).

### Raspberry Pi Pico W and I2C LCD Setup
Prepare the Raspberry Pi Pico W to display information on an I2C LCD as per [this video tutorial](https://youtu.be/bXLgxEcT1QU?si=CtYzVgTlwoT3zRW1).

### Servo Motor Integration with Raspberry Pi Pico W
To connect a servo motor to the Raspberry Pi Pico W for door access control, follow this guide on [servo motor control with MicroPython](https://www.hackster.io/raspberry-pi/projects). You will need to connect the servo's control wire to one of the Pico W's PWM-capable GPIO pins, and supply appropriate power to the servo.

## Running the System

1. **Start the Mosquitto MQTT Broker** on your PC to ensure communication infrastructure is ready.
2. **Power the ESP32-CAM** and **Raspberry Pi Pico W**; they should automatically connect to Wi-Fi and the MQTT broker, respectively.
3. **Execute the face recognition script** on your PC. This script analyzes video feeds from the ESP32-CAM, recognizes faces, and communicates with the Pico W to manage access control.

## Extending the System

Integrating RFID provides a versatile and secure entry system. Future enhancements can include more sophisticated access control logic, additional sensors for enhanced security, or integration with other IoT devices.

## Contributing

We welcome contributions! Please read through our contribution guidelines before making a pull request.

## License

