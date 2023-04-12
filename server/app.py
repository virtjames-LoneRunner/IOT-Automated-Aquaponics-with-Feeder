from flask import Flask, request
import mysql.connector
# import sqlite3
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# db = sqlite3.connect('../database/main.db', check_same_thread=False)

db = mysql.connector.connect(
    host="localhost",
    user="thesis",
    password="",
    database="automated_aquaponics",
    connect_timeout=60
)
dB_cursor = db.cursor()


@app.route("/dashboard")
@cross_origin()
def dashboard():
    dB_cursor.execute(
        "SELECT * FROM data_rows ORDER BY id DESC LIMIT 0, 1")
    data = dB_cursor.fetchone()

    data_json = {
        "id": data[0], "date_time": data[1],
        "temperature": data[2], "pH_level": data[3],
        "water_level": data[4], "humidity": data[5],
        "dissolved_oxygen": data[6]
    }
    db.commit()
    return {"message": "", "data": data_json}


@app.route("/settings", methods=["GET", "POST"])
@cross_origin()
def settings():
    if request.method == "POST":
        # save settings
        # print(request.json)
        try:
            req = request.json
            dB_cursor.execute(f"""UPDATE settings SET
                                    default_feed_amount = {req['default_feed_amount']}, min_temperature = {req['min_temperature']}, max_temperature = {req['max_temperature']},
                                    min_water_level = {req['min_water_level']}, max_water_level = {req['max_water_level']}, pH_level = {req['pH_level']},
                                    DO_level = {req['DO_level']}
                                WHERE id = {req['id']}""")
            db.commit()
            return {"message": "Success"}

        except Exception as e:
            print(e)
            return {"message": f'An error occured: {e}'}

    else:
        dB_cursor.execute(
            "SELECT * FROM settings WHERE id = 1")
        settings_data = dB_cursor.fetchone()
        settings_json = {
            "id": settings_data[0], "default_feed_amount": settings_data[1],
            "min_temperature": settings_data[2], "max_temperature": settings_data[3],
            "min_water_level": settings_data[4], "max_water_level": settings_data[5],
            "pH_level": settings_data[6], "DO_level": settings_data[7]
        }

        return {"settings_data": settings_json}


@app.route('/feeding-schedules', methods=['GET', 'POST', 'DELETE'])
@cross_origin()
def feeding_schedules():
    if request.method == 'POST':
        req = request.json
        dB_cursor.execute(
            "SELECT default_feed_amount FROM settings WHERE id = 1")
        settings_data = dB_cursor.fetchone()
        turns = float(req['feed_amount']) / settings_data[0]

        dB_cursor.execute(f"""INSERT INTO feeding_schedules(time_scheduled, feed_amount, turns, done_for_the_day)
                             VALUES ('{req["time_scheduled"]}', {
                                     req["feed_amount"]}, {turns}, {0})
                         """)
        db.commit()
        return {"settings_data": settings_data}

    elif request.method == "DELETE":
        sched_id = int(request.args.get('id'))

        dB_cursor.execute(
            f"DELETE from feeding_schedules WHERE id = {sched_id}")
        db.commit()

        return {"message": "DELETED"}

    else:
        try:
            dB_cursor.execute(
                "SELECT * FROM feeding_schedules ORDER BY time_scheduled DESC")
        except mysql.connector.errors.OperationalError as e:
            print("Lost connection to MySQL server during query. Retrying...")
            db.reconnect(attempts=3, delay=5)
        scheds = dB_cursor.fetchall()
        # sorted_scheds = []
        print(scheds)
        scheds_json = []
        if scheds:
            for sched in scheds:
                scheds_json.append({
                    "id": sched[0], "time_scheduled": str(sched[1]),
                    "feed_amount": sched[2], "turns": sched[3],
                    "done_for_the_day": sched[4]
                })
            # sorted_scheds = sorted(
            #     scheds_json, key=lambda d: d['time_scheduled'])
        else:
            scheds_json = []
        db.commit()
        return {"schedules": scheds_json}


@ app.route('/user-details', methods=['GET', 'POST'])
@ cross_origin()
def user_details():
    if request.method == 'POST':
        req = request.json
        dB_cursor.execute(
            f"""UPDATE user_details SET mobile_number = {req["mobile_number"]} WHERE id = {request.args["id"]}""")
        db.commit()
        return {"message": "updated"}

    else:
        dB_cursor.execute(
            "SELECT * FROM user_details")
        user_details_data = dB_cursor.fetchone()
        user_json = {
            "id": user_details_data[0],
            "mobile_number": user_details_data[1]
        }
        return {"user_details": user_json}


@ app.route('/actions', methods=['GET', 'POST'])
@ cross_origin()
def actions():
    if request.method == 'POST':
        pass
    else:

        try:
            dB_cursor.execute(
                "SELECT * FROM actions ORDER BY id DESC limit 50")
        except mysql.connector.errors.OperationalError as e:
            print("Lost connection to MySQL server during query. Retrying...")
            db.reconnect(attempts=3, delay=5)

        actions_data = dB_cursor.fetchall()
        actions_json = []

        for action in actions_data:
            try:
                actions_json.append({
                    "id": action[0], "datetime_added": action[1], "datetime_executed": action[2],
                    "motor": action[3], "turns": action[4], "pump": action[5], "sol_in": action[6], "sol_out": action[7],
                    "done_executing": action[8], "remarks": action[9], "cause": action[10]
                })
            except:
                continue

        return {"actions": actions_json}

# {
#     "id": sched[0], "datetime_added": sched[1], "datetime_executed": sched[2],
#     "motor": sched[3], "turns": sched[4], "pump": sched[5], "sol_in": sched[6], "sol_out": sched[7],
#     "done_executing": sched[8], "remarks": sched[9], "cause": sched[10]
# }
