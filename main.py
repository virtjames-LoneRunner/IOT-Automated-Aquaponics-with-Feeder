import sqlite3
import serial
import time
from datetime import datetime
from datetime import timedelta
from log import log

db = sqlite3.connect('database/main.db')
dB_cursor = db.cursor()


input_arduino = serial.Serial('COM4', 9600)
# output_arduino = serial.Serial('COM11', 9600)

input_data = []
output_data = [0, 12, 13, 14, 15, 16, 17, 18]
previous_output_data = []

# settings_data = []
new_settings = []
read_settings = False
command_string = ''

previous_time_for_data = datetime.now()
try:
    while True:
        # print("LISTENING")
        # if output_data != previous_output_data:
        #     print(True)
        #     previous_output_data = output_data
        # output_arduino.write(bytearray(output_data))
        while input_arduino.in_waiting:
            command_string = input_arduino.readline()
            # print("COMMAND: ", command_string)
        try:
            if command_string:
                log(f"LENGTH: {len(command_string)}")
                if len(command_string) == 3:
                    command_string = int(command_string)
                    if command_string == 1:
                        settings_data = dB_cursor.execute(
                            "SELECT * FROM settings;").fetchone()

                        now = datetime.now()
                        input_arduino.write(bytearray([1]))
                        input_arduino.write(bytearray([now.minute, now.hour]))

                        if settings_data:
                            # input_arduino.write(bytearray([2]))
                            settings_data = list(settings_data)
                            for i in range(0, len(settings_data)):
                                settings_data[i] = int(settings_data[i])

                            input_arduino.write(bytearray([settings_data[0], settings_data[1], settings_data[2],
                                                           settings_data[3], settings_data[4], settings_data[5],
                                                           settings_data[6]]))

                elif len(command_string) == 16:
                    data = command_string.decode()
                    # print("SETTINGS: ", data.split(','))
                    new_settings = []
                    for i in data:
                        try:
                            new_settings.append(int(i))
                        except:
                            continue
                    log(f"SETTINGS: {new_settings}")

                    settings_data = dB_cursor.execute(
                        "SELECT * FROM settings;").fetchone()

                    log(settings_data)
                    if not settings_data:
                        dB_cursor.execute(
                            f"""INSERT INTO settings(default_feed_amount, min_temperature, max_temperature,
                                                    min_water_level, max_water_level, min_pH_level, max_pH_level) 
                                                    VALUES ({new_settings[0]}, {new_settings[1]}, {new_settings[2]}, 
                                                            {new_settings[3]}, {new_settings[4]}, {new_settings[5]}, 
                                                            {new_settings[6]})""")
                    else:
                        dB_cursor.execute(
                            f"""UPDATE settings SET default_feed_amount = {new_settings[0]}, min_temperature = {new_settings[1]}, max_temperature = {new_settings[2]}, 
                                                    min_water_level = {new_settings[3]}, max_water_level = {new_settings[4]}, min_ph_level = {new_settings[5]}, 
                                                    max_pH_level = {new_settings[6]}
                                where id = 1;""")
                    db.commit()

                elif len(command_string) > 30:
                    sec = datetime.now().second
                    if previous_time_for_data == sec or previous_time_for_data == sec+1:
                        continue
                    data = command_string.decode()
                    data = data.split(",")
                    new_data = []
                    # data = data.split(",")
                    for i in data:
                        try:
                            new_data.append(float(i))
                        except:
                            continue
                    log(new_data)
                    # temperature, pH_level, water_level, humidity, dissolved_oxygen
                    dB_cursor.execute(f"""INSERT INTO data_rows(date_time, temperature, pH_level, water_level, humidity, dissolved_oxygen) 
                                                               VALUES ("{(datetime.now())}", 
                                                                        {new_data[0]}, {new_data[3]}, 
                                                                        {new_data[2]}, {new_data[4]}, 
                                                                        {new_data[1]})""")

                    db.commit()
                    previous_time_for_data = datetime.now().second

            # change command_string back to a string
            command_string = ''

        except Exception as error:
            log(error)


except KeyboardInterrupt:
    log("ERROR OCCURED")

except Exception as e:
    log(e)

input_arduino.close()
