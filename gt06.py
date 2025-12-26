import struct

def bytes_to_imei(data):
    imei_bytes = data[4:12]
    imei = ""
    for b in imei_bytes:
        high = b >> 4
        low = b & 0x0F
        if high <= 9:
            imei += str(high)
        if low <= 9:
            imei += str(low)
    return imei

def parse_location_packet(data):
    # Latitude & Longitude (4 bytes each)
    lat_raw = struct.unpack(">I", data[11:15])[0]
    lon_raw = struct.unpack(">I", data[15:19])[0]

    # GT06 coordinate conversion: divide by 1000000.0 for degrees
    latitude = lat_raw / 1000000.0
    longitude = lon_raw / 1000000.0

    speed = data[19]  # km/h

    return latitude, longitude, speed

def is_gt06_packet(data):
    return data[:2] == b'\x78\x78' or data[:2] == b'\x79\x79'

def packet_type(data):
    return data[3]
