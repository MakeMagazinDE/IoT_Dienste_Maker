# Listing 3
# Sending Data to Cayenne
from umqtt.simple import MQTTClient
from machine import Pin
import network
import time
import dht
import onewire

GPIO_DHT22_PIN = 13
temperature = 0.0

#wifi setting
SSID="unserWLAN"    #SSID des WLANs
PASSWORD="123456pw" #Passwort
SERVER = "mqtt.mydevices.com" #Server hier Cayenne
CLIENT_ID = "xxxxxxxx-b3d8-11eb-yyyyy-sdfsdfsdfsdf"  #client ID
username='wwerwsv-a32d3-11eb-asde4-b32ea624e442'     #MQTT username
password='79ab2aaafa10c06f02ae5c18536cfe13ba319851b' #MQTT password
TOPIC = ("v1/%s/things/%s/data/1" % (username, CLIENT_ID))

def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ssid,passwd)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
    
def senddata():
    # read sensor data
    try:
        dht22.measure()
        temperature = dht22.temperature()
    except OSError as o_err:
        print("Unable to get DHT22 sensor data: '{}'".format(o_err))

    time.sleep_ms(500)
    c.publish(TOPIC, str(temperature))
    print("%d °C"%temperature)
    time.sleep(15)

# Connect to WIFI/Server
connectWifi(SSID,PASSWORD)
server=SERVER
c = MQTTClient(CLIENT_ID, server,0,username,password)
c.connect()

# Setup Sensor
dht22 = dht.DHT22(Pin(GPIO_DHT22_PIN, Pin.IN, Pin.PULL_UP))

while True:
    try:
        senddata()
    except OSError:
        pass
    