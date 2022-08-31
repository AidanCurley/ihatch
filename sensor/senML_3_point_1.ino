#include <ArduinoJson.h>

#include <WiFi.h>
#include <HTTPClient.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>

#include "time.h"

#define uS_TO_S_FACTOR 1000000
#define TIME_TO_SLEEP  10

RTC_DATA_ATTR const char* ssid = "Rampage";
RTC_DATA_ATTR const char* password = "Z0Ybuguv123";
RTC_DATA_ATTR String url = "http://51.142.124.189:5000/log_measurement";
RTC_DATA_ATTR const int capacity = JSON_OBJECT_SIZE(5);

RTC_DATA_ATTR String sensorId = "2";

RTC_DATA_ATTR const char* ntp = "pool.ntp.org";
RTC_DATA_ATTR long gmtOffset = 0;
RTC_DATA_ATTR int daylightOffset = 3600;

RTC_DATA_ATTR float lastTemperature = 0.0;
RTC_DATA_ATTR float lastHumidity = 0.0;

RTC_DATA_ATTR float minTempVariance = 0.1;
RTC_DATA_ATTR float minHumidityVariance = 0.1;

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    //Serial.println("Failed to obtain time");
    return(0);
  }
  time(&now);
  return now;
}

void setup() {
  dht.begin();
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);

  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  // Set local time
  configTime(gmtOffset, daylightOffset, ntp);

  int disconnectedCounter = 0;
  int responseCode;

  while(disconnectedCounter < 3){
    StaticJsonDocument<256> doc;

    if(WiFi.status()== WL_CONNECTED){
      Serial.println("Connected");
      float currentTemperature = dht.readTemperature();
      float currentHumidity = dht.readHumidity();
      boolean isChanged = false;
      String json = "";

      JsonObject doc_base = doc.createNestedObject();

      doc_base["bn"] = sensorId;
      doc_base["bt"] = getTime();

      if ((currentTemperature - lastTemperature >= minTempVariance) || (currentTemperature - currentTemperature <= -minTempVariance)){
        JsonObject doc_0 = doc.createNestedObject();

        doc_0["n"] = "temperature";
        doc_0["v"] = String(currentTemperature);
        doc_0["u"] = "Cel";

        lastTemperature = currentTemperature;
        isChanged = true;
      }

      if ((currentHumidity - lastHumidity >= minHumidityVariance) || (currentHumidity - lastHumidity <= -minHumidityVariance)){
        JsonObject doc_1 = doc.createNestedObject();

        doc_1["n"] = "humidity";
        doc_1["v"] = String(currentHumidity);
        doc_1["u"] = "%RH";

        lastHumidity = currentHumidity;
        isChanged = true;
     }

     String payload;
     serializeJson(doc, payload);

     if (isChanged == true) {
       WiFiClient client;
       HTTPClient http;

       http.begin(client, url);

       http.addHeader("Content-Type", "application/json");

       Serial.println(payload);
       responseCode = http.POST(payload);
       Serial.println("ResponseCode:" + String(responseCode));

       http.end();
     }

     esp_deep_sleep_start();
   }
   disconnectedCounter ++;
 }
}

void loop(){}