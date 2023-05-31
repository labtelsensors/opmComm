'''
This code reads the optical power measured by an OPM4 continuously.

''' 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import serial
import io
import time 
from datetime import datetime

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

# Serial Parameters
name = 'COM4'

# OPM Parameters
delayTx = 10e-3    # Tx delay (s)
delayRx = 200e-3   # Rx delay (s)
smpRate = 5e-1     # OPM Sampling rate (s)

# Open Serial Port
ser = openPort(name)

if ser:    
    f = open("../measurements.txt","w")

    # Set wavelength 
    writeOPM(ser,delayTx,':INP:WAVE 5')
    time.sleep(delayRx)
    ser.reset_input_buffer()

    # Read the measurements and write to a text file
    msg_list = list()
    while True:
        writeOPM(ser,delayTx,':OUTP:MEAS?') # send command
        msg = ser.read_until(expected='\r'.encode('utf-8')).decode('utf-8') # read response    
        if len(msg)==41:                    # check expected length
            msg_list.append(msg)            # save msg to list
            f.write("{}, {}".format(datetime.now(),msg)) # write to file
            print(msg)                      # print in terminal
        else: 
            ser.reset_input_buffer()        # discard buffer

