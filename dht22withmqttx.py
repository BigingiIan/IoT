from machine import Pin
import dht
import time
import network
from umqtt.simple import MQTTClient

# === CONFIG ===
DHT_PIN = 27
SSID = "Wokwi-GUEST"
PASSWORD = ""
MQTT_BROKER = "broker.mqttdashboard.com"  # Your broker IP
MQTT_PORT = 1883
MQTT_CLIENT_ID = "mqttx_6a57f866"
MQTT_TOPIC_TEMP = b"dht22/temperature"
MQTT_TOPIC_HUM = b"dht22/humidity"
READ_DELAY = 5  # seconds between publishes

# === INIT ===
sensor = dht.DHT22(Pin(DHT_PIN))
sta_if = network.WLAN(network.STA_IF)
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)

def connect_wifi():
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        timeout = 0
        while not sta_if.isconnected() and timeout < 20:
            time.sleep(0.5)
            timeout += 1
        if sta_if.isconnected():
            print("WiFi connected:", sta_if.ifconfig())
        else:
            print("WiFi failed. Halting.")
            while True: time.sleep(1)
            
def connect_mqtt():
    try:
        client.connect()
        print(f"Connected to MQTT broker {MQTT_BROKER}")
        return True
    except OSError as e:
        print(f"MQTT connect failed: {e}")
        return False

def read_dht22():
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        if temp is None or hum is None:
            return None, None
        return temp, hum
    except OSError:
        return None, None

# === STARTUP ===
connect_wifi()
if not connect_mqtt():
    print("Halting due to MQTT failure")
    while True: time.sleep(1)

print("DHT22 + MQTT starting...")
time.sleep(2)  # Sensor warmup

# === MAIN LOOP ===
consecutive_fails = 0

while True:
    time.sleep(READ_DELAY)
    
    temp, hum = read_dht22()
    
    if temp is None:
        consecutive_fails += 1
        print(f"DHT22 read failed. Count: {consecutive_fails}")
        if consecutive_fails >= 5:
            print("ERROR: 5 consecutive DHT failures. Halting.")
            while True: time.sleep(1)
        continue
    
    consecutive_fails = 0
    
    # Publish to MQTT
    try:
        client.publish(MQTT_TOPIC_TEMP, str(temp))
        client.publish(MQTT_TOPIC_HUM, str(hum))
        print(f"Published -> Temp: {temp:.1f}°C  Humidity: {hum:.1f}%")
    except OSError as e:
        print(f"MQTT publish failed: {e}")
        # Try reconnecting
        try:
            client.connect()
        except:
            print("MQTT reconnect failed")
