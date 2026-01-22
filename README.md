coal-mine-dashboard/
├── 📄 app.py                          # Main Dash application
├── 📄 requirements.txt                # Python dependencies
├── 📄 config.py                      # Configuration settings
├── 📄 run_dashboard.py               # Production runner script
│
├── 📂 models/                        # AI Model Integration
│   ├── __init__.py
│   ├── ensemble_ai.py               # Hybrid AI model (SVM+RF+NB)
│   ├── risk_classifier.py          # Risk assessment logic
│   └── model_loader.py              # Load your trained models
│
├── 📂 data/                         # Data Management
│   ├── __init__.py
│   ├── sensor_simulator.py         # Helmet sensor data simulation
│   ├── database_manager.py         # SQLite/database operations
│   └── data_processor.py           # Real-time data processing
│
├── 📂 components/                   # Dashboard Components
│   ├── __init__.py
│   ├── layout.py                   # Main dashboard layout
│   ├── helmet_status.py            # Individual helmet displays
│   ├── gas_sensors.py              # Gas sensor components
│   ├── health_monitor.py           # Physiological monitoring
│   ├── ai_risk_display.py          # AI risk assessment UI
│   ├── alert_system.py             # Alert management
│   └── charts.py                   # Real-time charts
│
├── 📂 callbacks/                    # Dash Callbacks
│   ├── __init__.py
│   ├── real_time_updates.py        # Real-time data callbacks
│   ├── helmet_callbacks.py         # Helmet-specific callbacks
│   ├── alert_callbacks.py          # Alert system callbacks
│   └── emergency_callbacks.py      # Emergency response
│
├── 📂 assets/                       # Static Assets
│   ├── 📄 style.css               # Custom CSS styling
│   ├── 📄 mining_theme.css         # Industrial theme
│   ├── 🖼️ logo.png                # Company/project logo
│   └── 🔊 alert_sounds/           # Alert sound files
│       ├── critical_alert.mp3
│       ├── warning_alert.mp3
│       └── emergency_alarm.mp3
│
├── 📂 utils/                        # Utility Functions
│   ├── __init__.py
│   ├── communication.py            # LoRa/ZigBee simulation
│   ├── emergency_protocols.py      # Emergency response logic
│   ├── logging_config.py           # Logging setup
│   └── helpers.py                  # General helper functions
│
├── 📂 database/                     # Database Schema
│   ├── schema.sql                  # Database schema
│   ├── init_db.py                  # Database initialization
│   └── coal_mine_data.db           # SQLite database file
│
└── 📂 docs/                         # Documentation
    ├── setup_guide.md              # Setup instructions
    ├── user_manual.md              # User manual
    └── patent_compliance.md        # Patent feature mapping
