from __future__ import print_function
from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE
import time, struct

def init():
    port = input("Enter serial port (a.e. COM5): ") # Set this to your serial port.
    baudrate = 9600

    # Prepare serial connection.
    ser = Serial(port, baudrate=baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE)
    ser.flushInput()

    HEADER_BYTE = b"\xAA"
    COMMANDER_BYTE = b"\xC0"
    TAIL_BYTE = b"\xAB"

    byte, previousbyte = b"\x00", b"\x00"


def get_sensor_data():
    global HEADER_BYTE, COMMANDER_BYTE, TAIL_BYTE, ser
    previousbyte = byte
    byte = ser.read(size=1)
    #print(byte)
    
    # We got a valid packet header.
    if previousbyte == HEADER_BYTE and byte == COMMANDER_BYTE:
        packet = ser.read(size=8) # Read 8 more bytes
        #print(packet)
        
        # Decode the packet - little endian, 2 shorts for pm2.5 and pm10, 2 ID bytes, checksum.
        readings = struct.unpack('<HHcccc', packet)
        
        # Measurements.µg/m³
        pm_25 = readings[0]/10.0
        pm_10 = readings[1]/10.0
        
        # ID
        id = packet[4:6]
        id_bytes=bytes(id).hex()
        #print(id)
        
        # Prepare checksums.
        checksum = readings[4][0]
        calculated_checksum = sum(packet[:6]) & 0xFF
        checksum_verified = (calculated_checksum == checksum)
        #print(checksum_verified)
        
        # Message tail.
        tail = readings[5]
        
        if tail == TAIL_BYTE and checksum_verified:
            #print("PM 2.5:", pm_25, "μg/m^3  PM 10:", pm_10, "μg/m^3")
            return pm_25, pm_10, id_bytes
        
def print(pm_25, pm_10, id_bytes):
    print("PM 2.5:", pm_25, "μg/m^3  PM 10:", pm_10, "μg/m^3", "ID:", id_bytes)