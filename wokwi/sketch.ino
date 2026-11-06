/*
  Cerradura por Gestos — Miguel Ruiz (Clase 14)
  ESP32 en Wokwi que abre o cierra una cerradura según el gesto reconocido en la app.

  Pega este código en sketch.ino de tu copia del proyecto:
  https://wokwi.com/projects/377066087789108225

  Mensaje esperado (tópico cerradura_miguelruiz):  {"gesto": "Abre"}  o  {"gesto": "Cierra"}
  - Abre   -> servo (pin 13) a 180°, LED pin 18 encendido, LED pin 5 apagado
  - Cierra -> servo a 0°,           LED pin 18 apagado,   LED pin 5 encendido
*/

#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ESP32Servo.h>

// ── Debe coincidir con la app (panel lateral → CONEXIÓN MQTT) ──
const char* ssid        = "Wokwi-GUEST";
const char* password    = "";
const char* mqtt_server = "broker.mqttdashboard.com";
const int   mqtt_port   = 1883;
const char* TOPICO      = "cerradura_miguelruiz";

const int PIN_ABIERTO = 18;
const int PIN_CERRADO = 5;
const int PIN_SERVO   = 13;

WiFiClient espClient;
PubSubClient client(espClient);
Servo cerrojo;

void setup_wifi() {
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password, 6);   // Wokwi-GUEST usa el canal 6
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
}

void abrir() {
  digitalWrite(PIN_ABIERTO, HIGH);
  digitalWrite(PIN_CERRADO, LOW);
  cerrojo.write(180);
  Serial.println("-> Cerradura ABIERTA");
}

void cerrar() {
  digitalWrite(PIN_ABIERTO, LOW);
  digitalWrite(PIN_CERRADO, HIGH);
  cerrojo.write(0);
  Serial.println("-> Cerradura CERRADA");
}

void callback(char* topic, byte* payload, unsigned int length) {
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, payload, length);
  if (error) {
    Serial.print("JSON inválido: ");
    Serial.println(error.f_str());
    return;
  }

  String gesto = doc["gesto"] | "";
  gesto.trim();
  gesto.toLowerCase();
  Serial.print("Gesto recibido: ");
  Serial.println(gesto);

  if (gesto == "abre") {
    abrir();
  } else if (gesto == "cierra") {
    cerrar();
  } else {
    Serial.println("-> Gesto no reconocido");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando al broker MQTT...");
    // ID único para no chocar con otras simulaciones conectadas al mismo broker
    String clientId = "esp32-cerradura-miguelruiz-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println(" conectado");
      client.subscribe(TOPICO);
      Serial.print("Escuchando el tópico: ");
      Serial.println(TOPICO);
    } else {
      Serial.print(" falló, rc=");
      Serial.print(client.state());
      Serial.println(" (reintento en 5 s)");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ABIERTO, OUTPUT);
  pinMode(PIN_CERRADO, OUTPUT);
  cerrojo.setPeriodHertz(50);
  cerrojo.attach(PIN_SERVO, 500, 2400);
  cerrar();   // empieza cerrada
  randomSeed(micros());
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
