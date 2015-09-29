#include <Servo.h>
 
Servo tiltServo;  
Servo panServo;
    
int tiltRange = 40;
int panRange = 60;

int posTilt = 100;
int posPan = -30;
const int analogInPin = A0;  
float sensorValue, inches, cm;   
 

 
void setup() {
    tiltServo.attach(10);  
    panServo.attach(9);
    Serial.begin(9600);
    Serial.println("BEGIN");
    Serial.flush();
}
 
void loop() {
  
  for (posTilt = 90; posTilt <= 90 + tiltRange; posTilt += 1) { 
    tiltServo.write(posTilt);              
    delay(100);   

    for (posPan = 0; posPan <= 0 + panRange; posPan +=1) {
     panServo.write(posPan);
     delay(20);
     
     sensorValue = analogRead(analogInPin);
     cm = 10650.08 * pow(sensorValue,-0.935) - 8;
     
     Serial.print(posPan);
     Serial.print(" ");
     Serial.print(posTilt);
     Serial.print(" ");
     Serial.println(cm);

    }
        
  }
  
}


