from flask import Flask, render_template, jsonify, request, redirect
import threading
from listener import start_server
from db import init_db, get_latest, get_db, list_vehicles, add_vehicle, list_drivers, add_driver, list_assignments, assign_driver, unassign_driver
from config import WEB_PORT
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "ytwl-secret"
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("map.html")

@app.route("/api/latest")
def api_latest():
    return jsonify(get_latest())

@app.route("/api/violations")
def api_violations():
    db = get_db()
    c = db.cursor()
    c.execute("""
        SELECT imei, speed, speed_limit, latitude, longitude, timestamp
        FROM speed_violations
        ORDER BY id DESC
        LIMIT 200
    """)
    rows = c.fetchall()
    db.close()

    return jsonify([
        {
            "imei": r[0],
            "speed": r[1],
            "limit": r[2],
            "lat": r[3],
            "lon": r[4],
            "time": r[5]
        } for r in rows
    ])

def push_location(data):
    socketio.emit("gps_update", data)

@app.route("/vehicles", methods=["GET", "POST"])
def vehicles():
    if request.method == "POST":
        add_vehicle(
            request.form["name"],
            request.form["imei"],
            request.form["plate"],
            request.form["speed_limit"]
        )
        return redirect("/vehicles")

    return render_template(
        "vehicles.html",
        vehicles=list_vehicles()
    )

@app.route("/drivers", methods=["GET", "POST"])
def drivers():
    if request.method == "POST":
        add_driver(
            request.form["name"],
            request.form["phone"]
        )
        return redirect("/drivers")

    return render_template(
        "drivers.html",
        drivers=list_drivers()
    )

@app.route("/assign", methods=["GET", "POST"])
def assign():
    if request.method == "POST":
        if "unassign" in request.form:
            unassign_driver(request.form["unassign"])
        else:
            assign_driver(
                request.form["imei"],
                request.form["driver_id"]
            )
        return redirect("/assign")

    return render_template(
        "assign.html",
        vehicles=list_vehicles(),
        drivers=list_drivers(),
        assignments=list_assignments()
    )

if __name__ == "__main__":
    init_db()
    
    tcp_thread = threading.Thread(target=start_server, daemon=True)
    tcp_thread.start()
    
    socketio.run(app, host="0.0.0.0", port=8000)


