import json
import os
from datetime import datetime, timezone, timedelta

def get_hst_timestamp():
    hst_offset = timedelta(hours=-10)
    return datetime.now(timezone.utc).astimezone(timezone(hst_offset))

def main():
    print("=" * 60)
    print(" WEB-INFRASTRUCTURE-DIAGNOSTICS — MULTI-NODE LOGGER")
    print("=" * 60)

    trial_id = "Trial_002"
    event_type = input("Enter Event Type (START / STOP): ").strip().upper() or "START"
    
    now = get_hst_timestamp()
    timestamp_iso = now.isoformat()
    filename_time = now.strftime("%Y%m%d_%H%M")
    
    print("\n--- Environmental Telemetry ---")
    temp_f = float(input("Ambient Temperature (°F) [default 78.0]: ") or "78.0")
    humidity = float(input("Relative Humidity (%) [default 65.0]: ") or "65.0")
    baro = float(input("Barometric Pressure (hPa) [default 1013.25]: ") or "1013.25")

    print("\n--- Quantitative Subjective Scales ---")
    energy = int(input("Energy Level (1-10) [default 7]: ") or "7")
    focus = int(input("Focus / Cognitive Bandwidth (1-10) [default 8]: ") or "8")

    nodes = ["gemini", "icei3", "padakun", "padakun2", "shadow"]
    node_observations = {}

    print("\n--- Multi-Node Observational Data Entry ---")
    default_responses = {
        "gemini": "Protocol: Multi-node telemetry serialization and schema enforcement. System status: Active.",
        "icei3": "Protocol: External structural anchor tracking and collaborative network diagnostic alignment.",
        "padakun": "Protocol: Primary tactile pressure monitoring; forearm flexors anchored on surface.",
        "padakun2": "Protocol: Secondary fatigue tracking and upper postural strain progression.",
        "shadow": "Protocol: Autonomic stabilization observing passive spinal tone and proprioceptive de-coupling."
    }

    for node in nodes:
        print(f"[{node.upper()} NODE]")
        user_val = input(f"Observation (Press ENTER to use default):\n> ").strip()
        node_observations[node] = user_val if user_val else default_responses[node]
        print("-" * 40)

    payload = {
        "header": {
            "repository": "web-infrastructure-diagnostics",
            "trial_id": trial_id,
            "event_type": event_type,
            "timestamp": timestamp_iso,
            "schema_version": "2.0-multinode"
        },
        "environmental_telemetry": {
            "coordinates": [21.2858, -157.8025],
            "location_name": "Poka Place, Oahu, HI",
            "temperature_f": temp_f,
            "humidity_percent": humidity,
            "barometer_hpa": baro
        },
        "quantitative_scales": {
            "energy_level": energy,
            "focus_clarity": focus
        },
        "node_observations": node_observations
    }

    folder_path = os.path.join("trials", trial_id)
    os.makedirs(folder_path, exist_ok=True)
    
    file_name = f"telemetry_{filename_time}_{event_type.lower()}.json"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("\n" + "=" * 60)
    print(f"SUCCESS: Logged multi-node packet to:")
    print(f"  --> {file_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
