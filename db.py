import sqlite3
from config import DB_NAME

def get_db():
    db = sqlite3.connect(DB_NAME, check_same_thread=False)
    db.execute("PRAGMA journal_mode=WAL;")
    return db

def init_db():
    db = get_db()
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        name TEXT,
        imei TEXT PRIMARY KEY,
        plate TEXT,
        speed_limit INTEGER DEFAULT 80
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imei TEXT,
        driver_id INTEGER,
        active INTEGER DEFAULT 1
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS gps_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imei TEXT,
        timestamp TEXT,
        latitude REAL,
        longitude REAL,
        speed REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS speed_violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imei TEXT,
        speed REAL,
        speed_limit INTEGER,
        latitude REAL,
        longitude REAL,
        timestamp TEXT
    )
    """)

    db.commit()
    db.close()


def save_gps(imei, lat, lon, speed, timestamp):
    db = get_db()
    c = db.cursor()
    c.execute("""
        INSERT INTO gps_data (imei, timestamp, latitude, longitude, speed)
        VALUES (?, ?, ?, ?, ?)
    """, (imei, timestamp, lat, lon, speed))
    db.commit()
    db.close()

def get_latest(limit=200):
    db = get_db()
    c = db.cursor()
    c.execute("""
        SELECT imei, timestamp, latitude, longitude, speed
        FROM gps_data
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    db.close()

    return [
        {"imei": r[0], "timestamp": r[1], "lat": r[2], "lon": r[3], "speed": r[4]}
        for r in rows
    ]

def get_speed_limit(imei):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT speed_limit FROM vehicles WHERE imei=?", (imei,))
    row = c.fetchone()
    db.close()
    return row[0] if row else 80  # default 80 km/h

def log_violation(imei, speed, limit, lat, lon, timestamp):
    db = get_db()
    c = db.cursor()
    c.execute("""
        INSERT INTO speed_violations
        (imei, speed, speed_limit, latitude, longitude, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (imei, speed, limit, lat, lon, timestamp))
    db.commit()
    db.close()

def violation_count(imei, minutes=60):
    db = get_db()
    c = db.cursor()
    c.execute("""
        SELECT COUNT(*)
        FROM speed_violations
        WHERE imei=?
        AND timestamp >= datetime('now', ?)
    """, (imei, f"-{minutes} minutes"))
    count = c.fetchone()[0]
    db.close()
    return count

def list_vehicles():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT imei, plate, speed_limit FROM vehicles")
    rows = c.fetchall()
    db.close()
    return rows

def add_vehicle(imei, plate, limit):
    db = get_db()
    c = db.cursor()
    c.execute(
        "INSERT OR REPLACE INTO vehicles VALUES (?, ?, ?)",
        (imei, plate, limit)
    )
    db.commit()
    db.close()

def list_drivers():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, name, phone FROM drivers")
    rows = c.fetchall()
    db.close()
    return rows

def add_driver(name, phone):
    db = get_db()
    c = db.cursor()
    c.execute(
        "INSERT INTO drivers (name, phone) VALUES (?, ?)",
        (name, phone)
    )
    db.commit()
    db.close()

def list_assignments():
    db = get_db()
    c = db.cursor()
    c.execute("""
        SELECT a.imei, v.plate, d.name, d.phone
        FROM assignments a
        JOIN vehicles v ON a.imei = v.imei
        JOIN drivers d ON a.driver_id = d.id
        WHERE a.active = 1
    """)
    rows = c.fetchall()
    db.close()
    return rows

def assign_driver(imei, driver_id):
    db = get_db()
    c = db.cursor()
    # Deactivate previous assignments for this vehicle
    c.execute("UPDATE assignments SET active = 0 WHERE imei = ?", (imei,))
    # Create new assignment
    c.execute("INSERT INTO assignments (imei, driver_id, active) VALUES (?, ?, 1)", (imei, driver_id))
    db.commit()
    db.close()

def unassign_driver(imei):
    db = get_db()
    c = db.cursor()
    c.execute("UPDATE assignments SET active = 0 WHERE imei = ?", (imei,))
    db.commit()
    db.close()
