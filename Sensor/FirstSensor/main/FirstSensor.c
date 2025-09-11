#include <stdio.h> //libraries 
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


void app_main(void)
{
 adc1_config_width(ADC_WIDTH_BIT_12); 
    adc1_config_channel_atten(TEMP_SENSOR_PIN, ADC_ATTEN_DB_0);
    adc1_config_channel_atten(HUM_SENSOR_PIN, ADC_ATTEN_DB_0);
    adc1_config_channel_atten(AIR_SENSOR_PIN, ADC_ATTEN_DB_0);


    esp_adc_cal_characteristics_t cal_low;
    esp_adc_cal_characteristics_t cal_high;

    esp_adc_cal_value_t t_low = esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_0, ADC_WIDTH_BIT_12, VREF, &cal_low);
    esp_adc_cal_value_t t_high = esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_0, ADC_WIDTH_BIT_12, VREF, &cal_high);








while(1){
   

    int raw_temp = adc1_get_raw(TEMP_SENSOR_PIN);
    int raw_hum = adc1_get_raw(HUM_SENSOR_PIN);
    int raw_air = adc1_get_raw(AIR_SENSOR_PIN);

   
    uint32_t mv_temp = esp_adc_cal_raw_to_voltage(raw_temp, &cal_low);
    uint32_t mv_hum = esp_adc_cal_raw_to_voltage(raw_hum, &cal_low);
    uint32_t mv_air = esp_adc_cal_raw_to_voltage(raw_air, &cal_high);



     float v_temp = mv_temp / 1000.0f;
     float tempC  = (v_temp - 0.5f) * 100.0f;

     printf("RAW  -> temp:%4d  hum:%4d  air:%4d\n", raw_temp, raw_hum, raw_air);
     printf("mV   -> temp:%4u  hum:%4u  air:%4u\n", mv_temp, mv_hum, mv_air);
     printf("TEMP -> %.2f °C\n\n", tempC);

     vTaskDelay(pdMS_TO_TICKS(READ_DELAY_MS));


   



}



}