import tkinter as tk
import requests
import threading
import time

SERVER_URL = "http://127.0.0.1:5050"

class SmartACGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart AC Control Panel")

        # רכיבי GUI
        self.temp_label = tk.Label(root, text="Temperature: -- °C", font=("Arial", 16))
        self.temp_label.pack(pady=5)

        self.motion_label = tk.Label(root, text="Motion: --", font=("Arial", 14))
        self.motion_label.pack(pady=5)

        self.ac_label = tk.Label(root, text="AC Status: --", font=("Arial", 14))
        self.ac_label.pack(pady=5)

        self.mode_label = tk.Label(root, text="Mode: --", font=("Arial", 12))
        self.mode_label.pack(pady=5)

        self.warning_label = tk.Label(root, text="", fg="red", font=("Arial", 12))
        self.warning_label.pack(pady=10)

        # כפתורים
        self.manual_on_btn = tk.Button(root, text="Turn ON", command=lambda: self.send_manual(True), state="disabled")
        self.manual_off_btn = tk.Button(root, text="Turn OFF", command=lambda: self.send_manual(False), state="disabled")
        self.toggle_mode_btn = tk.Button(root, text="Toggle Mode", command=self.toggle_mode)
        self.manual_on_btn.pack()
        self.manual_off_btn.pack()
        self.toggle_mode_btn.pack(pady=10)

        # עדכון GUI ברקע
        self.update_loop()

    def send_manual(self, state):
        try:
            response = requests.post(f"{SERVER_URL}/manual", json={"value": state})
            print(f"Manual command sent: {'ON' if state else 'OFF'}")
        except Exception as e:
            print(f"Error sending manual command: {e}")

    def toggle_mode(self):
        # שיטה פשוטה: נשלח פקודה הפוכה למצב הקיים דרך כפתור ידני
        # (לא מושלם – עדיף endpoint ייעודי, אבל נסתפק בזה כרגע)
        try:
            current = requests.get(f"{SERVER_URL}/ac_status").json()
            if current["mode"] == "auto":
                self.send_manual(current["ac_on"])  # הפעל ידני
            else:
                # הפעל מצב אוטומטי על ידי שינוי ישיר (עוקף קצת)
                requests.post(f"{SERVER_URL}/manual", json={"value": current["ac_on"]})
                print("Switched to manual mode")
        except:
            pass

    def update_loop(self):
        def loop():
            while True:
                try:
                    # עדכון סטטוס
                    status = requests.get(f"{SERVER_URL}/ac_status").json()
                    mode = status["mode"]
                    ac = "ON" if status["ac_on"] else "OFF"
                    self.ac_label.config(text=f"AC Status: {ac}")
                    self.mode_label.config(text=f"Mode: {mode.upper()}")

                    # שליטה על כפתורים
                    if mode == "manual":
                        self.manual_on_btn.config(state="normal")
                        self.manual_off_btn.config(state="normal")
                    else:
                        self.manual_on_btn.config(state="disabled")
                        self.manual_off_btn.config(state="disabled")

                    # נתוני טמפ’ ותנועה (נשלוף מהדאטה)
                    latest_temp = self.get_latest_value("temperature")
                    latest_motion = self.get_latest_value("motion")

                    if latest_temp:
                        temp_val = float(latest_temp)
                        self.temp_label.config(text=f"Temperature: {temp_val:.1f} °C")
                        if temp_val > 30:
                            self.warning_label.config(text="⚠️ WARNING: High temperature!")
                        else:
                            self.warning_label.config(text="")

                    if latest_motion:
                        motion_str = "Yes" if latest_motion == "True" else "No"
                        self.motion_label.config(text=f"Motion: {motion_str}")

                except Exception as e:
                    print(f"[GUI] Error: {e}")

                time.sleep(2)

        threading.Thread(target=loop, daemon=True).start()

    def get_latest_value(self, sensor_type):
        try:
            import sqlite3
            conn = sqlite3.connect("ac_data.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT value FROM sensor_data
                WHERE sensor = ?
                ORDER BY timestamp DESC LIMIT 1
            """, (sensor_type,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else None
        except:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartACGUI(root)
    root.mainloop()
