import sqlite3

DB_NAME = "ac_data.db"

def view_all_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    
    print(f"\n{'ID':<5} {'Timestamp':<25} {'Sensor':<15} {'Value':<10}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<25} {row[2]:<15} {row[3]:<10}")
    
    conn.close()

if __name__ == "__main__":
    view_all_data()
