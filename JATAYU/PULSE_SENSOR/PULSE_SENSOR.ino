#define USE_ARDUINO_INTERRUPTS true
#include <PulseSensorPlayground.h>

// Constants
const int PULSE_SENSOR_PIN = 34;  // ESP32 ADC pin (Use any ADC1 pin: 32-39)
const int LED_PIN = 2;            // ESP32 built-in LED (or change as needed)
const int THRESHOLD = 550;        // Adjust based on signal quality

// Create PulseSensor object
PulseSensorPlayground pulseSensor;

void setup() {
  Serial.begin(115200);  // Higher baud rate for ESP32
  pinMode(LED_PIN, OUTPUT);

  // Configure PulseSensor
  pulseSensor.analogInput(PULSE_SENSOR_PIN);
  pulseSensor.blinkOnPulse(LED_PIN);
  pulseSensor.setThreshold(THRESHOLD);

  // Initialize PulseSensor
  if (pulseSensor.begin()) {
    Serial.println("PulseSensor initialized successfully!");
  } else {
    Serial.println("Failed to initialize PulseSensor.");
  }
}

void loop() {
  // Get BPM value
  int currentBPM = pulseSensor.getBeatsPerMinute();

  // Check if heartbeat detected
  if (pulseSensor.sawStartOfBeat()) {
    Serial.println("♥ Heartbeat detected!");
    Serial.print("BPM: ");
    Serial.println(currentBPM);
    digitalWrite(LED_PIN, HIGH); // Blink LED
    delay(50);
    digitalWrite(LED_PIN, LOW);
  }

  delay(10);  // Sampling delay
}
