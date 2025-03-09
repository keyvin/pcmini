from machine import Pin
from button import Button
import time
import sys
import uselect


#switch  is active low


b1_pin = 20
b2_pin = 21
switch_pin = 22

#true if active high, false otherwise
switch_on = False
switch_off = not switch_on
if switch_on == False:
    switch = Pin(switch_pin, Pin.IN, Pin.PULL_UP)
else:
    switch = Pin(switch_pin, Pin.IN, Pin.PULL_DOWN)


digits = {1:"bc", 2:"abged", 3:"abgcd", 4:"fgbc", 5:"afgcd", 6:"afegcd", 7:"fabc", 8:"abcdefg", 9:"abfgc",0:"abcdef"}
segment_1 = {'a':7,'b':6,'c':0,'d':5,'e':4,'f':3,'g':2, 'p':1}
segment_2 = {'a':15,'b':14,'c':13,'d':12,'e':11,'f':10,'g':9, 'p':8}

segment_pins = []



for i in range(0,16):
    segment_pins.append(Pin(i,Pin.OUT))
    segment_pins[i].on()


def b1_callback():
    print("button 1 pressed")

    
def b2_callback():
    print("button 2 pressed")

b1 = Button(b1_pin, b1_callback, 1, 200, pullup=False)
b2 = Button(b2_pin, b2_callback, debounce_ms=1, long_press_ms=5, pullup=False)

print("Hello World!")

a = Pin(20,Pin.IN)

def blank_segments():
    pass
def stop_emulator():
    pass


#reverse for C.A. vs C.C.

def out_digit(digit1,digit2, segment1, segment2):
    for i in range(0,15):
        segment_pins[i].on()    
        
    for i in digits[digit1]:        
        segment_pins[segment1[i]].off()

    for i in digits[digit2]:        
        segment_pins[segment2[i]].off()

switched_off = 0
connecting = 2
connected = 3
emulator_active = 4

is_switch_on = True
state =  emulator_active


timeout_count = 0


#assumes

poll_input = uselect.poll()
poll_input.register(sys.stdin, uselect.POLLIN)

#our mainloop

while True:
    #Check if value of switch has changed
  
    if switch.value() == switch_on and is_switch_on == False:
        time.sleep(.1) #debounce with a blocking sleep
        if switch.value() == switch_on:
            print("ON!")
            is_switch_on = True
            state = connecting
            print("C\n")
    elif switch.value() == switch_off and is_switch_on == True:
        time.sleep(.1) #time debounce
        if switch.value() == switch_off:
            is_switch_on = False
            blank_segments()
            stop_emulator()
            state = switched_off
    #switch is the same
    if is_switch_on:
        if state == connecting:
            #check if we've gotten anything in stdin (our serial)
            if poll_input.poll(10000):
                c = input()
                print(c)
                if c == "Connected!": #use newlines to avoid buffering issues
                    print("Connected\n")
                    state = connected
                    print("E\n")
            else:
                print ("C\n")
                time.sleep(.1)
            #update throbber if enough time has passed
        if state == connected:
            if poll_input.poll(1000):
                c = input()
                if c == "Started!": #use newlines to avoid buffering issues
                    state = emulator_active
                    timeout_count = 0
                    print("S\n")
            else:
                print ("S\n")
                time.sleep(1)
                
        if state == emulator_active:                        

            if poll_input.poll(1): #1s timeout
                s=input()                
            else:
  
                timeout_count = timeout_count + 1                 
                if timeout_count == 10000:
                    state = connecting
                    print("C\n")
            #parse status (speed, emulator type)
            #set 7segments
                
            #get status (still connected, still running, speed)
            #check emulator still running
            #show speed:
            #check buttons:
            if b1.check():
               out_digit(0,1,segment_1,segment_2)         
            if b2.check():
                out_digit(0,2,segment_1,segment_2)   
