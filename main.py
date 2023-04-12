# import sqlite3
import mysql.connector
import serial
import time
from datetime import datetime
from datetime import timedelta
import traceback

from checks import check_if_pump_needs_on, check_if_sols_needs_on
from log import log

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="automated_aquaponics"
)
dB_cursor = db.cursor(buffered=True)


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
                        dB_cursor.execute(
                            "SELECT * FROM settings;")
                        settings_data = dB_cursor.fetchone()
                        now = datetime.now()
                        input_arduino.write(bytearray([1]))
                        input_arduino.write(bytearray([now.minute, now.hour]))

                        if settings_data:
                            # input_arduino.write(bytearray([2]))
                            settings_data = list(settings_data)
                            for i in range(0, len(settings_data)):
                                settings_data[i] = int(settings_data[i])

                            # start at index 1 to skip ID
                            input_arduino.write(bytearray([settings_data[1], settings_data[2],
                                                           settings_data[3], settings_data[4], settings_data[5],
                                                           settings_data[6], settings_data[7]]))

                elif 30 > len(command_string) > 10:
                    data = command_string.decode()
                    # print("SETTINGS: ", data)
                    data = data.split(',')
                    new_settings = []
                    for i in data:
                        try:
                            new_settings.append(int(i))
                        except:
                            continue
                    log(f"SETTINGS: {new_settings}")

                    dB_cursor.execute(
                        "SELECT * FROM settings;")
                    settings_data = dB_cursor.fetchone()

                    log(f"SETTINGS DATA: {settings_data}")
                    if not settings_data:
                        dB_cursor.execute(
                            f"""INSERT INTO settings(default_feed_amount, min_temperature, max_temperature,
                                                    min_water_level, max_water_level, pH_level, DO_level) 
                                                    VALUES ({new_settings[0]}, {new_settings[1]}, {new_settings[2]}, 
                                                            {new_settings[3]}, {new_settings[4]}, {new_settings[5]}, 
                                                            {new_settings[6]})""")
                    else:
                        dB_cursor.execute(
                            f"""UPDATE settings SET default_feed_amount = {new_settings[0]}, min_temperature = {new_settings[1]}, max_temperature = {new_settings[2]}, 
                                                    min_water_level = {new_settings[3]}, max_water_level = {new_settings[4]}, pH_level = {new_settings[5]}, 
                                                    DO_level = {new_settings[6]}
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
                    log(f"NEW DATA: {new_data}")

                    # CHECK if action needs to be taken
                    dB_cursor.execute(
                        "SELECT * FROM settings;")
                    settings_data = dB_cursor.fetchone()
                    if settings_data:
                        # input_arduino.write(bytearray([2]))
                        settings_data = list(settings_data)
                        for i in range(0, len(settings_data)):
                            settings_data[i] = int(settings_data[i])

                    # temperature, pH_level, water_level, humidity, dissolved_oxygen
                    dB_cursor.execute(f"""INSERT INTO data_rows(date_time, temperature, pH_level, water_level, humidity, dissolved_oxygen) 
                                                               VALUES ("{(datetime.now())}", 
                                                                        {new_data[0]}, {new_data[3]}, 
                                                                        {new_data[2]}, {new_data[4]}, 
                                                                        {new_data[1]})""")

                    # settings(default_feed_amount, min_temperature, max_temperature,
                    #          min_water_level, max_water_level, pH_level, DO_level)

                    # actions table
                    # datetime_added DATETIME,
                    # datetime_executed DATETIME,

                    # motor INT default 0,
                    # turns FLOAT,
                    # pump INT,
                    # sol_in INT,
                    # sol_out INT,

                    # done_executing BOOLEAN
                    # Default States
                    current_dateTime = datetime.now()
                    actions = {"datetime_added": current_dateTime, "datetime_executed": None,
                               "motor": 0, "turns": 0, "pump": 0, "sol_in": 0, "sol_out": 0}

                    dB_cursor.execute(
                        "SELECT * FROM actions WHERE datetime_executed is null")
                    unfinished_actions = dB_cursor.fetchall()

                    # log(f"SETTINGS: {settings_data}")
                    if settings_data and len(unfinished_actions) < 3:
                        # Feeding action
                        dB_cursor.execute(
                            "SELECT id, time_scheduled, turns, done_for_the_day FROM feeding_schedules where done_for_the_day = 0")

                        feeding_schedule = dB_cursor.fetchone()
                        if feeding_schedule:
                            time = str(feeding_schedule[1]).split(':')
                            current_dateTime = datetime.now()
                        # ONLY ADD SCHEDULE FOR THE CURRENT HOUR OF THE DAY
                            if int(time[0]) != current_dateTime.hour:
                                feeding_schedule = None

                        if feeding_schedule:
                            actions['turns'] = feeding_schedule[2]

                            # UPDATE ROW IN TABLE
                            dB_cursor.execute(
                                f"UPDATE feeding_schedules SET done_for_the_day = 1 WHERE id = {feeding_schedule[0]};")

                        action_cause = ''
                        pump_on, action_cause = check_if_pump_needs_on(
                            settings_data, new_data, action_cause)

                        actions['pump'] = pump_on

                        sol_in, sol_out, action_cause = check_if_sols_needs_on(
                            settings_data, new_data, action_cause)
                        actions['sol_in'] = sol_in
                        actions['sol_out'] = sol_out

                        # add pump on schedule here as well as corresponding table
                        dB_cursor.execute(f"""
                            INSERT INTO actions(datetime_added, motor, turns, pump, sol_in, sol_out, done_executing, remarks, cause)
                                        VALUES ('{actions['datetime_added']}', {actions['motor']}, {actions['turns']},
                                                {actions['pump']}, {actions['sol_in']}, {actions['sol_out']}, {0}, 'settings: {settings_data} data: {new_data}', '{action_cause}')
                        """)

                    db.commit()
                    previous_time_for_data = datetime.now().second

            # change command_string back to a string
            command_string = ''
        # except InternalError:
        #     dB_cursor.fetchall()

        except Exception as error:
            log(traceback.print_exc())

        command_string = ''

except KeyboardInterrupt:
    log("ERROR OCCURED")

except Exception as e:
    log(e)

input_arduino.close()
