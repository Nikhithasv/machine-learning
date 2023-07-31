Arduino code for mq6 sensor interfaced with Arduino uno:
#define MQ2pin (0)

float sensorValue;  //variable to store sensor value
String nk = "";

void setup()
{
  Serial.begin(9600); // sets the serial port to 9600
  //Serial.println("Gas sensor warming up!");
  delay(20000); // allow the MQ-2 to warm up
}

void loop()
{
 
  sensorValue = analogRead(MQ2pin); // read analog input pin 0
  
  //Serial.print("Sensor Value: ");
  //sensorValue = String(sensorValue)
  //
  nk = nk + sensorValue;
  Serial.print(nk);
  nk = "";
  
  if(sensorValue > 130)
  {
    //Serial.print(" | Smoke detected!");
  }
  
  Serial.println("\n");
  delay(2000); // wait 2s for next reading
}

