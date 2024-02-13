from umqtt.simple import MQTTClient
import network
import time
from machine import I2C, Pin, SoftSPI
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from myservo import Servo
from mfrc522 import MFRC522


broker_address = "192.168.53.153"  # Modify if your broker is on a different host
topic1 = "pc/to_pico"
topic2 = "pico/to_pc"
wifi_ssid = 'ShvartzBerg'
wifi_pwd = '123Q123q'

# RFID init:
sck = Pin(2, Pin.OUT)
copi = Pin(3, Pin.OUT) # Controller out, peripheral in
cipo = Pin(4, Pin.OUT) # Controller in, peripheral out
spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=copi, miso=cipo)
sda = Pin(5, Pin.OUT)
reader = MFRC522(spi, sda)

# Servo init
servo=Servo(16)


# LCD Configuration
I2C_ADDR = 63
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16	

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)



def connect_wifi(timeout=10):
    wlan = network.WLAN(network.STA_IF)
    print("Connecting to Wi-Fi:", wifi_ssid)
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_pwd)
    start_time = time.time()
    
    while not wlan.isconnected():
        if time.time() - start_time > timeout:
            print("Failed to connect within the timeout period. Retrying...")
            # Optionally, reset the network interface or take other actions
            wlan.active(False)
            time.sleep(5)  # Wait for a bit before retrying
            wlan.active(True)
            wlan.connect(wifi_ssid, wifi_pwd)
            start_time = time.time()  # Reset the start time for the next attempt
            
        time.sleep(0.1)
    
    print("Connected!")
    print('IP:', wlan.ifconfig()[0])


def connect_mqtt():
    print("Connecting to MQTT broker...")
    global client
    while True:
        try:
            client = MQTTClient("pico_client", broker_address)
            client.set_callback(on_message)
            client.connect()
            client.subscribe(topic1)
            print("Connected to MQTT!")
            break  # Exit the loop once connected
        except OSError as e:
            print("Failed to connect to MQTT broker. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying

# Callback function to handle messages
def on_message(topic1, msg):
    print(f"Received `{msg.decode()}` from `{topic1.decode()}` topic1")
    message = msg.decode()
    lcd.clear()
    lcd.putstr(message)
    time.sleep(1)
    if msg.decode() != "Unrecognized Face!":
        open_door()
    else:
        lcd.clear()
        lcd.putstr('Use card instead')
        time.sleep(1)

    

def publish_message(msg):
    try:
        client.publish(topic2, msg, 1)
        print(f"Sent MQTT message: {msg}")
    except Exception as e:
        print(f"Error sending MQTT message: {e}")
        

def check_RFID():
    try:
        (status, tag_type) = reader.request(reader.CARD_REQIDL)#Read the card type number
        if status == reader.OK:
            (status, raw_uid) = reader.anticoll()#Reads the card serial number of the selected card
            if status == reader.OK:
                print('Card Detected')
                print('  - Tag Type: 0x%02x' % tag_type)
                print('  - uid: 0x%02x%02x%02x%02x' % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print('')
                if reader.select_tag(raw_uid) == reader.OK:#Read card memory capacity
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    if reader.auth(reader.AUTH, 8, key, raw_uid) == reader.OK:#Verification card password
                        publish_message("316581537")
                        # For future implementation, we will send the real card id...
                        #print(bytearray(reader.read(8)))
                        #reader.Read_Data(key, raw_uid)
                        open_door()

                        reader.stop_crypto1()
                    else:
                        print("AUTH ERROR")
                else:
                    print("FAILED TO SELECT TAG")
    except Exception as e:
        print(str(e))

def open_door():
    lcd.clear()
    lcd.putstr("Door opens!")  
    servo.ServoAngle(180)
    time.sleep(3)
    lcd.clear()    
    servo.ServoAngle(0)    

connect_wifi()
connect_mqtt()

# Main loop to listen for incoming messages
while True:
 #   servo.ServoAngle(0)
 #   time.sleep(1)
 #   servo.ServoAngle(180)
 #   time.sleep(1)
    try:
        check_RFID()
        client.check_msg()
        time.sleep(0.1)  # Add a short delay to allow for CPU idle
    except OSError as e:
        print("Connection lost. Attempting to reconnect...")
        connect_mqtt()

# Disconnect from broker and Wi-Fi when done (if needed)
client.disconnect()
wlan.disconnect()
