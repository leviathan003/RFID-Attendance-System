import serial
import time
from datetime import datetime
from db import record_entry_exit, get_all_valid_tags, get_tag_roll_dict

port = "COM3" 
baud = 9600
ser = serial.Serial(port, baud, timeout=1)

LED_G = 7
LED_R = 6
BUZZER = 5

AUTHORIZED_TAGS = get_all_valid_tags()
TAG_ROLL_MAP = get_tag_roll_dict()

def read_rfid():
    line = ser.readline().decode().strip()
    return line if line else None

def send_to_arduino(led, led_state, buzzer, buzzer_state, row1, row2):
    message = f"{led},{led_state},{buzzer},{buzzer_state},{row1},{row2}\n"
    ser.write(message.encode())

def grant_access(tag, date):
    now = datetime.now().strftime("%H:%M   %d/%m/%y")
    roll = TAG_ROLL_MAP[tag]
    status = record_entry_exit(tag, datetime.now().strftime("%H:%M:%S"), date)
    send_to_arduino(LED_G, "HIGH", BUZZER, "ON", now, f"{roll} {status}")
    time.sleep(2)
    send_to_arduino(LED_G, "LOW", BUZZER, "OFF", "TAG YOUR", "ID CARD")

def deny_access():
    now = datetime.now().strftime("%H:%M   %d/%m/%y")
    send_to_arduino(LED_R, "HIGH", BUZZER, "ON", now, "UNAUTHORIZED ID")
    time.sleep(3)
    send_to_arduino(LED_R, "LOW", BUZZER, "OFF", "TAG YOUR", "ID CARD")

def main():
    user_date = input("Enter date for attendance table (DD/MM/YYYY): ")
    user_date = user_date.replace("/","_")
    send_to_arduino(LED_R, "LOW", BUZZER, "OFF", "TAG YOUR", "ID CARD")
    while True:
        try:
            tag = read_rfid()
            if tag:
                if tag in AUTHORIZED_TAGS:
                    grant_access(tag, user_date)
                else:
                    print("UNAUTHORIZED ID")
                    deny_access()
        except KeyboardInterrupt:
            print("Program stopped.")
            break

if __name__ == "__main__":
    main()
