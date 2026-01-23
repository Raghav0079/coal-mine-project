"""
Configuration file for Coal Mine Safety Dashboard
Contains safety thresholds, helmet configurations, and system settings
"""

# Gas Safety Thresholds (based on mining safety standards)
GAS_SAFETY_THRESHOLDS = {
    "carbon_monoxide_co": {
        "safe": 25,  # ppm - Normal levels
        "warning": 50,  # ppm - Increased monitoring required
        "danger": 100,  # ppm - Immediate action required
        "critical": 200,  # ppm - Emergency evacuation
    },
    "methane_ch4": {
        "safe": 1.0,  # % - Normal levels
        "warning": 1.5,  # % - Warning level
        "danger": 2.0,  # % - Danger level
        "critical": 2.5,  # % - Critical level
    },
    "oxygen_o2": {
        "safe": 19.5,  # % - Safe minimum oxygen level
        "warning": 19.0,  # % - Warning level
        "danger": 18.5,  # % - Dangerous level
        "critical": 18.0,  # % - Critical level
    },
    "hydrogen_sulfide_h2s": {
        "safe": 10,  # ppm - Safe level
        "warning": 15,  # ppm - Warning level
        "danger": 20,  # ppm - Danger level
        "critical": 50,  # ppm - Critical level
    },
    "carbon_dioxide_co2": {
        "safe": 500,  # ppm - Normal levels
        "warning": 800,  # ppm - Warning level
        "danger": 1200,  # ppm - Danger level
        "critical": 1500,  # ppm - Critical level
    },
}

# Environmental Safety Thresholds
ENVIRONMENTAL_THRESHOLDS = {
    "temperature": {
        "safe": 30,  # °C - Safe working temperature
        "warning": 35,  # °C - Warning level
        "danger": 40,  # °C - Dangerous heat level
        "critical": 45,  # °C - Critical heat level
    },
    "humidity": {
        "safe": 80,  # % - Safe humidity level
        "warning": 90,  # % - Warning level
        "danger": 95,  # % - Dangerous humidity
        "critical": 98,  # % - Critical humidity
    },
}

# Physiological Safety Thresholds (from patent specifications)
HEALTH_THRESHOLDS = {
    "heart_rate": {
        "safe": 100,  # bpm - Normal working heart rate
        "warning": 120,  # bpm - Elevated heart rate
        "danger": 140,  # bpm - High stress level
        "critical": 160,  # bpm - Critical stress level
    },
    "stress_level": {
        "safe": 0.3,  # ratio - Normal stress
        "warning": 0.5,  # ratio - Elevated stress
        "danger": 0.7,  # ratio - High stress
        "critical": 0.9,  # ratio - Critical stress
    },
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    "update_interval": 2000,  # milliseconds - Real-time update frequency
    "data_buffer_size": 100,  # number of readings to store per helmet
    "max_helmets": 50,  # maximum number of helmets supported
    "alert_retention": 1000,  # maximum number of alerts to keep in memory
}

# Helmet Configuration
HELMET_LOCATIONS = [
    "Tunnel A-1",
    "Tunnel A-2",
    "Tunnel A-3",
    "Tunnel B-1",
    "Tunnel B-2",
    "Tunnel B-3",
    "Tunnel C-1",
    "Tunnel C-2",
    "Tunnel C-3",
    "Central Hub",
    "Exit Shaft",
    "Equipment Bay",
    "Ventilation Shaft",
    "Main Corridor",
]

# Communication Protocol Settings (from patent)
COMMUNICATION_CONFIG = {
    "lora_frequency": 915,  # MHz - LoRa frequency
    "zigbee_channel": 11,  # ZigBee channel
    "transmission_power": 20,  # dBm
    "network_timeout": 30,  # seconds
    "retry_attempts": 3,
}

# AI Model Configuration (from your trained models)
AI_MODEL_CONFIG = {
    "ensemble_weights": {
        "random_forest": 0.4,  # Weight for Random Forest
        "svm": 0.35,  # Weight for SVM
        "naive_bayes": 0.25,  # Weight for Naive Bayes
    },
    "risk_confidence_thresholds": {
        "low": 0.3,
        "medium": 0.6,
        "high": 0.8,
        "critical": 0.9,
    },
    "feature_count": 128,  # Number of features for AI model
    "prediction_classes": 6,  # Number of risk classes (1-6)
}

# Emergency Protocol Configuration
EMERGENCY_CONFIG = {
    "auto_alert_levels": ["danger", "critical"],
    "evacuation_trigger_conditions": {
        "methane_level": 2.5,  # % CH4
        "co_level": 200,  # ppm CO
        "oxygen_level": 18.0,  # % O2 (below this level)
        "multiple_warnings": 3,  # Number of simultaneous warnings
    },
    "alert_escalation_time": 300,  # seconds - Time before escalating alerts
    "emergency_contact_list": [
        "Mine Safety Officer",
        "Emergency Response Team",
        "Medical Team",
        "Mine Supervisor",
    ],
}

# Database Configuration
DATABASE_CONFIG = {
    "db_path": "database/coal_mine_data.db",
    "backup_interval": 3600,  # seconds - Database backup frequency
    "data_retention_days": 90,  # days - How long to keep historical data
    "batch_insert_size": 100,  # Number of records to insert at once
}

# Logging Configuration
LOGGING_CONFIG = {
    "log_level": "INFO",
    "log_file": "logs/dashboard.log",
    "max_log_size": "10MB",
    "backup_count": 5,
}
