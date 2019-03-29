/*
   LoRaLib Receive Example

   This example listens for LoRa transmissions and tries to
   receive them. To successfully receive data, the following
   settings have to be the same on both transmitter 
   and receiver:
    - carrier frequency
    - bandwidth
    - spreading factor
    - coding rate
    - sync word
    - preamble length

   For more detailed information, see the LoRaLib Wiki
   https://github.com/jgromes/LoRaLib/wiki

   For full API reference, see the GitHub Pages
   https://jgromes.github.io/LoRaLib/
*/

// include the library
#include <LoRaLib.h>

// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 7, en = 6, d4 = A0, d5 = A1, d6 = A2, d7 = A3;

// create instance of LoRa class using SX1278 module
// this pinout corresponds to KITE Shield
// https://github.com/jgromes/KiteShield
// NSS pin:   10 (4 on ESP32/ESP8266 boards)
// DIO0 pin:  2
// DIO1 pin:  3

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
SX1278 lora = new LoRa;

void setup() {
  lcd.begin(16, 2);

  digitalWrite(8, HIGH);
  lcd.print("Initializing...");
  delay(1000);
  Serial.begin(9600);

  // initialize SX1278 with default settings
  Serial.print(F("Initializing ... "));
  // carrier frequency:           434.0 MHz
  // bandwidth:                   125.0 kHz
  // spreading factor:            9
  // coding rate:                 7
  // sync word:                   0x12
  // output power:                17 dBm
  // current limit:               100 mA
  // preamble length:             8 symbols
  // amplifier gain:              0 (automatic gain control)
  int state = lora.begin(434.0, 125.0, 12);
  if (state == ERR_NONE) {
    Serial.println(F("success!"));
  } else {
    Serial.print(F("failed, code "));
    Serial.println(state);
    while (true);
  }
}

void loop() {
  digitalWrite(8, HIGH);
  lcd.setCursor(0, 0);
  lcd.print("Listening now ...");
  
  Serial.print("Waiting for incoming transmission ... ");

  // you can receive data as an Arduino String
  String str;
  int state = lora.receive(str);

  // you can also receive data as byte array
  /*
    byte byteArr[8];
    int state = lora.receive(byteArr, 8);
  */

  if (state == ERR_NONE) {
    // packet was successfully received
    Serial.println("success!");

    // print data of the packet
    Serial.print("Data:\t\t\t");
    Serial.println(str);

    lcd.setCursor(0, 0);
    lcd.print("Received new msg :");
    lcd.setCursor(0, 1);
    lcd.print(str);
    delay(500);

    // print RSSI (Received Signal Strength Indicator) 
    // of the last received packet
    Serial.print("RSSI:\t\t\t");
    Serial.print(lora.getRSSI());
    Serial.println(" dBm");

    // print SNR (Signal-to-Noise Ratio) 
    // of the last received packet
    Serial.print("SNR:\t\t\t");
    Serial.print(lora.getSNR());
    Serial.println(" dB");

    // print frequency error
    // of the last received packet
    Serial.print("Frequency error:\t");
    Serial.print(lora.getFrequencyError());
    Serial.println(" Hz");

  } else if (state == ERR_RX_TIMEOUT) {
    // timeout occurred while waiting for a packet
    Serial.println("timeout!");

  } else if (state == ERR_CRC_MISMATCH) {
    // packet was received, but is malformed
    Serial.println("CRC error!");

  }
}
