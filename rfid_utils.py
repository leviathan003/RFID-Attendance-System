import serial, time
from datetime import datetime
from db import record_entry_exit, get_tag_roll_dict

port = "COM3"  
baud = 9600
ser = serial.Serial(port, baud, timeout=1)

LED_G = 7
LED_R = 6
BUZZER = 5

def read_rfid():
    line = ser.readline().decode().strip()
    return line if line else None

def sendMessageToArduino(led, led_state, buzzer, buzzer_state, row1, row2):
    message = f"{led},{led_state},{buzzer},{buzzer_state},{row1},{row2}\n"
    ser.write(message.encode())

def grant_access(tag, date):
    date = date.replace("/","_")
    now = datetime.now().strftime("%H:%M   %d/%m/%y")
    roll = get_tag_roll_dict()[tag]
    status = record_entry_exit(tag, datetime.now().strftime("%H:%M:%S"), date)
    sendMessageToArduino(LED_G, "HIGH", BUZZER, "ON", now, f"{roll} {status}")
    time.sleep(2)
    sendMessageToArduino(LED_G, "LOW", BUZZER, "OFF", "TAG YOUR", "ID CARD")

def deny_access():
    now = datetime.now().strftime("%H:%M   %d/%m/%y")
    sendMessageToArduino(LED_R, "HIGH", BUZZER, "ON", now, "UNAUTHORIZED ID")
    time.sleep(3)
    sendMessageToArduino(LED_R, "LOW", BUZZER, "OFF", "TAG YOUR", "ID CARD")
