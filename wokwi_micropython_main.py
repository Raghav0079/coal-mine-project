# main.py - MicroPython code for Wokwi Coal Mine Sensor Helmet
# Place this code in your Wokwi project's main.py file

import urequests
import network
import ujson
import time
import random
from machine import Pin, ADC
import dht

# WiFi Configuration (Wokwi default)
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# MQTT Configuration - Using HTTP webhook as MQTT alternative for Wokwi
# Since Wokwi Python doesn't support MQTT directly, we'll use HTTP POST
WEBHOOK_URL = "https://maker.ifttt.com/trigger/wokwi_sensor/with/key/YOUR_IFTTT_KEY"

# Alternative: Use a simple HTTP endpoint for testing
# You can set up a simple server or use RequestBin for testing
HTTP_ENDPOINT = "https://webhook.site/YOUR-UNIQUE-URL"

# Sensor Configuration
DHT_PIN = 15  # DHT22 connected to pin 15
CO2_PIN = 34  # Analog pin for CO2 sensor simulation
CH4_PIN = 35  # Analog pin for CH4 sensor simulation
H2S_PIN = 32  # Analog pin for H2S sensor simulation

# Sensor thresholds
CO2_THRESHOLD = 1000  # ppm
CO_THRESHOLD = 50  # ppm (using as CH4 for now)

# Initialize sensors
dht_sensor = dht.DHT22(Pin(DHT_PIN))
co2_adc = ADC(Pin(CO2_PIN))
ch4_adc = ADC(Pin(CH4_PIN))
h2s_adc = ADC(Pin(H2S_PIN))

# Set ADC attenuation for full range (0-3.3V)
co2_adc.atten(ADC.ATTN_11DB)
ch4_adc.atten(ADC.ATTN_11DB)
h2s_adc.atten(ADC.ATTN_11DB)

# Helmet identifier
HELMET_ID = "HELMET_001"


def connect_wifi():
    """Connect to WiFi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print(f"Connecting to WiFi: {WIFI_SSID}")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        # Wait for connection
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
            print(".", end="")

        if wlan.isconnected():
            print(f"\nWiFi connected! IP: {wlan.ifconfig()[0]}")
            return True
        else:
            print("\nFailed to connect to WiFi")
            return False

    return True


def read_dht22():
    """Read temperature and humidity from DHT22"""
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temp, humidity
    except Exception as e:
        print(f"DHT22 error: {e}")
        # Return simulated values if sensor fails
        return random.uniform(24, 35), random.uniform(60, 85)


def read_gas_sensors():
    """Read analog gas sensor values and convert to realistic readings"""

    # Read ADC values (0-4095 for 12-bit ADC)
    co2_raw = co2_adc.read()
    ch4_raw = ch4_adc.read()
    h2s_raw = h2s_adc.read()

    # Convert to sensor readings with some realism
    # CO2: 300-1200 ppm range
    co2_ppm = 300 + (co2_raw / 4095) * 900 + random.uniform(-20, 20)

    # CH4: 0-5% range
    ch4_percent = (ch4_raw / 4095) * 5 + random.uniform(-0.1, 0.1)

    # O2: Inverse relationship, 18-22% (lower ADC = higher O2)
    o2_percent = 22 - (co2_raw / 4095) * 4 + random.uniform(-0.2, 0.2)

    # H2S: 0-30 ppm range
    h2s_ppm = (h2s_raw / 4095) * 30 + random.uniform(-1, 1)

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
    temp, humidity = read_dht22()

    # Read gas sensors
    gas_data = read_gas_sensors()

    # Create complete data package
    sensor_data = {
        "helmet_id": HELMET_ID,
        "co2": gas_data["co2"],
        "ch4": gas_data["ch4"],
        "o2": gas_data["o2"],
        "h2s": gas_data["h2s"],
        "temp": round(temp, 1),
        "humidity": round(humidity, 1),
        "timestamp": time.time(),
    }

    return sensor_data


def send_data_http(data):
    """Send sensor data via HTTP POST (alternative to MQTT for Wokwi)"""
    try:
        # Convert data to JSON
        json_data = ujson.dumps(data)

        # Send HTTP POST (you'll need to set up an endpoint)
        # For testing, you can use webhook.site or RequestBin

        # Example using a webhook service
        headers = {"Content-Type": "application/json"}

        # Uncomment and modify URL for your endpoint
        # response = urequests.post(HTTP_ENDPOINT, data=json_data, headers=headers)
        # print(f"HTTP Response: {response.status_code}")
        # response.close()

        # For now, just print the data
        print("Sensor Data:", json_data)

        return True

    except Exception as e:
        print(f"HTTP send error: {e}")
        return False


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


def main():
    """Main execution function"""
    print("🏭 Coal Mine Safety Helmet - Wokwi Sensor")
    print("=" * 50)

    # Connect to WiFi
    if not connect_wifi():
        print("Cannot proceed without WiFi connection")
        return

    print(f"Helmet ID: {HELMET_ID}")
    print("Starting sensor monitoring...")
    print("Data will be displayed every 3 seconds")
    print("-" * 50)

    reading_count = 0

    while True:
        try:
            reading_count += 1

            # Read all sensors
            sensor_data = create_sensor_data()

            # Check for alerts
            alerts = check_alerts(sensor_data)

            # Display data
            print(f"\n📊 Reading #{reading_count} - {time.time()}")
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

            # Send data (currently just prints, modify for your endpoint)
            send_data_http(sensor_data)

            # Wait before next reading
            time.sleep(3)

        except KeyboardInterrupt:
            print("\n🛑 Stopping sensor monitoring...")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(1)


# Run the main function
if __name__ == "__main__":
    main()
