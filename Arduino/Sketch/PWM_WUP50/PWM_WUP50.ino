//
#define DUTY_CYCLE_PARAMETER_ID_OFFSET 16
#define FEEDBACK_PARAMETER_ID_OFFSET 32
// Parameter test
#define PARAMETER_TEST_STEP_DURATION 30 //seconds
// M03 test
#define M03_START_DURATION 15000 //milliseconds
#define M03_OPERATION_MIN_DURATION 900000 //milliseconds
#define M03_OPERATION_MAX_DURATION 300000 //milliseconds
#define M03_CYCLE_NUMBER 20 //number

#define ARDUINO_UNO 1 
#define ARDUINO_MEGA 2
#define ARDUINO_PORTENTA 3

#define ARDUINO ARDUINO_MEGA
const bool PWM_TIMER_MODE = true;

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
  #define OUT_PWM_number 6
  #define OUT_PWM_01_PIN 6    //yellow
  #define OUT_PWM_02_PIN 7    //white
  #define OUT_PWM_03_PIN 8    //brown
  #define OUT_PWM_04_PIN 44   //purple
  #define OUT_PWM_05_PIN 45   //blue
  #define OUT_PWM_06_PIN 46   //green
  #define OUT_PWM_07_PIN 2
  #define OUT_PWM_08_PIN 3
  #define OUT_PWM_09_PIN 5
  #define OUT_PWM_10_PIN 9
  #define IN_ENABLE_number 6
  #define IN_PUMP1_ENABLE 22
  #define IN_PUMP2_ENABLE 24
  #define IN_PUMP3_ENABLE 26
  #define IN_PUMP4_ENABLE 28
  #define IN_PUMP5_ENABLE 30
  #define IN_PUMP6_ENABLE 32
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
int PWM_duty_cycles[10] = {10, 10, 10, 10, 10, 10, 10, 10, 10, 10};

int IN_pins[6] = {IN_PUMP1_ENABLE, IN_PUMP2_ENABLE, IN_PUMP3_ENABLE, IN_PUMP4_ENABLE, IN_PUMP5_ENABLE, IN_PUMP6_ENABLE};
unsigned long enable_start_time[6] = {0, 0, 0, 0, 0, 0};
int parameter_counter[6] = {0, 0, 0, 0, 0, 0};
int test_counter[6] = {0, 0, 0, 0, 0, 0};

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
unsigned long parameter_test_time = 0;
unsigned long verbose_time=0;
//unsigned long lastPrint = 0;
unsigned long lastTime_us = 0;

unsigned long M03_current_cycle_start_time = 0;
int           M03_cycle_number = 0;
String        M03_cycle_phase = "";

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
  for (int i = 0; i < OUT_PWM_number; i++) 
  {
    pinMode(OUT_pins[i], OUTPUT);
  }
  
  for (int i = 0; i < IN_ENABLE_number; i++)
  {
    pinMode(IN_pins[i], INPUT_PULLUP);
  }
  
  if (PWM_TIMER_MODE)
  {
    TCCR4B = TCCR4B & B11111000 | B00000100; // 122.55 Hz
    TCCR5B = TCCR5B & B11111000 | B00000100;  //  122.55 Hz
    configure_duty_cycles_timer_PWM(false);
  }
  Serial.println("riverificare inizializzazione");

  // 
  M03_current_cycle_start_time = millis();
  M03_cycle_phase = "M03_Starting";
  M03_cycle_number = 1;
  for (int i = 0; i < OUT_PWM_number; i++)
  {
    PWM_duty_cycles[i]=10;
  }
  configure_duty_cycles_timer_PWM(false);

  // imposta la velocità a 9600 bps
  Serial.begin(9600);

  PWM_period_us = (unsigned long)(1000000 / PWM_freq_Hz);
  Serial.print("PWM_period_us: ");
  Serial.println(PWM_period_us);


  //setta il tempo di attesa pari a 1 periodo
  current_waiting_time_PWM = 1 * PWM_period_us; // qua ci va aggiunta la frequenza
  //Serial.print("current_waiting_time_PWM ");
  //Serial.println(current_waiting_time_PWM);
  //setta il current index a -1;
  current_index_PWM = -1;

}

void loop() 
{
  
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
          //String msg = encode_data();
          //Serial.println(msg);
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

  if (PWM_TIMER_MODE)
  {
    if (millis() - parameter_test_time >= 1000) //run once each second
    {
      current_index_PWM += 1;
      /*
      for (int i = 0; i < IN_ENABLE_number; i++)
      {
        //PWM_duty_cycles[i]=10*current_index_PWM;
        //do_parameter_sequence(i);
        exec_test_sequence(i, "operation_max");
      } 
      configure_duty_cycles_timer_PWM(true);
      */
    
      exec_M03_sequence();
      parameter_test_time = millis();
    }

    if ((millis() - verbose_time) >= 990) //run once each second
    {
      //print_duty_cycles_value();
      //print_input_values();
      //print_parameter_counter();
      //print_test_counter();
      verbose_time = millis();
    }
  }
}


void do_parameter_sequence(int pump_index)
{
  int enable_state = digitalRead(IN_pins[pump_index]);
  unsigned long currentTime = millis();
  unsigned long start_time = enable_start_time[pump_index];

  // ---- Detect button press (rising edge) ----
  if (enable_state == LOW)
  {
    parameter_counter[pump_index] +=1;
  }else{
    parameter_counter[pump_index] = 0;
  }

// ---- Set PWM according to time elapsed ----
  if (  (PARAMETER_TEST_STEP_DURATION*0 == parameter_counter[pump_index])                                                                       ) { PWM_duty_cycles[pump_index]=10; }      
  if (  (PARAMETER_TEST_STEP_DURATION*0 < parameter_counter[pump_index]) && (parameter_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*1)  ) { PWM_duty_cycles[pump_index]=25; }
  if (  (PARAMETER_TEST_STEP_DURATION*1 < parameter_counter[pump_index]) && (parameter_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*2)  ) { PWM_duty_cycles[pump_index]=50; }
  if (  (PARAMETER_TEST_STEP_DURATION*2 < parameter_counter[pump_index]) && (parameter_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*3)  ) { PWM_duty_cycles[pump_index]=75; }
  if (  (PARAMETER_TEST_STEP_DURATION*3 < parameter_counter[pump_index]) && (parameter_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*4)  ) { PWM_duty_cycles[pump_index]=85; }
  if (  (PARAMETER_TEST_STEP_DURATION*4 < parameter_counter[pump_index]) && (parameter_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*5)  ) { PWM_duty_cycles[pump_index]=95; }
  if (  (PARAMETER_TEST_STEP_DURATION*5 < parameter_counter[pump_index])                                                                        ) { PWM_duty_cycles[pump_index]=10; }      
}

void exec_test_sequence(int pump_index, String test_type)
{
  int enable_state = digitalRead(IN_pins[pump_index]);
  unsigned long currentTime = millis();
  unsigned long start_time = enable_start_time[pump_index];

  // ---- Detect button press (rising edge) ----
  if (enable_state == LOW)
  {
    test_counter[pump_index] +=1;
  }else{
    test_counter[pump_index] = 0;
  }
  if (test_type == "parameter")
  {  
    // ---- Set PWM according to time elapsed ----
    if (  (PARAMETER_TEST_STEP_DURATION*0 == test_counter[pump_index])                                                                  ) { PWM_duty_cycles[pump_index]=10; }      
    if (  (PARAMETER_TEST_STEP_DURATION*0 < test_counter[pump_index]) && (test_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*1)  ) { PWM_duty_cycles[pump_index]=25; }
    if (  (PARAMETER_TEST_STEP_DURATION*1 < test_counter[pump_index]) && (test_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*2)  ) { PWM_duty_cycles[pump_index]=50; }
    if (  (PARAMETER_TEST_STEP_DURATION*2 < test_counter[pump_index]) && (test_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*3)  ) { PWM_duty_cycles[pump_index]=75; }
    if (  (PARAMETER_TEST_STEP_DURATION*3 < test_counter[pump_index]) && (test_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*4)  ) { PWM_duty_cycles[pump_index]=85; }
    if (  (PARAMETER_TEST_STEP_DURATION*4 < test_counter[pump_index]) && (test_counter[pump_index] <=  PARAMETER_TEST_STEP_DURATION*5)  ) { PWM_duty_cycles[pump_index]=95; }
    if (  (PARAMETER_TEST_STEP_DURATION*5 < test_counter[pump_index])                                                                   ) { PWM_duty_cycles[pump_index]=10; }      
    return;
  }
  if (test_type == "operation_max")
  {
    // ---- Set PWM according to time elapsed ----
    if (test_counter[pump_index] == 0  ) {
      PWM_duty_cycles[pump_index]=10; 
      }
    else { 
      PWM_duty_cycles[pump_index]=95;
      }      
    return;
  }
  Serial.println("exec_test_sequence() - test_type selection error");
}

int pwm_from_percentage(int percent) 
{
  int ret=0;
  if (percent < 0) return 255; //0;
  if (percent > 100) return 0;//255;
  ret=255-(percent * 255 / 100);
  return ret;
}

void configure_duty_cycles_timer_PWM(bool verbose)
{
  if (verbose)
  {
    print_duty_cycles_value();
  }
  for (int i = 0; i < OUT_PWM_number; i++)
  {
    analogWrite(OUT_pins[i], pwm_from_percentage(PWM_duty_cycles[i]));
  }
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
    //configure_duty_cycles_manual_PWM();
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

void print_duty_cycles_value()
{
    Serial.print("duty cycles: ");
    for (int i = 0; i < OUT_PWM_number; i++) 
    {
      Serial.print(i);
      Serial.print(":");
      Serial.print(PWM_duty_cycles[i]);
      Serial.print(":");
      Serial.print(pwm_from_percentage(PWM_duty_cycles[i]));
      Serial.print(" - ");
    }
    Serial.println("");
}

void print_parameter_counter()
{
    Serial.print("Parameter counter : ");
    for (int i = 0; i < OUT_PWM_number; i++) 
    {
      Serial.print(i);
      Serial.print(":");
      Serial.print(parameter_counter[i]);
      Serial.print(" - ");
    }
    Serial.println("");
}

void print_test_counter()
{
    Serial.print("Test counter : ");
    for (int i = 0; i < OUT_PWM_number; i++) 
    {
      Serial.print(i);
      Serial.print(":");
      Serial.print(test_counter[i]);
      Serial.print(" - ");
    }
    Serial.println("");
}

void print_input_values()
{
      Serial.print("inputs --> ");
      for (int i = 0; i < IN_ENABLE_number; i++) 
      {
        Serial.print(IN_pins[i]);
        Serial.print(":");
        if (digitalRead(IN_pins[i]) == HIGH) {Serial.print("H");}
        if (digitalRead(IN_pins[i]) == LOW) {Serial.print("L");}
        Serial.print(":");
        Serial.print(" - ");
      }
      Serial.println("");
}
long get_last_pump_feedback(int pump_ID)
{
  return 500; //random(pump_ID*1000, (pump_ID+1)*1000);
}