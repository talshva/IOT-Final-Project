from umqtt.simple import MQTTClient
import network
import time

broker_address = "192.168.48.153"  # Modify if your broker is on a different host
topic = "pico/data"
wifi_ssid = 'ShvartzBerg'
wifi_pwd = '123Q123q'


def connect_wifi():
    print("Connecting to Wi-Fi: ", wifi_ssid)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_pwd)
    while not wlan.isconnected():
        utime.sleep(0.1)
    print("Connected!")
    print('IP: ', wlan.ifconfig()[0])


def connect_mqtt():
    # Setup MQTT client
    print("Connecting to MQTT broker...")
    global client
    client = MQTTClient("pico_client", broker_address, port=1883)  # Replace with your MQTT broker's IP
    client.set_callback(on_message)
    client.connect()
    client.subscribe(topic)
    print("Connected!")


# Callback function to handle messages
def on_message(topic, msg):
    print(f"Received `{msg}` from `{topic}` topic")
    # Add code to display on LCD, turn on LED, and move servo here

def handle_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode()
    print(f"Received message on topic {topic}: {message}")

connect_wifi()
connect_mqtt()

# Main loop to listen for incoming messages
while True:
    client.wait_msg()

# Disconnect from broker and Wi-Fi when done (if needed)
client.disconnect()
wlan.disconnect()

