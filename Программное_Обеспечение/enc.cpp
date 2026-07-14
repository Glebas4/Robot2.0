#include <GyverPID.h>

class Motor_Encoder
{
  public:
    int pin1, pin2, enc;
    int rounds = 0;
    unsigned long speed_pulse = 0, timer = 0;
    float target = 0;
    const uint8_t ppr = 275;
    const int interval = 50;

    init(){
      GyverPID pid(2.0, 0.5, 0.1, interval);
      pid.setLimits(0, 255);
    }

    Motor_Encoder(int _pin1, int _pin2, int _enc){
        pin1 = _pin1;
        pin2 = _pin2;
        enc  = _enc;
    }

    void count_pulse(){
      speed_pulse++;
    }

    uint8_t set_speed(unsigned long time){
      float spd = (((float)speed_pulse / ppr)/ time) * 1000;
      speed_pulse = 0;
      timer = millis();

      pid.input = spd;
      return pid.getResult();

    }

};


void setup(){}
void loop(){}
