#include <stdio.h>
#include <stdint.h>
#include "driver/gpio.h"

#define TEMP_SENSOR_PIN ADC1_CHANNEL_0 // GPIO36 if you are using ESP32 
#define HUM_SENSOR_PIN ADC1_CHANNEL_3  // GPIO39 if you are using ESP32
#define AIR_SENSOR_PIN ADC1_CHANNEL_6  // GPIO34 if you are using ESP32


uint32_t Temp_reader;
uint32_t Hum_reader;
uint32_t Air_reader;













void app_main(void)
{
Temp_reader = 0XFF;
Hum_reader = 0XFF;
Air_reader = 0XFF;


while(1){

}
}

