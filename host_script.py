import serial
from time import sleep
s = serial.Serial('/dev/ttyACM0', 115200)

while True:
    sleep(.11)
   # s.write(b'f')
    input = s.read(1)    
    print(input)
    
    if input == b"C":
        print("Sent")
        s.write(b'C')
    if input == b'E':
        print("Sent Start")
        s.write(b'S')
        Running=True
        while Running:
            s.write(b's1')
            sleep(1)
    