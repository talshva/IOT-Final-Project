import paho.mqtt.client as mqtt

# Configuration (adjust as needed)
broker_address = "localhost"  # Modify if your broker is on a different host
topic = "pico/data"
qos = 1  # QoS 1: At least once delivery

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def send_data(client, value):   
    try:
        client.publish(topic, value, qos)
        print(f"Sent data: {value}")    
    except Exception as e:
        print(f"Error sending data: {e}")  

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect

# Connect to broker
client.connect(broker_address, 1883)

# Enter main loop to receive user input and send data
while True:
    data = input("Enter data to send: ")
    send_data(client, data)

# Disconnect from broker when done
client.disconnect()