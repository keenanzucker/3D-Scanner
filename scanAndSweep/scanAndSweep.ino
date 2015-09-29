#include <Servo.h>
 
Servo tiltServo;  
Servo panServo;
    
int tiltRange = 20;
int panRange = 60;

int posTilt = 100;
int posPan = -30;
const int analogInPin = A0;  
float sensorValue, inches, cm;   
 

 
void setup() {
    tiltServo.attach(10);  
    panServo.attach(9);
    Serial.begin(9600);
    Serial.print("BEGIN");
    Serial.flush();
}
 
void loop() {
  
  for (posTilt = 100; posTilt <= 100 + tiltRange; posTilt += 1) { 
    tiltServo.write(posTilt);              
    delay(100);   

    for (posPan = -30; posPan <= -30 + panRange; posPan +=1) {
     
     panServo.write(posPan);
     delay(15);
     
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


