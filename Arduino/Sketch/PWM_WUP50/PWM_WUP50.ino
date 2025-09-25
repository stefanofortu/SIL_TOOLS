int OUT_01_pin = 3;
int IN_01_pin = 2;
int OUT_02_pin = 5;
int IN_02_pin = 4;
int OUT_03_pin = 6;
int IN_03_pin = 7;
int OUT_04_pin = 9;
int IN_04_pin = 8;
int OUT_05_pin = 10;
int IN_05_pin = 12;
int OUT_06_pin = 11;
int IN_06_pin = 13;

int OUT_01_dutyCycle = 50;
const unsigned long manual_PWM_OUT1_period = 10;
unsigned long manual_PWM_OUT1_highTime;
unsigned long manual_PWM_OUT1_lowTime;
unsigned long manual_PWM_OUT1_previousMillis = 0;
bool manual_PWM_OUT1_outputState = false;

int OUT_02_dutyCycle = 50;
int OUT_03_dutyCycle = 50;
int OUT_04_dutyCycle = 50;
int OUT_05_dutyCycle = 50;
int OUT_06_dutyCycle = 50;

//gestione timer
unsigned long lastTime = 0;
unsigned long lastPrint = 0;

uint8_t data_TX[20];

//lettura PWM
volatile unsigned long IN_01_lowStart = 0;
volatile unsigned long IN_01_lowDuration = 0;
volatile unsigned long IN_01_pump_feedback_duration_volatile = 0;
volatile unsigned long IN_01_pump_feedback_time_volatile=0;
unsigned long IN_01_pump_feedback_duration = 0;
unsigned long IN_01_pump_feedback_time = 0;
unsigned long IN_01_pump_last_feedback_time = 0;

void setup() {
  // imposta pins come output
  pinMode(OUT_01_pin, OUTPUT);
  pinMode(OUT_02_pin, OUTPUT);
  pinMode(OUT_03_pin, OUTPUT);
  pinMode(OUT_04_pin, OUTPUT);
  pinMode(OUT_05_pin, OUTPUT);
  pinMode(OUT_06_pin, OUTPUT);

  configure_duty_cycles();
  randomSeed(analogRead(A0));

  // imposta la velocità a 9600 bps
  Serial.begin(9600);

  pinMode(IN_01_pin, INPUT);
  pinMode(IN_01_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(IN_01_pin), measure_IN_01_low_duration, CHANGE);

  pinMode(IN_02_pin, INPUT_PULLUP);
  pinMode(IN_03_pin, INPUT_PULLUP);
  pinMode(IN_04_pin, INPUT_PULLUP);
  pinMode(IN_05_pin, INPUT_PULLUP);
  pinMode(IN_06_pin, INPUT_PULLUP);
}

void loop() {

  // spostare questo blocci in "setup"
  // genera un segnale PWM con duty cycle del 50%
  //analogWrite(OUT_01_pin, map(OUT_01_dutyCycle, 0, 100, 0, 255));
  analogWrite(OUT_02_pin, map(OUT_02_dutyCycle, 0, 100, 0, 255));
  analogWrite(OUT_03_pin, map(OUT_03_dutyCycle, 0, 100, 0, 255));
  analogWrite(OUT_04_pin, map(OUT_04_dutyCycle, 0, 100, 0, 255));
  analogWrite(OUT_05_pin, map(OUT_05_dutyCycle, 0, 100, 0, 255));
  analogWrite(OUT_06_pin, map(OUT_06_dutyCycle, 0, 100, 0, 255));
  
  if (Serial.available()) {
    String message = Serial.readStringUntil('\n');  // legge fino a newline
    message.trim();  // rimuove spazi vuoti o newline extra
    //Serial.println(message);

    int separator_1 = message.indexOf(':');
    int separator_2 = message.indexOf(':', separator_1 + 1);
    //int index_rcvd_value = message.indexOf(':', index_pin_number + 1);
    String command = message.substring(0, separator_1);
    String pin_number = message.substring(separator_1 + 1, separator_2);
    String rcvd_value = message.substring(separator_2 + 1);

    if (command == "1"){
      String msg = encode_data();
      //Serial.write(data_TX, 10);
      Serial.println(msg);
    }else{
      if (command == "2"){
        if (pin_number == "1") {OUT_01_dutyCycle = rcvd_value.toInt(); Serial.println("DC #1 set");}
        if (pin_number == "2") {OUT_02_dutyCycle = rcvd_value.toInt(); Serial.println("DC #2 set");}
        if (pin_number == "3") {OUT_03_dutyCycle = rcvd_value.toInt(); Serial.println("DC #3 set");}
        if (pin_number == "4") {OUT_04_dutyCycle = rcvd_value.toInt(); Serial.println("DC #4 set");}
        if (pin_number == "5") {OUT_05_dutyCycle = rcvd_value.toInt(); Serial.println("DC #5 set");}
        if (pin_number == "6") {OUT_06_dutyCycle = rcvd_value.toInt(); Serial.println("DC #6 set");}
        configure_duty_cycles();
      } 
      else {
        if (command == "3"){
          if (pin_number == "1") {Serial.println(IN_01_pump_feedback_duration);}
        }else{
          Serial.println("Comando sconosciuto");
        }
      }
    }

  }

  const byte lunghezza = 4;
  byte data_buffer[3];
  /*
  if ( Serial.available() >= 3) {
    Serial.readBytes(data_buffer, 3);
    Serial.print("Ricevuti: ");
    for (byte i = 0; i < 3; i++) {
      Serial.print(data_buffer[i]);
      Serial.print(" ");
    }
    Serial.println();
    if (data_buffer[0] == 1){
      Serial.println("Status asked");
      encode_data();
      Serial.write(data_TX, 10);
    }
    if (data_buffer[0] == 2){
      Serial.println("change DC");
      encode_data();
      Serial.write(data_TX, 10);
      }
    }
  }*/

  if (millis() - lastTime >= 2000) {
    lastTime = millis();
    //print_status();
  }
  
  if (manual_PWM_OUT1_outputState && (millis() - manual_PWM_OUT1_previousMillis >= manual_PWM_OUT1_highTime)) {
    // Turn OFF
    manual_PWM_OUT1_outputState = false;
    manual_PWM_OUT1_previousMillis = millis();
    digitalWrite(OUT_01_pin, LOW);
    configure_duty_cycles();
    //int val = random(0, 100);
    //if (val == 1) {manual_PWM_OUT1_lowTime = 500;}
  } else if (!manual_PWM_OUT1_outputState && (millis() - manual_PWM_OUT1_previousMillis >= manual_PWM_OUT1_lowTime)) {
    // Turn ON
    manual_PWM_OUT1_outputState = true;
    manual_PWM_OUT1_previousMillis = millis();
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
      Serial.println("Simulation of a Request: Pump unresponsive");
      feedback = 1;
    }else{
      Serial.print("Simulation of a Request: now it's time ");
      Serial.print(millis());
      Serial.print(": last low detected @ ");
      Serial.print(IN_01_pump_feedback_time);
      Serial.print(" for ");
      Serial.print(IN_01_pump_feedback_duration);
      Serial.println("ms");
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

}

void print_status(){
  Serial.println("01_DC:" + String(OUT_01_dutyCycle));
  Serial.println("02_DC:" + String(OUT_02_dutyCycle));
  Serial.println("03_DC:" + String(OUT_03_dutyCycle));
  Serial.println("04_DC:" + String(OUT_04_dutyCycle));
  Serial.println("05_DC:" + String(OUT_05_dutyCycle));
  Serial.println("06_DC:" + String(OUT_06_dutyCycle));
}

String encode_data(){
    String reply_message;
    reply_message = reply_message + "1:" + String(OUT_01_dutyCycle) + ":";
    reply_message = reply_message + "2:" + String(OUT_02_dutyCycle) + ":";
    reply_message = reply_message + "3:" + String(OUT_03_dutyCycle) + ":";
    reply_message = reply_message + "4:" + String(OUT_04_dutyCycle) + ":";
    reply_message = reply_message + "5:" + String(OUT_05_dutyCycle) + ":";
    reply_message = reply_message + "6:" + String(OUT_06_dutyCycle);
    return reply_message;
}

void configure_duty_cycles(){
  manual_PWM_OUT1_highTime = manual_PWM_OUT1_period * OUT_01_dutyCycle/100;
  manual_PWM_OUT1_lowTime  = manual_PWM_OUT1_period - manual_PWM_OUT1_highTime;
}

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