#include <WiFi.h>
#include <HTTPClient.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>

#include "time.h"

const char* ssid = "Rampage";
const char* password = "Z0Ybuguv123";
String url = "http://51.142.124.189:5000/log_measurement";

unsigned long lastTime = 0;
unsigned int timerDelay = 300000;  // 5 mins

String sensorId = "3";

const char* ntp = "pool.ntp.org";
const long  gmtOffset = 0;
const int   daylightOffset = 3600;

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

String readDHTTemperature() {
    float celsius = dht.readTemperature();
    return String(celsius);
}

String readDHTHumidity() {
    float humidity = dht.readHumidity();
    return String(humidity);
}

String getTimeStamp(){
    struct tm timeinfo;
    char timeString[80];

    getLocalTime(&timeinfo);
    strftime(timeString, sizeof(timeString), "%A, %B %d %Y %H:%M:%S", &timeinfo);

    return timeString;
}

void setup() {
    // Start tje sensor and the wifi connection
    dht.begin();
    WiFi.begin(ssid, password);

    while(WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
    // Set local time
    configTime(gmtOffset, daylightOffset, ntp);
}

int disconnectedCounter = 0;

void loop() {
    if ((millis() - lastTime) > timerDelay) {

      if (disconnectedCounter > 3) {
          Serial.println("Cannot connect to API");  // Should actually send an email to the user
      }

      if(WiFi.status()== WL_CONNECTED){

          WiFiClient client;
          HTTPClient http;

          http.begin(client, url);

          http.addHeader("Content-Type", "application/json");
          int responseCode = http.POST("{\"sensor_id\":\"" + sensorId + "\",\"date_time\":\"" + getTimeStamp() +
                "\",\"temperature\":\"" + readDHTTemperature() + "\",\"humidity\":\"" + readDHTHumidity() + "\"}");

          http.end();

          // increase or reset disconnected counter
          if (responseCode != 200) {
              disconnectedCounter ++;
          } else {
              disconnectedCounter = 0;
          }
      }
      else {
          disconnectedCounter ++;
      }
      lastTime = millis();
    }
}