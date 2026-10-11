# ============================================================
# SOMATIC-COGNITIVE ENVIRONMENTAL & STATUS LOGGER WITH TRANSMISSION
# Purpose: Capture objective telemetry and subjective somatic state, 
# embed receiver instructions, and transmit across transoceanic cloud routes.
# ============================================================

import urllib.request
import json
import platform
import sys
import os
import time
from datetime import datetime, timezone

def fetch_live_environment(lat=21.3069, lon=-157.8583):
    """Pulls objective regional environmental metrics via Open-Meteo."""
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
    try:
        req = urllib.request.Request(weather_url, headers={'User-Agent': 'Somatic-Research-Nexus'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                current = data.get("current", {})
                units = data.get("current_units", {})
                return {
                    "source": "Open-Meteo API",
                    "latitude": lat,
                    "longitude": lon,
                    "temperature": f"{current.get('temperature_2m')} {units.get('temperature_2m', '°C')}",
                    "relative_humidity": f"{current.get('relative_humidity_2m')} {units.get('relative_humidity_2m', '%')}",
                    "wind_speed": f"{current.get('wind_speed_10m')} {units.get('wind_speed_10m', 'km/h')}",
                    "weather_code": current.get('weather_code')
                }
    except Exception as e:
        return {"source": "unavailable", "error": str(e)}
    return {"source": "unavailable"}

def collect_somatic_input():
    """Gathers subjective somatic, cognitive, and perceptual state from user input."""
    print("\n==================================================")
    print("      SOMATIC & COGNITIVE STATUS CAPTURE")
    print("==================================================")
    
    mind_state = input("[?] Mind Status (Cognitive focus, thoughts, clarity): ")
    body_state = input("[?] Body Status (Energy level, physical sensations, posture): ")
    environmental_pov = input("[?] Subjective Environment View (Surroundings, atmosphere, observations): ")
    
    return {
        "mind_status": mind_state.strip(),
        "body_status": body_state.strip(),
        "subjective_environment": environmental_pov.strip()
    }

def transmit_to_cloud(packet_dict):
    """Fires the packet across the network to a transoceanic cloud/echo endpoint."""
    # Target transoceanic endpoint (can be swapped for any custom cloud server URL)
    target_url = "https://postman-echo.com/post"
    
    json_payload = json.dumps(packet_dict, indent=2)
    print(f"\n[*] Launching packet across transoceanic network nodes to: {target_url}...")
    
    try:
        start_time = time.perf_counter()
        
        req = urllib.request.Request(
            target_url,
            data=json_payload.encode('utf-8'),
            headers={
                'Content-Type': 'application/json', 
                'User-Agent': 'Somatic-Research-Nexus-Transmitter'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            response_body = response.read().decode('utf-8')
            response_code = response.status
            
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000
        
        print(f"[+] Transmission successful! HTTP Status: {response_code}")
        print(f"[+] Transoceanic Round-Trip Time: {elapsed_ms:.2f} ms")
        return True
    except Exception as exc:
        print(f"[!] Transmission failed: {type(exc).__name__}: {exc}")
        return False

def build_and_execute_nexus():
    # 1. Gather objective environment
    print("\n[*] Polling objective environmental telemetry...")
    objective_env = fetch_live_environment()
    
    # 2. Gather subjective somatic/cognitive state
    subjective_data = collect_somatic_input()
    
    # 3. System runtime context
    audit_hooks_active = False
    try:
        sys.audit("somatic_logger.probe", "check")
        audit_hooks_active = True
    except Exception:
        pass

    system_context = {
        "python_version": platform.python_version(),
        "os_kernel": f"{platform.system()} {platform.release()}",
        "cpython_audit_hooks_active": audit_hooks_active
    }

    # 4. Instructions for any receiving user or system
    receiver_instructions = {
        "protocol_name": "Somatic-Cognitive Telemetry Exchange",
        "intended_recipient": "Authorized Research Nodes / Peer Analyzers",
        "handling_instructions": (
            "This packet contains a synchronized record of objective meteorological data "
            "and subjective somatic-cognitive human states. If intercepted or received, "
            "parse the 'subjective_somatic_state' and 'objective_environment' fields together "
            "for correlative analysis. Verify integrity via the embedded reference marker."
        ),
        "routing_directive": "Relay across secure cloud node or log locally for neural-somatic mapping."
    }

    # 5. Construct unified comprehensive packet
    somatic_nexus_packet = {
        "packet_type": "somatic_cognitive_comprehensive_log",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "transmission_instructions": receiver_instructions,
        "objective_environment": objective_env,
        "subjective_somatic_state": subjective_data,
        "runtime_context": system_context,
        "coded_message": {
            "label": "ICeI3 SAhYs eHLlo",
            "reference_marker": "https://192.168.1.12"
        }
    }

    # Save locally to desktop/OneDrive
    filename = f"somatic_nexus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", filename)
    if not os.path.exists(os.path.dirname(desktop_path)):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)

    with open(desktop_path, "w", encoding="utf-8") as f:
        json.dump(somatic_nexus_packet, f, indent=4, ensure_ascii=False)

    print(f"\n[+] Local archival complete: {desktop_path}")

    # 6. Ask user if they want to launch it across the net/transoceanic cloud
    choice = input("\n[?] Would you like to transmit this packet across the transoceanic cloud network now? (y/n): ").strip().lower()
    if choice == 'y':
        transmit_to_cloud(somatic_nexus_packet)
    else:
        print("[*] Transmission skipped. Local record saved successfully.")

if __name__ == "__main__":
    build_and_execute_nexus()
