import mysql.connector
import time
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="automated_aquaponics",
    connect_timeout=60,
    raise_on_warnings=True
)

dB_cursor = db.cursor(buffered=True)

# TEST 1
for i in range(100000):
    dB_cursor.execute("""SELECT id, datetime_added, datetime_executed,
                                    motor, turns, pump,
                                    sol_in, sol_out, done_executing
                                FROM actions WHERE done_executing = 0""")
    action_to_execute = dB_cursor.fetchone()
    print(action_to_execute)
    if (action_to_execute):
        dB_cursor.execute(f"""UPDATE actions SET datetime_executed = '{datetime.now()}', done_executing = 1
                                WHERE id = {action_to_execute[0]};                  
            """)
    db.commit()
    # time.sleep(1)

# TEST 2
# for i in range(1000):
#     dB_cursor.execute("""SELECT id, datetime_added, datetime_executed,
#                                     motor, turns, pump,
#                                     sol_in, sol_out, done_executing
#                                 FROM actions WHERE done_executing = 2""")
#     action_to_execute = dB_cursor.fetchone()
#     print(action_to_execute)

# TEST 3
# for i in range(2):
#     dB_cursor.execute("""SELECT id, datetime_added, datetime_executed,
#                                     motor, turns, pump,
#                                     sol_in, sol_out, done_executing
#                                 FROM actions WHERE done_executing = 0""")
#     action_to_execute = dB_cursor.fetchone()
#     print(action_to_execute)
