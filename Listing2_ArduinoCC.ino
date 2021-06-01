//Listing 2: Code von create.arduino.cc
//NodeMCU1.0 und DHT22 auf Arduino Cloud
#include "arduino_secrets.h"	// von create.arduino.cc laden/anpasen
#include "thingProperties.h"	// von create.arduino.cc laden
#include "DHT.h"

#define DHTPIN 12 // D6
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // Initialize serial and wait for port to open:
  Serial.begin(9600);
  // This delay gives the chance to wait for a Serial Monitor without blocking if none is found
  delay(1500); 
  dht.begin();
  // Defined in thingProperties.h
  initProperties();

  // Connect to Arduino IoT Cloud
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
  delay(1500); 
}

void loop() {
  ArduinoCloud.update();  
  temp = dht.readTemperature();
  humi = dht.readHumidity();
  Serial.print(temp);
  Serial.print("   ");
  Serial.println(humi);
  delay(15000);
}