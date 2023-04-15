# import sqlite3
import mysql.connector
import serial
import time
from datetime import datetime
from datetime import timedelta
from log import log

# allow time to initialize
time.sleep(5)
db = mysql.connector.connect(
    host="localhost",
    user="thesis",
    password="",
    database="automated_aquaponics",
    connect_timeout=60,
    raise_on_warnings=True,
)

dB_cursor = db.cursor(buffered=True)



f = open('/home/raspberry/thesis/slave_log.txt', 'a')

f.write("STARTED")
try:
#    input_arduino = serial.Serial('/dev/ttyACM0', 9600)
    input_arduino = serial.Serial('/dev/ttyACM1', 9600)
except Exception as e:
    f.write(e)

f.write("ARDUINO LOADED")


# output_arduino = serial.Serial('COM11', 9600)

input_data = []
output_data = [0, 12, 13, 14, 15, 16, 17, 18]
previous_output_data = []

# settings_data = []
new_settings = []
read_settings = False
command_string = ''

previous_time_for_data = datetime.now()

new_commands = False
count = 0
# try:
log("INITIALIZING")
time.sleep(4)
while True:
    while input_arduino.in_waiting:
        command_string = input_arduino.readline()
    dB_cursor.execute("""SELECT id, datetime_added, datetime_executed,
                                motor, turns, pump,
                                sol_in, sol_out, done_executing
                            FROM actions WHERE done_executing = 0""")
    action_to_execute = dB_cursor.fetchone()

    # {motor, turns, pump, sol_in, sol_out}
    if action_to_execute:
        log(f"EXECUTING: {action_to_execute}")
        executed_at = datetime.now()
        input_arduino.write(bytearray([2]))
        input_arduino.write(
            bytearray([action_to_execute[3], int(action_to_execute[4]), action_to_execute[5],
                       action_to_execute[6], action_to_execute[7]]))
        dB_cursor.execute(f"""UPDATE actions SET datetime_executed = '{executed_at}', done_executing = 1
                                WHERE id = {action_to_execute[0]};                  
            """)

    db.commit()
    # time.sleep(0.25)

    # except Exception as error:
    #     log(error)

    # change command_string back to a string
    command_string = ''


# except KeyboardInterrupt:
#     log("ERROR OCCURED")

# except Exception as e:
#     log(e)

input_arduino.close()

# except Exception as e:
#     print(e)
