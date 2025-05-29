import requests
import time

STATUS_URL = "http://127.0.0.1:5050/ac_status"

last_state = None

def check_relay_status():
    global last_state
    try:
        response = requests.get(STATUS_URL)
        status = response.json().get("ac_on")
        if status != last_state:
            print(f"[RELAY] AC turned {'ON' if status else 'OFF'}")
            last_state = status
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to get AC status: {e}")

if __name__ == "__main__":
    while True:
        check_relay_status()
        time.sleep(5)
