#Things I've learned -
#Use streams, not input.
#Don't use b'' on the micropython side


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
    print('M')
    pass
    #print("button 1 pressed")

    
def b2_callback():
    print('R')
    #print("button 2 pressed")

b1 = Button(b1_pin, b1_callback, 1, long_press_ms = 1000, pullup=False)
b2 = Button(b2_pin, b2_callback, debounce_ms=1, long_press_ms=1000, pullup=False)


a = Pin(20,Pin.IN)

class BlinkDot:
    def __init__(self, dot_pin, interval=1000):
        self.pin = dot_pin
        self.time_since_switch = time.ticks_ms()
        self.interval = interval
    def checkBlink(self):        
        if time.ticks_diff(time.ticks_ms(), self.time_since_switch) > self.interval:
            self.pin.toggle()
            self.time_since_switch = time.ticks_ms()

def blank_segments():
    for i in segment_pins:
        i.on()
        
def stop_emulator():
    print("Q")




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

is_switch_on = False
state =  switched_off


timeout_count = 0

blink_dot1 = BlinkDot(segment_pins[8], 1000)
blink_dot1.checkBlink()

#assumes

poll_input = uselect.poll()
poll_input.register(sys.stdin, uselect.POLLIN)
digits_to_read = 0
in_digits = [0,0]
#our mainloop

while True:
    #Check if value of switch has changed
  
    if switch.value() == switch_on and is_switch_on == False:
        time.sleep(.1) #debounce with a blocking sleep
        if switch.value() == switch_on:
            is_switch_on = True
            state = connecting
            print("C")
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
            if poll_input.poll(100):
                c = sys.stdin.read(1)                
            
                if c == "C": #use newlines to avoid buffering issues
                    print("f")
                    state = connected
                    print("E")
            else:
                print ("C")
                time.sleep(.1)
                blink_dot1.checkBlink()
            #update throbber if enough time has passed
        if state == connected:
            if poll_input.poll(100):
                c = sys.stdin.read(1)
                if c == "S": #use newlines to avoid buffering issues
                    state = emulator_active
                    timeout_count = 0
                    print("S")
            else:
                print ("E")
                time.sleep(1)
                
        if state == emulator_active:                        

            if poll_input.poll(1): #1ms timeout
                s=sys.stdin.read(1)
                if s == 'S':
                    timeout_count = 0
                timeout_count = 0
            else:
                timeout_count = timeout_count + 1                 
            if timeout_count == 10000:
                state = connecting
                print("C")
            elif timeout_count == 1000:
                print('S')
            if s == 'D': #next two characters should be digits
                digits_to_read = 2
            elif digits_to_read > 0:        
                in_digits[digits_to_read-1] = int(s.strip())
                digits_to_read = digits_to_read -1
                if digits_to_read == 0:
                    out_digit(in_digits[0],in_digits[1],segment_1, segment_2)
                
                
            #parse status (speed, emulator type)
            #set 7segments
                
            #get status (still connected, still running, speed)
            #check emulator still running
            #show speed:
            #check buttons:
            if b1.check():
                print("X")        
            if b2.check():
                print("Y")