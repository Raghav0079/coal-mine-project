#!/usr/bin/env python3
"""
Coal Mine Safety Dashboard - Phase 2: Real-time Data Simulation
Sensor-Fused AI Helmet for Real-Time Coal Mine Threat Assessment

Phase 2 Features:
- Real-time data simulation with 2-second updates
- Dynamic sensor readings that change over time
- Live gas metrics display (CO2, CH4, O2, H2S)
- Data buffer management for continuous monitoring
- Alert notifications when thresholds are exceeded
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import random
import numpy as np
import time
from collections import deque

# Initialize Dash app with custom styling
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
)

app.title = "Coal Mine Safety Dashboard"

# Static sample data for Phase 1 (will be replaced with real-time in Phase 2)
SAMPLE_HELMETS = {
    "HELMET_001": {"miner": "John Smith", "location": "Tunnel A-1", "status": "ACTIVE"},
    "HELMET_002": {
        "miner": "Maria Garcia",
        "location": "Tunnel A-2",
        "status": "ACTIVE",
    },
    "HELMET_003": {"miner": "David Chen", "location": "Tunnel B-1", "status": "ACTIVE"},
    "HELMET_004": {
        "miner": "Sarah Johnson",
        "location": "Tunnel B-2",
        "status": "ACTIVE",
    },
    "HELMET_005": {
        "miner": "Michael Brown",
        "location": "Tunnel C-1",
        "status": "ACTIVE",
    },
    "HELMET_006": {
        "miner": "Lisa Wilson",
        "location": "Tunnel C-2",
        "status": "OFFLINE",
    },
    "HELMET_007": {
        "miner": "Robert Davis",
        "location": "Central Hub",
        "status": "ACTIVE",
    },
    "HELMET_008": {
        "miner": "Emma Taylor",
        "location": "Exit Shaft",
        "status": "ACTIVE",
    },
}

# Real-time data storage and simulation parameters
DATA_BUFFER_SIZE = 100  # Store last 100 readings per helmet
UPDATE_INTERVAL = 2000  # 2 seconds in milliseconds

# Initialize data buffers for each helmet
real_time_data = {}
data_timestamps = {}
for helmet_id in SAMPLE_HELMETS.keys():
    real_time_data[helmet_id] = {
        "co2": deque(maxlen=DATA_BUFFER_SIZE),
        "ch4": deque(maxlen=DATA_BUFFER_SIZE),
        "o2": deque(maxlen=DATA_BUFFER_SIZE),
        "h2s": deque(maxlen=DATA_BUFFER_SIZE),
        "temp": deque(maxlen=DATA_BUFFER_SIZE),
        "humidity": deque(maxlen=DATA_BUFFER_SIZE),
    }
    data_timestamps[helmet_id] = deque(maxlen=DATA_BUFFER_SIZE)

# Base sensor readings for simulation (will vary around these values)
BASE_SENSOR_DATA = {
    "HELMET_001": {
        "co2": 420,
        "ch4": 0.8,
        "o2": 20.5,
        "h2s": 3,
        "temp": 28,
        "humidity": 72,
    },
    "HELMET_002": {
        "co2": 450,
        "ch4": 1.2,
        "o2": 20.1,
        "h2s": 5,
        "temp": 30,
        "humidity": 75,
    },
    "HELMET_003": {
        "co2": 380,
        "ch4": 0.5,
        "o2": 20.8,
        "h2s": 2,
        "temp": 26,
        "humidity": 68,
    },
    "HELMET_004": {
        "co2": 520,
        "ch4": 1.5,
        "o2": 19.8,
        "h2s": 7,
        "temp": 32,
        "humidity": 78,
    },
    "HELMET_005": {
        "co2": 410,
        "ch4": 0.9,
        "o2": 20.3,
        "h2s": 4,
        "temp": 29,
        "humidity": 71,
    },
    "HELMET_006": {"co2": 0, "ch4": 0, "o2": 0, "h2s": 0, "temp": 0, "humidity": 0},
    "HELMET_007": {
        "co2": 395,
        "ch4": 0.6,
        "o2": 20.6,
        "h2s": 3,
        "temp": 27,
        "humidity": 70,
    },
    "HELMET_008": {
        "co2": 370,
        "ch4": 0.4,
        "o2": 20.9,
        "h2s": 2,
        "temp": 25,
        "humidity": 65,
    },
}

# Sensor variation parameters for realistic simulation
SENSOR_VARIATION = {
    "co2": {"noise": 15, "drift": 0.02, "spike_chance": 0.05, "spike_magnitude": 100},
    "ch4": {"noise": 0.1, "drift": 0.001, "spike_chance": 0.03, "spike_magnitude": 0.5},
    "o2": {"noise": 0.2, "drift": 0.001, "spike_chance": 0.02, "spike_magnitude": -1.0},
    "h2s": {"noise": 0.5, "drift": 0.01, "spike_chance": 0.04, "spike_magnitude": 5},
    "temp": {"noise": 1.0, "drift": 0.005, "spike_chance": 0.01, "spike_magnitude": 5},
    "humidity": {
        "noise": 2.0,
        "drift": 0.01,
        "spike_chance": 0.02,
        "spike_magnitude": 10,
    },
}


def generate_realistic_sensor_reading(helmet_id, sensor_type, previous_value=None):
    """Generate realistic sensor readings with noise, drift, and occasional spikes"""
    base_value = BASE_SENSOR_DATA[helmet_id][sensor_type]
    variation = SENSOR_VARIATION[sensor_type]

    # If helmet is offline, return 0
    if SAMPLE_HELMETS[helmet_id]["status"] == "OFFLINE":
        return 0

    # Start with base value if no previous reading
    if previous_value is None:
        current_value = base_value
    else:
        current_value = previous_value

    # Add random noise
    noise = random.gauss(0, variation["noise"])

    # Add gradual drift
    drift = random.gauss(0, variation["drift"] * base_value)

    # Occasional spikes (simulating environmental events)
    spike = 0
    if random.random() < variation["spike_chance"]:
        spike = random.gauss(0, variation["spike_magnitude"])

    # Calculate new value
    new_value = current_value + noise + drift + spike

    # Apply sensor-specific constraints
    if sensor_type == "co2":
        new_value = max(200, min(2000, new_value))  # CO2 physical limits
    elif sensor_type == "ch4":
        new_value = max(0, min(5, new_value))  # CH4 percentage limits
    elif sensor_type == "o2":
        new_value = max(15, min(22, new_value))  # O2 percentage limits
    elif sensor_type == "h2s":
        new_value = max(0, min(50, new_value))  # H2S ppm limits
    elif sensor_type == "temp":
        new_value = max(15, min(50, new_value))  # Temperature limits
    elif sensor_type == "humidity":
        new_value = max(30, min(95, new_value))  # Humidity limits

    return round(new_value, 2)


def update_all_sensor_data():
    """Update sensor data for all helmets"""
    current_time = datetime.now()

    for helmet_id in SAMPLE_HELMETS.keys():
        # Generate new readings based on previous values
        for sensor_type in ["co2", "ch4", "o2", "h2s", "temp", "humidity"]:
            # Get previous value if available
            previous_value = None
            if len(real_time_data[helmet_id][sensor_type]) > 0:
                previous_value = real_time_data[helmet_id][sensor_type][-1]

            # Generate new reading
            new_reading = generate_realistic_sensor_reading(
                helmet_id, sensor_type, previous_value
            )

            # Store in buffer
            real_time_data[helmet_id][sensor_type].append(new_reading)

        # Store timestamp
        data_timestamps[helmet_id].append(current_time)


def get_current_readings(helmet_id):
    """Get the most recent readings for a helmet"""
    if helmet_id not in real_time_data or len(real_time_data[helmet_id]["co2"]) == 0:
        # Return base data if no real-time data available
        return BASE_SENSOR_DATA[helmet_id]

    return {
        "co2": real_time_data[helmet_id]["co2"][-1],
        "ch4": real_time_data[helmet_id]["ch4"][-1],
        "o2": real_time_data[helmet_id]["o2"][-1],
        "h2s": real_time_data[helmet_id]["h2s"][-1],
        "temp": real_time_data[helmet_id]["temp"][-1],
        "humidity": real_time_data[helmet_id]["humidity"][-1],
    }


# Initialize with some initial data
for _ in range(5):  # Generate 5 initial readings
    update_all_sensor_data()
    time.sleep(0.1)  # Small delay between initial readings


def get_status_color(value, thresholds):
    """Get color based on threshold values"""
    if value == 0:
        return "#6c757d"  # Gray for offline
    elif value <= thresholds["safe"]:
        return "#28a745"  # Green - Safe
    elif value <= thresholds["warning"]:
        return "#ffc107"  # Yellow - Warning
    elif value <= thresholds["danger"]:
        return "#fd7e14"  # Orange - Danger
    else:
        return "#dc3545"  # Red - Critical


def create_metric_card(title, value, unit, icon, thresholds, description=""):
    """Create a metric display card with color coding"""
    color = get_status_color(value, thresholds)
    status_text = "OFFLINE" if value == 0 else "NORMAL"

    if value > 0:
        if value > thresholds["danger"]:
            status_text = "CRITICAL"
        elif value > thresholds["warning"]:
            status_text = "WARNING"
        elif value > thresholds["safe"]:
            status_text = "CAUTION"

    return html.Div(
        [
            html.Div(
                [
                    html.I(
                        className=f"fas {icon}",
                        style={
                            "fontSize": "24px",
                            "color": color,
                            "marginBottom": "10px",
                        },
                    ),
                    html.H3(
                        title,
                        style={"color": "#2c3e50", "margin": "0", "fontSize": "16px"},
                    ),
                    html.Div(
                        [
                            html.Span(
                                f"{value}",
                                style={
                                    "fontSize": "32px",
                                    "fontWeight": "bold",
                                    "color": color,
                                },
                            ),
                            html.Span(
                                f" {unit}",
                                style={
                                    "fontSize": "14px",
                                    "color": "#6c757d",
                                    "marginLeft": "5px",
                                },
                            ),
                        ]
                    ),
                    html.Div(
                        status_text,
                        style={
                            "fontSize": "12px",
                            "fontWeight": "bold",
                            "color": color,
                            "marginTop": "5px",
                            "letterSpacing": "1px",
                        },
                    ),
                    html.P(
                        description,
                        style={
                            "fontSize": "11px",
                            "color": "#6c757d",
                            "margin": "5px 0 0 0",
                        },
                    ),
                ]
            )
        ],
        className="metric-card",
        style={
            "backgroundColor": "white",
            "borderRadius": "10px",
            "padding": "20px",
            "textAlign": "center",
            "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
            "border": f"3px solid {color}",
            "margin": "10px",
            "minHeight": "180px",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
        },
    )


def create_helmet_status_card(helmet_id, helmet_info, gas_data):
    """Create individual helmet status overview card"""
    status_color = "#28a745" if helmet_info["status"] == "ACTIVE" else "#6c757d"

    return html.Div(
        [
            html.H5(helmet_id, style={"margin": "0 0 10px 0", "color": "#2c3e50"}),
            html.P(
                helmet_info["miner"],
                style={"margin": "0", "fontWeight": "bold", "color": "#495057"},
            ),
            html.P(
                helmet_info["location"],
                style={"margin": "0 0 10px 0", "fontSize": "12px", "color": "#6c757d"},
            ),
            html.Div(
                [
                    html.Div(
                        helmet_info["status"],
                        style={
                            "color": status_color,
                            "fontWeight": "bold",
                            "fontSize": "12px",
                        },
                    ),
                    html.Hr(style={"margin": "8px 0"}),
                    html.Div(f"CO₂: {gas_data['co2']}ppm", style={"fontSize": "11px"}),
                    html.Div(f"CH₄: {gas_data['ch4']}%", style={"fontSize": "11px"}),
                    html.Div(f"O₂: {gas_data['o2']}%", style={"fontSize": "11px"}),
                    html.Div(f"H₂S: {gas_data['h2s']}ppm", style={"fontSize": "11px"}),
                ]
            ),
        ],
        style={
            "backgroundColor": "white",
            "borderRadius": "8px",
            "padding": "15px",
            "border": f"2px solid {status_color}",
            "margin": "10px",
            "fontSize": "13px",
        },
    )


# Gas thresholds for color coding (based on mining safety standards)
GAS_THRESHOLDS = {
    "co2": {"safe": 500, "warning": 800, "danger": 1200},  # ppm
    "ch4": {"safe": 1.0, "warning": 1.5, "danger": 2.0},  # %
    "o2": {"safe": 19.5, "warning": 19.0, "danger": 18.5},  # % (inverted logic)
    "h2s": {"safe": 10, "warning": 15, "danger": 20},  # ppm
    "temp": {"safe": 30, "warning": 35, "danger": 40},  # °C
    "humidity": {"safe": 80, "warning": 90, "danger": 95},  # %
}

# App Layout
app.layout = html.Div(
    [
        # Header Section
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            [
                                html.I(
                                    className="fas fa-hard-hat",
                                    style={"marginRight": "15px"},
                                ),
                                "COAL MINE SAFETY DASHBOARD",
                            ],
                            style={
                                "color": "white",
                                "margin": "0",
                                "textAlign": "center",
                            },
                        ),
                        html.P(
                            "Sensor-Fused AI Helmet for Real-Time Threat Assessment",
                            style={
                                "color": "#cccccc",
                                "margin": "5px 0 0 0",
                                "textAlign": "center",
                                "fontSize": "16px",
                            },
                        ),
                    ]
                )
            ],
            style={
                "backgroundColor": "#1a252f",
                "padding": "25px",
                "marginBottom": "20px",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
            },
        ),
        # Status Bar
        html.Div(
            [
                html.Div(
                    [
                        html.I(
                            className="fas fa-users",
                            style={"fontSize": "20px", "marginRight": "10px"},
                        ),
                        html.Span("7 ACTIVE HELMETS", style={"fontWeight": "bold"}),
                    ],
                    style={"color": "#28a745", "padding": "10px 20px"},
                ),
                html.Div(
                    [
                        html.I(
                            className="fas fa-exclamation-triangle",
                            style={"fontSize": "20px", "marginRight": "10px"},
                        ),
                        html.Span("2 WARNINGS", style={"fontWeight": "bold"}),
                    ],
                    style={"color": "#ffc107", "padding": "10px 20px"},
                ),
                html.Div(
                    [
                        html.I(
                            className="fas fa-clock",
                            style={"fontSize": "20px", "marginRight": "10px"},
                        ),
                        html.Span(
                            datetime.now().strftime("%H:%M:%S"),
                            id="current-time",
                            style={"fontWeight": "bold"},
                        ),
                    ],
                    style={"color": "#17a2b8", "padding": "10px 20px"},
                ),
                html.Div(
                    [
                        html.I(
                            className="fas fa-robot",
                            style={"fontSize": "20px", "marginRight": "10px"},
                        ),
                        html.Span("AI SYSTEM: ACTIVE", style={"fontWeight": "bold"}),
                    ],
                    style={"color": "#6f42c1", "padding": "10px 20px"},
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-around",
                "backgroundColor": "#f8f9fa",
                "borderRadius": "10px",
                "margin": "0 20px 30px 20px",
                "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
            },
        ),
        # Control Panel
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            [
                                html.I(
                                    className="fas fa-hard-hat",
                                    style={"marginRight": "10px"},
                                ),
                                "Select Helmet for Detailed View:",
                            ],
                            style={
                                "fontWeight": "bold",
                                "color": "#2c3e50",
                                "marginBottom": "10px",
                            },
                        ),
                        dcc.Dropdown(
                            id="helmet-selector",
                            options=[
                                {
                                    "label": f"{helmet_id} - {info['miner']} ({info['location']})",
                                    "value": helmet_id,
                                }
                                for helmet_id, info in SAMPLE_HELMETS.items()
                            ],
                            value="HELMET_001",
                            style={"marginBottom": "20px"},
                            className="helmet-dropdown",
                        ),
                    ]
                )
            ],
            style={"margin": "0 20px 30px 20px"},
        ),
        # Real-time update interval component
        dcc.Interval(
            id="interval-component",
            interval=UPDATE_INTERVAL,  # Update every 2 seconds
            n_intervals=0,
        ),
        # Store component for real-time data
        dcc.Store(id="live-data-store"),
        # Main Dashboard Content
        html.Div(
            [
                # Status indicators for real-time updates
                html.Div(
                    [
                        html.Div(
                            [
                                html.I(
                                    className="fas fa-circle",
                                    style={"color": "#28a745", "marginRight": "8px"},
                                ),
                                "LIVE DATA",
                                html.Span(
                                    id="last-update-time",
                                    style={
                                        "marginLeft": "10px",
                                        "fontSize": "12px",
                                        "color": "#6c757d",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "fontSize": "14px",
                                "fontWeight": "bold",
                                "color": "#2c3e50",
                            },
                        ),
                    ],
                    style={
                        "backgroundColor": "#f8f9fa",
                        "padding": "10px 20px",
                        "borderRadius": "8px",
                        "marginBottom": "20px",
                        "border": "1px solid #dee2e6",
                    },
                ),
                # Gas Metrics Section
                html.Div(
                    [
                        html.H3(
                            [
                                html.I(
                                    className="fas fa-wind",
                                    style={"marginRight": "10px"},
                                ),
                                "Gas Level Monitoring",
                                html.Span(
                                    "(Live Updates Every 2s)",
                                    style={
                                        "fontSize": "14px",
                                        "color": "#6c757d",
                                        "fontWeight": "normal",
                                        "marginLeft": "10px",
                                    },
                                ),
                            ],
                            style={"color": "#2c3e50", "marginBottom": "20px"},
                        ),
                        html.Div(id="gas-metrics-display", children=[]),
                    ],
                    style={"marginBottom": "40px"},
                ),
                # Environmental Conditions Section
                html.Div(
                    [
                        html.H3(
                            [
                                html.I(
                                    className="fas fa-thermometer-half",
                                    style={"marginRight": "10px"},
                                ),
                                "Environmental Conditions",
                            ],
                            style={"color": "#2c3e50", "marginBottom": "20px"},
                        ),
                        html.Div(id="environmental-metrics-display", children=[]),
                    ],
                    style={"marginBottom": "40px"},
                ),
                # All Helmets Status Overview
                html.Div(
                    [
                        html.H3(
                            [
                                html.I(
                                    className="fas fa-th-large",
                                    style={"marginRight": "10px"},
                                ),
                                "All Helmets Status Overview",
                            ],
                            style={
                                "color": "#2c3e50",
                                "marginBottom": "20px",
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            id="all-helmets-display",
                            children=[
                                html.Div(
                                    "Loading helmet status...",
                                    style={"textAlign": "center", "padding": "20px"},
                                )
                            ],
                        ),
                    ]
                ),
            ],
            style={"margin": "0 20px"},
        ),
        # Footer
        html.Div(
            [
                html.P(
                    [
                        "🏭 Coal Mine Safety Dashboard v1.0 | ",
                        "Patent: Sensor-Fused AI Helmet for Real-Time Threat Assessment | ",
                        f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    ],
                    style={"textAlign": "center", "color": "#6c757d", "margin": "0"},
                )
            ],
            style={
                "backgroundColor": "#f8f9fa",
                "padding": "20px",
                "marginTop": "50px",
                "borderTop": "1px solid #dee2e6",
            },
        ),
    ]
)


# Real-time data update callback
@app.callback(
    [Output("live-data-store", "data"), Output("last-update-time", "children")],
    [Input("interval-component", "n_intervals")],
)
def update_live_data(n_intervals):
    """Update sensor data every interval"""
    # Generate new sensor readings
    update_all_sensor_data()

    # Get current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # Prepare data for storage
    current_data = {}
    for helmet_id in SAMPLE_HELMETS.keys():
        current_data[helmet_id] = get_current_readings(helmet_id)

    return current_data, f"Last updated: {current_time}"


# Callback for updating dashboard based on helmet selection and real-time data
@app.callback(
    [
        Output("gas-metrics-display", "children"),
        Output("environmental-metrics-display", "children"),
    ],
    [Input("helmet-selector", "value"), Input("live-data-store", "data")],
)
def update_dashboard(selected_helmet, live_data):
    """Update dashboard displays based on selected helmet and real-time data"""
    if not selected_helmet or not live_data:
        return [], []

    # Get real-time data for selected helmet
    data = live_data.get(selected_helmet, get_current_readings(selected_helmet))
    helmet_info = SAMPLE_HELMETS.get(selected_helmet, {})

    # Check for alerts
    alerts = []
    if data["co2"] > GAS_THRESHOLDS["co2"]["warning"]:
        alerts.append("CO₂ Alert")
    if data["ch4"] > GAS_THRESHOLDS["ch4"]["warning"]:
        alerts.append("Methane Alert")
    if data["o2"] < 19.5:
        alerts.append("Low Oxygen Alert")
    if data["h2s"] > GAS_THRESHOLDS["h2s"]["warning"]:
        alerts.append("H₂S Alert")

    # Gas Metrics Cards with real-time data
    gas_cards = html.Div(
        [
            # Alert banner if any alerts
            (
                html.Div(
                    [
                        html.I(
                            className="fas fa-exclamation-triangle",
                            style={"marginRight": "10px", "fontSize": "18px"},
                        ),
                        "ALERTS: " + ", ".join(alerts),
                    ],
                    style={
                        "backgroundColor": "#fff3cd",
                        "color": "#856404",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "marginBottom": "20px",
                        "border": "1px solid #ffeaa7",
                        "fontWeight": "bold",
                        "display": "flex",
                        "alignItems": "center",
                    },
                )
                if alerts
                else html.Div()
            ),
            html.Div(
                [
                    create_metric_card(
                        "Carbon Dioxide",
                        data["co2"],
                        "ppm",
                        "fa-smog",
                        GAS_THRESHOLDS["co2"],
                        "Safe: <500ppm",
                    ),
                    create_metric_card(
                        "Methane",
                        data["ch4"],
                        "%",
                        "fa-fire",
                        GAS_THRESHOLDS["ch4"],
                        "Safe: <1.0%",
                    ),
                    create_metric_card(
                        "Oxygen",
                        data["o2"],
                        "%",
                        "fa-lungs",
                        {"safe": 21, "warning": 19.5, "danger": 19.0},
                        "Safe: >19.5%",
                    ),
                    create_metric_card(
                        "Hydrogen Sulfide",
                        data["h2s"],
                        "ppm",
                        "fa-skull-crossbones",
                        GAS_THRESHOLDS["h2s"],
                        "Safe: <10ppm",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                    "gap": "10px",
                },
            ),
        ]
    )

    # Environmental Metrics Cards with real-time data
    env_cards = html.Div(
        [
            html.Div(
                [
                    create_metric_card(
                        "Temperature",
                        data["temp"],
                        "°C",
                        "fa-thermometer-half",
                        GAS_THRESHOLDS["temp"],
                        "Safe: <30°C",
                    ),
                    create_metric_card(
                        "Humidity",
                        data["humidity"],
                        "%",
                        "fa-tint",
                        GAS_THRESHOLDS["humidity"],
                        "Safe: <80%",
                    ),
                    create_metric_card(
                        "Helmet Status",
                        1 if helmet_info["status"] == "ACTIVE" else 0,
                        helmet_info["status"],
                        "fa-hard-hat",
                        {"safe": 1, "warning": 1, "danger": 1},
                        f"Location: {helmet_info['location']}",
                    ),
                    create_metric_card(
                        "Miner",
                        0,
                        helmet_info["miner"],
                        "fa-user",
                        {"safe": 1, "warning": 1, "danger": 1},
                        "Assigned Worker",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                    "gap": "10px",
                },
            )
        ]
    )

    return gas_cards, env_cards


# Callback for updating all helmets overview
@app.callback(
    Output("all-helmets-display", "children"),
    [Input("live-data-store", "data")],
)
def update_all_helmets_display(live_data):
    """Update all helmets status display with real-time data"""
    if not live_data:
        return html.Div(
            "Loading helmet status...", style={"textAlign": "center", "padding": "20px"}
        )

    helmet_cards = []
    for helmet_id, helmet_info in SAMPLE_HELMETS.items():
        current_data = live_data.get(helmet_id, get_current_readings(helmet_id))
        helmet_cards.append(
            create_helmet_status_card(helmet_id, helmet_info, current_data)
        )

    return html.Div(
        helmet_cards,
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
            "gap": "10px",
            "margin": "0 10px",
        },
    )


if __name__ == "__main__":
    print("🚀 Starting Coal Mine Safety Dashboard - Phase 2")
    print("📊 Features: Real-time data simulation with live updates")
    print("🔄 Update Interval: 2 seconds")
    print("🌐 Access dashboard at: http://127.0.0.1:8050")
    print("⛑️  Monitoring 8 helmet sensors with dynamic data")
    print("🚨 Alert system: Active for threshold violations")
    print("💾 Data Buffer: Storing last 100 readings per helmet")

    app.run(debug=True, host="127.0.0.1", port=8050)
