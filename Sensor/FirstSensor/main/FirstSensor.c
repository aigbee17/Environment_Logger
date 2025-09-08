#include <stdio.h>
#include <stdint.h>
#include "driver/gpio.h"
#include "driver/adc.h"
#include "esp_adc_cal.h"
#include "driver/adc.h"

#define TEMP_SENSOR_PIN ADC1_CHANNEL_0 // GPIO36 if you are using ESP32 
#define HUM_SENSOR_PIN ADC1_CHANNEL_3  // GPIO39 if you are using ESP32
#define AIR_SENSOR_PIN ADC1_CHANNEL_6  // GPIO34 if you are using ESP32
#define READ_DELAY_MS 1800000 // 30 minutes in milliseconds
#define VREF 1100 // Reference voltage in mV
#define ADC_WIDTH ADC_WIDTH_BIT_12 // 12-bit ADC resolution
#define ADC_ATTEN ADC_ATTEN_DB_0

uint32_t Temp_reader;
uint32_t Hum_reader;
uint32_t Air_reader;

void app_main(void)
{
Temp_reader = 0XFF;
Hum_reader = 0XFF;
Air_reader = 0XFF;




while(1){
    adc1_config_width(ADC_WIDTH_BIT_12);
    adc1_config_channel_atten(TEMP_SENSOR_PIN, ADC_ATTEN_DB_0);
    adc1_config_channel_atten(HUM_SENSOR_PIN, ADC_ATTEN_DB_0);
    adc1_config_channel_atten(AIR_SENSOR_PIN, ADC_ATTEN_DB_0);

    int raw_temp = adc1_get_raw(TEMP_SENSOR_PIN);
    int raw_hum = adc1_get_raw(HUM_SENSOR_PIN);
    int raw_air = adc1_get_raw(AIR_SENSOR_PIN);

    

}
}

