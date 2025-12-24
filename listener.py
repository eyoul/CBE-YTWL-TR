import socket
from datetime import datetime
from enforcement import enforce_speed
from config import HOST, TCP_PORT
from db import save_gps, get_speed_limit, log_violation
from alerts import handle_alert

from gt06 import (
    bytes_to_imei,
    parse_location_packet,
    is_gt06_packet,
    packet_type
)

import random

def simulate_vehicles():
    for i in range(2, 1001):  # 2–1000
        imei = f"SIM{i:04d}"
        lat = 9.03 + random.uniform(-0.05, 0.05)
        lon = 38.74 + random.uniform(-0.05, 0.05)
        speed = random.randint(40, 100)
        push_location({"imei": imei, "lat": lat, "lon": lon, "speed": speed, "overspeed": speed>80})


def process_gps_packet(imei, lat, lon, speed, timestamp):
    limit = get_speed_limit(imei)
    
    # Save GPS
    save_gps(imei, lat, lon, speed, timestamp)
    
    # Check overspeed
    if speed > limit:
        log_violation(imei, speed, limit, lat, lon, timestamp)
        status = handle_alert(imei, speed, limit, lat, lon)
        return {"imei": imei, "lat": lat, "lon": lon, "speed": speed, "overspeed": True, "status": status}
    
    return {"imei": imei, "lat": lat, "lon": lon, "speed": speed, "overspeed": False}

def build_ack(proto, serial):
    return b'\x78\x78\x05' + bytes([proto]) + serial + b'\x0D\x0A'

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, TCP_PORT))
    server.listen(100)
    print(f"[GT06] Listening on {TCP_PORT}")

    while True:
        conn, addr = server.accept()
        data = conn.recv(2048)

        if not data or not is_gt06_packet(data):
            conn.close()
            continue

        proto = packet_type(data)
        serial = data[-6:-4]

        # LOGIN PACKET (0x01)
        if proto == 0x01:
            imei = bytes_to_imei(data)
            print(f"[LOGIN] IMEI {imei}")
            conn.send(build_ack(proto, serial))

        # LOCATION PACKET (0x12)
        elif proto == 0x12:
            imei = bytes_to_imei(data)
            lat, lon, speed = parse_location_packet(data)

            save_gps(
                imei=imei,
                lat=lat,
                lon=lon,
                speed=speed,
                timestamp=datetime.utcnow().isoformat()
            )

            print(f"[GPS] {imei} {lat},{lon} {speed}km/h")
            conn.send(build_ack(proto, serial))

        conn.close()

