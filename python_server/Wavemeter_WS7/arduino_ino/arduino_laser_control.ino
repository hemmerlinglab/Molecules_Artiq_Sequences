int  val       = 3;
int  noofbytes = 0;
int  chan      = 0;
char buf[5];


void setup()
{
   Serial.begin(115200);
   analogWriteResolution(12);
   analogWrite(DAC0,2048);
   analogWrite(DAC1,2048);
}

int conv(char ch)
{
  switch(int(ch)) {
    case 176 : return 0; break;
    case 49  : return 1; break;
    case 50  : return 2; break;
    case 179 : return 3; break;
    case 52  : return 4; break;
    case 181 : return 5; break;
    case 182 : return 6; break;
    case 55  : return 7; break;
    case 56  : return 8; break;
    case 185 : return 9; break;
  }
}

void loop()
{
  
  if (Serial.available() > 0) {
                
					 // read the incoming byte:
                noofbytes = Serial.readBytes(buf,5);
                chan = conv(buf[4]);                
                val = conv(buf[3]) + 10*conv(buf[2]) + 100*conv(buf[1]) + 1000*conv(buf[0]);
                
                //chan = 1;
                if(chan==1){
                  analogWrite(DAC0,val);
                }

                //chan = 2;
                if(chan==2){
                  analogWrite(DAC1,val);
                }
                // analogRead values go from 0 to 1023, analogWrite values from 0 to 255
              
        }
        
  delay(2);
  
}
