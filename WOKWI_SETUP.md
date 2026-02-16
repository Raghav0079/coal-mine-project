# Coal Mine Safety Dashboard - Wokwi Integration

This dashboard now supports real-time data from your Wokwi simulator via MQTT, with automatic fallback to simulation when no real data is available.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install paho-mqtt
   ```

2. **Run the Dashboard**
   ```bash
   python app.py
   ```

3. **Test with Simulation** (Optional)
   ```bash
   python test_mqtt.py
   ```

## 📡 MQTT Configuration

### Default Settings
- **Broker**: `broker.hivemq.com` (free public broker)
- **Port**: `1883`
- **Topic**: `wokwi/coalmine/sensors`

### Customize Settings
Edit `wokwi_config.py` to change MQTT settings:
```python
MQTT_BROKER = "your-mqtt-broker.com"
MQTT_PORT = 1883
MQTT_TOPIC = "your/custom/topic"
MQTT_USERNAME = "your_username"  # if needed
MQTT_PASSWORD = "your_password"  # if needed
```

## 🔧 Wokwi Simulator Setup

### 1. Create Your Wokwi Project
1. Go to [wokwi.com](https://wokwi.com)
2. Create a new ESP32 project
3. Add sensors to your circuit:
   - CO2 sensor (or potentiometer as analog input)
   - CH4 sensor (or potentiometer as analog input)
   - O2 sensor (or potentiometer as analog input)
   - H2S sensor (or potentiometer as analog input)
   - Temperature sensor (or potentiometer as analog input)
   - Humidity sensor (or potentiometer as analog input)

### 2. Use the Provided Arduino Code
Copy the code from `wokwi_sensor_code.ino` into your Wokwi project.

### 3. Add Required Libraries
In Wokwi, add these libraries to your `libraries.txt`:
```
PubSubClient
ArduinoJson
```

### 4. Circuit Connections
Connect your sensors to analog pins A0-A5:
- A0: CO2 sensor
- A1: CH4 sensor (Methane)
- A2: O2 sensor (Oxygen)
- A3: H2S sensor (Hydrogen Sulfide)
- A4: Temperature sensor
- A5: Humidity sensor

## 📊 JSON Data Format

Your Wokwi simulator should send data in this JSON format:

```json
{
  "helmet_id": "HELMET_001",
  "co2": 450.5,
  "ch4": 1.2,
  "o2": 20.5,
  "h2s": 5.0,
  "temp": 28.5,
  "humidity": 72.3,
  "timestamp": "2026-02-16T10:30:00"
}
```

### Supported Helmet IDs
- HELMET_001 through HELMET_008
- You can modify the helmet mapping in `wokwi_config.py`

## 🧪 Testing Your Setup

### Option 1: Test Script
Run the test script to simulate MQTT messages:
```bash
python test_mqtt.py
```

### Option 2: Manual Testing
Use any MQTT client to send test messages to verify connectivity:
```bash
# Example using mosquitto_pub
mosquitto_pub -h broker.hivemq.com -t wokwi/coalmine/sensors -m '{"helmet_id":"HELMET_001","co2":450,"ch4":1.2,"o2":20.5,"h2s":5,"temp":28.5,"humidity":72.3}'
```

## 🚨 Dashboard Features

### Real-time Status
- **Green**: Receiving live data from Wokwi
- **Yellow**: MQTT connected but no recent data
- **Red**: MQTT disconnected

### Data Sources
1. **Primary**: Live data from Wokwi simulator (when available)
2. **Fallback**: Realistic simulation (when Wokwi data unavailable)

### Sensor Thresholds
- **CO2**: Safe <500ppm, Warning <800ppm, Danger <1200ppm
- **CH4**: Safe <1%, Warning <1.5%, Danger <2%
- **O2**: Safe >19.5%, Warning >19%, Danger >18.5%
- **H2S**: Safe <10ppm, Warning <15ppm, Danger <20ppm
- **Temperature**: Safe <30°C, Warning <35°C, Danger <40°C
- **Humidity**: Safe <80%, Warning <90%, Danger <95%

## 🔧 Troubleshooting

### Common Issues

1. **MQTT Connection Failed**
   - Check internet connection
   - Verify broker address in config
   - Try alternative broker: `mqtt.eclipseprojects.io`

2. **No Data Received**
   - Verify Wokwi simulator is running
   - Check MQTT topic matches between Wokwi and dashboard
   - Use test script to verify dashboard receives data

3. **Authentication Required**
   - Set username/password in `wokwi_config.py`
   - Some brokers require account creation

### Alternative MQTT Brokers
```python
# Free public brokers you can try
MQTT_BROKER = "broker.hivemq.com"           # HiveMQ
MQTT_BROKER = "mqtt.eclipseprojects.io"     # Eclipse
MQTT_BROKER = "test.mosquitto.org"          # Mosquitto
```

## 📱 Mobile Access

The dashboard is responsive and works on mobile devices. Access it from any device on your network using your computer's IP address:
```
http://YOUR_IP_ADDRESS:8050
```

## 🔒 Security Notes

- The default setup uses public MQTT brokers (not secure)
- For production, use private MQTT brokers with authentication
- Consider using MQTT over TLS (port 8883) for encrypted communication

## 📈 Data Retention

- Dashboard stores last 100 readings per helmet in memory
- Data is lost when dashboard restarts
- For persistent storage, consider integrating a database

## 🛠️ Advanced Configuration

### Custom Sensor Mapping
Edit the `HELMET_MAPPING` in `wokwi_config.py` to map custom Wokwi sensor IDs to dashboard helmet IDs.

### Multiple Wokwi Simulators
You can run multiple Wokwi simulators with different helmet IDs to simulate an entire mining operation.

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify MQTT connectivity with test script
3. Ensure JSON format matches expected structure
4. Test with simulation mode first

## 🎯 Next Steps

1. Enhance your Wokwi circuit with actual sensor modules
2. Add GPS tracking for helmet location
3. Implement two-way communication (dashboard to helmet)
4. Add data logging and historical analysis
5. Integrate with mining safety protocols
