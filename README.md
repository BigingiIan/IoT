# IoT Projects Collection

Personal repo for all my ESP32 / MicroPython / Arduino IoT experiments. Each subfolder is a standalone project with its own wiring, code, and docs.

# Repo Structure
iot-projects/
├── esp32-dht22-mqtt/          # Temperature + humidity to MQTT
├── esp32-plant-monitor/       # Soil moisture + auto-watering
├── esp32-rgb-matrix/          # MQTT-controlled LED matrix
├── wokwi-sims/                # Quick Wokwi test circuits
└── http://README.md                  # You are here

## Projects

### 1. ESP32 DHT22 + MQTT `esp32-dht22-mqtt/`
MicroPython sensor node that publishes temp/humidity to MQTT. Tested in Wokwi.

**Stack**: ESP32, MicroPython, DHT22, MQTT  
**Key notes**: Use GPIO 4, not ADC2 pins like 27, when WiFi is active on real hardware. Wokwi doesn't enforce this.  
**Dashboard**: MQTTX, Freeboard.io, Home Assistant  
**Status**: Working in simulation

### 2. More projects coming soon...
Add a new folder per project. Keep a `README.md` inside each with wiring, setup, and quirks.

### Hardware I Use

| Board | Use Case | Notes |
| --- | --- | --- |
| ESP32 DevKitC V4 | WiFi + sensors | ADC2 pins conflict with WiFi |
| ESP8266 NodeMCU | Simple MQTT nodes | Less RAM, no BLE |
| Arduino Nano | Non-WiFi projects | Use with ESP-01 for WiFi |

### Common Tools

1. **Simulation**: [Wokwi](https://wokwi.com) - use `Wokwi-GUEST` WiFi for MQTT
2. **MQTT Brokers**: `test.mosquitto.org`, `broker.hivemq.com`, local Mosquitto
3. **Dashboards**: MQTTX, Node-RED, Home Assistant, Freeboard.io
4. **IDE**: Thonny for MicroPython, Arduino IDE for C++

### General ESP32 Gotchas

1. **ADC2 vs WiFi**: GPIO 0, 2, 12-15, 25-27 fail with `analogRead`/`dht.read()` when WiFi is on. Use ADC1: GPIO 32-39, 4, 5, etc.
2. **Power**: DHT22 needs 3.3V. Some modules have onboard regulators and work with 5V.
3. **Public MQTT**: Don't send sensitive data to public brokers. Use unique topics to avoid collisions.
4. **Wokwi specifics**: Internal pull-ups exist on virtual components. `machine.unique_id()` is random per simulation.

## Contributing / Notes to Self

1. One folder = one project. Each gets own `main.py`, `diagram.json`, `README.md`
2. Put pin diagrams/schematics as `.png` in each project folder
3. Tag commits with `wokwi-tested` or `hardware-tested`
4. For real deployments, replace public brokers with local Mosquitto + auth


---
Last updated: 2026-06-23
