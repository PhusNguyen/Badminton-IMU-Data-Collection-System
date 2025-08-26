/* Include all the necessary libraries */
#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <WiFi.h>

/* Define the WiFi credentials */
// const char* ssid = "Kopite";
// const char* password = "Youwillneverwalkalone";
const char* ssid = "Luffy";
const char* password = "$CCTN1991**";

/* IP address to send data to*/
// const char* host = "10.156.82.201";
const char* host = "192.168.0.208";
const int port = 44444;

/* Create an instance of the MPU6050 and wifi library */
Adafruit_MPU6050 mpu;
WiFiUDP udp;

/* Time variables*/
unsigned long StartTime, StartTime_data;
unsigned long CurrentTime, CurrentTime_data;

/* Data transfer variables */
unsigned int bufferIndex = 0;
unsigned int megaData = 0;
#define DATA_READ_TIME 10
#define PACKET_SIZE 240

/* Create buffer */
uint8_t buffer[PACKET_SIZE];

/* Prototype functions */
void storeFloatBytes(float sensorValue, uint8_t *buffer, unsigned int &index);

void setup() 
{
    Serial.begin(115200);
    while (!Serial) 
    {
        delay(10); // wait for serial port to connect
    }

    /* Initialize the MPU6050 sensor */
    if (!mpu.begin())
    {
        Serial.println("Failded to find MPU6050 chip");
        while (1)
        {
            delay(10); // halt the program if sensor initialization fails
        }
    }
    Serial.println("MPU6050 Found!");

    /* Set the accelerometer and gyro range */
    mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
    Serial.print("Accelerometer range set to: ");
    switch (mpu.getAccelerometerRange()) 
    {
        case MPU6050_RANGE_2_G:
            Serial.println("±2g");
            break;
        case MPU6050_RANGE_4_G:
            Serial.println("±4g");
            break;
        case MPU6050_RANGE_8_G:
            Serial.println("±8g");
            break;
        case MPU6050_RANGE_16_G:
            Serial.println("±16g");
            break;
        default:
            Serial.println("Unknown range");
            break;
    }

    mpu.setGyroRange(MPU6050_RANGE_2000_DEG);
    Serial.print("Gyro range set to: ");
    switch (mpu.getGyroRange()) 
    {
        case MPU6050_RANGE_250_DEG:
            Serial.println("±250°/s");
            break;
        case MPU6050_RANGE_500_DEG:
            Serial.println("±500°/s");
            break;
        case MPU6050_RANGE_1000_DEG:
            Serial.println("±1000°/s");
            break;
        case MPU6050_RANGE_2000_DEG:
            Serial.println("±2000°/s");
            break;
        default:
            Serial.println("Unknown range");
            break;
    }

    /* Set filter bandwidth */
    mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
    Serial.print("Filter bandwidth set to: ");
    switch (mpu.getFilterBandwidth()) 
    {        case MPU6050_BAND_260_HZ:
            Serial.println("260 Hz");
            break;
        case MPU6050_BAND_184_HZ:
            Serial.println("184 Hz");
            break;
        case MPU6050_BAND_94_HZ:
            Serial.println("94 Hz");
            break;
        case MPU6050_BAND_44_HZ:
            Serial.println("44 Hz");
            break;
        case MPU6050_BAND_21_HZ:    
            Serial.println("21 Hz");
            break;
        case MPU6050_BAND_10_HZ:
            Serial.println("10 Hz");
            break;
        case MPU6050_BAND_5_HZ:
            Serial.println("5 Hz");
            break;
        default:
            Serial.println("Unknown range");
    }

    /* Connect to WiFi */
    WiFi.begin(ssid, password);
    Serial.println("");

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.println("");
    delay(100);

    StartTime_data = millis();
}

void loop()
{
  /* Read 1 megaData every 10ms 10 times repeatedly */
  while (bufferIndex < PACKET_SIZE)
  {
    /* Get the current time */
    CurrentTime_data = millis();
    if (CurrentTime_data - StartTime_data >= DATA_READ_TIME)
    {
        /* Read sensor data */
        sensors_event_t a, g, temp;
        mpu.getEvent(&a, &g, &temp);

        /* Split float values into bytes and store in buffer */
        storeFloatBytes(a.acceleration.x, buffer, bufferIndex);
        storeFloatBytes(a.acceleration.y, buffer, bufferIndex);
        storeFloatBytes(a.acceleration.z, buffer, bufferIndex);
        storeFloatBytes(g.gyro.x, buffer, bufferIndex);
        storeFloatBytes(g.gyro.y, buffer, bufferIndex);
        storeFloatBytes(g.gyro.z, buffer, bufferIndex);

        StartTime_data = CurrentTime_data; // Reset start time
      }
  }
  /* Initialize UDP protocol to transmit data */
  udp.beginPacket(host, port);
  udp.write(buffer, PACKET_SIZE);
  udp.endPacket();

  /* Reset buffer index */
  bufferIndex = 0;
}

/* Function to extract bytes from float and store in buffer */
void storeFloatBytes(float sensorValue, uint8_t *buffer, unsigned int &index)
{
    uint8_t *bytePtr = reinterpret_cast<uint8_t*>(&sensorValue);
    for (int i = 3; i >= 0; i--)
    {
        buffer[index++] = bytePtr[i];
        if (index >= PACKET_SIZE) 
        {
            break; // Ensure we don't exceed the buffer size
        }
    }
}