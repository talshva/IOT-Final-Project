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
import time
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pytz

# -------------------Function Definitions ----------------------

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    now = datetime.now(tz_jerusalem)
    # Add name to local csv file
    with open(attendance_file, 'a', newline='') as f:
        df = pd.DataFrame([[name, now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S')]], columns=["Name", "Date", "Time"])
        df.to_csv(f, mode='a', header=False, index=False)
    # Upload name to influxDB (to be shown later on grafana)
    p = influxdb_client.Point("attendance").tag("user", name).field("value", 1).time(now, influxdb_client.WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=p)
    
    
def upload_to_drive(file_name):
    file_path = os.path.join(captured_dir, file_name)
    f = drive.CreateFile({'parents': [{'id': folder}], 'title': file_name})
    f.SetContentFile(file_path)
    f.Upload()
    print(f"Uploaded {file_name} to Google Drive")

def publish_message(msg):
    try:
        mqtt_client.publish(topic1, msg, qos)
        print(f"Sent MQTT message: {msg}")
    except Exception as e:
        print(f"Error sending MQTT message: {e}")


def on_message(client, userdata, msg):
    person_id = str(msg.payload.decode("utf-8"))
    print(f"Detected ID: {person_id}")
    # for future implementation we will use some database...
    if person_id == "316581537":   
        markAttendance("Tal_Card")


def get_time_based_greeting():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 18:
        return "Good Afternoon"
    else:
        return "Good Night"

# ---------- Configurations and Initialization ------------------

# Paths:
base_dir = os.path.dirname(__file__)
authorized_dir = os.path.join(base_dir, "Authorized_faces")
captured_dir = os.path.join(base_dir, "Captured")
attendance_file = os.path.join(base_dir, "Attendance.csv")
url = "http://192.168.11.25/cam-hi.jpg"

# MQTT Configuration:
# pico's ip:  192.168.48.58
broker_address = "192.168.11.153" # PC's ip
topic1 = "pc/to_pico"
topic2 = "pico/to_pc"
qos = 1
mqtt_client = mqtt.Client()
mqtt_client.connect(broker_address, 1883, 60)
mqtt_client.loop_start()  # Start networking daemon
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker!" if rc == 0 else f"Failed to connect, return code {rc}\n")  
mqtt_client.on_connect = on_connect
# Adjust the subscription setup to listen to the new topic
mqtt_client.subscribe(topic2)
mqtt_client.on_message = on_message

# InfluxDB configurations
bucket = "IOT_PROJECT"
org = "Private"
token = "lGBO6gmsxGWnyV1wi929YTfZMIfhitIWtjUhbT-rH7XwfHqbNk8hMGeD4GdBEd1N5sF4OhgUZb5roCdudia8TQ=="
influxDB_url = "https://eu-central-1-1.aws.cloud2.influxdata.com"
tz_jerusalem = pytz.timezone('Asia/Jerusalem')
client = influxdb_client.InfluxDBClient(url=influxDB_url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Google Drive Authentication and Folder Setup
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
folder = "1T_ERl2luPeeVyt48L8yZDSgngw76-jyn"

# Ensure required directories exist
for directory in [authorized_dir, captured_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Load images and create encodings:
images = []
classNames = [os.path.splitext(cl)[0] for cl in os.listdir(authorized_dir) if os.path.isfile(os.path.join(authorized_dir, cl))]
for cl in os.listdir(authorized_dir):
    curImg = cv2.imread(os.path.join(authorized_dir, cl))
    if curImg is not None:
        images.append(curImg)
encodeListKnown = findEncodings(images)
print(f"People Database: {classNames}")


# Initialize variables to keep track of the last recognized person and the time they were recognized
last_recognized_name = None
first_recognition_time = time.time()
recognition_cooldown = 10  # Cooldown period in seconds
time_passed = 0
stranger_flag = 0

print('Initialization Complete!')


#  ---------- Main Loop for Face Detection, Uploading, and Attendance Logging ----------
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
while True:
    try:
    # Read ESP32-CAM frames:
        img_resp = urllib.request.urlopen(url)
        img = cv2.imdecode(np.array(bytearray(img_resp.read()), dtype=np.uint8), -1)
        imgS = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (0, 0), None, 0.25, 0.25)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        # Check if any faces are detected in the current frame
        if facesCurFrame:
            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                # Check for matching in our database:
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                if any(matches): # if found any face from the database:
                    current_time = time.time()
                    time_passed = int(current_time - first_recognition_time)
                    name = classNames[np.argmin(face_recognition.face_distance(encodeListKnown, encodeFace))]
                    if name != last_recognized_name or (time_passed) >= recognition_cooldown: # new face detected or countdown over
                        first_recognition_time = current_time
                        last_recognized_name = name
                        # Publish name to raspberry through mqtt:
                        greeting = get_time_based_greeting()
                        message = f"{greeting},{name}!" 
                        publish_message(message) 
    
                        # Draw green square:
                        y1, x2, y2, x1 = [coordinate * 4 for coordinate in faceLoc]
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)          
                        # Send message to grafana?
                    else: 
                        print(f"Skipping {name}, recently recognized.")
                    stranger_flag = 0
                else:
                    if not stranger_flag: # if first time recognizing a stranger
                        message = "Unrecognized Face!"
                        print(message)
                        publish_message(message) # Send this message to be printed on the lcd.
                        name = "Unknown"
                        # Add stranger to csv file:
                        markAttendance(name)
                        img_name = f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"   
                        # Saving the captured stranger locally and in drive:
                        cv2.imwrite(os.path.join(captured_dir, img_name), img)
                        upload_to_drive(img_name)
                        stranger_flag = 1  # Don't capture anymore stranger images until reset.     
                if name != "Unknown":
                    # Add Authorized person to csv file:
                    markAttendance(name)
                    img_name = f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"           
                    # Saving the captured image locally and in drive:
                    cv2.imwrite(os.path.join(captured_dir, img_name), img)
                    upload_to_drive(img_name)
                        
        # Display the updated frame on screen:
        cv2.imshow('live transmission', img)
        if cv2.waitKey(5) == ord('q'):
            break
        
    except Exception as e:
        print(f"Problem capturing image: \n{e}")

print("Done! Exiting...")
cv2.destroyAllWindows()
# Disconnect from broker when done
mqtt_client.disconnect()