#include <Arduino.h>
#include "config.h"
#include "wifi_manager.h"
#include "imu_sensor.h"
#include "udp_client.h"

WiFiManager wifi;
IMUSensor imu;
UDPClient udp(UDP_HOST, UDP_PORT);

unsigned long lastReadTime = 0;
unsigned int bufferIndex = 0;
uint8_t buffer[PACKET_SIZE];

void setup() {
    Serial.begin(115200);
    wifi.connect(WIFI_SSID, WIFI_PASSWORD);
    if (!imu.begin()) {
        Serial.println("Failed to find MPU6050 chip");
        while (1) delay(10);
    }
    lastReadTime = millis();
}

void loop() {
    if (bufferIndex < PACKET_SIZE) {
        unsigned long now = millis();
        if (now - lastReadTime >= DATA_READ_TIME) {
            imu.readToBuffer(buffer, bufferIndex);
            lastReadTime = now;
        }
    } else {
        udp.send(buffer, PACKET_SIZE);
        bufferIndex = 0;
    }
}