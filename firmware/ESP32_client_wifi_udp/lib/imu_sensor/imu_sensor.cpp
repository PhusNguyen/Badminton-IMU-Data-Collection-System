#include "imu_sensor.h"

bool IMUSensor::begin() {
    if (!mpu.begin()) return false;
    mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
    mpu.setGyroRange(MPU6050_RANGE_2000_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
    return true;
}

void IMUSensor::readToBuffer(uint8_t* buffer, unsigned int& index) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    storeFloatBytes(a.acceleration.x, buffer, index);
    storeFloatBytes(a.acceleration.y, buffer, index);
    storeFloatBytes(a.acceleration.z, buffer, index);
    storeFloatBytes(g.gyro.x, buffer, index);
    storeFloatBytes(g.gyro.y, buffer, index);
    storeFloatBytes(g.gyro.z, buffer, index);
}

void IMUSensor::storeFloatBytes(float value, uint8_t* buffer, unsigned int& index) {
    uint8_t* bytePtr = reinterpret_cast<uint8_t*>(&value);
    for (int i = 3; i >= 0; i--) {
        buffer[index++] = bytePtr[i];
    }
}