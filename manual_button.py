import requests

SERVER_URL = "http://127.0.0.1:5050/manual"

def send_manual_command(state):
    payload = {
        "sensor": "manual_button",
        "value": state  # True = turn ON, False = turn OFF
    }

    try:
        response = requests.post(SERVER_URL, json=payload)
        print(f"[+] Sent manual command: {'ON' if state else 'OFF'} | Server Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Failed to send manual command: {e}")

if __name__ == "__main__":
    while True:
        user_input = input("Enter 'on' to turn ON the AC or 'off' to turn OFF (or 'q' to quit): ").strip().lower()
        if user_input == 'on':
            send_manual_command(True)
        elif user_input == 'off':
            send_manual_command(False)
        elif user_input == 'q':
            break
        else:
            print("[!] Invalid input.")
