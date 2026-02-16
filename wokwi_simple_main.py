# Simplified Wokwi Sensor Code (for web-based Wokwi environment)
# Copy this code to your Wokwi main.py file
# Note: This uses simulated HTTP requests since full networking isn't available in web Wokwi

import random
import time
import json

# Sensor thresholds
CO2_THRESHOLD = 1000  # ppm
CO_THRESHOLD = 50  # ppm (using as CH4 equivalent)

# Helmet configuration
HELMET_ID = "HELMET_001"

# Simulated sensor pins (for display purposes)
DHT_PIN = 15
CO2_PIN = 34
CH4_PIN = 35
H2S_PIN = 32

print("🏭 Coal Mine Safety Helmet - Wokwi Sensor Simulator")
print("=" * 50)
print(f"Helmet ID: {HELMET_ID}")
print("Starting sensor monitoring...")
print("\n💡 In real Wokwi with networking, data would be sent to:")
print("   http://YOUR_COMPUTER_IP:8051/sensor_data")
print("-" * 50)


def read_dht22_simulated():
    """Simulate DHT22 temperature and humidity readings"""
    # Simulate realistic coal mine conditions
    temp = random.uniform(24, 35) + random.gauss(0, 2)  # 24-35°C with variation
    humidity = random.uniform(60, 85) + random.gauss(0, 5)  # 60-85% with variation

    # Keep within realistic bounds
    temp = max(15, min(45, temp))
    humidity = max(30, min(95, humidity))

    return round(temp, 1), round(humidity, 1)


def read_gas_sensors_simulated():
    """Simulate gas sensor readings"""

    # CO2: Simulate varying levels with occasional spikes
    co2_base = random.uniform(350, 600)
    if random.random() < 0.1:  # 10% chance of spike
        co2_base += random.uniform(200, 500)
    co2_ppm = co2_base + random.gauss(0, 20)

    # CH4: Usually low in coal mines, occasional detection
    ch4_base = random.uniform(0.3, 1.2)
    if random.random() < 0.05:  # 5% chance of higher reading
        ch4_base += random.uniform(0.5, 1.5)
    ch4_percent = ch4_base + random.gauss(0, 0.1)

    # O2: Should be around 20.9%, lower values are dangerous
    o2_base = random.uniform(19.5, 20.9)
    o2_percent = o2_base + random.gauss(0, 0.2)

    # H2S: Toxic gas, usually very low
    h2s_base = random.uniform(0, 8)
    if random.random() < 0.08:  # 8% chance of detection
        h2s_base += random.uniform(5, 15)
    h2s_ppm = h2s_base + random.gauss(0, 1)

    # Ensure realistic bounds
    co2_ppm = max(200, min(2000, co2_ppm))
    ch4_percent = max(0, min(5, ch4_percent))
    o2_percent = max(16, min(23, o2_percent))
    h2s_ppm = max(0, min(50, h2s_ppm))

    return {
        "co2": round(co2_ppm, 1),
        "ch4": round(ch4_percent, 2),
        "o2": round(o2_percent, 1),
        "h2s": round(h2s_ppm, 1),
    }


def create_sensor_data():
    """Create complete sensor data package"""

    # Read environmental sensors
    temp, humidity = read_dht22_simulated()

    # Read gas sensors
    gas_data = read_gas_sensors_simulated()

    # Create complete data package
    sensor_data = {
        "helmet_id": HELMET_ID,
        "co2": gas_data["co2"],
        "ch4": gas_data["ch4"],
        "o2": gas_data["o2"],
        "h2s": gas_data["h2s"],
        "temp": temp,
        "humidity": humidity,
        "timestamp": time.time(),
    }

    return sensor_data


def check_alerts(data):
    """Check for alert conditions"""
    alerts = []

    if data["co2"] > CO2_THRESHOLD:
        alerts.append(f"CO2 ALERT: {data['co2']} ppm")

    if data["ch4"] > 2.0:  # 2% methane threshold
        alerts.append(f"METHANE ALERT: {data['ch4']}%")

    if data["o2"] < 19.5:  # Low oxygen threshold
        alerts.append(f"LOW OXYGEN: {data['o2']}%")

    if data["h2s"] > 15:  # H2S threshold
        alerts.append(f"H2S ALERT: {data['h2s']} ppm")

    if data["temp"] > 35:  # High temperature
        alerts.append(f"HIGH TEMP: {data['temp']}°C")

    return alerts


def send_data_simulation(data):
    """Simulate sending data (in real Wokwi, this would be HTTP POST)"""
    json_data = json.dumps(data, indent=2)

    print(f"\n📤 Simulated HTTP POST to bridge:")
    print(f"URL: http://YOUR_COMPUTER_IP:8051/sensor_data")
    print(f"Data: {json_data}")

    # In real Wokwi with network access, you would use:
    # import urequests
    # response = urequests.post("http://YOUR_COMPUTER_IP:8051/sensor_data",
    #                          json=data,
    #                          headers={'Content-Type': 'application/json'})


# Main execution loop
reading_count = 0

while True:
    try:
        reading_count += 1

        # Read all sensors
        sensor_data = create_sensor_data()

        # Check for alerts
        alerts = check_alerts(sensor_data)

        # Display data
        print(f"\n📊 Reading #{reading_count} - Helmet: {HELMET_ID}")
        print(f"🌡️  Temperature: {sensor_data['temp']}°C")
        print(f"💧 Humidity: {sensor_data['humidity']}%")
        print(f"💨 CO2: {sensor_data['co2']} ppm")
        print(f"🔥 CH4: {sensor_data['ch4']}%")
        print(f"💨 O2: {sensor_data['o2']}%")
        print(f"☠️  H2S: {sensor_data['h2s']} ppm")

        # Show alerts if any
        if alerts:
            print("🚨 ALERTS:")
            for alert in alerts:
                print(f"   ⚠️  {alert}")
        else:
            print("✅ All readings within safe limits")

        # Simulate sending data
        send_data_simulation(sensor_data)

        # Wait before next reading
        time.sleep(3)

    except KeyboardInterrupt:
        print("\n🛑 Stopping sensor monitoring...")
        break
    except Exception as e:
        print(f"❌ Error in main loop: {e}")
        time.sleep(1)
