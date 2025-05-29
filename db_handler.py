import sqlite3
from datetime import datetime

DB_NAME = "ac_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sensor TEXT,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_sensor_data(sensor, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sensor_data (timestamp, sensor, value)
        VALUES (?, ?, ?)
    """, (datetime.now().isoformat(), sensor, str(value)))
    conn.commit()
    conn.close()
