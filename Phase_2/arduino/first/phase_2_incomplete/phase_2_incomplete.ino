#include <SoftwareSerial.h>
#include <Servo.h>

SoftwareSerial mySerial(8,9);
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
char c;
void setup()
{
myservo.attach(3);
mySerial.begin(9600);   
Serial.begin(9600);   
delay(100);
pinMode(4, OUTPUT);
pinMode(5, OUTPUT);
}
void loop()
{
if (Serial.available()>0)
mySerial.write(Serial.read());
if (mySerial.available()>0)
{
c = mySerial.read();
if(c == 'F')
{
  Serial.write(c);
  for (pos = 0; pos <= 180; pos += 1) 
    { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
    }
  for (pos = 180; pos >= 0; pos -= 1) 
  { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}
if (c == 'A')
{
  digitalWrite(4,HIGH);
  digitalWrite(5,LOW);
}
if (c == 'B')
{
  digitalWrite(5,HIGH);
  digitalWrite(4,LOW);
}
if (c == 'C')
{
  digitalWrite(4,LOW);
  digitalWrite(5,LOW);
}
}
}
