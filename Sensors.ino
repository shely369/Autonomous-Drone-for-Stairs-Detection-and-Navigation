const int trigPin1 = 8;  // Bottom sensor
const int echoPin1 = 3;  // Bottom sensor echo
const int trigPin2 = 11; // Front sensor
const int echoPin2 = 6;  // Front sensor echo
const int ledPin1 = 4;   // Blue light - bottom sensor
const int ledPin2 = 5;   // Green light - front sensor

void setup() {
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  float distance1 = measureDistance(trigPin1, echoPin1); // bottom sensor
  float distance2 = measureDistance(trigPin2, echoPin2); // front sensor

  // Turn on/off LED based on threshold (e.g., 30 cm)
  digitalWrite(ledPin1, distance1 < 30 ? HIGH : LOW);
  digitalWrite(ledPin2, distance2 < 30 ? HIGH : LOW);

  // Send a single JSON string over Serial
  Serial.print("{\"sensor1\": ");
  Serial.print(distance1, 2); // 2 decimal places
  Serial.print(", \"sensor2\": ");
  Serial.print(distance2, 2);
  Serial.println("}");

  delay(100);
}

float measureDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  float distance = (duration * 0.0343) / 2;
  return distance;
}
