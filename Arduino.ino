#include <DHT.h>
#include <OneWire.h>
#define DHTPIN 2
OneWire ds(3);
int temperature = 0; // Глобальная переменная для хранения значение температуры с датчика DS18B20
long lastUpdateTime = 0; // Переменная для хранения времени последнего считывания с датчика
const int TEMP_UPDATE_TIME = 1000; // Определяем периодичность проверок

DHT dht(DHTPIN, DHT22); 
void setup() {
  pinMode(6, OUTPUT);
  Serial.begin(9600);
  dht.begin();
  digitalWrite(6, HIGH);
}

void loop() {
  if (Serial.available()){
    char r = Serial.read();
    if (r == 'H') {
      float h = dht.readHumidity(); //Измеряем влажность
      if (isnan(h)) {  // Проверка. Если не удается считать показания, выводится «Ошибка считывания», и программа завершает работу
        Serial.println("1000");
      }
      else{
        Serial.println(h);
      }
    }
    if (r == 'T') {
      float t = dht.readTemperature(); //Измеряем температуру
      if (isnan(t)) {  // Проверка. Если не удается считать показания, выводится «Ошибка считывания», и программа завершает работу
        Serial.println("1000");
      }
      else{
        Serial.println(t);
      }
    }
    if (r == '1'){
     digitalWrite(6, LOW);   // turn the LED on (LOW is the voltage level)            
    }
    if (r == '2'){
     digitalWrite(6, HIGH);   // turn the LED on (LOW is the voltage level)            
    }
    if (r == 't') {
      byte data[2];
      ds.reset();
      ds.write(0xCC);
      ds.write(0x44);
      if (millis() - lastUpdateTime > TEMP_UPDATE_TIME)
      {
        lastUpdateTime = millis();
        ds.reset();
        ds.write(0xCC);
        ds.write(0xBE);
        data[0] = ds.read();
        data[1] = ds.read();
        // Формируем значение
        temperature = (data[1] << 8) + data[0]; temperature = temperature >> 4;
        Serial.println(temperature);
        }
    }
  }
}
