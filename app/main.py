import sensor

sensor.init()
while True:
    sensor.print(sensor.get_sensor_data())