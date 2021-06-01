# Listing 1: ESP32 zu Blynk, blynklib_mp
# Blynk Library Demo
import blynklib_mp as blynklib
import network
import utime as time
from machine import Pin

# DHT22/AM2302
import dht

WIFI_SSID = 'SSID' # WLAN SSID
WIFI_PASS = '1234' # Passwort
BLYNK_AUTH = 'CWHcUKXsrhesIdHvMMQxB7qBlJJPELLE'
GPIO_DHT22_PIN = 13 # Pin der Datenleitung DHT-Sensor

print("Verbinde mit WLAN '{}'".format(WIFI_SSID))
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)
while not wifi.isconnected():
    time.sleep(1)
    print('WLAN...')
print('WLAN IP:', wifi.ifconfig()[0])

print("Verbinde mit Blynk Server...")
blynk = blynklib.Blynk(BLYNK_AUTH)

T_COLOR = '#f5b041'
H_COLOR = '#85c1e9'
ERR_COLOR = '#444444'

T_VPIN = 3 # virtueller Pin Temp.
H_VPIN = 4 # virtueller Pin Humi.

dht22 = dht.DHT22(Pin(GPIO_DHT22_PIN, Pin.IN, Pin.PULL_UP))

@blynk.handle_event('read V{}'.format(T_VPIN))
def read_handler(vpin):
    temperature = 0.0
    humidity = 0.0

    # Sensor Daten
    try:
        dht22.measure()
        temperature = dht22.temperature()
        humidity = dht22.humidity()
        print("%d°C   %d%%rel. Feuchte"%(temperature,humidity))
    except OSError as o_err:
        print("Keine DHT22-Sensor Daten: '{}'".format(o_err))

    # Farbe in App je nach Werten ändern
    if temperature != 0.0 and humidity != 0.0:
        blynk.set_property(T_VPIN, 'color', T_COLOR)
        blynk.set_property(H_VPIN, 'color', H_COLOR)
        blynk.virtual_write(T_VPIN, temperature)
        blynk.virtual_write(H_VPIN, humidity)
    else:
        # Rot = fehlerhafte Daten
        blynk.set_property(T_VPIN, 'color', ERR_COLOR)
        blynk.set_property(H_VPIN, 'color', ERR_COLOR)


while True:
    blynk.run()