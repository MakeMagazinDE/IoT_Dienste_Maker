# import general libraries
from machine import Pin
import time
from time import sleep
import network
from umqtt.simple import MQTTClient

# ThingSpeak Credentials:
SERVER = "mqtt.thingspeak.com"
CHANNEL_ID = "123456789"
WRITE_API_KEY = "U6ABAG49DZI3FKKI"
PUB_TIME_SEC = 30

# MQTT client object
client = MQTTClient("umqtt_client", SERVER)

# Create the MQTT topic string
topic = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY

# WiFi Credentials 
WiFi_SSID = "UnserFritzi"
WiFi_PASS = "UNsssudikS"

# define pin 0 (LED) as output
led = Pin(0, Pin.OUT)

# DHT
from dht import DHT22
dht22 = DHT22(Pin(13))

# Function to read DHT
def readDht():
    dht22.measure()
    return dht22.temperature(), dht22.humidity()


wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()
wlan.connect(WiFi_SSID,WiFi_PASS)
while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)

# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# if not wlan.isconnected():
#     print('connecting to network...')
#     wlan.connect(WiFi_SSID, WiFi_SSID)
#     while not wlan.isconnected():
#         pass
print('network config:', wlan.ifconfig())


while True:
    led.on()
    temp, hum, = readDht()
    payload = "field1="+str(temp)+"&field2="+str(hum)
    print(temp,hum)
    client.connect()
    client.publish(topic, payload)
    client.disconnect()
    led.off()
    time.sleep(PUB_TIME_SEC)

