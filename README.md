# Week 2 Sensor Integration and Data Acquisition 

## Files
- `Week2_Sensor_Integration_Report.docx` - submission-ready report
- `sensor_simulation.py` - reproducible Python simulation
- `sensor_data.csv` - simulated acquisition dataset
- `sensor_messages.jsonl` - JSONL message stream
- `sensor_network_architecture.png` - architecture diagram
- `sensor_trends.png` - temperature/humidity plot
- `motion_events.png` - PIR event plot
- `simulation_output_log.png` - sample console output

## Run
```bash
python -m pip install numpy matplotlib
python sensor_simulation.py
```

The included simulation is deterministic for the generated submission dataset. For a real MQTT transport, install `paho-mqtt`, configure a broker, and replace the commented publish point with an MQTT client connection using TLS and credentials.
