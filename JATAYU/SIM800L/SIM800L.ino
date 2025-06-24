#include <HardwareSerial.h>

#define SIM800_RX 4  // SIM800 TX -> ESP32 RX
#define SIM800_TX 2  // SIM800 RX -> ESP32 TX (Use 1K resistor)

HardwareSerial sim800(1);  // Create virtual "SoftwareSerial" using UART1

void setup() {
    Serial.begin(115200);
    sim800.begin(9600, SERIAL_8N1, SIM800_RX, SIM800_TX);

    Serial.println("Initializing SIM800L...");
    delay(1000);

    sim800.println("AT");  // Check connection
    delay(500);
    sim800.println("AT+CMGF=1");  // Set SMS mode to text
    delay(500);
    sim800.println("AT+CMGS=\"+917904042868\"");  // Replace with your phone number
    delay(500);
    sim800.print("Hello from ESP32 + SIM800L!");  // SMS message
    delay(500);
    sim800.write(26);  // Send message (CTRL+Z)
}

void loop() {
    while (sim800.available()) {
        Serial.write(sim800.read());  // Print SIM800L response
    }
}