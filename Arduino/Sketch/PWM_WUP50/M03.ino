
void exec_M03_sequence()
{
  long current_time = millis();
  Serial.println(M03_cycle_phase);
  if (M03_cycle_phase == "M03_Starting")
  {
      //Serial.println(current_time - M03_current_cycle_start_time);
    if ((current_time - M03_current_cycle_start_time) > M03_START_DURATION)
    {
      M03_cycle_phase = "Operation_MAX";
      M03_current_cycle_start_time = current_time;
      for (int i = 0; i < OUT_PWM_number; i++)
      {
        PWM_duty_cycles[i]=95;
      }
      configure_duty_cycles_timer_PWM(false);
    }
  }
  else
  {
    if (M03_cycle_phase == "Operation_MAX")
    {
      Serial.println(current_time - M03_current_cycle_start_time);
      if ((current_time - M03_current_cycle_start_time) > (M03_OPERATION_MAX_DURATION))
      {
        M03_cycle_phase = "Operation_MIN";
        M03_current_cycle_start_time = current_time;
        for (int i = 0; i < OUT_PWM_number; i++)
        {
          PWM_duty_cycles[i]=10;
        }
        configure_duty_cycles_timer_PWM(false);
      }
    }
    else
    {
      if (M03_cycle_phase == "Operation_MIN")
      {
        //Serial.println(current_time - M03_current_cycle_start_time);
        if ((current_time - M03_current_cycle_start_time) > M03_OPERATION_MIN_DURATION)
        {
          Serial.print("Completed cycle ");
          Serial.println(M03_cycle_number);
          M03_cycle_number +=1;
          if (M03_cycle_number <= M03_CYCLE_NUMBER)
          {
            M03_cycle_phase = "Operation_MAX";
            M03_current_cycle_start_time = current_time;

            for (int i = 0; i < OUT_PWM_number; i++)
            {
              PWM_duty_cycles[i]=95;
            }
            configure_duty_cycles_timer_PWM(false);
          }
          else
          {
            M03_cycle_phase = "Test_completed";
            M03_current_cycle_start_time = current_time;

            for (int i = 0; i < OUT_PWM_number; i++)
            {
              PWM_duty_cycles[i]=10;
            }
            configure_duty_cycles_timer_PWM(false);
          }
        }
      }
      else
      {
        if (M03_cycle_phase == "Test_completed")
        {
          for (int i = 0; i < OUT_PWM_number; i++)
          {
            PWM_duty_cycles[i]=10;
          }
          configure_duty_cycles_timer_PWM(false);
        }
        else
        {
            Serial.println("exec_M03_sequence() - M03_cycle_phase incorrect");
        }
      }
    }
  }
}