
#include "DHT.h"
#include <SPI.h>
#include <WiFi.h>

#define DHTPIN 4

#define DHTTYPE DHT11

DHT dht(DHTPIN,DHTTYPE);


float humidityData;
float temperatureData;
const char* ssid = "akshay";
//password of your WPA Network
const char* password = "alskdjfhg";
char server[] = "192.168.43.242";
WiFiClient client; 

/* Setup for Ethernet and RFID */
//WiFiServer server(80);
void setup() {
  Serial.begin(9600);
  dht.begin();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}
//------------------------------------------------------------------------------


/* Infinite Loop */
void loop(){
  humidityData = dht.readHumidity();
  temperatureData = dht.readTemperature(); 
  Sending_To_phpmyadmindatabase(); 
  delay(1000); // interval
}


  void Sending_To_phpmyadmindatabase()   //CONNECTING WITH MYSQL
 {
  //WiFiClient client = server.available();
   if (client.connect(server, 80)) {
    Serial.println("New Client.");          // print a message out in the serial port
    String currentLine = ""; 
    Serial.println("connected");
    // Make a HTTP request:
    Serial.print("GET /testcode/dht.php?hum=");
    client.print("GET /testcode/dht.php?hum=");     //YOUR URL
    Serial.print(humidityData);
    client.print(humidityData);
    client.print("&temp=");
    Serial.print("&temp=");
    client.print(temperatureData);
    Serial.println(temperatureData);
    client.print(" ");      //SPACE BEFORE HTTP/1.1
    client.print("HTTP/1.1");
    client.println();
    client.println("Host: 192.168.1.44");
    client.println("Connection: close");
    client.println();
      
    
    
  } else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
 }
