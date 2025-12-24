from db import get_speed_limit, log_violation

OVERSPEED_TOLERANCE = 5  # km/h

def enforce_speed(imei, speed, lat, lon, timestamp):
    limit = get_speed_limit(imei)

    if speed > (limit + OVERSPEED_TOLERANCE):
        log_violation(
            imei=imei,
            speed=speed,
            limit=limit,
            lat=lat,
            lon=lon,
            timestamp=timestamp
        )
        return True, limit

    return False, limit
