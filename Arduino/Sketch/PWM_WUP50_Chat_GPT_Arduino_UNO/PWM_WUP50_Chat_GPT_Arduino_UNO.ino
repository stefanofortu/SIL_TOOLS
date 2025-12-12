void setup() {
  // Set Timer1 prescaler to 256 → ~62 Hz
  TCCR1B = (TCCR1B & 0b11111000) | 0x05;

  pinMode(9, OUTPUT);
}

void loop() {
  analogWrite(9, 128);  // 50% duty cycle
}