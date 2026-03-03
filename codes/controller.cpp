#include <Arduino.h>
#include <Ultrasonic.h>


const bool FORWARD = true;
const bool CW = true;
const bool BACKWARD = false;
const bool CCW = false;


class MOTOR
{
  public:
    uint8_t _pin1, _pin2; 

    MOTOR(uint8_t in_1, uint8_t in_2)
    {
      _pin1 = in_1;
      _pin2 = in_2;
    }
      
    void stop()
    {
      //this->on(!this->dir, 255);
      digitalWrite(_pin1, 1);
      digitalWrite(_pin2, 1);
    }



    void on(bool dir, uint8_t speed)
    {
      if(dir)
        {
          analogWrite(_pin1, speed);
          digitalWrite(_pin2, 0);
        }
      else
        {
          analogWrite(_pin2, speed);
          digitalWrite(_pin1, 0);
        }
    }

    void reverse()
    {
      uint8_t n = _pin1;
      _pin1 =_pin2;
      _pin2 = n;
    }
};


MOTOR motor_R(6, 5);
MOTOR motor_L(9, 10);

Ultrasonic sonar_L(12, 11);
Ultrasonic sonar_F(8, 7);
Ultrasonic sonar_R(3, 2);


void setup() 
{
  Serial.begin(115200);
}


void loop() 
{ 

  if (Serial.available()>1) 
      {
        char data[3]; 
        Serial.readBytes(data, 3);
      
        uint8_t key = data[0];
        uint8_t cmd = data[1];
        uint8_t val = data[2];


        switch(key)
              {

                case 0: //Right motor manual control
                      switch(cmd)
                      {
                        case 0: motor_L.on(BACKWARD, val); break;
                        case 1: motor_L.on(FORWARD, val); break;
                        case 2: motor_L.stop(); break;       
                        default: break;
                      }

                      break;

              
                case 1: //Left motor manual control
                      switch(cmd)
                      {
                        case 0: motor_R.on(BACKWARD, val); break;
                        case 1: motor_R.on(FORWARD, val); break;
                        case 2: motor_R.stop(); break;       
                        default: break;
                      }

                      break;

                      
                case 2: //Stop motors
                      motor_L.stop(); 
                      motor_R.stop(); 
                      break;

                case 3:
                      uint8_t l = sonar_L.read();
                      uint8_t f = sonar_F.read();
                      uint8_t r = sonar_R.read();
                      char dist[3];
  
                      dist[0] = l;
                      dist[1] = f;
                      dist[2] = r;

                      Serial.write(dist, 3);
                      break;

                default: break;         
              }
      }  

}
