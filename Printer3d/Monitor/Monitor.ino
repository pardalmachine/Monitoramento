
 
int AdcP=0;
int valor=0;

void setup() {

  Serial.begin(115200);
  
}

void loop() {
  valor = analogRead(AdcP);
  Serial.println(valor);
  delay(1000);
  // put your main code here, to run repeatedly:

}
