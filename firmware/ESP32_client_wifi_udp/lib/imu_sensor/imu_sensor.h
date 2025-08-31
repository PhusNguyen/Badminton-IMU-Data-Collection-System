#pragma once
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

class IMUSensor {
public:
    bool begin();
    void readToBuffer(uint8_t* buffer, unsigned int& index);
private:
    Adafruit_MPU6050 mpu;
    void storeFloatBytes(float value, uint8_t* buffer, unsigned int& index);
};