'''
This code reads multiple optical power meters continuously
until 'exit' is written in the command line.

''' 
import matplotlib.pyplot as plt
import logging
import serial
import re
import time 
from datetime import datetime
import threading
import queue

def openPort(port_name,baud_rate=115200,time_out=1):
    '''
    Try to open a serial port. 
    Parameters: port_name - string - serial port name
                baud_rate - int - baud rate
                time_out - int - timeout
    Return: ser - Serial - serial object
    '''
    try:
        ser = serial.Serial(port=port_name, baudrate=baud_rate, timeout=time_out)
    except serial.SerialException as err:
        logging.error(err)
        return 
    except TypeError as err:
        logging.error(err)
        return 
    return ser

def writeOPM(ser,delay,command):
    '''
    Write a command to the serial port. 
    Parameters: ser - Serial - serial object
                delay - int - time delay between bytes
                command - string - command to be written
    '''
    ser.reset_input_buffer()
    for byte in command:
        ser.flush()
        ser.write(byte.encode('utf-8')) # Write command
        time.sleep(delay)
    
    ser.write("\r".encode('utf-8'))     # Carriage return 
    ser.flush()

def getKeyboardInput(input_queue):
    char_key = input()
    input_queue.put(char_key)

def getOPMMeasurement(_queue,ser):    
    writeOPM(ser,delayTx,':OUTP:MEAS?') # send command
    msg = ser.read_until(expected='\r'.encode('utf-8')).decode('utf-8') # read response  
    if len(msg)==41:                    # check expected length
        _queue.put(msg)  
    else: 
        ser.reset_input_buffer()        # discard buffer

def setWavelength(ser):
    writeOPM(ser,delayTx,':INP:WAVE 5')
    time.sleep(delayRx)
    ser.reset_input_buffer()

def getInfoFromMsg(msg):
    try:
        info = pattern.findall(msg)[0]
        return info
    except:
        return ''
     
# Serial Parameters
name_opm = ['COM3','COM4']

# OPM Parameters
delayTx = 10e-3    # Tx delay (s)
delayRx = 200e-3   # Rx delay (s)
smpRate = 5e-1     # OPM Sampling rate (s)

# Open Serial Port
ser0 = openPort(name_opm[0])
ser1 = openPort(name_opm[1])

# regex expression
pattern = re.compile("nm,(.*) dBm,  0.00 dBm,")

# Instantiate queue and thread for keyboard
input_queue = queue.Queue()
input_thread = threading.Thread(target=getKeyboardInput, args=(input_queue,), daemon=True)
input_thread.start()

# Instantiate opm threads
opm_arg = [ser0, ser1]
opm_queue = [queue.Queue() for arg in opm_arg]

# File parameters
file_path = "C:/Users/Mariana Lyra/Documents/Python/OPM_AFL/data/measurements.txt"
f = open(file_path,"w")

if (ser0.is_open) & (ser1.is_open):    

    # Set wavelength 
    setWavelength(ser0)
    setWavelength(ser1)

    # Read the measurements and write to a text file
    msg_list = list()
    print('Program has started.') 
    opm_threads = [threading.Thread(target=getOPMMeasurement, args=(opm_queue[i],opm_arg[i],), daemon=True) for i in range(len(opm_arg))]
    [t.start() for t in opm_threads]   
    
    while True:
        if ((opm_threads[0].is_alive() == False) & (opm_threads[1].is_alive() == False)):
            # Start threads
            opm_threads = [threading.Thread(target=getOPMMeasurement, args=(opm_queue[i],opm_arg[i],), daemon=True) for i in range(len(opm_arg))]
            [t.start() for t in opm_threads]

        # Collect measurements
        if ((opm_queue[0].empty() == False) & (opm_queue[1].empty() == False)):
            msg = [q.get(block=True,timeout=1) for q in opm_queue]
            info = [getInfoFromMsg(m) for m in msg]            
            f.write("{}, {}, {}\r".format(datetime.now(), info[0], info[1])) # write to file        

        #time.sleep(delayRx)
        # Check keyboard input
        if (input_queue.qsize() > 0):
            char_key = input_queue.get()
            if (char_key.lower() == 'exit'):
                break
            else:
                input_thread.join()
                input_thread = threading.Thread(target=getKeyboardInput, args=(input_queue,), daemon=True)
                input_thread.start()       
    
    print('Program ended.')
    f.close()