import serial
import time

def initialise_uart(uart):
    port = serial.Serial(
        port=uart,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        # timeout=0.5, # IMPORTANT, can be lower or higher
        # inter_byte_timeout=0.1 # Alternative
    )
    return port


def read_uart(port):
    t = time.time()
    read_buffer = b''
    t_wait = 0.5

    job = True
    while job:
        if time.time() < t + t_wait:
            if port.inWaiting():
                c = port.read()  # attempt to read a character from Serial
                if c == b'\r':
                    #read_buffer += c
                    pass

                elif c == b'\n':
                    #read_buffer += c  # add the newline to the buffer
                    job = False

                else:
                    read_buffer += c  # add to the buffer

        else:
            read_buffer = ""
            job = False

    return read_buffer