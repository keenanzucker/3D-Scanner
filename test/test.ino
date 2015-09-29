#include <Servo.h>

Servo botservo;  // create servo object to control a servo
Servo topservo;
int cm = 0;
byte i; // variables to store position of each servo
byte j;

void setup() {
  botservo.attach(9);   // attaches servos to respective pins
  topservo.attach(10);
  Serial.begin(9600);   // open serial connection
  topservo.write(180);  // reset position of servos
  botservo.write(0);
  delay(1000);
}

void loop() {
  for(i = 92; i >= 70; i-=1) { // sweep top servo
    topservo.write(i); // move servo to next position
    delay(100);

    if(i%2 == 0) { // alternate direction of pan servo sweept servo
      for(j=40; j <= 96; j+=1) {
        int sensorValue = analogRead(A0); // Convert IR sensor to distance:
        cm = 10650.08 * pow(sensorValue,-0.935) - 8;
        Serial.print(j); //print out data on servo positions and ir distance
        Serial.print(",");
        Serial.print(i);
        Serial.print(",");
        Serial.println(cm);

        botservo.write(j); // move servo to next position
        delay(20);
      }
    }
    else {
      for(j=96; j >= 40; j-=1) {
        int sensorValue = analogRead(A0); // Convert IR sensor to distance:
        cm = 10650.08 * pow(sensorValue,-0.935) - 8;
        Serial.print(j); //print out data on servo positions and ir distance
        Serial.print(",");
        Serial.print(i);
        Serial.print(",");
        Serial.println(cm);

        botservo.write(j); //move servo to next position
        delay(20);
      }
    }
  }
}
