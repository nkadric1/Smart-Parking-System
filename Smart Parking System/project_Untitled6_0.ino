#include <MeMCore.h>
#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>

MeUltrasonicSensor ultrasonic_3(3);
MeLineFollower linefollower_2(2);
MeDCMotor motor_9(9);
MeDCMotor motor_10(10);

void move(int direction, int speed) {
  int leftSpeed = 0;
  int rightSpeed = 0;
  if(direction == 1) {
    leftSpeed = -speed;
    rightSpeed = -speed;
  } else if(direction == 2) {
    leftSpeed = speed;
    rightSpeed = speed;
  } else if(direction == 3) {
    leftSpeed = speed;
    rightSpeed =- speed;
  } else if(direction == 4) {
    leftSpeed = -speed;
    rightSpeed = speed;
  }
  motor_9.run((9) == M1 ? -(leftSpeed) : (leftSpeed));
  motor_10.run((10) == M1 ? -(rightSpeed) : (rightSpeed));
}


#define THRESHOLD 500
#define SAFE_DISTANCE 15
#define SPEED 150

void setup() {
  pinMode(A7, INPUT);
  while(!((0 ^ (analogRead(A7) > 10 ? 0 : 1))))
  {
    _loop();
  }
  int i=0;
  while(1){
    if(i>=2)
    {
      i=0;
      while(1)
      {
        while(linefollower_2.readSensors() <= 2.000000){

        move(1, 100);

      }
      if(linefollower_2.readSensors() == 3.000000){
     
       if(ultrasonic_3.distanceCm() > 15)
       {
       
        while(linefollower_2.readSensors()==3.00000){
          move(1,100);

        }
       if(linefollower_2.readSensors()<=2.0000 && i==0){
          i++;
          move(4, 335 );
delay(368);
}
while(linefollower_2.readSensors()==3.00000 &&i==1){
  move(1,100);}
  if(linefollower_2.readSensors()<=2.00000 &&i==1){
    while(1)
    move(1,0);
}
       }
       else {
        i=0;
        while(linefollower_2.readSensors()==3.0000)
        move(1,100);
        while(linefollower_2.readSensors()<=2.00000){
          move(1,100);
        }
          if(linefollower_2.readSensors() == 3.000000){
     
       if(ultrasonic_3.distanceCm() > 15)
       {
        while(linefollower_2.readSensors()==3.00000 ){
          move(1,100);
        }
      if(linefollower_2.readSensors()<=2.0000){
          i++;
          move(4, 335 );
delay(368);
}
while(linefollower_2.readSensors()==3.00000 && i==1){
  move(1,100);}
  if(linefollower_2.readSensors()<=2.00000 && i==1){
    while(1)
    move(1,0);
}
       }
      }}}
      }
    }
   while(linefollower_2.readSensors() <= 2.000000){

        move(1, 80);

      }

      if(linefollower_2.readSensors() == 3.000000){
i++;
        move(4, 330);
while(linefollower_2.readSensors()!=0.00000);
      }
  }
_loop();
}

void _loop() {
}

void loop() {
  _loop();
}
