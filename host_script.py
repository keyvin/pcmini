import serial
import subprocess
from evdev import UInput, ecodes as e
from time import sleep
import os

import ctypes
from signal import SIGABRT

dosbox_x_control_key = e.KEY_F12
dosbox_x_speed_up = e.KEY_MINUS
dosbox_x_speed_down = e.KEY_EQUAL
dosbox_x_show_menu = e.KEY_C
dosbox_x_reset = e.KEY_R
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
        match speed:
            case 240:
                s.write(b'D04')
            case 750:   
                s.write(b'D08')
            case 1510:
                s.write(b'D12')
            case 3000:
                s.write(b'D20')
            case 3300:
                s.write(b'D22')
            case 4595:
                s.write(b'D25')
            case 6075:
                s.write(b'D33')
            case 12019:
                s.write(b'D36')
            case 23880:
                s.write(b'D60')
            case 33445:
                s.write(b'D66')
            case 43500:
                s.write(b'D75')
            case 97240:
                s.write(b'D99')
        
    #LOG: CPU:3300 cycles (auto)

#leaving this interesting snippit
c_globals = ctypes.CDLL(None) # POSIX

@ctypes.CFUNCTYPE(None, ctypes.c_int)
def sigabrt_handler(sig):
    dbx.terminate()
    print('SIGABRT')

c_globals.signal(SIGABRT, sigabrt_handler)

def send_control(key1, key2):
    ui = UInput()
    ui.write(e.EV_KEY, key1,1)
    ui.write(e.EV_KEY, key2,1)
                #ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)  # KEY_A up
    ui.write(e.EV_KEY, key1, 0)
    ui.write(e.EV_KEY, key2, 0)
    ui.syn()
    ui.close()

#try:
if __name__ == '__main__':
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
                s.write(b'S') #send keep alive
                input = s.read(1)
                print(input)
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
                if input == b'R':
                    print("Reset VM")
                    send_control(dosbox_x_control_key, dosbox_x_reset)
            dbx.kill()

#except ex:
    #print (ex)
    dbx.kill()
