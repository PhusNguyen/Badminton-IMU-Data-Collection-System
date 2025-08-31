#pragma once
#include <WiFi.h>

class WiFiManager {
public:
    void connect(const char* ssid, const char* password);
};