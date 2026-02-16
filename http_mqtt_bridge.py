#!/usr/bin/env python3
"""
HTTP to MQTT Bridge for Wokwi Integration
This bridge receives HTTP POST requests from Wokwi and forwards them to MQTT
Run this alongside your dashboard to enable Wokwi communication
"""

import json
import threading
import time
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuration
HTTP_PORT = 8051  # Port for HTTP server (different from dashboard)
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "wokwi/coalmine/sensors"

# Initialize Flask app
app = Flask(__name__)

# MQTT client
mqtt_client = None
mqtt_connected = False


def setup_mqtt():
    """Setup MQTT client for forwarding data"""
    global mqtt_client, mqtt_connected

    def on_connect(client, userdata, flags, rc):
        global mqtt_connected
        if rc == 0:
            mqtt_connected = True
            print(f"✅ Bridge connected to MQTT broker: {MQTT_BROKER}")
        else:
            mqtt_connected = False
            print(f"❌ Failed to connect to MQTT broker. Return code: {rc}")

    def on_disconnect(client, userdata, rc):
        global mqtt_connected
        mqtt_connected = False
        print(f"📡 Bridge disconnected from MQTT broker. Return code: {rc}")

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect

    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        return True
    except Exception as e:
        print(f"❌ Failed to setup MQTT client: {e}")
        return False


@app.route("/sensor_data", methods=["POST"])
def receive_sensor_data():
    """Receive sensor data from Wokwi via HTTP POST"""
    try:
        # Get JSON data from request
        sensor_data = request.get_json()

        if not sensor_data:
            return jsonify({"error": "No JSON data provided"}), 400

        print(f"📨 Received from Wokwi: {sensor_data}")

        # Add timestamp if not present
        if "timestamp" not in sensor_data:
            sensor_data["timestamp"] = datetime.now().isoformat()

        # Forward to MQTT if connected
        if mqtt_connected and mqtt_client:
            json_string = json.dumps(sensor_data)
            result = mqtt_client.publish(MQTT_TOPIC, json_string)

            if result.rc == 0:
                print(f"✅ Forwarded to MQTT: {sensor_data['helmet_id']}")
                return jsonify({"status": "success", "forwarded_to_mqtt": True}), 200
            else:
                print(f"❌ Failed to forward to MQTT")
                return jsonify({"status": "error", "mqtt_error": True}), 500
        else:
            print(f"⚠️ MQTT not connected, data received but not forwarded")
            return jsonify({"status": "received", "forwarded_to_mqtt": False}), 200

    except Exception as e:
        print(f"❌ Error processing sensor data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def get_status():
    """Get bridge status"""
    return jsonify(
        {
            "bridge_status": "running",
            "mqtt_connected": mqtt_connected,
            "mqtt_broker": MQTT_BROKER,
            "mqtt_topic": MQTT_TOPIC,
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/test", methods=["POST"])
def test_endpoint():
    """Test endpoint for debugging"""
    try:
        data = request.get_json() or {}
        print(f"🧪 Test data received: {data}")
        return jsonify({"message": "Test successful", "received_data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_flask_app():
    """Run Flask app in a separate thread"""
    print(f"🌐 Starting HTTP server on port {HTTP_PORT}")
    app.run(host="0.0.0.0", port=HTTP_PORT, debug=False, threaded=True)


def main():
    print("🌉 HTTP to MQTT Bridge for Wokwi Integration")
    print("=" * 60)
    print(f"📡 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"📋 MQTT Topic: {MQTT_TOPIC}")
    print(f"🌐 HTTP Server: http://localhost:{HTTP_PORT}")
    print("=" * 60)

    # Setup MQTT connection
    print("🔄 Connecting to MQTT broker...")
    if setup_mqtt():
        print("✅ MQTT setup complete")
    else:
        print("❌ MQTT setup failed, continuing with HTTP only")

    print("\n📡 Bridge Endpoints:")
    print(f"  POST http://localhost:{HTTP_PORT}/sensor_data - Send sensor data")
    print(f"  GET  http://localhost:{HTTP_PORT}/status - Check bridge status")
    print(f"  POST http://localhost:{HTTP_PORT}/test - Test endpoint")

    print("\n🚀 Bridge is running...")
    print("💡 Update your Wokwi code to send POST requests to:")
    print(f"   http://YOUR_COMPUTER_IP:{HTTP_PORT}/sensor_data")
    print("\nPress Ctrl+C to stop")

    try:
        # Start Flask in main thread
        run_flask_app()
    except KeyboardInterrupt:
        print("\n🛑 Stopping bridge...")
        if mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
        print("✅ Bridge stopped")


if __name__ == "__main__":
    main()
