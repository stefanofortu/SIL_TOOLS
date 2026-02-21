/*
void configure_duty_cycles(){
  manual_PWM_OUT_highTime = manual_PWM_OUT_period_Hz * OUT_01_dutyCycle/100;
  manual_PWM_OUT_lowTime  = manual_PWM_OUT_period_Hz - manual_PWM_OUT_highTime;
}
*/

void code_part_to_move_in_original_loop()
{ 
  if (!PWM_TIMER_MODE)
    {

      if ((micros() - lastTime_us) >= current_waiting_time_PWM) 
      {
        lastTime_us = micros();
        //waiting_time_PWM = 
        if (current_index_PWM == -1) // se index == -1, allora vuol dire che il PWM è tutto in fase zero
        {
          for (int i = 0; i < OUT_PWM_number; i++) 
          {
            digitalWrite(OUT_pins[i], LOW);
          }
          current_index_PWM = 0;
          current_waiting_time_PWM = PWM_duty_cycles_high_time_us_differential[0];
        }else{
          if (current_index_PWM < 9) //fino al penultimo, metti il ritardo del vettore successivo
          {
            //Serial.print("===================================");
            //Serial.print("current_index_PWM : ");
            //Serial.println(current_index_PWM);
            //Serial.print("PWM_duty_cycles_output_activation_order[current_index_PWM] : ");
            //Serial.println(PWM_duty_cycles_output_activation_order[current_index_PWM]);
            //Serial.print("OUT_pins[PWM_duty_cycles_output_activation_order[current_index_PWM]] ");
            //Serial.println(OUT_pins[PWM_duty_cycles_output_activation_order[current_index_PWM]]);
            
            digitalWrite(OUT_pins[PWM_duty_cycles_output_activation_order[current_index_PWM]], LOW);
            current_waiting_time_PWM = PWM_duty_cycles_high_time_us_differential[current_index_PWM+1];
            current_index_PWM +=1;
          }else{
            if (current_index_PWM == 9)
            {
              digitalWrite(OUT_pins[PWM_duty_cycles_output_activation_order[9]], LOW);
              current_waiting_time_PWM = rest_time_PWM;
              current_index_PWM = -1;
              //for (int i = 0; i < 10; i++) 
              //{
              //  digitalWrite(OUT_pins[i], LOW);
              //}
            }
            else
            {
              Serial.println("Error in current_index_PWM value");
            }
          }
        }
        //PWM_duty_cycles_output_activation_order[i]
        //  waiting_time_PWM = 100;
        //  print_status();
        //Serial.print("current_index_PWM : ");
        //Serial.println(current_index_PWM);
        //Serial.print("current_waiting_time_PWM : ");
        //Serial.println(current_waiting_time_PWM);
      }
    }
}
void configure_duty_cycles_manual_PWM()
{
  /*
  Serial.print("default duty: ");
  Serial.print("PWM_duty_cycles ");
  for (int i = 0; i < OUT_PWM_number; i++) 
  {
    Serial.print(i);
    Serial.print(":");
    Serial.print(PWM_duty_cycles[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
  for (int i = 0; i < OUT_PWM_number; i++) 
  {
    PWM_duty_cycles_high_time_us[i] = (unsigned long) (PWM_period_us/100 * PWM_duty_cycles[i]) ;
  }
  /*
  Serial.print("PWM_duty_cycles_high_time_us ");
  for (int i = 0; i < OUT_PWM_number; i++) 
  {
    Serial.print(i);
    Serial.print(":");
    Serial.print(PWM_duty_cycles_high_time_us[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
  //rest_time_PWM = differenza tra periodo (Periodo * 1'000'000 us) e il max dutycycle - inteso PWM_duty_cycles_high_time_us
  int size_duty_cycle = sizeof(PWM_duty_cycles_high_time_us) / sizeof(PWM_duty_cycles_high_time_us[0]);
  /*
  Serial.print("size_duty_cycle: ");
  Serial.print(size_duty_cycle);
  Serial.println("");
  */
  unsigned long max_high_time = findMax(PWM_duty_cycles_high_time_us, size_duty_cycle);
  /*
  Serial.print("max_high_time: ");
  Serial.print(max_high_time);
  Serial.println("");
  */
  rest_time_PWM = PWM_period_us - max_high_time;
  /*
  Serial.print("rest_time_PWM: ");
  Serial.print(rest_time_PWM);
  Serial.println("");
  */
  // Inizializza orderedIndex con gli indici originali: 0,1,2,3,4
  for (int i = 0; i < OUT_PWM_number; i++)
  {
    PWM_duty_cycles_output_activation_order[i] = i;
  }

  // Ordina gli indici in base ai valori dell'array original
  for (int i = 0; i < OUT_PWM_number - 1 ; i++) 
  {
    for (int j = 0; j < OUT_PWM_number - i - 1; j++) 
    {
      if (PWM_duty_cycles[PWM_duty_cycles_output_activation_order[j]] > PWM_duty_cycles[PWM_duty_cycles_output_activation_order[j + 1]]) 
      {
        // Scambia gli indici
        int temp = PWM_duty_cycles_output_activation_order[j];
        PWM_duty_cycles_output_activation_order[j] = PWM_duty_cycles_output_activation_order[j + 1];
        PWM_duty_cycles_output_activation_order[j + 1] = temp;
      }
    }
  }
  /*
  Serial.print("PWM_duty_cycles_output_activation_order ");
  for (int i = 0; i < OUT_PWM_number; i++) 
  {
    Serial.print(PWM_duty_cycles_output_activation_order[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
  for (int i = 0; i < OUT_PWM_number; i++)
  {
    //here the time is not "differential", is the effective time, but ordered
    PWM_duty_cycles_high_time_us_differential[i] = PWM_duty_cycles_high_time_us[PWM_duty_cycles_output_activation_order[i]];
  }
  /*
  Serial.print("PWM_duty_cycles_high_time_us_ordered ");
  for (int i = 0; i < OUT_PWM_number; i++) 
  {
    Serial.print(PWM_duty_cycles_high_time_us_differential[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
  for (int i = 9; i > 0; i--)
  {
    PWM_duty_cycles_high_time_us_differential[i] = PWM_duty_cycles_high_time_us_differential[i] - PWM_duty_cycles_high_time_us_differential[i-1];
  }
  /*
  Serial.print("PWM_duty_cycles_high_time_us_differential ");
  for (int i = 0; i < OUT_PWM_number; i++) 
  {
    Serial.print(PWM_duty_cycles_high_time_us_differential[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
}


unsigned long findMax(unsigned long array[], int size) {
  unsigned long maxVal = array[0]; // Start with the first element
  for (int i = 1; i < size; i++) {
    if (array[i] > maxVal) {
      maxVal = array[i];
    }
  }
  return maxVal;
}