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

RTC_DATA_ATTR String sensorId = "1";

RTC_DATA_ATTR const char* ntp = "pool.ntp.org";
RTC_DATA_ATTR long gmtOffset = 0;
RTC_DATA_ATTR int daylightOffset = 3600;

RTC_DATA_ATTR float lastTemperature = 0.0;
RTC_DATA_ATTR float lastHumidity = 0.0;

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);


String getTimeStamp(){
  struct tm timeinfo;
  char timeString[80];

  getLocalTime(&timeinfo);
  strftime(timeString, sizeof(timeString), "%A, %B %d %Y %H:%M:%S", &timeinfo);

  return timeString;
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
    StaticJsonDocument<384> doc;

    if(WiFi.status()== WL_CONNECTED){
      Serial.println("Connected");
      float currentTemperature = dht.readTemperature();
      float currentHumidity = dht.readHumidity();
      boolean isChanged = false;
      String json = "";

      if (currentTemperature - lastTemperature != 0.0){
        isChanged = true;

        JsonObject doc_0 = doc.createNestedObject();

        doc_0["sensor_id"] = sensorId;
        doc_0["date_time"] = getTimeStamp();
        doc_0["m_type"] = "temperature";
        doc_0["measurement"] = String(currentTemperature);

        lastTemperature = currentTemperature;

      }

      if (currentHumidity - lastHumidity != 0.0){
        isChanged = true;
        JsonObject doc_1 = doc.createNestedObject();

        doc_1["sensor_id"] = sensorId;
        doc_1["date_time"] = getTimeStamp();
        doc_1["m_type"] = "humidity";
        doc_1["measurement"] = String(currentHumidity);

        lastHumidity = currentHumidity;
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