from machine import Pin
from button import Button
import time


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

b1 = Button(20, b1_callback, 1, 200, False)
b2 = Button(21, b2_callback, debounce_ms=1, long_press_ms=5, pullup=False)

print("Hello World!")

a = Pin(20,Pin.IN)

#reverse for C.A. vs C.C.

def out_digit(digit1,digit2, segment1, segment2):
    for i in range(0,15):
        segment_pins[i].on()    
        
    for i in digits[digit1]:        
        segment_pins[segment1[i]].off()

    for i in digits[digit2]:        
        segment_pins[segment2[i]].off()



while True:
    for i in range(0,9):
        for j in range(0,9):
            out_digit(i, j, segment_1, segment_2)        
            time.sleep(1)
