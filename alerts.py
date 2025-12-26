import requests
import smtplib
from email.mime.text import MIMEText
from config import (
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS
)

def handle_alert(imei, speed, limit, lat, lon):
    """Handle overspeed alert by sending notifications"""
    message = f"Overspeed Alert: {imei} {speed}km/h (limit: {limit})"
    send_telegram(message)
    send_email("Overspeed Alert", message, "admin@example.com")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload, timeout=5)

def send_email(subject, body, to_email):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print(f"[Email] Alert sent to {to_email}")
    except Exception as e:
        print(f"[Email] Failed to send alert: {e}")
