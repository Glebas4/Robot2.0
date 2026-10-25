#include <Arduino.h>
#include <Ultrasonic.h>
#include <FastLED.h>


#define MOTOR_RIGHT 0
#define BWD 0
#define MOTOR_LEFT 1
#define FWD 1
#define STOP 2
#define SONAR_READ 2
#define LED 3
#define ON 1
#define OFF 0


#define leds_num 5
#define led_pin 4

#define R1 6
#define R2 5

#define L1 9
#define L2 10

#define sonar_L_trig 12
#define sonar_L_echo 11

#define sonar_F_trig 8
#define sonar_F_echo 7

#define sonar_R_trig 3
#define sonar_R_echo 2


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
};


MOTOR motor_R(R1, R2);
MOTOR motor_L(L1, L2);

Ultrasonic sonar_L(sonar_L_trig, sonar_L_echo);
Ultrasonic sonar_F(sonar_F_trig, sonar_F_echo);
Ultrasonic sonar_R(sonar_R_trig, sonar_R_echo);

CRGB leds[leds_num];


void setup() 
{
  Serial.begin(115200);
  FastLED.addLeds<WS2812, led_pin, GRB>(leds, leds_num);
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

                case MOTOR_RIGHT: //Right motor manual control
                      switch(cmd)
                      {
                        case BWD: motor_L.on(BACKWARD, val); break;
                        case FWD: motor_L.on(FORWARD, val); break;
                        case STOP: motor_L.stop(); break;       
                        default: break;
                      }

                      break;

              
                case MOTOR_LEFT: //Left motor manual control
                      switch(cmd)
                      {
                        case BWD: motor_R.on(BACKWARD, val); break;
                        case FWD: motor_R.on(FORWARD, val); break;
                        case STOP: motor_R.stop(); break;       
                        default: break;
                      }

                      break;


                case LED:                
                      switch(cmd)
                      {
                        case ON: FastLED.showColor(CRGB::White); break;
                        case OFF: FastLED.showColor(CRGB::Black); break;
                        default: break;
                      }
                      
                      break; 


                case SONAR_READ:
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
