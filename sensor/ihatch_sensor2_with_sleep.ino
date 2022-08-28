#include <WiFi.h>
#include <HTTPClient.h>

#include <Adafruit_Sensor.h>
#include <DHT.h>

#include "time.h"


#define uS_TO_S_FACTOR 1000000
#define TIME_TO_SLEEP  900

RTC_DATA_ATTR const char* ssid = "Rampage";
RTC_DATA_ATTR const char* password = "Z0Ybuguv123";
RTC_DATA_ATTR String url = "http://51.142.124.189:5000/log_measurement";

RTC_DATA_ATTR String sensorId = "testing";

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
  Serial.begin(9600);
  dht.begin();
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

    if(WiFi.status()== WL_CONNECTED){

      float currentTemperature = dht.readTemperature();
      float currentHumidity = dht.readHumidity();

      if (currentTemperature - lastTemperature != 0.0){
        WiFiClient client;
        HTTPClient http;

        http.begin(client, url);

        http.addHeader("Content-Type", "application/json");

        responseCode = http.POST("{\"sensor_id\":\"" + sensorId + "\",\"date_time\":\"" + getTimeStamp() + "\",\"temperature\":\"" + currentTemperature + "\"}");

        lastTemperature = currentTemperature;
        http.end();
      }

      if (currentHumidity - lastHumidity != 0.0){
        WiFiClient client;
        HTTPClient http;

        http.begin(client, url);

        http.addHeader("Content-Type", "application/json");

        responseCode = http.POST("{\"sensor_id\":\"" + sensorId + "\",\"date_time\":\"" + getTimeStamp() + "\",\"humidity\":\"" + currentHumidity + "\"}");

        lastHumidity = currentHumidity;
        http.end();
      }

      // sleep if post was successful, otherwise increase disconnected counter
      if (responseCode = 200)
        esp_deep_sleep_start();
      } else {
        disconnectedCounter ++;
      }
    }
    disconnectedCounter ++;
  }

void loop(){}