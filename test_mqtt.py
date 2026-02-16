#!/usr/bin/env python3
"""
MQTT Test Script for Coal Mine Dashboard
This script simulates MQTT messages from a Wokwi sensor for testing purposes.
Run this script to test your dashboard before setting up the actual Wokwi simulator.
"""

import json
import random
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# MQTT Configuration (should match your dashboard settings)
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "wokwi/coalmine/sensors"

# Test helmet IDs
HELMET_IDS = ["HELMET_001", "HELMET_002", "HELMET_003"]


def on_connect(client, userdata, flags, rc):
    """Callback for MQTT connection"""
    if rc == 0:
        print(f"✅ Connected to MQTT broker: {MQTT_BROKER}")
    else:
        print(f"❌ Failed to connect to MQTT broker. Return code: {rc}")


def generate_sensor_data(helmet_id):
    """Generate realistic sensor data"""
    return {
        "helmet_id": helmet_id,
        "co2": round(random.uniform(350, 800), 2),
        "ch4": round(random.uniform(0.5, 2.0), 2),
        "o2": round(random.uniform(19.0, 21.0), 2),
        "h2s": round(random.uniform(1, 15), 2),
        "temp": round(random.uniform(24, 35), 2),
        "humidity": round(random.uniform(60, 85), 2),
        "timestamp": datetime.now().isoformat(),
    }


def main():
    print("🧪 MQTT Test Script for Coal Mine Dashboard")
    print(f"📡 Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"📋 Topic: {MQTT_TOPIC}")
    print("🚀 Starting to send test data...")
    print("Press Ctrl+C to stop")

    # Setup MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect

    try:
        # Connect to broker
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        # Send test data every 3 seconds
        while True:
            for helmet_id in HELMET_IDS:
                sensor_data = generate_sensor_data(helmet_id)
                json_data = json.dumps(sensor_data)

                result = client.publish(MQTT_TOPIC, json_data)
                if result.rc == 0:
                    print(
                        f"📤 Sent data for {helmet_id}: CO2={sensor_data['co2']}, CH4={sensor_data['ch4']}"
                    )
                else:
                    print(f"❌ Failed to send data for {helmet_id}")

            time.sleep(3)  # Send data every 3 seconds

    except KeyboardInterrupt:
        print("\n🛑 Stopping test script...")
        client.loop_stop()
        client.disconnect()
        print("✅ Disconnected from MQTT broker")


if __name__ == "__main__":
    main()
