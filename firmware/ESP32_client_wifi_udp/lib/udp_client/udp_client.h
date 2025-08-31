#pragma once
#include <WiFiUdp.h>

class UDPClient {
public:
    UDPClient(const char* host, int port);
    void send(const uint8_t* buffer, size_t size);
private:
    WiFiUDP udp;
    const char* host;
    int port;
};