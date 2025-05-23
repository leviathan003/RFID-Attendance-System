import serial
from db import register_newTagID, get_all_valid_tags

port = "COM3"  
baud = 9600
ser = serial.Serial(port, baud, timeout=1)

LED_G = 7
LED_R = 6
BUZZER = 5

AUTHORIZED_TAGS = get_all_valid_tags()

def read_rfid():
    line = ser.readline().decode().strip()
    return line if line else None

def main():
    while True:
        try:
            tag = read_rfid()
            if tag:
                if tag not in AUTHORIZED_TAGS:
                    name = input("Enter name of candidate: ")
                    roll = input("Enter roll number of candidate: ")
                    register_newTagID(tag,roll,name)
                    return
                else:
                    print("Error: Tag already registered!!")
        except KeyboardInterrupt:
            print("Program stopped.")
            break

if __name__ == "__main__":
    main()
