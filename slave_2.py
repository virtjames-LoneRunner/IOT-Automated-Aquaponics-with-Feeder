import sqlite3
import serial
import time
from datetime import datetime
from datetime import timedelta
from log import log

db = sqlite3.connect('database/main.db')
dB_cursor = db.cursor()


input_arduino = serial.Serial('COM3', 9600)
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
# try:
while True:
    while input_arduino.in_waiting:
        command_string = input_arduino.readline()
        # print("COMMAND: ", command_string)
    # try:
    # if command_string:
        # log(f"LENGTH: {len(command_string)}")
        # log(f"COMMAND: {command_string}")

    # input_command = input("COMMAND: ")
    # command_list = input_command.split(',')
    # commands = []
    # for command_ in command_list:
    #     commands.append(int(command_))

    # input_command = input("COMMAND_prompt: ")
    # input_command = 1
    # commands = [0, 0, 1, 1, 0]

    action_to_execute = dB_cursor.execute("""SELECT id, datetime_added, datetime_executed, 
                                                motor, turns, pump, 
                                                sol_in, sol_out, done_executing 
                                        FROM actions WHERE done_executing = 0""").fetchone()

    # {motor, turns, pump, sol_in, sol_out}
    if action_to_execute:
        log(f"EXECUTING: {action_to_execute}")
        executed_at = datetime.now()
        input_arduino.write(bytearray([2]))
        input_arduino.write(
            bytearray([action_to_execute[3], int(action_to_execute[4]), action_to_execute[5],
                       action_to_execute[6], action_to_execute[7]]))
        # input_arduino.write(bytearray([0, 0, 1, 1, 0]))

        # update action record
        # print(f"""UPDATE actions SET datetime_executed = '{executed_at}', done_executing = 1
        #                         WHERE id = {action_to_execute[0]};
        #     """)
        dB_cursor.execute(f"""UPDATE actions SET datetime_executed = '{executed_at}', done_executing = 1
                                WHERE id = {action_to_execute[0]};                  
            """)

        db.commit()
    # input_arduino.write(bytearray([1]))

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
