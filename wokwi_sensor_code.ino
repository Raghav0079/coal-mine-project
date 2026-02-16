/*
  Coal Mine Safety Helmet Sensor - Wokwi Example
  
  This Arduino code simulates mining helmet sensors and sends data via MQTT
  Use this code in your Wokwi project to connect to the dashboard
  
  Required libraries in Wokwi:
  - WiFi
  - PubSubClient (for MQTT)
  - ArduinoJson
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// WiFi Configuration (Wokwi automatically provides this)
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// MQTT Configuration - Match these with your dashboard config
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "wokwi/coalmine/sensors";

// Sensor pins (adjust based on your Wokwi circuit)
const int CO2_PIN = A0;      // CO2 sensor analog pin
const int CH4_PIN = A1;      // Methane sensor analog pin
const int O2_PIN = A2;       // Oxygen sensor analog pin
const int H2S_PIN = A3;      // H2S sensor analog pin
const int TEMP_PIN = A4;     // Temperature sensor pin
const int HUMIDITY_PIN = A5; // Humidity sensor pin

// Helmet ID (change for different helmets)
const char* helmet_id = "HELMET_001";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastSensorRead = 0;
const unsigned long SENSOR_INTERVAL = 2000; // Send data every 2 seconds

void setup() {
  Serial.begin(115200);
  
  // Initialize sensor pins
  pinMode(CO2_PIN, INPUT);
  pinMode(CH4_PIN, INPUT);
  pinMode(O2_PIN, INPUT);
  pinMode(H2S_PIN, INPUT);
  pinMode(TEMP_PIN, INPUT);
  pinMode(HUMIDITY_PIN, INPUT);
  
  // Connect to WiFi
  setupWiFi();
  
  // Setup MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(mqttCallback);
  
  Serial.println("Coal Mine Safety Helmet Sensor Ready!");
}

void loop() {
  // Maintain MQTT connection
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
  
  // Read and send sensor data
  unsigned long now = millis();
  if (now - lastSensorRead >= SENSOR_INTERVAL) {
    readAndSendSensorData();
    lastSensorRead = now;
  }
  
  delay(100);
}

void setupWiFi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    // Create a random client ID
    String clientId = "WokwiHelmet-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void readAndSendSensorData() {
  // Read analog values and convert to sensor readings
  // These conversions are simplified - adjust based on your actual sensors
  
  float co2 = map(analogRead(CO2_PIN), 0, 4095, 300, 1000) + random(-20, 20);
  float ch4 = (analogRead(CH4_PIN) / 4095.0) * 3.0 + (random(-10, 10) / 100.0);
  float o2 = 20.9 - (analogRead(O2_PIN) / 4095.0) * 2.0 + (random(-5, 5) / 100.0);
  float h2s = map(analogRead(H2S_PIN), 0, 4095, 0, 20) + random(-2, 2);
  float temp = map(analogRead(TEMP_PIN), 0, 4095, 20, 40) + (random(-10, 10) / 10.0);
  float humidity = map(analogRead(HUMIDITY_PIN), 0, 4095, 40, 90) + random(-5, 5);
  
  // Create JSON payload
  DynamicJsonDocument doc(1024);
  doc["helmet_id"] = helmet_id;
  doc["co2"] = round(co2 * 100) / 100.0;
  doc["ch4"] = round(ch4 * 100) / 100.0;
  doc["o2"] = round(o2 * 100) / 100.0;
  doc["h2s"] = round(h2s * 100) / 100.0;
  doc["temp"] = round(temp * 100) / 100.0;
  doc["humidity"] = round(humidity * 100) / 100.0;
  doc["timestamp"] = millis();
  
  // Convert to string
  String jsonString;
  serializeJson(doc, jsonString);
  
  // Publish to MQTT
  if (client.publish(mqtt_topic, jsonString.c_str())) {
    Serial.println("Sensor data sent: " + jsonString);
  } else {
    Serial.println("Failed to send sensor data");
  }
}
