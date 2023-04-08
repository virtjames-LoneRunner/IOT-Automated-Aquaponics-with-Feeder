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
try:
    while True:
        # print("LISTENING")
        # if output_data != previous_output_data:
        #     print(True)
        #     previous_output_data = output_data
        # output_arduino.write(bytearray(output_data))
        while input_arduino.in_waiting:
            command_string = input_arduino.readline()
            print("COMMAND: ", command_string)
        try:
            if command_string:
                log(f"LENGTH: {len(command_string)}")
                log(f"COMMAND: {command_string}")
                # input_arduino.write(bytearray([int(input_command)]))
                #     input_arduino.write(
                #         bytearray([1, 1, 0, 0, 0]))
                #     print("WRITTEN")
                # if len(command_string) == 3:
                #     input_arduino.write(bytearray([2]))
                #     input_arduino.write(bytearray([1, 2, 1, 0, 0]))
                #     print("WRITTEN")

            # input_command = input("COMMAND: ")
            # command_list = input_command.split(',')
            # commands = []
            # for command_ in command_list:
            #     commands.append(int(command_))

            # input_command = input("COMMAND_prompt: ")
            input_command = 1
            commands = []
            if input_command:
                input_arduino.write(bytearray([2]))
                input_arduino.write(
                    bytearray(commands))
                # input_arduino.write(bytearray([0, 0, 1, 1, 0]))

            # input_arduino.write(bytearray([1]))

        except Exception as error:
            log(error)

        # change command_string back to a string
        command_string = ''


except KeyboardInterrupt:
    log("ERROR OCCURED")

except Exception as e:
    log(e)

input_arduino.close()
