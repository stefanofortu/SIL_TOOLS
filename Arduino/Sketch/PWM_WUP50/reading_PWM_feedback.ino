

/*
void measure_IN_01_low_duration() {
  static bool IN_01_pin_wasLow = false;

  if (digitalRead(IN_01_pin) == LOW) {
    IN_01_lowStart = millis();
    IN_01_pin_wasLow = true;
  } else {
    // fai il conteggio - filtra i tempi minori di 200ms
    if (IN_01_pin_wasLow) {
      IN_01_lowDuration = millis() - IN_01_lowStart;
      if (IN_01_lowDuration > 300){
        IN_01_pump_feedback_duration_volatile = IN_01_lowDuration;
        IN_01_pump_feedback_time_volatile = millis();
        Serial.print("Set low duration @ time ");
        Serial.print(millis());
        Serial.print(" for ");
        Serial.print(IN_01_pump_feedback_duration_volatile);
        Serial.println("ms");
      }
      IN_01_pin_wasLow = false;
    } //else - do nothing
  }
}
*/

  
/*
  if (millis() - lastTime >= 10000) 
  {
    lastTime = millis();
    //print_status();
    //configure_duty_cycles_manual_PWM();
  }
*/
  /*
  if (manual_PWM_OUT_outputState && (millis() - manual_PWM_OUT_previousMillis >= manual_PWM_OUT_highTime)) {
    // Turn OFF
    manual_PWM_OUT_outputState = false;
    manual_PWM_OUT_previousMillis = millis();
    digitalWrite(OUT_01_pin, LOW);
    configure_duty_cycles();
    //int val = random(0, 100);
    //if (val == 1) {manual_PWM_OUT1_lowTime = 500;}
  } else if (!manual_PWM_OUT_outputState && (millis() - manual_PWM_OUT_previousMillis >= manual_PWM_OUT_lowTime)) {
    // Turn ON
    manual_PWM_OUT_outputState = true;
    manual_PWM_OUT_previousMillis = millis();
    digitalWrite(OUT_01_pin, HIGH);
    configure_duty_cycles();
  }
  
  if ( ( millis() - lastPrint ) > 10000) {
    noInterrupts();
    IN_01_pump_feedback_duration = IN_01_pump_feedback_duration_volatile;
    IN_01_pump_feedback_time = IN_01_pump_feedback_time_volatile;
    interrupts();

    int feedback = 0;
    if (IN_01_pump_last_feedback_time == IN_01_pump_feedback_time){
      //Serial.println("Simulation of a Request: Pump unresponsive");
      feedback = 1;
    }else{
      //Serial.print("Simulation of a Request: now it's time ");
      //Serial.print(millis());
      //Serial.print(": last low detected @ ");
      //Serial.print(IN_01_pump_feedback_time);
      //Serial.print(" for ");
      //Serial.print(IN_01_pump_feedback_duration);
      //Serial.println("ms");
    }
    if ( (450 < IN_01_pump_feedback_duration) && (IN_01_pump_feedback_duration > 550) )
    {
      feedback = 0; // ok
    }
    if ( (900 < IN_01_pump_feedback_duration) && (IN_01_pump_feedback_duration > 1100) )
    {
      feedback = 2; // DRY RUN
    }
    if ( (1350 < IN_01_pump_feedback_duration) && (IN_01_pump_feedback_duration > 1650) )
    {
      feedback = 3; // BLOCKED
    }

    IN_01_pump_last_feedback_time = IN_01_pump_feedback_time;

    //Serial.println(lastPrint);
    //Serial.println(IN_01_lsld);
    
    //IN_01_last_lowDuration = 0;
    lastPrint = millis();
  }
  */