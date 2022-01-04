USB-UART -> I2C bridge built on Atmega 328p. Main purpose of this project was to simplify interfacing new I2C modules without need to reprogram microcontroller each time I change something. I know there are cheap and ready-to-use solutions, but I also wanted to learn about UART and I2C. :)

Communication with Atmega can be performed using any UART terminal or my Python interface, which can be found in interface dir.

As for now, I2C bridge works in two modes: scanner mode and write mode. You can find description of this 
modes below:

Scanner mode:
This mode allows to find out the address of I2C peripheral device. If scanner is initialised, Atmega sweeps through I2C bus, 
sending all of possible addresses. If a device responds to a call, Atmega sends its address through UART.
UART communication - just send the mode code, which is ASCII value of **s** through UART to initialise the scanner.

Write mode:
This mode allows to send some data from PC to I2C bus. In order to translate it, Atmega expects following command:

            mode_code address data_length data, 

where:
mode_code - similarly to scanner mode, it is ASCII value of **w** letter
address - address of I2C device
data_length - amount of bytes that need to be sent on i2c bus
data - data bytes that will be sent on i2c bus

HW configuration:
For USB -> UART converter, I used CH340 module.
Atmega is working with 11,0592 MHz crystal oscillator.
For Atmega 328p, I used following fuse configuration.
        lfuse:w:0xff:m -U hfuse:w:0xd1:m -U efuse:w:0xff:m
Device schematic can be found in repo.
