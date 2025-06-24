#define MOTOR_IN1 18
#define MOTOR_IN2 19
#define MOTOR_EN 5


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
  // Rotate Motor Forward
  Serial.println("Motor Forward");
  digitalWrite(MOTOR_IN1, HIGH);
  digitalWrite(MOTOR_IN2, LOW);
  delay(2000); // Run forward for 2 seconds
  
   // Stop the Motor
  Serial.println("Motor Stop");
  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, LOW);
  delay(2000); // Pause for 2 seconds

  // Rotate Motor Backward
  Serial.println("Motor Backward");
  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, HIGH);
  delay(2000); // Run backward for 2 seconds

  // Stop the Motor
  Serial.println("Motor Stop");
  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, LOW);
  delay(2000); // Pause for 2 seconds
}
