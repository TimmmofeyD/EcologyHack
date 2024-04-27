from sensor import Sensor


#Select port for serial connection
port = input("Enter serial port (a.e. COM5): ")
#init air dirtiness sensor
sds011 = Sensor(port)
#infinite loop for sensor scan and information print
while True:
    sds011.print(sds011.get_sensor_data())