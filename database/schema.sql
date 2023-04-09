CREATE TABLE IF NOT EXISTS data_rows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time DATETIME,
    temperature FLOAT,
    pH_level FLOAT,
    water_level FLOAT,
    humidity FLOAT,
    dissolved_oxygen FLOAT
);


CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    default_feed_amount FLOAT,
    min_temperature FLOAT,
    max_temperature FLOAT,
    min_water_level FLOAT,
    max_water_level FLOAT,
    pH_level FLOAT,
    DO_level FLOAT
);

CREATE TABLE IF NOT EXISTS user_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mobile_number VARCHAR(20)
);


CREATE TABLE IF NOT EXISTS feeding_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_scheduled TIME,
    feed_amount FLOAT,
    turns FLOAT,
    done_for_the_day BOOLEAN
);


CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime_added DATETIME,
    datetime_executed DATETIME NULL,

    motor INT default 0,
    turns FLOAT,
    pump INT,
    sol_in INT,
    sol_out INT,

    done_executing BOOLEAN,
    remarks VARCHAR(255) NULL,
    cause VARCHAR(255) NULL
);