uint16_t WRITE, index2 = 0, BYTE1, BYTE2;
uint8_t index1 = 0;
//char *ptr;
char READ1[6], READ2[6];
char inCharacter;
bool end_READ1 = false, end_READ2 = true;

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  WRITE = ((PIND & B11111100) >> 2) | ((PINB & B00111111) << 6) | ((PINC & B00001111) << 12);
  delayMicroseconds(300);
  Serial.println(WRITE);

  
  //WRITE[0] = ((PIND & B11111100) >> 2) | ((PINB & B00000011) << 6);
  //WRITE[1] = ((PINB & B00111100) << 2) | (PINC & B00001111);
  //WRITE[2] = (byte)('\n');
  //Serial.write(WRITE,3);
  
  //if (READ1[0] != '\0')
  //{
    DDRD |= ((BYTE1 << 2));
    DDRD &= ((BYTE1 << 2) | B00000011);

    DDRB |= ((BYTE1 >> 6) & B00111111);
    DDRB &= ((BYTE1 >> 6) | B11000000);

    DDRC |= ((BYTE1 >> 12) & B00001111);
    DDRC &= ((BYTE1 >> 12) | B11110000);
  //}
  //if (READ2[0] != '\0')
  //{
    PORTD |= ((BYTE2 << 2));
    PORTD &= ((BYTE2 << 2) | B00000011);

    PORTB |= ((BYTE2 >> 6) & B00111111);
    PORTB &= ((BYTE2 >> 6) | B11000000);

    PORTC |= ((BYTE2 >> 12) & B00001111);
    PORTC &= ((BYTE2 >> 12) | B11110000);
  //}
  
 Serial.flush();


}


void serialEvent()
{
  while (Serial.available())
  {
    inCharacter = (char)(Serial.read());
    if (inCharacter == ',')
    {
      READ1[index1++] = '\0';
      BYTE1 = atoi(READ1);
      memset(READ1, 0, sizeof(READ1));
      end_READ1 = true;
      end_READ2 = false;
      index1 = 0;
    }
    else if (inCharacter == '\n')
    {
      READ2[index2++] = '\0';
      BYTE2 = atoi(READ2);
      memset(READ2, 0, sizeof(READ2));
      end_READ2 = true;
      end_READ1 = false;
      index2 = 0;
    }

    else if (end_READ1 == false && end_READ2 == true)
      READ1[index1++] = inCharacter;
    else if (end_READ2 == false && end_READ1 == true)
      READ2[index2++] = inCharacter;
  }
}
