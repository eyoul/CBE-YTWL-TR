
import socket, time, struct, random

HOST = "127.0.0.1"  # Replace with your EC2 public IP
PORT = 9000

imei = "355442200991235"
lat, lon = 9.03, 38.74
speed = 50

def build_gt06_login_packet(imei):
    """Build GT06 login packet (protocol 0x01)"""
    packet = b'\x78\x78'  # Start bits
    packet += b'\x0D'    # Length (13 bytes)
    packet += b'\x01'    # Protocol ID (login)
    
    # IMEI (8 bytes) - convert string to BCD format properly
    imei_bcd = b''
    for i in range(0, len(imei), 2):
        pair = imei[i:i+2]
        if len(pair) == 2:
            high = int(pair[0])
            low = int(pair[1])
            imei_bcd += bytes([(high << 4) | low])
        else:  # odd length, pad with F
            high = int(pair[0])
            imei_bcd += bytes([(high << 4) | 0xF])
    packet += imei_bcd
    
    # Serial number (2 bytes)
    packet += struct.pack('>H', random.randint(1, 65535))
    
    # CRC (2 bytes) - simplified
    packet += b'\x00\x00'
    
    # End bits
    packet += b'\x0D\x0A'
    
    return packet

def build_gt06_location_packet(imei, lat, lon, speed):
    """Build GT06 location packet (protocol 0x12)"""
    packet = b'\x78\x78'  # Start bits
    packet += b'\x25'    # Length (37 bytes)
    packet += b'\x12'    # Protocol ID (location)
    
    # IMEI (8 bytes) - convert string to BCD format properly
    imei_bcd = b''
    for i in range(0, len(imei), 2):
        pair = imei[i:i+2]
        if len(pair) == 2:
            high = int(pair[0])
            low = int(pair[1])
            imei_bcd += bytes([(high << 4) | low])
        else:  # odd length, pad with F
            high = int(pair[0])
            imei_bcd += bytes([(high << 4) | 0xF])
    packet += imei_bcd
    
    # Timestamp (4 bytes) - simplified
    packet += struct.pack('>I', int(time.time()))
    
    # Latitude (4 bytes) - convert to GT06 format (multiply by 1000000)
    lat_raw = int(lat * 1000000.0)
    packet += struct.pack('>I', lat_raw)
    
    # Longitude (4 bytes)
    lon_raw = int(lon * 1000000.0)
    packet += struct.pack('>I', lon_raw)
    
    # Speed (1 byte)
    packet += bytes([speed])
    
    # Fill remaining bytes with zeros
    packet += b'\x00' * 18
    
    # Serial number (2 bytes)
    packet += struct.pack('>H', random.randint(1, 65535))
    
    # CRC (2 bytes) - simplified
    packet += b'\x00\x00'
    
    # End bits
    packet += b'\x0D\x0A'
    
    return packet

# First send login packet
print("Sending login packet...")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    login_packet = build_gt06_login_packet(imei)
    s.sendall(login_packet)
    resp = s.recv(1024)
    print("Login response:", resp.hex())
    s.close()
except Exception as e:
    print("Login error:", e)
    time.sleep(5)

# Then send location packets in loop
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        location_packet = build_gt06_location_packet(imei, lat, lon, speed)
        s.sendall(location_packet)
        resp = s.recv(1024)
        print(f"Location response ({lat},{lon}):", resp.hex())
        s.close()
        
        # Update coordinates
        lat += 0.001
        lon += 0.001
        speed = random.randint(40, 120)
        
        time.sleep(5)
    except Exception as e:
        print("Location error:", e)
        time.sleep(5)

