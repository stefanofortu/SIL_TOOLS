// Universal PWM function for Arduino Mega
// Supports Timer1, Timer3, Timer4, Timer5 (16-bit timers)

struct TimerConfig {
  volatile uint8_t *tccra;
  volatile uint8_t *tccrb;
  volatile uint16_t *icr;
  volatile uint16_t *ocr;
  uint8_t com;
};

TimerConfig getTimerConfig(uint8_t pin) {
  switch (pin) {
    // Timer1
    case 11: return { &TCCR1A, &TCCR1B, &ICR1, &OCR1A, COM1A1 };
    case 12: return { &TCCR1A, &TCCR1B, &ICR1, &OCR1B, COM1B1 };
    // Timer3
    case 5:  return { &TCCR3A, &TCCR3B, &ICR3, &OCR3A, COM3A1 };
    case 2:  return { &TCCR3A, &TCCR3B, &ICR3, &OCR3B, COM3B1 };
    case 3:  return { &TCCR3A, &TCCR3B, &ICR3, &OCR3C, COM3C1 };
    // Timer4
    case 6:  return { &TCCR4A, &TCCR4B, &ICR4, &OCR4A, COM4A1 };
    case 7:  return { &TCCR4A, &TCCR4B, &ICR4, &OCR4B, COM4B1 };
    case 8:  return { &TCCR4A, &TCCR4B, &ICR4, &OCR4C, COM4C1 };
    // Timer5
    case 46: return { &TCCR5A, &TCCR5B, &ICR5, &OCR5A, COM5A1 };
    case 45: return { &TCCR5A, &TCCR5B, &ICR5, &OCR5B, COM5B1 };
    case 44: return { &TCCR5A, &TCCR5B, &ICR5, &OCR5C, COM5C1 };
    default: return { nullptr, nullptr, nullptr, nullptr, 0 };
  }
}

void setPWM(uint8_t pin, uint16_t freq, float duty) {
  TimerConfig cfg = getTimerConfig(pin);
  if (!cfg.tccra) return; // Invalid pin

  pinMode(pin, OUTPUT);

  // Reset timer registers
  *(cfg.tccra) = 0;
  *(cfg.tccrb) = 0;

  // Calculate TOP (ICR)
  // f = 16MHz / (prescaler * (1 + TOP))
  uint32_t prescaler = 8; // Good balance for low-mid frequencies
  uint32_t top = (16000000UL / (prescaler * freq)) - 1;

  // Configure Fast PWM with ICR as TOP
  *(cfg.tccra) = (1 << cfg.com) | (1 << WGM11);
  *(cfg.tccrb) = (1 << WGM13) | (1 << WGM12);

  // Set prescaler to 8
  *(cfg.tccrb) |= (1 << CS11);

  // Set frequency
  *(cfg.icr) = top;

  // Set duty cycle
  *(cfg.ocr) = (uint16_t)(duty * top / 100.0);
}

void setup() {
  // Example: 100 Hz, 50% duty on pin 11
  setPWM(11, 100, 50);

  // Another example: 500 Hz, 75% duty on pin 5
  setPWM(5, 500, 75);
}

void loop() {
  // PWM runs automatically in hardware
  setPWM(11, 100, 50);   // 100 Hz, 50% duty on pin 11
  setPWM(6, 2000, 25);   // 2 kHz, 25% duty on pin 6
  setPWM(45, 50, 90);    // 50 Hz, 90% duty on pin 45 (good for servo testing)
}