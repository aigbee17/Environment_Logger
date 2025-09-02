#include <stdio.h>
#include <stdint.h>
#include "driver/gpio.h"




uint32_t Temp_reader;
uint32_t Hum_reader;
uint32_t Air_reader;










void app_main(void)
{
Temp_reader = 0XFF;
Hum_reader = 0XFF;
Air_reader = 0XFF;
}

