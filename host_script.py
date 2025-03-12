import serial
import subprocess
from evdev import UInput, ecodes as e
from time import sleep
import os

dosbox_x_control_key = e.KEY_F12
dosbox_x_speed_up = e.KEY_MINUS
dosbox_x_speed_down = e.KEY_EQUAL
dosbox_x_show_menu = e.KEY_ESC
s = serial.Serial('/dev/ttyACM0', 115200)


def parse_speeds(line=None):
    if line:
        x = line.find("CPU:")
        line = ''.join(line[x:-1])
        print(line)
        line = line.split(':')[1]
        line = line.split(' ')[0]
        print(line)
        speed = int(line)
        if speed<300:
            s.write(b'D04')
        elif speed >= 300 and speed <1000:
            s.write(b'D08')
        elif speed >=1000 and speed < 1500:
            s.write(b'D12')
        elif speed >=1500 and speed <= 3300:
            s.write(b'D16')
        elif speed > 3300 and speed < 12000:
            s.write(b'D33')
        elif speed > 12000 and speed < 40000:
            s.write(b'D66')
    #LOG: CPU:3300 cycles (auto)


def send_control(key1, key2):
    ui = UInput()
    ui.write(e.EV_KEY, key1,1)
    ui.write(e.EV_KEY, key2,1)
                #ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)  # KEY_A up
    ui.write(e.EV_KEY, key1, 0)
    ui.write(e.EV_KEY, key2, 0)
    ui.syn()
    ui.close()

while True:
    sleep(.11)
   # s.write(b'f')
    input = s.read(1)    
    print(input)
    
    if input == b"C":
        s.write(b'C')
    if input == b'E':

        print("Sent Start")
        dbx = subprocess.Popen(['dosbox-x'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        os.set_blocking(dbx.stdout.fileno(), False)
        os.set_blocking(dbx.stderr.fileno(), False)
        
        s.write(b'S')
        s.write(b'D16')
        while True:
            s.write(b's') #send keep alive
            input = s.read(1)
            if input == b'X':
                print ("Speed Down")
                send_control(dosbox_x_control_key, dosbox_x_speed_up)
                sleep(.1)
                msg = dbx.stderr.readlines()

                parse_speeds(msg[-1])
            if input == b'Y':
                print ("speed Up")
                send_control(dosbox_x_control_key, dosbox_x_speed_down)  
                sleep(.1)
                msg = dbx.stderr.readlines()
                parse_speeds(msg[-1])
            if input == b'Q':
                break
            if input == b'M':
                print("show menu")
                send_control(dosbox_x_control_key, dosbox_x_show_menu)
            
        dbx.kill()