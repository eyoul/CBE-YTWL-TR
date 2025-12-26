# listener.py
import socket
from datetime import datetime
from config import HOST, TCP_PORT
from db import save_gps, get_speed_limit, log_violation
from alerts import handle_alert
from gt06 import bytes_to_imei, parse_location_packet, is_gt06_packet, packet_type
import random

# We'll store socketio here dynamically
_socketio = None

def init_socketio(socketio):
    global _socketio
    _socketio = socketio

def push_location(data):
    if _socketio:
        print(f"[WebSocket] Emitting GPS update: {data}")
        _socketio.emit("gps_update", data)
    else:
        print(f"[WebSocket] SocketIO not initialized, cannot emit: {data}")

def process_gps_packet(imei, lat, lon, speed, timestamp):
    limit = get_speed_limit(imei)
    save_gps(imei, lat, lon, speed, timestamp)
    overspeed = speed > limit
    status = None
    if overspeed:
        log_violation(imei, speed, limit, lat, lon, timestamp)
        status = handle_alert(imei, speed, limit, lat, lon)
    data = {"imei": imei, "lat": lat, "lon": lon, "speed": speed, "overspeed": overspeed, "status": status}
    push_location(data)
    return data

def build_ack(proto, serial):
    return b'\x78\x78\x05' + bytes([proto]) + serial + b'\x0D\x0A'

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, TCP_PORT))
        server.listen(100)
        print(f"[GT06] Server listening on {HOST}:{TCP_PORT}")
    except Exception as e:
        print(f"[GT06] Failed to bind to {HOST}:{TCP_PORT} - {e}")
        return
    
    while True:
        try:
            conn, addr = server.accept()
            print(f"[GT06] Connection from {addr}")
            data = conn.recv(2048)
            
            if not data:
                print("[GT06] No data received")
                conn.close()
                continue
                
            print(f"[GT06] Received data: {data.hex()}")
            
            if not is_gt06_packet(data):
                print(f"[GT06] Invalid GT06 packet format: {data.hex()}")
                conn.close()
                continue

            proto = packet_type(data)
            serial = data[-6:-4]
            print(f"[GT06] Protocol: 0x{proto:02X}, Serial: {serial.hex()}")

            # LOGIN
            if proto == 0x01:
                imei = bytes_to_imei(data)
                print(f"[GT06] LOGIN - IMEI: {imei}")
                ack = build_ack(proto, serial)
                conn.send(ack)
                print(f"[GT06] Sent login ACK: {ack.hex()}")

            # LOCATION
            elif proto == 0x12:
                imei = bytes_to_imei(data)
                lat, lon, speed = parse_location_packet(data)
                timestamp = datetime.utcnow().isoformat()
                print(f"[GT06] GPS - IMEI: {imei}, Lat: {lat}, Lon: {lon}, Speed: {speed} km/h")
                process_gps_packet(imei, lat, lon, speed, timestamp)
                ack = build_ack(proto, serial)
                conn.send(ack)
                print(f"[GT06] Sent location ACK: {ack.hex()}")
            else:
                print(f"[GT06] Unsupported protocol: 0x{proto:02X}")

            conn.close()
            
        except Exception as e:
            print(f"[GT06] Error processing connection: {e}")
            try:
                conn.close()
            except:
                pass
