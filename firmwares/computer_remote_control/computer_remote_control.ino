/*
//    ROFI remove control program. Version 1.0
//      This program allows ROFI to be actuated remotely (via USB cable) by a the Robot 
//      Poser application running on a desktop computer.
//
//    Copyright (C) 2012  Jonathan Dowdall, Project Biped (www.projectbiped.com)
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <Servo.h> 

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Constants
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
const int  pingPin                   = 4;                           // digitial pin number on the arduino board that has the ping data line plugged into it
const int  numberOfServos            = 12;                          // there are 12 servos 
const int  messageLength             = 3 + numberOfServos * 2;      // the number of bytes in a message from the control program  

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//pin assignments
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*
right leg
   Pin
    22 : ankle                      servo 0
    24 : lower leg                  servo 1
    26 : knee                       servo 2
    28 : middle leg                 servo 3    
    30 : upper leg                  servo 4
    32 : hip                        servo 5    
    
left leg
   Pin
    38 : ankle                      servo 6
    40 : lower leg                  servo 7
    42 : knee                       servo 8  
    44 : middle leg                 servo 9    
    46 : upper leg                  servo 10
    48 : hip                        servo 11   
*/
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
int pins[numberOfServos] = {22,24,26,28,30,32,38,40,42,44,46,48};  // the pin for each servo 

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Variables
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Servo servos[numberOfServos];  // create servo object to control a servo 

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void setup()
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
{
  //initialize the servos
  InitializeServos();  
  
  //establist a connection with the remote controller (the poser application)
  EstablistConnection();
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void EstablistConnection()
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
{
  //wait for a second to begin (keeps the communication line open in case a new program is being downloaded)
  delay(1000);  
  
  //start up the communication
  Serial.begin(9600);

  //buffer to hold the incoming message
  int inputBuffer[40];
  
  //broadcast our id until someone responds
  while(true)
  {
    //broadcast id
    Serial.print("ROFI");  
    
    //wait for a bit
    delay(100);  
    
    //look for a response
    if(Serial.available() > 1)
    {
      for(int b = 0; b < 2; b++)
        inputBuffer[b] = Serial.read();
        
      // make sure someone friendly is on the line
      if(inputBuffer[0] == (int)'h' && inputBuffer[1] == (int)'i')
      {
            Serial.print("connected");  
            break;
      }
    }      
  }  
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void InitializeServos()
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
{  
  // Assign the correct pin to each servo.
  for(int s = 0; s < numberOfServos; s++)
    servos[s].attach(pins[s]);  
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void loop()
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
{  
  // check to see if there are enough bytes on the serial line for a message
  if (Serial.available() >= messageLength) 
    // read the incoming message
    if( ReadMessage() )    
      // respond to the computer that is controlling the robot
      SendResponse();      
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
bool ReadMessage()
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
{
  // buffer to hold the incoming message
  int inputBuffer[100];

  // read the message
  int index = 0;
  while(Serial.available() > 0)
  {
    inputBuffer[index] = Serial.read();
    index++;
  }

  // make sure the message starts with "cmd" ... otherwise it isn't a valid message
  if(inputBuffer[0] == (int)'c' && inputBuffer[1] == (int)'m' && inputBuffer[2] == (int)'d')
  {
    //set the servo positions
    for (int servo = 0; servo < numberOfServos; servo++)
    {      
      // each servo position is sent as a 2 byte value (high byte, low byte) integer (from -32,768 to 32,767)
      // this number is encoding the angle of the servo. The number is 100 * the servo angle.  This allows for the
      // storage of 2 significant digits(i.e. the value can be from -60.00 to 60.00 and every value in between).
      // Also remember that the servos have a range of 120 degrees. The angle is written in positions
      // which range from a minimum of 800 (-60 degrees) and go to a maximum of 2200 (60 degrees)
      int value = word(inputBuffer[servo*2 + 1 + 3], inputBuffer[servo*2 + 0 + 3]);      
      
      // flip for the left leg.
      if(servo >= numberOfServos/2)
        value = map(value, -6000,6000,6000,-6000);
      
      servos[servo].write(map(value, -6000,6000,800,2200));              // tell servo to go to position in variable 'pos' 
    }

    // a valid messgae was received    
    return true;
  }  
  else
    // the message wasn't valid
    return false;  
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void SendResponse()
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
{
  // Measure the distance 
  //unsigned int distance = MeasureDistance();
  unsigned int distance = 0;
  
  // Send the distance back (cast it to a byte array ... an int has a high and low byte).
  Serial.write((uint8_t*)&distance, 2);
  
  // Send the robot status (0 = happy).
  Serial.write((byte)0);

  // End the response.
  Serial.print("done");  
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// some of the code below was found on http://arduino.cc/en/Tutorial/Ping?from=Tutorial.UltrasoundSensor.  Thanks Arduino guys!
//  credit:
//    by David A. Mellis
//    modified 30 Aug 2011
//    by Tom Igoe
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
long MeasureDistance()
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
{
  // establish variables for duration of the ping, 
  // and the distance result in inches and centimeters:
  long duration, inches, cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);

  // The same pin is used to read the signal from the PING))): a HIGH
  // pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(pingPin, INPUT);
  duration = pulseIn(pingPin, HIGH);

  // convert the time into a distance
  inches = microsecondsToInches(duration);
  cm = microsecondsToCentimeters(duration);

  return inches;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
long microsecondsToInches(long microseconds)
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
{
  // According to Parallax's datasheet for the PING))), there are
  // 73.746 microseconds per inch (i.e. sound travels at 1130 feet per
  // second).  This gives the distance travelled by the ping, outbound
  // and return, so we divide by 2 to get the distance of the obstacle.
  // See: http://www.parallax.com/dl/docs/prod/acc/28015-PING-v1.3.pdf
  return microseconds / 74 / 2;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
long microsecondsToCentimeters(long microseconds)
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
{
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}
