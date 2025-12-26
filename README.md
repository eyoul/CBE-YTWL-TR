# YTWL GPS Tracker

A real-time GPS tracking system for YTWL devices with web interface, vehicle management, and overspeed monitoring.

## Features

### 🚗 Core Functionality
- **Real-time GPS Tracking** - Live location updates via Socket.IO
- **YTWL Device Support** - TCP listener for GT06 protocol
- **Vehicle Management** - Add/edit vehicles with IMEI tracking
- **Driver Management** - Driver registration and assignment
- **Speed Monitoring** - Automatic overspeed detection and alerts
- **Modern Web UI** - Responsive design with navigation

### 📡 Technical Stack
- **Backend:** Python Flask with Socket.IO
- **Database:** SQLite with WAL mode for performance
- **Frontend:** HTML5 with Leaflet.js mapping
- **Real-time:** Socket.IO for live updates
- **Styling:** Modern CSS with glassmorphism effects
- **Protocol:** GT06/YTWL TCP communication

### 🗺️ Project Structure
```
CBE-YTWL-TR/
├── app.py              # Main Flask application
├── listener.py          # YTWL TCP server
├── config.py           # Configuration settings
├── db.py               # Database operations
├── alerts.py           # Notification system
├── requirements.txt     # Python dependencies
├── templates/          # HTML templates
│   ├── base.html      # Navigation layout
│   ├── map.html       # Live GPS map
│   ├── vehicles.html   # Vehicle management
│   ├── drivers.html    # Driver management
│   └── assign.html     # Driver assignments
├── static/             # Static assets
│   └── style.css      # Custom styles
├── docker-compose.yml   # Container orchestration
├── Dockerfile          # Container configuration
├── nginx.conf          # Web server config
├── EC2-DEPLOYMENT.md # AWS deployment guide
└── systemd/           # Service files
    └── gps.service    # System service
```

### 🚀 Quick Start

#### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

#### Docker Development
```bash
# Build and run
docker-compose up

# View logs
docker-compose logs -f
```

### 📱 Web Interface

#### Pages
- **Map** - Live GPS tracking with real-time markers
- **Vehicles** - Add/edit vehicles with speed limits
- **Drivers** - Manage driver profiles
- **Assignments** - Link drivers to vehicles

#### Features
- **Real-time Updates** - Instant location changes
- **Overspeed Alerts** - Visual and email notifications
- **Responsive Design** - Mobile-friendly interface
- **Modern UI** - Glassmorphism effects and smooth animations

### 📡 YTWL Device Integration

#### Connection Details
- **TCP Port:** 9000
- **Protocol:** GT06/YTWL
- **Data Format:** Binary GPS packets
- **Authentication:** IMEI-based device registration

#### Test Device
- **IMEI:** 355442200991235
- **Status:** Configured and ready for testing
- **Expected Data:** GPS coordinates, speed, timestamp

### 🔧 Configuration

#### Environment Variables
```python
# config.py
DB_NAME = "gps.db"           # SQLite database
HOST = "0.0.0.0"             # TCP server host
TCP_PORT = 9000              # YTWL device port
WEB_PORT = 8000               # Flask app port
```

#### Alert Settings
```python
# Telegram notifications
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

# Email notifications
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_email@gmail.com"
SMTP_PASS = "your_app_password"
```

### 🚀 Deployment

#### AWS EC2
- **Containerized:** Docker with Nginx reverse proxy
- **Scalable:** Horizontal scaling support
- **Secure:** HTTPS with Let's Encrypt
- **Monitoring:** Logs and health checks

See [EC2-DEPLOYMENT.md](EC2-DEPLOYMENT.md) for detailed deployment instructions.

### 📊 Database Schema

#### Tables
- **vehicles** - Vehicle registry (name, imei, plate, speed_limit)
- **drivers** - Driver profiles (id, name, phone)
- **assignments** - Driver-vehicle links (imei, driver_id, active)
- **gps_data** - Location history (imei, timestamp, lat, lon, speed)
- **speed_violations** - Overspeed events (imei, speed, limit, location, time)

### 🔒 Security Features

- **Input Validation** - Form sanitization
- **SQL Injection Protection** - Parameterized queries
- **CORS Support** - Cross-origin resource sharing
- **Rate Limiting** - Request throttling (configurable)

### 📈 Monitoring

#### Real-time Metrics
- **Device Status** - Online/offline tracking
- **Speed Monitoring** - Live speed updates
- **Location History** - GPS trail visualization
- **Alert System** - Overspeed notifications

#### Logging
- **Application Logs** - Flask and Socket.IO events
- **Database Logs** - Query performance tracking
- **Error Tracking** - Exception handling and reporting

### 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Add tests if applicable
5. Submit pull request

### 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

### 📞 Support

For technical support or questions:
- **Issues:** GitHub Issues page
- **Documentation:** This README and EC2-DEPLOYMENT.md
- **Device Testing:** Use IMEI 355442200991235 for testing

---

**Current Test Configuration:**
- **Vehicle:** Suzuki (AA000069)
- **IMEI:** 355442200991235
- **Driver:** John Devid (+251912434043)
- **Status:** Ready for production deployment

