#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("TAG YOUR");
  lcd.setCursor(0, 1);
  lcd.print("ID CARD");
}

void loop() {
  // Handle incoming serial command from Python
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();  // Remove any newline or carriage return

    int parts[5];
    String fields[6];
    int index = 0, lastIndex = 0;

    for (int i = 0; i < 5; i++) {
      parts[i] = input.indexOf(',', lastIndex);
      fields[i] = input.substring(lastIndex, parts[i]);
      lastIndex = parts[i] + 1;
    }
    fields[5] = input.substring(lastIndex);

    int ledPin = fields[0].toInt();
    String ledState = fields[1];
    int buzzerPin = fields[2].toInt();
    String buzzerState = fields[3];
    String line1 = fields[4];
    String line2 = fields[5];

    pinMode(ledPin, OUTPUT);
    pinMode(buzzerPin, OUTPUT);
    digitalWrite(ledPin, ledState == "HIGH" ? HIGH : LOW);
    digitalWrite(buzzerPin, buzzerState == "ON" ? HIGH : LOW);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(line1);
    lcd.setCursor(0, 1);
    lcd.print(line2);
  }

  // Handle RFID detection and send UID to Python
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String content = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      content += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
      content += String(mfrc522.uid.uidByte[i], HEX);
      if (i < mfrc522.uid.size - 1) content += " ";
    }
    content.toUpperCase();
    Serial.println(content);
    delay(1000);  // Prevent multiple reads of same tag
  }
}
