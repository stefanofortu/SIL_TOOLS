#define DUTY_CYCLE_PARAMETER_ID_OFFSET 16
#define FEEDBACK_PARAMETER_ID_OFFSET 32
#define MAX_NUMBER_OF_PUMP 10

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
  #define IN_PWM_01_PIN 22
  #define IN_PWM_02_PIN 23
  #define IN_PWM_03_PIN 24
  #define IN_PWM_04_PIN 25
  #define IN_PWM_05_PIN 26
  #define IN_PWM_06_PIN 27
  #define IN_PWM_07_PIN 28
  #define IN_PWM_08_PIN 29
  #define IN_PWM_09_PIN 30
  #define IN_PWM_10_PIN 31
#elif ARDUINO == ARDUINO_PORTENTA
  #define OUT_01_PIN 1
#endif

/**********************************************************************
* VARIABILI GENERICHE
**********************************************************************/
unsigned long lastTime_us = 0;
unsigned long last_input_read_ms = 0;  // stores the last time input was read
unsigned long last_slow_update_ms = 0;  // stores the last time input was read
const unsigned long input_sampling_interval_ms = 1;  // 1 ms interval

int OUT_pins[MAX_NUMBER_OF_PUMP] = {OUT_PWM_01_PIN, OUT_PWM_02_PIN, OUT_PWM_03_PIN, OUT_PWM_04_PIN, OUT_PWM_05_PIN, OUT_PWM_06_PIN, OUT_PWM_07_PIN, OUT_PWM_08_PIN, OUT_PWM_09_PIN, OUT_PWM_10_PIN};
int IN_pins[MAX_NUMBER_OF_PUMP] = {IN_PWM_01_PIN, IN_PWM_02_PIN, IN_PWM_03_PIN, IN_PWM_04_PIN, IN_PWM_05_PIN, IN_PWM_06_PIN, IN_PWM_07_PIN, IN_PWM_08_PIN, IN_PWM_09_PIN, IN_PWM_10_PIN};

/**********************************************************************
* VARIABILI SOTTO PARAMETRI ESTERNI
**********************************************************************/
int number_of_pumps = MAX_NUMBER_OF_PUMP;

/**********************************************************************
* VARIABILI PER LA GESTIONE DEL PWM CUSTOM
**********************************************************************/
int PWM_duty_cycles[MAX_NUMBER_OF_PUMP] = {10, 20, 10, 20, 50, 60, 10, 50, 87, 5};
float PWM_freq_Hz = 100;
unsigned long PWM_period_us;
unsigned long PWM_duty_cycles_high_time_us[MAX_NUMBER_OF_PUMP] = {0, 20, 30, 40, 50, 60, 70, 80, 90, 50};
unsigned long PWM_duty_cycles_high_time_us_differential[MAX_NUMBER_OF_PUMP] = {0, 20, 30, 40, 50, 60, 70, 80, 90, 50};
unsigned long current_waiting_time_PWM = 0;
unsigned long rest_time_PWM = 0;
int PWM_duty_cycles_output_activation_order[MAX_NUMBER_OF_PUMP] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
int current_index_PWM = 0;

/**********************************************************************
* VARIABILI PER IL FEEDBACK POMPA
**********************************************************************/
// queste variabile vanno definite come volatile, perchè così non viene otimizzata dal compilatore
volatile unsigned int pump_feedback_ms[MAX_NUMBER_OF_PUMP] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
volatile unsigned int last_pump_feedback_ms[MAX_NUMBER_OF_PUMP] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
bool use_timer1_for_sampling = true;


void setup() 
{
  // imposta la velocità a 9600 bps
  Serial.begin(9600);


  // set all the output pins come DIGITAL OUT
  for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
  {
    pinMode(OUT_pins[i], OUTPUT);
  }

  /**********************************************
  * SETUP PER LA GESTIONE DEL PWM CUSTOM
  **********************************************/
  // set all the output pins come DIGITAL OUT
  PWM_period_us = (unsigned long)(1000000 / PWM_freq_Hz);
  //Serial.print("PWM_period_us: ");
  //Serial.println(PWM_period_us);
  configure_duty_cycles_manual_PWM();

  //setta il tempo di attesa pari a 1 periodo
  current_waiting_time_PWM = 1 * PWM_period_us; // qua ci va aggiunta la frequenza
  //Serial.print("current_waiting_time_PWM ");
  //Serial.println(current_waiting_time_PWM);
  //setta il current index a -1;
  current_index_PWM = -1;

  /*****************************************
  * Configurazione input 
  *****************************************/
  // --- Set pins as inputs ---
  for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
  {
    pinMode(IN_pins[i], INPUT);
  }
  Serial.println("controllare INPUT_PULLUP");
  // --- Configure Timer1 for 1kHz interrupt ---
  noInterrupts();
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1  = 0;
  OCR1A = 249;                          // (16MHz / (64 * 1000Hz)) - 1 = 249
  TCCR1B |= (1 << WGM12);               // CTC mode
  TCCR1B |= (1 << CS11) | (1 << CS10);  // prescaler = 64
  if (use_timer1_for_sampling == true)
  {
    TIMSK1 |= (1 << OCIE1A);              // enable compare interrupt
  }else{
    TIMSK1 &= ~(1 << OCIE1A);             // disabilita l’interrupt di confronto A
  }
  interrupts();

/*
  // Configura Timer1
  noInterrupts();           // disattiva interrupt globali
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1  = 0;
  OCR1A = 6249;             // valore di confronto per 10 Hz
  TCCR1B |= (1 << WGM12);   // modalità CTC
  TCCR1B |= (1 << CS12);    // prescaler = 256
  TIMSK1 |= (1 << OCIE1A);  // abilita interrupt su OCR1A
  interrupts();             // riattiva interrupt globali
*/
  Serial.println("If the 10 digital inputs are all on the same port (e.g., D2–D7 on Port D), read all 8 pins at once using direct port access, which is nearly instantaneous:");
}

void loop() 
{ 
  if (Serial.available()) 
  {
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
          Serial.println("non gestito");
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

  /**********************************************
  * LOOP PER LA GESTIONE DEL PWM CUSTOM
  **********************************************/
  if ((micros() - lastTime_us) >= current_waiting_time_PWM) 
  {
    lastTime_us = micros();
    //waiting_time_PWM = 
    if (current_index_PWM == -1) // se index == -1, allora vuol dire che il PWM è tutto in fase zero
    {
      for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
      {
        digitalWrite(OUT_pins[i], HIGH);
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
        }
        else
        {
          Serial.println("Error in current_index_PWM value");
        }
      }
    }
    //Serial.print("current_index_PWM : ");
    //Serial.println(current_index_PWM);
    //Serial.print("current_waiting_time_PWM : ");
    //Serial.println(current_waiting_time_PWM);
  }
  
  unsigned long current_ms = millis();

  if (use_timer1_for_sampling == false)
  {
    // duration of this loop = 64 us
    if ((current_ms - last_input_read_ms) >= input_sampling_interval_ms) 
    {
      last_input_read_ms = current_ms;
      for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
      {
        int value = digitalRead(IN_pins[i]);
        if (value == HIGH)
        {
          last_pump_feedback_ms[i] = pump_feedback_ms[i];
          pump_feedback_ms[i] = 0;
        }else{
          if (pump_feedback_ms[i] < 65500) // prevent overflow
          {
            pump_feedback_ms[i] = pump_feedback_ms[i] + 1;
          }
        }
      }
    }
  }

  if ((current_ms - last_slow_update_ms) >= 1*1000) 
  {
    last_slow_update_ms = current_ms;
    Serial.print("pump_feedback_ms ");
    for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
    {
      Serial.print(pump_feedback_ms[i]);
      Serial.print(" - ");
    }
    Serial.println("");
  }

  
  /*
  const int inputPin = 2;   // digital input pin
  const unsigned long interval = 1;  // 1 ms interval

  void setup() {
    Serial.begin(115200);
    pinMode(inputPin, INPUT);
  }

  void loop() {
    


  }



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

/*
ISR(TIMER1_COMPA_vect) 
{
  for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
  {
    bool value = digitalRead(IN_pins[i]);
    if (value == HIGH)
    {
      //Serial.println("high");
      last_pump_feedback_ms[i] = pump_feedback_ms[i];
      pump_feedback_ms[i] = 0;
    }
    else
    {
      if (pump_feedback_ms[i] < 65500) // prevent overflow
      {
        pump_feedback_ms[i] = pump_feedback_ms[i] + 1;
        //if (i == 0){  Serial.println(pump_feedback_ms[0]);}
      }
    }
  }
}
*/
/*
unsigned long startPress;
unsigned long duration;

void loop() {
  if (digitalRead(2) == LOW) {   // pulsante premuto
    startPress = micros();
    while(digitalRead(2) == LOW); // aspetta rilascio
    duration = micros() - startPress;
    Serial.print("Durata pressione: ");
    Serial.print(duration);
    Serial.println(" µs");
*/
ISR(TIMER1_COMPA_vect) 
{
    bool value[10];
    //bool value = digitalRead(IN_pins[i]);
    value[0] = PINA & (1 << PA0); // Bit 0 → D22
    value[1] = PINA & (1 << PA1); // Bit 1 → D23
    value[2] = PINA & (1 << PA2); // Bit 2 → D24
    value[3] = PINA & (1 << PA3); // Bit 3 → D25
    value[4] = PINA & (1 << PA4); // Bit 4 → D26
    value[5] = PINA & (1 << PA5); // Bit 5 → D27
    value[6] = PINA & (1 << PA6); // Bit 6 → D28
    value[7] = PINA & (1 << PA7); // Bit 7 → D29
    value[8] = PINC & (1 << PC0);     // legge D30
    value[9] = PINC & (1 << PC1);     // legge D31
    
    for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
    {

      if (value[i] == HIGH)
      {
        //Serial.println("high");
        last_pump_feedback_ms[i] = pump_feedback_ms[i];
        pump_feedback_ms[i] = 0;
      }
      else
      {
        if (pump_feedback_ms[i] < 65500) // prevent overflow
        {
          pump_feedback_ms[i] = pump_feedback_ms[i] + 1;
          //if (i == 0){  Serial.println(pump_feedback_ms[0]);}
        }
      }
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
  //Serial.print("set_parameter_value_from_serial(): parameter_ID_value: ");
  //Serial.println(parameter_ID_value);
  int parameter_value_int = (int) strtol(parameter_value_hex.c_str(), NULL, 16);
  //Serial.print("set_parameter_value_from_serial(): parameter_value_int: ");
  //Serial.println(parameter_value_int);

  if (17 <= parameter_ID_value && parameter_ID_value <= 26)
  {
    PWM_duty_cycles[parameter_ID_value-DUTY_CYCLE_PARAMETER_ID_OFFSET-1] = parameter_value_int;
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

long get_last_pump_feedback(int pump_ID)
{
  return random(pump_ID*1000, (pump_ID+1)*1000);
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
  Serial.print("PWM_duty_cycles ");
  for (int i = 0; i < 10; i++) 
  {
    //Serial.print(i);
    //Serial.print(":");
    Serial.print(PWM_duty_cycles[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
  for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
  {
    PWM_duty_cycles_high_time_us[i] = (unsigned long) (PWM_period_us/100 * PWM_duty_cycles[i]) ;
  }

  /*
  Serial.print("PWM_duty_cycles_high_time_us ");
  for (int i = 0; i < 10; i++) 
  {
    //Serial.print(i);
    //Serial.print(":");
    Serial.print(PWM_duty_cycles_high_time_us[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
  //rest_time_PWM = differenza tra periodo (Periodo * 1'000'000 us) e il max dutycycle - inteso PWM_duty_cycles_high_time_us
  int size_duty_cycle = sizeof(PWM_duty_cycles_high_time_us) / sizeof(PWM_duty_cycles_high_time_us[0]);
  //Serial.print("size_duty_cycle: ");
  //Serial.print(size_duty_cycle);
  //Serial.println("");
  unsigned long max_high_time = findMax(PWM_duty_cycles_high_time_us, size_duty_cycle);
  //Serial.print("max_high_time: ");
  //Serial.print(max_high_time);
  //Serial.println("");
  rest_time_PWM = PWM_period_us - max_high_time;
  //Serial.print("rest_time_PWM: ");
  //Serial.print(rest_time_PWM);
  //Serial.println("");
  // Inizializza orderedIndex con gli indici originali: 0,1,2,3,4
  for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++)
  {
    PWM_duty_cycles_output_activation_order[i] = i;
  }

  // Ordina gli indici in base ai valori dell'array original
  for (int i = 0; i < MAX_NUMBER_OF_PUMP - 1 ; i++) 
  {
    for (int j = 0; j < MAX_NUMBER_OF_PUMP - i - 1; j++) 
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
  for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
  {
    Serial.print(PWM_duty_cycles_output_activation_order[i]);
    Serial.print(" - ");
  }
  Serial.println("");
  */
  for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++)
  {
    //here the time is not "differential", is the effective time, but ordered
    PWM_duty_cycles_high_time_us_differential[i] = PWM_duty_cycles_high_time_us[PWM_duty_cycles_output_activation_order[i]];
  }
  /*
  Serial.print("PWM_duty_cycles_high_time_us_ordered ");
  for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
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
  for (int i = 0; i < MAX_NUMBER_OF_PUMP; i++) 
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