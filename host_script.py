import serial
import subprocess
from evdev import UInput, ecodes as e
from time import sleep
s = serial.Serial('/dev/ttyACM0', 115200)

while True:
    sleep(.11)
   # s.write(b'f')
    input = s.read(1)    
    print(input)
    
    if input == b"C":
        s.write(b'C')
    if input == b'E':
        print("Sent Start")
        dbx = subprocess.Popen(['dosbox-x'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s.write(b'S')
        Running=True
        while Running:
            s.write(b's') #send keep alive
            input = s.read(1)
            if input == b'X':
                print ("Speed up")
                ui = UInput()
                # accepts only KEY_* events by default
                #ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 1)
                ui.write(e.EV_KEY, e.KEY_F12,1)
                ui.write(e.EV_KEY, e.KEY_MINUS,1)
                #ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)  # KEY_A up
                ui.write(e.EV_KEY, e.KEY_F12, 0)
                ui.write(e.EV_KEY, e.KEY_MINUS,0)
                ui.syn()
                ui.close()
            