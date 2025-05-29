import requests
import random
import time

SERVER_URL = "http://127.0.0.1:5050/sensor"  # אותו שרת כמו קודם

def generate_motion():
    return random.choice([True, False])

def send_motion():
    motion = generate_motion()
    payload = {
        "sensor": "motion",
        "value": motion
    }

    try:
        response = requests.post(SERVER_URL, json=payload)
        print(f"[+] Sent motion: {motion} | Server Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to send motion: {e}")

if __name__ == "__main__":
    while True:
        send_motion()
        time.sleep(10)
