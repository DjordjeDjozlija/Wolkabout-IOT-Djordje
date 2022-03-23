import os
import random
import sys
from time import sleep
import time                                    #IMPORTOVANJE SVIH POTREBNIH BIBLIOTEKA
import Adafruit_DHT
from gpiozero import LED
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#DODIJELJIVANJE GPIO PINOVA LEDOVKAMA
led1=LED(17) #CRVENA
led2=LED(27) #PLAVA
led3=LED(22) #ZUTA


#KONFIGURACIJA OLEDA I DODIJELJIVANJE SLEJV ADRESE OLEDA
RST = 24
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)


# INICIJALIZACIJA BIBILIOTEKE
disp.begin()

# BRISANJE DISPLEJA
disp.clear()
disp.display()


width = disp.width
height = disp.height
image = Image.new('1', (width, height))   #MONOHROMATSKA SLIKA, 1bitna boja
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = 2
shape_width = 20
top = padding
bottom = height-padding

x = padding

font = ImageFont.load_default()

draw.text((x, top),    'DJORDJE DJOZLIJA',  font=font, fill=255)
draw.text((x, top+15), 'HISTEREZISNO', font=font, fill=255)
draw.text((x, top+25), 'UPRAVLJANJE', font=font, fill=255)
draw.text((x, top+35), 'TEMPERATURE', font=font, fill=255)
draw.text((x, top+50), 'I PRIKAZ VLAZNOSTI', font=font, fill=255)
disp.image(image)
disp.display()


sensor = Adafruit_DHT.DHT11
pin = 4




module_path = os.sep + ".." + os.sep + ".." + os.sep
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + module_path)
import wolk 



def main():
    
    device = wolk.Device(key="temp", password="6TTGWM2QT1")   #GENERISALI SMO NAS DEVICE "GREJAC ZA KLIMU" i pomocu njegovih kredencijala
    wolk_device = wolk.WolkConnect(device)                    #key i passworda konektujemo nas raspi na kom je senzor na wolkabaout platformu
    wolk_device.connect()
    
    

    publish_period_seconds = 2

    while True:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)    #OCITAVANJA VLAZNOSTI I TEMP 
            if humidity is not None and temperature is not None:
                wolk_device.add_sensor_reading("temp", temperature)     #WOLK Cita TEMPERATURU !!!VAZNA JE REFERENCA PRIJE STVARI KOJA SE CITA
                wolk_device.publish()                                   #WOLK PUBLISHUJE NA IOT PLATFORMU
                print('Publishing "Temperatura": ' + str(temperature) + ' *C')    #SHELL ispisuje samo PUBLISHOVANJE TEMP I VLAZNOSTI
                wolk_device.add_sensor_reading("Humidity", humidity)
                print('Publishing "Vlaznost": ' + str(humidity) + ' %') 
                wolk_device.publish()
                time.sleep(publish_period_seconds)
                temperatura=temperature
                str_temp = str(temperature)+ ' *C'       #PRETVARANJE VRIJEDNOSTI SA SENZORA U STRING KOJI SE ISPISUJE NA OLEDU
                str_hum  = str(humidity) + ' %'
            if (temperatura <28):
                  draw.rectangle((0,0,width,height), outline=0, fill=0)     
                  draw.text((3,top), 'TEMPERATURA', font=font, fill=255)
                  draw.text((x+70,top), str_temp , font=font, fill=255)
                  draw.text((3,top+22), 'Ukljucen grejac', font=font, fill=255)     #ISPISIVANJE NA EKRANU KADA JE TEMP<28 i UKLJUCUJE SE PLAVA DIODA
                  draw.text((x,top+44), 'VLAZNOST' , font=font, fill=255)           #Ovo je naznaka za za zuti warning na IoT serveru 
                  draw.text((x+70, top+44), str_hum, font=font, fill=255)
                  disp.image(image)
                  disp.display()
                  led3.on()
                  led1.off()
                  led2.off()
            if(temperatura>34):
                  draw.rectangle((0,0,width,height), outline=0, fill=0)                
                  draw.text((3,top), 'TEMPERATURA', font=font, fill=255)
                  draw.text((x+70,top), str_temp , font=font, fill=255)
                  draw.text((3,top+22), 'Grejac iskljucen', font=font, fill=255)  #ISPISIVANJE NA EKRANU KADA JE TEMP>34 i UKLJUCUJE SE CRVENA DIODA
                  draw.text((x,top+44), 'VLAZNOST' , font=font, fill=255)         #Ovo je naznaka za za crveni alaram na IoT serveru              
                  draw.text((x+70, top+44), str_hum, font=font, fill=255)
                  disp.image(image)
                  disp.display()
                  led3.off()
                  led1.off()
                  led2.on()
            if (temperatura >26 and temperatura <33 ):
                  draw.rectangle((0,0,width,height), outline=0, fill=0)                
                  draw.text((3,top), 'TEMPERATURA', font=font, fill=255)
                  draw.text((x+70,top), str_temp , font=font, fill=255)
                  draw.text((3,top+22), 'Postignuta temp.', font=font, fill=255)  #ISPISIVANJE KADA JE POSTIGNUTA TEMP 26<temp<33 UKLJUCUJE SE ZUTA DIODA 
                  draw.text((x,top+44), 'VLAZNOST' , font=font, fill=255)         #Ovo je naznaka za ispravan rad (zelena boja) na upozorenjima
                  draw.text((x+70, top+44), str_hum, font=font, fill=255)
                  disp.image(image)
                  disp.display()
                  led3.off()
                  led1.on()
                  led2.off()
                
        except KeyboardInterrupt:
            print("\tReceived KeyboardInterrupt. Exiting script")   #PRITISKOM NA TASTATURU U SHELLU IZLAZIMO IZ SKRIPTE I OBJAVLJIVANJA
            wolk_device.disconnect()
            sys.exit()
            


if __name__ == "__main__":
    main()