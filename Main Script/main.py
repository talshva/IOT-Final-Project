import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import face_recognition
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import pandas as pd
import paho.mqtt.client as mqtt

# Configuration and Setup
base_dir = os.path.dirname(__file__)
path = os.path.join(base_dir, "Authorized_faces")
captured_dir = os.path.join(base_dir, "Captured")
attendance_file = os.path.join(base_dir, "Attendance.csv")
url = "http://192.168.48.25/cam-hi.jpg"

# MQTT Configuration
# pico's ip:  192.168.48.58
broker_address = "192.168.48.153" # PC's ip
topic = "pico/data"
qos = 1

# Ensure required directories exist
for directory in [path, captured_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

mqtt_client = mqtt.Client()
mqtt_client.connect(broker_address, 1883, 60)
mqtt_client.loop_start()  # Start networking daemon

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker!" if rc == 0 else f"Failed to connect, return code {rc}\n")
    
mqtt_client.on_connect = on_connect


# Google Drive Authentication and Folder Setup
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
folder = "1T_ERl2luPeeVyt48L8yZDSgngw76-jyn"


# -------------------Function Definitions ----------------------

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    now = datetime.now()
    with open(attendance_file, 'a', newline='') as f:
        df = pd.DataFrame([[name, now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S')]], columns=["Name", "Date", "Time"])
        df.to_csv(f, mode='a', header=False, index=False)

def upload_to_drive(file_name):
    file_path = os.path.join(captured_dir, file_name)
    f = drive.CreateFile({'parents': [{'id': folder}], 'title': file_name})
    f.SetContentFile(file_path)
    f.Upload()
    print(f"Uploaded {file_name} to Google Drive")

def publish_message(name):
    greeting = get_time_based_greeting()
    message = f"{greeting}, {name}!" 
    try:
        mqtt_client.publish(topic, message, qos)
        print(f"Sent MQTT message: {message}")
    except Exception as e:
        print(f"Error sending MQTT message: {e}")

def get_time_based_greeting():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 18:
        return "Good Afternoon"
    else:
        return "Good Night"



# ------------------Main ----------------------
# Load images and create encodings
images = []
classNames = [os.path.splitext(cl)[0] for cl in os.listdir(path) if os.path.isfile(os.path.join(path, cl))]
for cl in os.listdir(path):
    curImg = cv2.imread(os.path.join(path, cl))
    if curImg is not None:
        images.append(curImg)

encodeListKnown = findEncodings(images)
print(f"People Database: {classNames}")
print('Encoding Complete')

# Main Loop for Face Detection, Uploading, and Attendance Logging
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
while True:
    img_resp = urllib.request.urlopen(url)
    img = cv2.imdecode(np.array(bytearray(img_resp.read()), dtype=np.uint8), -1)
    imgS = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (0, 0), None, 0.25, 0.25)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        if any(matches):
            name = classNames[np.argmin(face_recognition.face_distance(encodeListKnown, encodeFace))]
            publish_message(name)  # Publish name to MQTT
            y1, x2, y2, x1 = [coordinate * 4 for coordinate in faceLoc]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
            img_name = f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
            cv2.imwrite(os.path.join(captured_dir, img_name), img)
            upload_to_drive(img_name)

    cv2.imshow('live transmission', img)
    if cv2.waitKey(5) == ord('q'):
        break

cv2.destroyAllWindows()
# Disconnect from broker when done
mqtt_client.disconnect()