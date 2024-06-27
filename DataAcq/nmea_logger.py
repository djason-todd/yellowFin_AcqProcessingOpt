import serial
import datetime
import os
import logging
from datetime import date
from setSysClockFromGGA import setClockfromGGA

serialPort = '/dev/ttyACM1'
setClockfromGGA(serialPort)

BUFFER_SIZE = 100

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with serial.Serial(port=serialPort, baudrate=115200, bytesize=8,
                   timeout=2, stopbits=serial.STOPBITS_ONE) as ser:
    currTS2 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    today = date.today()
    d4 = today.strftime("%m-%d-%Y")
    path = f"./Data/nmeadata/{d4}"
    
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Made Directory {path}")
    
    file_name = f"./Data/nmeadata/{d4}/{currTS2}.dat"
    file1 = open(file_name, 'w')
    buffer = []

    while True:
        line = ser.readline().decode('ascii', errors='replace')  # first read the line
        datestr = str(datetime.datetime.now())
        buffer.append(f'### {datestr} {line.strip()}')
        
        if len(buffer) >= BUFFER_SIZE:
            file1.write('\n'.join(buffer) + '\n')
            buffer = []

            file1.close()
            currTS2 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"./Data/nmeadata/{d4}/{currTS2}.dat"
            file1 = open(file_name, 'w')

    if buffer:
        file1.write('\n'.join(buffer) + '\n')
    file1.close()
