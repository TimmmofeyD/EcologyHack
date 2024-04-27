from __future__ import print_function
from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE
import time
import struct


class Sensor:

    def __init__(self, port):
        self.port = port  # Set this to your serial port.
        self.baudrate = 9600

        # Prepare serial connection.
        self.ser = Serial(port, baudrate=self.baudrate, bytesize=EIGHTBITS,
                          parity=PARITY_NONE, stopbits=STOPBITS_ONE)
        self.ser.flushInput()

        self.HEADER_BYTE = b"\xAA"
        self.COMMANDER_BYTE = b"\xC0"
        self.TAIL_BYTE = b"\xAB"

        self.byte, self.previousbyte = b"\x00", b"\x00"

    def get_sensor_data(self):
        self.previousbyte = self.byte
        self.byte = self.ser.read(size=1)
        # print(byte)

        # We got a valid packet header.
        if self.previousbyte == self.HEADER_BYTE and self.byte == self.COMMANDER_BYTE:
            packet = self.ser.read(size=8)  # Read 8 more bytes
            # print(packet)

            # Decode the packet - little endian, 2 shorts for pm2.5 and pm10, 2 ID bytes, checksum.
            readings = struct.unpack('<HHcccc', packet)

            # Measurements.µg/m³
            pm_25 = readings[0]/10.0
            pm_10 = readings[1]/10.0

            # ID
            sensor_id = packet[4:6]
            id_bytes = bytes(sensor_id).hex()
            # print(id)

            # Prepare checksums.
            checksum = readings[4][0]
            calculated_checksum = sum(packet[:6]) & 0xFF
            checksum_verified = (calculated_checksum == checksum)
            # print(checksum_verified)

            # Message tail.
            tail = readings[5]

            if tail == self.TAIL_BYTE and checksum_verified:
                # print("PM 2.5:", pm_25, "μg/m^3  PM 10:", pm_10, "μg/m^3")
                return pm_25, pm_10, id_bytes

    def print_data(self, pm_25="NaN", pm_10="NaN", id_bytes="NaN"):
        print("PM 2.5:", pm_25, "μg/m^3  PM 10:",
              pm_10, "μg/m^3", "ID:", id_bytes)
