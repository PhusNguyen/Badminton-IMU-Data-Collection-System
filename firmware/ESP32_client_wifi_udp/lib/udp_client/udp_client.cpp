#include "udp_client.h"

UDPClient::UDPClient(const char* host, int port) : host(host), port(port) {}

void UDPClient::send(const uint8_t* buffer, size_t size) {
    udp.beginPacket(host, port);
    udp.write(buffer, size);
    udp.endPacket();
}