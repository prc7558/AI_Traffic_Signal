/*
 * Traffic Light Controller for Arduino
 * Controls 3 LEDs (Red, Yellow, Green) based on commands from Python
 * 
 * Hardware Setup:
 * - Red LED on Pin 13
 * - Yellow LED on Pin 12
 * - Green LED on Pin 11
 * - Each LED connected through 220Ω resistor to ground
 */

// Define LED pins
const int RED_PIN = 13;
const int YELLOW_PIN = 12;
const int GREEN_PIN = 11;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set LED pins as output
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  
  // Turn all LEDs off initially
  digitalWrite(RED_PIN, LOW);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);
  
  // Startup blink to show system is ready
  for (int i = 0; i < 3; i++) {
    digitalWrite(RED_PIN, HIGH);
    delay(200);
    digitalWrite(RED_PIN, LOW);
    digitalWrite(YELLOW_PIN, HIGH);
    delay(200);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(GREEN_PIN, HIGH);
    delay(200);
    digitalWrite(GREEN_PIN, LOW);
  }
  
  Serial.println("Traffic Light Controller Ready");
}

void loop() {
  // Check if data is available from Python
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // Turn all LEDs off first
    digitalWrite(RED_PIN, LOW);
    digitalWrite(YELLOW_PIN, LOW);
    digitalWrite(GREEN_PIN, LOW);
    
    // Process command
    switch (command) {
      case 'R':  // Red light
        digitalWrite(RED_PIN, HIGH);
        Serial.println("RED ON");
        break;
        
      case 'Y':  // Yellow light
        digitalWrite(YELLOW_PIN, HIGH);
        Serial.println("YELLOW ON");
        break;
        
      case 'G':  // Green light
        digitalWrite(GREEN_PIN, HIGH);
        Serial.println("GREEN ON");
        break;
        
      default:
        Serial.println("Unknown command");
        break;
    }
  }
}
