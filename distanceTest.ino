const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
float sensorValue, inches, cm;    //Must be of type float for pow()

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(analogInPin);
//  inches = 4192.936 * pow(sensorValue,-0.935) - 3.937;
  cm = 10650.08 * pow(sensorValue,-0.935) - 8;
  delay(100);
  //Serial.print("Centimeters: ");
  Serial.println(cm);
}
