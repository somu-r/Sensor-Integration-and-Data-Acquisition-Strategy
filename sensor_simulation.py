"""
Week 2 - Sensor Integration and Data Acquisition Simulation
Requires: Python 3, numpy, matplotlib
Optional real MQTT transport: paho-mqtt + a local/public MQTT broker.

This simulation models:
- DS18B20 temperature sensor
- DHT22 humidity sensor
- PIR motion sensor
- Edge validation and threshold processing
- MQTT-style JSON messages
- Local CSV/JSONL persistence
"""

import json
import random
import time
from datetime import datetime, timezone

import numpy as np

random.seed(42)
np.random.seed(42)

SAMPLE_INTERVAL_SEC = 1
DEVICE_ID = "iot-node-01"
MQTT_TOPIC = "lab/iot-node-01/telemetry"

def read_temperature(i):
    return 24.0 + 1.2*np.sin(i/8.0) + np.random.normal(0, 0.18)

def read_humidity(i):
    return 62.0 - 4.0*np.sin(i/8.0) + np.random.normal(0, 0.8)

def read_motion(i):
    # Simulated PIR digital output
    forced_events = {4, 11, 12, 21, 26}
    return 1 if i in forced_events or random.random() < 0.08 else 0

def validate(t, h, m):
    return -40 <= t <= 85 and 0 <= h <= 100 and m in (0, 1)

def process(t, h, m):
    alerts = []
    if t > 25.5:
        alerts.append("HIGH_TEMPERATURE")
    if h < 55:
        alerts.append("LOW_HUMIDITY")
    if m == 1:
        alerts.append("MOTION_DETECTED")
    return alerts

records = []

for i in range(30):
    t = round(float(read_temperature(i)), 2)
    h = round(float(read_humidity(i)), 2)
    m = read_motion(i)

    if not validate(t, h, m):
        print("Rejected invalid sensor sample")
        continue

    message = {
        "device_id": DEVICE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature_c": t,
        "humidity_pct": h,
        "motion": m,
        "alerts": process(t, h, m),
    }

    # MQTT publish point:
    # mqtt_client.publish(MQTT_TOPIC, json.dumps(message), qos=1)
    print(
        f'{message["timestamp"]} | T={t:5.2f} C | '
        f'RH={h:5.2f}% | motion={m} | alerts={message["alerts"]}'
    )
    records.append(message)
    time.sleep(SAMPLE_INTERVAL_SEC)

with open("sensor_messages.jsonl", "w", encoding="utf-8") as f:
    for message in records:
        f.write(json.dumps(message) + "\n")
