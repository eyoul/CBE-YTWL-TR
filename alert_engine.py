from alerts import send_telegram, send_email
from db import violation_count
from config import MAX_WARNINGS

def handle_alert(imei, speed, limit, lat, lon):
    count = violation_count(imei)

    msg = (
        f"🚨 OVERSPEED ALERT\n"
        f"IMEI: {imei}\n"
        f"Speed: {speed} km/h\n"
        f"Limit: {limit} km/h\n"
        f"Violations (1h): {count}\n"
        f"Location: {lat},{lon}"
    )

    send_telegram(msg)

    if count >= MAX_WARNINGS:
        send_email(
            subject="🚨 Critical Overspeed Escalation",
            body=msg,
            to_email="fleet.manager@example.com"
        )
        return "ESCALATED"

    return "WARNED"
