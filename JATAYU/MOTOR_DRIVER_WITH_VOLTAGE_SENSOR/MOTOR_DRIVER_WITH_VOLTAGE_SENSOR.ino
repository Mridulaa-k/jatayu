#define MOTOR_IN1 18
#define MOTOR_IN2 19
#define MOTOR_EN 5
#define VOLTAGE_PIN 33

void setup() {
  Serial.begin(115200);
  pinMode(MOTOR_IN1,OUTPUT);
  pinMode(MOTOR_IN2,OUTPUT);
  pinMode(MOTOR_EN,OUTPUT);

  digitalWrite(MOTOR_IN1,LOW);
  digitalWrite(MOTOR_IN2,LOW);
  analogWrite(MOTOR_EN,255);
}

void loop() {
    float voltage = readVoltage();
    Serial.print("Voltage: ");
    Serial.println(voltage);
    delay(5000);
    if (voltage<6.0){
      Serial.println("Moving Forward");
      digitalWrite(MOTOR_IN1, HIGH);
      digitalWrite(MOTOR_IN2, LOW);
    }
    else{
      Serial.println("Stopping Motor");
      digitalWrite(MOTOR_IN1, LOW);
      digitalWrite(MOTOR_IN2, LOW);
    }
}

float readVoltage() {
    int sensorValue = analogRead(VOLTAGE_PIN);
    float voltage = (sensorValue / 1023.0) * 3.3; // Convert ADC value to voltage (ESP8266 uses 3.3V reference)
    return voltage;
}