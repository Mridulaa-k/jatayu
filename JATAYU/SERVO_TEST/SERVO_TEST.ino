#include <ESP32Servo.h>

Servo myServo;  // Create a Servo object
int servoPin = 4;  // Define the pin where the servo is connected

void setup() {
  myServo.attach(servoPin);  // Attach the servo to GPIO5
}

void loop() {
  myServo.write(0);
  delay(2000);
  myServo.write(90);
  delay(2000);
  myServo.write(180);
  delay(2000);
}