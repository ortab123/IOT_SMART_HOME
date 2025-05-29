import requests
import random
import time

SERVER_URL = "http://127.0.0.1:5050/sensor"  # שים לב - פורט 5050 תואם לשרת

def generate_temperature():
    return round(random.uniform(20.0, 30.0), 1)

def send_temperature():
    temperature = generate_temperature()
    payload = {
        "sensor": "temperature",
        "value": temperature
    }

    try:
        response = requests.post(SERVER_URL, json=payload)
        print(f"[+] Sent temperature: {temperature}°C | Server Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to send data: {e}")

if __name__ == "__main__":
    while True:
        send_temperature()
        time.sleep(10)
