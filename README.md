###
### Table of Contents
###

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [Code Description](#files)
4. [Future Work](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation

The drivers of OPM4 and OPM5 can be found in './drivers'. In addition, it is necessary to install the pySerial library, whose installation procedure can be found [here](https://pyserial.readthedocs.io/en/latest/pyserial.html). After that, the code should run with no issues using the Anaconda distribution of Python.

## Code Description

The code reads the optical power measured by an OPM4 or OPM 5 (AFL Telecommunications LLC, Spartanburg, USA) continuously and write them to a file.

## Future Work

TODO list:
1. Get serial port name automatically
2. Instantiate two serial objects
3. Threading for read both objects and update text file
4. Sincronize threads using an event and a callback function
5. Create class with all OPM commands
6. Get measurement from string and plot results
7. Create button to stop measurements and close serial port and text file.
 
Feel free to push your contributions to our repository!

These are complicated questions, indeed. The main goal is not to obtain an ultimate conclusion, but to play around with data and have a look at its behaviour. 

## Licensing, Authors, Acknowledgements

Feel free to use the code here as you would like!
