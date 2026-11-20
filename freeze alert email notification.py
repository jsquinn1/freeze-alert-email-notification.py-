import requests
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime

# --- CONFIGURATION ---
URL = "https://api.open-meteo.com/v1/forecast?latitude=39.10&longitude=-94.58&current_weather=true&temperature_unit=fahrenheit"
FREEZE_THRESHOLD = 32.0

SENDER_EMAIL = "enter e-mail @gmail.com"
APP_PASSWORD = "enter password"  # 16-character Gmail App Password
RECEIVER_EMAIL = "enter e-mail @gmail.com"

def send_email_alert(temp, timestamp):
    msg = EmailMessage()
    msg["Subject"] = f"Freeze Alert: {temp}°F"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.set_content(f"Warning: The temperature dropped to {temp}°F at {timestamp}.")

    try:
        # Connect securely to Gmail's SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print(" -> Email alert sent!")
    except Exception as e:
        print(f" -> Failed to send email: {e}")

def check_temperature():
    response = requests.get(URL)
    data = response.json()
    current_temp = data["current_weather"]["temperature"]
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Current temp: {current_temp}°F")

    if current_temp <= FREEZE_THRESHOLD:
        warning = f"[{timestamp}] FREEZE ALERT: {current_temp}°F\n"
        with open("freeze_log.txt", "a") as file:
            file.write(warning)
        
        # Trigger the email alert
        send_email_alert(current_temp, timestamp)

print("Starting temperature monitor... (Press Ctrl+C to stop)")
while True:
    check_temperature()
    time.sleep(60)
