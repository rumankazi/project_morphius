#include <SoftwareSerial.h>
#include <Servo.h>

int E=6;  // Enable Pin for motor 1
SoftwareSerial mySerial(8,9);   //BLE RX||TX
Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
int i = 0;
int pos = 0;    // variable to store the servo position
char c;
void setup()
{
myservo.attach(3);       //servo motor pwm given from this port
mySerial.begin(9600);   //BLE serial communication baud rate set
Serial.begin(9600);   
delay(100);
pinMode(4, OUTPUT);//pins 4&5 for l293d: controlling direction of motion
pinMode(5, OUTPUT);
pinMode(E, OUTPUT);//pwm providing output
}
void loop()
{
if (Serial.available()>0)
mySerial.write(Serial.read());   
if (mySerial.available()>0)  //checks serial data received from app via BLE
{
c = mySerial.read();
if(c == 3)  //for arm control of the base module
{
  Serial.write(c);
  for (pos = 0; pos <= 180; pos += 1) 
    { 
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
    }
  for (pos = 180; pos >= 0; pos -= 1) 
  { 
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}
if (c == 1) //for reverse motion 
{
 for(i=0;i<100;i=i+5)
  {
  analogWrite(E, i); //pwm used for smoother operation
  digitalWrite(5,LOW);
  digitalWrite(4,HIGH);
    }
  Serial.write(i); //prints on terminal
  c = 5;
}
delay(1000);
Serial.write(i);
if (c == 0) //for forward motion
{
  for(i=0;i<150;i=i+5)
  {
  analogWrite(E, i);
  digitalWrite(5,HIGH);
  digitalWrite(4,LOW);
    }
  Serial.write(i);
  c = 5;
}
if (c == 2)  //for stopping the module
{
  for(; i>=0; i = i-10)
  {
    analogWrite(E, i);
  } 
  digitalWrite(4,LOW);
  digitalWrite(5,LOW);
}
}
}
