# ============================================================
# TRANSOCEANIC REPOSITORY & CODED MESSAGE TRANSMITTER
# Purpose: Package repository data, deep telemetry, and coded 
# messages, then fire them across international borders and back.
# ============================================================

import urllib.request
import json
import time
import platform
import sys
import os
from datetime import datetime, timezone

def measure_transoceanic_trip(username="KAnoOoKAh"):
    # Using an international echo/testing node endpoint
    target_url = "https://postman-echo.com/post"
    api_url = f"https://api.github.com/users/{username}/repos"
    
    print(f"[*] Querying GitHub API for repository owner: {username}...")
    
    # Coded message payload containing your secure marker
    coded_message_payload = {
        "label": "ICeI3 SAhYs eHLlo",
        "reference_marker": "htps:/192.168.1.12",
        "transmission_intent": "transoceanic_decodable_signal",
        "status": "intact"
    }

    deep_runtime_payload = {
        "python_version": platform.python_version(),
        "os_kernel": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine(),
        "routing_path": "Transoceanic-International-Test-Node"
    }

    try:
        req = urllib.request.Request(
            api_url, 
            headers={'User-Agent': 'Global-Packet-Agent'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                raw_data = json.loads(response.read().decode('utf-8'))
                
                repos_summary = [{
                    "name": repo.get("name"),
                    "visibility": repo.get("visibility"),
                    "html_url": repo.get("html_url"),
                    "updated_at": repo.get("updated_at")
                } for repo in raw_data]
                
                # Comprehensive international packet
                data_packet = {
                    "packet_type": "transoceanic_round_trip_nexus",
                    "owner": username,
                    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                    "total_public_repositories": len(repos_summary),
                    "repositories": repos_summary,
                    "deep_runtime_telemetry": deep_runtime_payload,
                    "coded_message": coded_message_payload
                }
                
                json_packet_string = json.dumps(data_packet, indent=2)
                
                print(f"[*] Packet packed with coded message ['ICeI3 SAhYs eHLlo']. Launching across international network nodes...")
                
                # --- START TRANSOCEANIC STOPWATCH ---
                start_time = time.perf_counter()
                
                target_req = urllib.request.Request(
                    target_url,
                    data=json_packet_string.encode('utf-8'),
                    headers={'Content-Type': 'application/json', 'User-Agent': 'Global-Packet-Agent'},
                    method='POST'
                )
                
                with urllib.request.urlopen(target_req, timeout=15) as target_response:
                    response_body = target_response.read().decode('utf-8')
                    response_code = target_response.status
                    
                # --- STOP TRANSOCEANIC STOPWATCH ---
                end_time = time.perf_counter()
                elapsed_ms = (end_time - start_time) * 1000
                
                response_json = json.loads(response_body)
                echoed_data = response_json.get("data", {})
                if isinstance(echoed_data, str):
                    echoed_data = json.loads(echoed_data)
                    
                echoed_msg = echoed_data.get("coded_message", {})
                
                print(f"\n[+] Transoceanic landing successful! HTTP Status: {response_code}")
                print(f" Total International Round-Trip Time: {elapsed_ms:.2f} ms")
                print(f"[+] Verified: Packet made the international trip and returned!")
                print(f"    - Target Endpoint: {target_url}")
                print(f"    - Intercepted Message Label: {echoed_msg.get('label')}")
                print(f"    - Intercepted Reference Marker: {echoed_msg.get('reference_marker')}")
                
            else:
                print(f"[!] GitHub status error: {response.status}")
                
    except Exception as exc:
        print(f"[!] Transoceanic transmission error: {type(exc).__name__}: {exc}")

if __name__ == "__main__":
    measure_transoceanic_trip("KAnoOoKAh")
