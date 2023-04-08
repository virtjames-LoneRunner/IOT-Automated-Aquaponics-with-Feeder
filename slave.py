import sqlite3
import serial
import time
from datetime import datetime
import random

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
command_input = ''
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
            command_input = input("COMMAND:  ")
            input_command = command_input.split(',')

            command_input = []
            for com in input_command:
                command_input.append(int(com))

            if command_string:
                command_input = ''
                print("LENGTH: ", len(command_string))
                if len(command_string):
                    print("COMMAND: ", command_string)
                    command_string = int(command_string)

                    if command_string == 1:
                        input_arduino.write(bytearray([1]))
                        input_arduino.write(bytearray([0, 1]))

            elif command_input:
                # time.sleep(3)
                input_arduino.write(2)
                command = command_input

                input_arduino.write(
                    bytearray(command))
                print("SENT DATA: ", command)

            # change command_string back to a string
            command_string = ''
            command_input = ''

        except Exception as error:
            print(error)

except KeyboardInterrupt:
    print("ERROR OCCURED")

except Exception as e:
    print(e)

input_arduino.close()

# except Exception as e:
#     print(e)
