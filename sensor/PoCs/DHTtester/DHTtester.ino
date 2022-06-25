// Example testing sketch for various DHT humidity/temperature sensors
// Written by ladyada, public domain

// REQUIRES the following Arduino libraries:
// - DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library
// - Adafruit Unified Sensor Lib: https://github.com/adafruit/Adafruit_Sensor

#include "DHT.h"

#define DHTPIN 2     // Digital pin connected to the DHT sensor

#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321


// Initialize DHT sensor.
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println(F("DHT22 test!"));

  dht.begin();
}

void loop() {
  // Wait 5 seconds between measurements.
  delay(5000);

  float humidity = dht.readHumidity();
  
  // Read temperature as Celsius (the default)
  float celsius = dht.readTemperature();
  
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float fahrenheit = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(celsius) || isnan(fahrenheit)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  Serial.print(F("Humidity: "));
  Serial.print(humidity);
  Serial.print(F("%  Temperature: "));
  Serial.print(celsius);
  Serial.print(F("°C "));
  Serial.print(fahrenheit);
  Serial.print(F("°F "));
  Serial.println(F(""));
}
