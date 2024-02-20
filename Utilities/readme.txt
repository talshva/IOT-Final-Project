# IoT Project Setup and Execution Guide

Welcome to the IoT Project documentation. This guide outlines the steps required for the pre-run setup, running the project, and visualizing the attendance data in Grafana.

## Pre-Run Setup Instructions

Before launching the project, please ensure the following setup steps are completed:

### 1. Mosquitto Service
- **Stop Mosquitto Service**: Ensure Mosquitto isn't running by executing "Stop Mosquitto Service" from the Utilities directory.

### 2. Clear InfluxDB Bucket Data
- **Initial Setup**: For the first run, clear the InfluxDB bucket data using "Clear InfluxDB" script located in the utilities directory.

### 3. Google Drive Folder Cleanup
- **Captured Images**: Ensure the Google Drive folder designated for captured images is cleared.

### 4. Local Storage Cleanup
- **Captured Images and Attendance Log**: Clear both the local captured image folder and the attendance CSV file.

### 5. WiFi Connectivity
- **Network Configuration**: Confirm all devices are connected to the "ShvartzBerg" network or another specified network.
    - If using a different network, reconfigure the WiFi settings as follows:
        - **PC Server**: Adjust the IP addresses in the `main.py` file under the configuration code section.
        - **ESP32-CAM**: Update settings in the `main.py` file via Thonny, connecting the ESP32 using a USB-to-Serial adapter.
        - **Raspberry Pi Pico W**: Modify the `main.py` file settings via Thonny.

### 6. Device Connectivity
- **Check Connections**: Ensure all devices are connected and operational.

## Running the Project

To start the project and initiate all components:

1. **Execute "Run_Project_Server"**: This script will start the Mosquitto server and the main project application. It will prompt for Google Drive authentication; follow the instructions to allow image uploads.

2. **Project Execution**: After verifying Google Drive authentication, the script will begin capturing faces and logging attendance data.

## Visualizing Attendance Data

For real-time attendance data visualization in Grafana:

1. **Run "Run_Grafana_Server" Script**: Located in the utilities directory, this script starts the Grafana server.

2. **Access Grafana Dashboard**: Click on the "Grafana Server" link provided by the script to view the attendance data.

## Additional Notes

- Ensure all pre-run setup steps are followed accurately to avoid issues during project execution.
- The project is designed to work within a specific network setup. Changes to the network configuration may require adjustments to device settings.

For support or further information, please consult the project documentation or contact the project maintainer.

