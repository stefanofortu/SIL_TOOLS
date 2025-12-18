#define DUTY_CYCLE_PARAMETER_ID_OFFSET 16
#define FEEDBACK_PARAMETER_ID_OFFSET 32

#define ARDUINO_UNO 1 
#define ARDUINO_MEGA 2
#define ARDUINO_PORTENTA 3

#define ARDUINO ARDUINO_MEGA

#if ARDUINO == ARDUINO_UNO
  #define OUT_PWM_01_PIN 3
  #define OUT_PWM_02_PIN 5
  #define OUT_PWM_03_PIN 6
  #define OUT_PWM_04_PIN 9
  #define OUT_PWM_05_PIN 10
  #define OUT_PWM_06_PIN 11
  #define OUT_PWM_07_PIN 19
  #define OUT_PWM_08_PIN 19
  #define OUT_PWM_09_PIN 19
  #define OUT_PWM_10_PIN 19
#elif ARDUINO == ARDUINO_MEGA
  #define OUT_PWM_01_PIN 2
  #define OUT_PWM_02_PIN 3
  #define OUT_PWM_03_PIN 5
  #define OUT_PWM_04_PIN 6
  #define OUT_PWM_05_PIN 7
  #define OUT_PWM_06_PIN 8
  #define OUT_PWM_07_PIN 9
  #define OUT_PWM_08_PIN 44
  #define OUT_PWM_09_PIN 45
  #define OUT_PWM_10_PIN 46
#elif ARDUINO == ARDUINO_PORTENTA
  #define OUT_01_PIN 1
#endif

//int OUT_01_pin = 3;
//int IN_01_pin = 2;
//int OUT_02_pin = 5;
//int IN_02_pin = 4;
//int OUT_03_pin = 6;
//int IN_03_pin = 7;
//int OUT_04_pin = 9;
//int IN_04_pin = 8;
//int OUT_05_pin = 10;
//int IN_05_pin = 12;
//int OUT_06_pin = 11;
//int IN_06_pin = 13;

//int OUT_07_pin = 19;

//int OUT_01_dutyCycle = 50;
//const unsigned long manual_PWM_OUT_period_Hz = 75;
//unsigned long manual_PWM_OUT_highTime;
//unsigned long manual_PWM_OUT_lowTime;
//unsigned long manual_PWM_OUT_previousMillis = 0;
//bool manual_PWM_OUT_outputState = false;

int OUT_pins[10] = {OUT_PWM_01_PIN, OUT_PWM_02_PIN, OUT_PWM_03_PIN, OUT_PWM_04_PIN, OUT_PWM_05_PIN, OUT_PWM_06_PIN, OUT_PWM_07_PIN, OUT_PWM_08_PIN, OUT_PWM_09_PIN, OUT_PWM_10_PIN};
int PWM_duty_cycles[10] = {10, 20, 10, 20, 50, 60, 10, 50, 87, 5};
float PWM_freq_Hz = 100;
unsigned long PWM_period_us;
unsigned long PWM_duty_cycles_high_time_us[10] = {0, 20, 30, 40, 50, 60, 70, 80, 90, 50};
unsigned long PWM_duty_cycles_high_time_us_differential[10] = {0, 20, 30, 40, 50, 60, 70, 80, 90, 50};
unsigned long current_waiting_time_PWM = 0;
unsigned long rest_time_PWM = 0;
int PWM_duty_cycles_output_activation_order[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
int current_index_PWM = 0;
 
//int OUT_02_dutyCycle = 50;
//int OUT_03_dutyCycle = 50;
//int OUT_04_dutyCycle = 50;
//int OUT_05_dutyCycle = 50;
//int OUT_06_dutyCycle = 50;
//int OUT_07_dutyCycle = 0;
//int OUT_08_dutyCycle = 0;
//int OUT_09_dutyCycle = 0;
//int OUT_10_dutyCycle = 0;

//gestione timer
//unsigned long lastTime = 0;
//unsigned long lastPrint = 0;
unsigned long lastTime_us = 0;

//uint8_t data_TX[20];

//lettura PWM
//volatile unsigned long IN_01_lowStart = 0;
//volatile unsigned long IN_01_lowDuration = 0;
//volatile unsigned long IN_01_pump_feedback_duration_volatile = 0;
//volatile unsigned long IN_01_pump_feedback_time_volatile=0;
//unsigned long IN_01_pump_feedback_duration = 0;
//unsigned long IN_01_pump_feedback_time = 0;
//unsigned long IN_01_pump_last_feedback_time = 0;

void setup() 
{
  for (int i = 0; i < 10; i++) 
  {
    pinMode(OUT_pins[i], OUTPUT);
  }

  // imposta pins come output
  //pinMode(OUT_01_pin, OUTPUT);
  //pinMode(OUT_02_pin, OUTPUT);
  //pinMode(OUT_03_pin, OUTPUT);
  //pinMode(OUT_04_pin, OUTPUT);
  //pinMode(OUT_05_pin, OUTPUT);
  //pinMode(OUT_06_pin, OUTPUT);

  //configure_duty_cycles();
  //configure_duty_cycles_manual_PWM();
  //randomSeed(analogRead(A0));

  // imposta la velocità a 9600 bps
  Serial.begin(9600);

  //pinMode(IN_01_pin, INPUT);
  //pinMode(IN_01_pin, INPUT_PULLUP);
  //attachInterrupt(digitalPinToInterrupt(IN_01_pin), measure_IN_01_low_duration, CHANGE);

  //pinMode(IN_02_pin, INPUT_PULLUP);
  //pinMode(IN_03_pin, INPUT_PULLUP);
  //pinMode(IN_04_pin, INPUT_PULLUP);
  //pinMode(IN_05_pin, INPUT_PULLUP);
  //pinMode(IN_06_pin, INPUT_PULLUP);

  PWM_period_us = (unsigned long)(1000000 / PWM_freq_Hz);
  Serial.print("PWM_period_us: ");
  Serial.println(PWM_period_us);

  configure_duty_cycles_manual_PWM();

  //setta il tempo di attesa pari a 1 periodo
  current_waiting_time_PWM = 1 * PWM_period_us; // qua ci va aggiunta la frequenza
  //Serial.print("current_waiting_time_PWM ");
  //Serial.println(current_waiting_time_PWM);
  //setta il current index a -1;
  current_index_PWM = -1;

}

void loop() {

  // spostare questo blocci in "setup"
  // genera un segnale PWM con duty cycle del 50%
  //analogWrite(OUT_01_pin, map(OUT_01_dutyCycle, 0, 100, 0, 255));
  //analogWrite(OUT_02_pin, map(OUT_02_dutyCycle, 0, 100, 0, 255));
  //analogWrite(OUT_03_pin, map(OUT_03_dutyCycle, 0, 100, 0, 255));
  //analogWrite(OUT_04_pin, map(OUT_04_dutyCycle, 0, 100, 0, 255));
  //analogWrite(OUT_05_pin, map(OUT_05_dutyCycle, 0, 100, 0, 255));
  //analogWrite(OUT_06_pin, map(OUT_06_dutyCycle, 0, 100, 0, 255));
  
  if (Serial.available()) {
    String message = Serial.readStringUntil('\n');  // legge fino a newline
    message.trim();  // rimuove spazi vuoti o newline extra
    //Serial.print("Arduino received message:  ");
    //Serial.println(message);

    int separator = message.indexOf(':');
    String command = message.substring(0, separator);

    if (command == "0"){
      Serial.println("Arduino_COM_OK");
    }else{
      if (command == "1"){
        Serial.println("PWM");
      }else{
        if (command == "2")
        {
          String msg = encode_data();
          Serial.println(msg);
        } 
        else  
        {
          if (command == "3") // GET A PARAMETER
          {
              String parameter_ID = message.substring(separator + 1);
              get_parameter_value_on_serial(parameter_ID);
          }
          else{
            if (command == "4") // SET A PARAMETER
            {
                int value_separator = message.indexOf(':',separator + 1);
                String parameter_ID = message.substring(separator + 1, value_separator);
                String parameter_value_hex = message.substring(value_separator + 1);
                set_parameter_value_from_serial(parameter_ID, parameter_value_hex);
            } 
            else 
            {
              Serial.print("Command unknowm. Frame received: ");
              Serial.println(message);
            }
          }
        }
      }
    }
  }

  if ((micros() - lastTime_us) >= current_waiting_time_PWM) 
  {
    lastTime_us = micros();
    //waiting_time_PWM = 
    if (current_index_PWM == -1) // se index == -1, allora vuol dire che il PWM è tutto in fase zero
    {
      for (int i = 0; i < 10; i++) 
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
        
        digitalWrite(OUT_pins[PWM_duty_cycles_output_activation_order[current_index_PWM]], HIGH);
        current_waiting_time_PWM = PWM_duty_cycles_high_time_us_differential[current_index_PWM+1];
        current_index_PWM +=1;
      }else{
        if (current_index_PWM == 9)
        {
          digitalWrite(OUT_pins[PWM_duty_cycles_output_activation_order[9]], HIGH);
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

}

void get_parameter_value_on_serial(String parameter_id_hex)
{
  int parameter_ID_value = (int) strtol(parameter_id_hex.c_str(), NULL, 16);
  //Serial.print("parameter_ID_value: ");
  //Serial.println(parameter_ID_value);
  if ( (1+DUTY_CYCLE_PARAMETER_ID_OFFSET) <= parameter_ID_value && parameter_ID_value <= (10+DUTY_CYCLE_PARAMETER_ID_OFFSET))
  {
    int index = (parameter_ID_value - DUTY_CYCLE_PARAMETER_ID_OFFSET - 1);
    int duty_cyle = PWM_duty_cycles[index];;
    char hex_feedback_value[5];  // 2 digits max + null terminator
    sprintf(hex_feedback_value, "%04X", duty_cyle);
    Serial.print("3:");
    Serial.print(parameter_id_hex);
    Serial.print(":");
    Serial.println(hex_feedback_value);
  }

  if (33 <= parameter_ID_value && parameter_ID_value <= 42)
  {
    long pump_feedback = 0;
    if (parameter_ID_value == 33) {pump_feedback = get_last_pump_feedback(1); }//Serial.println("get feedback pump 1");}
    if (parameter_ID_value == 34) {pump_feedback = get_last_pump_feedback(2); }//Serial.println("get feedback pump 2");}
    if (parameter_ID_value == 35) {pump_feedback = get_last_pump_feedback(3); }//Serial.println("get feedback pump 3");}
    if (parameter_ID_value == 36) {pump_feedback = get_last_pump_feedback(4); }//Serial.println("get feedback pump 4");}
    if (parameter_ID_value == 37) {pump_feedback = get_last_pump_feedback(5); }//Serial.println("get feedback pump 5");}
    if (parameter_ID_value == 38) {pump_feedback = get_last_pump_feedback(6); }//Serial.println("get feedback pump 6");}
    if (parameter_ID_value == 39) {pump_feedback = get_last_pump_feedback(7); }//Serial.println("get feedback pump 7");}
    if (parameter_ID_value == 40) {pump_feedback = get_last_pump_feedback(8); }//Serial.println("get feedback pump 8");}
    if (parameter_ID_value == 41) {pump_feedback = get_last_pump_feedback(9); }//Serial.println("get feedback pump 9");}
    if (parameter_ID_value == 42) {pump_feedback = get_last_pump_feedback(10); }//Serial.println("get feedback pump 10");}
    char hex_feedback_value[5];  // 2 digits max + null terminator
    sprintf(hex_feedback_value, "%04X", pump_feedback);
    Serial.print("3:");
    Serial.print(parameter_id_hex);
    Serial.print(":");
    Serial.println(hex_feedback_value);
  }
}

void set_parameter_value_from_serial(String parameter_id_hex, String parameter_value_hex)
{
  int parameter_ID_value = (int) strtol(parameter_id_hex.c_str(), NULL, 16);
  /*
  Serial.print("set_parameter_value_from_serial(): parameter_ID_value: ");
  Serial.println(parameter_ID_value);
  */
  int parameter_value_int = (int) strtol(parameter_value_hex.c_str(), NULL, 16);
  /*
  Serial.print("set_parameter_value_from_serial(): parameter_value_int: ");
  Serial.println(parameter_value_int);
  */
  if (17 <= parameter_ID_value && parameter_ID_value <= 26)
  {
    PWM_duty_cycles[parameter_ID_value-17] = parameter_value_int;
    configure_duty_cycles_manual_PWM();
    char hex_pwm_value[3];  // 2 digits max + null terminator
    sprintf(hex_pwm_value, "%02X", parameter_value_int);
    Serial.print("4:");
    Serial.print(parameter_id_hex);
    Serial.print(":");
    Serial.println(hex_pwm_value);
    //Serial.println();
  }else{
    Serial.println("Wrong parameter ID received from serial");
  }
}

/*
void print_status(){
  Serial.println("01_DC:" + String(OUT_01_dutyCycle));
  Serial.println("02_DC:" + String(OUT_02_dutyCycle));
  Serial.println("03_DC:" + String(OUT_03_dutyCycle));
  Serial.println("04_DC:" + String(OUT_04_dutyCycle));
  Serial.println("05_DC:" + String(OUT_05_dutyCycle));
  Serial.println("06_DC:" + String(OUT_06_dutyCycle));
}
*/


long get_last_pump_feedback(int pump_ID)
{
  return 500; //random(pump_ID*1000, (pump_ID+1)*1000);
}

String encode_data(){
    String reply_message = "";
    char hexString[3];
    sprintf(hexString, "%02X", PWM_duty_cycles[0]);
    reply_message = reply_message + "11:" + String(hexString) + ":";

    sprintf(hexString, "%02X", PWM_duty_cycles[1]);
    reply_message = reply_message + "12:" + String(hexString) + ":";

    sprintf(hexString, "%02X", PWM_duty_cycles[2]);
    reply_message = reply_message + "13:" + String(hexString) + ":";

    sprintf(hexString, "%02X", PWM_duty_cycles[3]);
    reply_message = reply_message + "14:" + String(hexString) + ":";

    sprintf(hexString, "%02X", PWM_duty_cycles[4]);
    reply_message = reply_message + "15:" + String(hexString) + ":";

    sprintf(hexString, "%02X", PWM_duty_cycles[5]);
    reply_message = reply_message + "16:" + String(hexString) + ":";

    sprintf(hexString, "%02X", PWM_duty_cycles[6]);
    reply_message = reply_message + "17:" + String(hexString) + ":";

    sprintf(hexString, "%02X", PWM_duty_cycles[7]);
    reply_message = reply_message + "18:" + String(hexString) + ":";

    sprintf(hexString, "%02X", PWM_duty_cycles[8]);
    reply_message = reply_message + "19:" + String(hexString) + ":";

    sprintf(hexString, "%02X", PWM_duty_cycles[9]);
    reply_message = reply_message + "1A:" + String(hexString);
    return reply_message;
}
/*
void configure_duty_cycles(){
  manual_PWM_OUT_highTime = manual_PWM_OUT_period_Hz * OUT_01_dutyCycle/100;
  manual_PWM_OUT_lowTime  = manual_PWM_OUT_period_Hz - manual_PWM_OUT_highTime;
}
*/
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
void configure_duty_cycles_manual_PWM()
{
  /*
  Serial.print("default duty: ");
  Serial.print("PWM_duty_cycles ");
  for (int i = 0; i < 10; i++) 
  {
    Serial.print(i);
    Serial.print(":");
    Serial.print(PWM_duty_cycles[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
  for (int i = 0; i < 10; i++) 
  {
    PWM_duty_cycles_high_time_us[i] = (unsigned long) (PWM_period_us/100 * PWM_duty_cycles[i]) ;
  }
  /*
  Serial.print("PWM_duty_cycles_high_time_us ");
  for (int i = 0; i < 10; i++) 
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
  for (int i = 0; i < 10; i++)
  {
    PWM_duty_cycles_output_activation_order[i] = i;
  }

  // Ordina gli indici in base ai valori dell'array original
  for (int i = 0; i < 10 - 1 ; i++) 
  {
    for (int j = 0; j < 10 - i - 1; j++) 
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
  for (int i = 0; i < 10; i++) 
  {
    Serial.print(PWM_duty_cycles_output_activation_order[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
  for (int i = 0; i < 10; i++)
  {
    //here the time is not "differential", is the effective time, but ordered
    PWM_duty_cycles_high_time_us_differential[i] = PWM_duty_cycles_high_time_us[PWM_duty_cycles_output_activation_order[i]];
  }
  /*
  Serial.print("PWM_duty_cycles_high_time_us_ordered ");
  for (int i = 0; i < 10; i++) 
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
  for (int i = 0; i < 10; i++) 
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