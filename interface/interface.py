import serial
from serial.tools import list_ports
import binascii
import os
import platform


if "Windows" in str(platform.os):
    clear_cmd = 'cls'
else:
    clear_cmd = 'clear'

class I2CCommandFree():

    def __init__(self):
        self.address = str()
        self.data = str()
        self.command_raw = str()
        self.command = str()
        self.length = str()

    def get_command_raw(self):
        while(True):
            self.command_raw = input("Type address and data to be sent: ")
            self.command_raw = self.command_raw.replace(' ', '')
            if len(self.command_raw)%2 != 0:
                print("Wrong input length. Try again.")
            elif int(self.command_raw[:2], 16) > 127:
                print("Wrong address. Try again.")
            else:
                break

    def extract_address_and_data(self):
        self.address = self.command_raw[:2]
        self.data = self.command_raw[2:]

    def calculate_length(self):
        length_raw = int(len(self.data)/2)
        length_hex = hex(length_raw)[2:]
        if len(length_hex) == 1:
            length_hex = '0' + length_hex
        self.length = length_hex

    def prepare_command(self):
        cmd_code = '77'
        self.calculate_length()
        command_str = f"{cmd_code}{self.address}{self.length}{self.data}"
        self.command = binascii.unhexlify(command_str)
        
class I2CCommandFixed():

    def __init__(self):
        self.address = str()
        self.data = str()
        self.command = str()
        self.length = str()

    def get_address(self):
        print("Specify address:")
        while(True):
            self.address = input()
            if len(self.address) != 2:
                print("wrong address, try again:")
            else:
                break
    
    def get_data(self):
        print("type data to be send:")
        data_raw = input()
        self.data = data_raw.replace(' ', '')
        if len(self.data)%2 != 0:
            print("data length error. Try again")\

    def calculate_length(self):
        length_raw = int(len(self.data)/2)
        length_hex = hex(length_raw)
        length_hex = length_hex[2:]
        if len(length_hex) == 1:
            length_hex = '0' + length_hex
        self.length = length_hex

    def prepare_command(self):
        cmd_code = '77'
        self.calculate_length()
        command_raw = f"{cmd_code}{self.address}{self.length}{self.data}"
        self.command = binascii.unhexlify(command_raw)


def serial_init():
    print("Available ports:\n")
    print("%-5s %-10s"%("id", "port"))
    port_list = serial.tools.list_ports.comports()
    for index, port in enumerate(port_list):
        print("%-5i %-10s"%(index, port.name))
    port_nr = input("\n"+"Select port id: ")
    ser_port = str(port_list[int(port_nr)]).split(' ')[0]
    
    ser_dev = serial.Serial(port=ser_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2)
    return ser_dev

def mode_selection():
    os.system(clear_cmd)
    while 1:
        print("Select work mode of terminal:\n")
        print("1 - fixed address mode")
        print("2 - free mode")
        print("3 - scanner")
        mode = input()
        if mode == '1' or mode == '2' or mode == '3':
            break
        else: 
            print("Wrong input. Try again:")
    os.system(clear_cmd)
    return mode

def fixed_mode(ser_dev):
    I2C_command = I2CCommandFixed()
    I2C_command.get_address()
    while(1):
        I2C_command.get_data()
        I2C_command.prepare_command()
        ser_dev.write(I2C_command.command)

def free_mode(ser_dev):
    I2C_command = I2CCommandFree()
    while(True):
        I2C_command.get_command_raw()
        I2C_command.extract_address_and_data()
        I2C_command.prepare_command()
        ser_dev.write(I2C_command.command)

def scanner(ser_dev):
    ser_dev.flush()
    cmd_code = '73'
    command = binascii.unhexlify(cmd_code)
    ser_dev.write(command)
    reply = ser_dev.read(2)
    reply = reply.hex()
    if len(reply) == 4:
        if "ff" in reply:
            print("Found nothing.")
        else:
            address = "0x" + reply[2:]
            print(f"Found I2C device at address: {address}")
    else: 
        print("Read timeout. Check electric connection.")


ser_dev = serial_init()
mode = mode_selection()
if mode == '1':
    fixed_mode(ser_dev)
elif mode == '2': 
    free_mode(ser_dev)
elif mode == '3':
    scanner(ser_dev)