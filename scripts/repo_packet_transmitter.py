# ============================================================
# REPOSITORY DATA PACKET TRANSMITTER
# Purpose: Fetch repository telemetry for KAnoOoKAh,
# structure it into a JSON packet, and transmit it.
# ============================================================

import urllib.request
import json
import time
from datetime import datetime, timezone

def measure_and_echo_trip(username="KAnoOoKAh"):
    api_url = f"https://api.github.com/users/{username}/repos"
    
    print(f"[*] Querying GitHub API for repository owner: {username}...")
    
    try:
        # Fetch your public repository data from GitHub
        req = urllib.request.Request(
            api_url, 
            headers={'User-Agent': 'Global-Packet-Agent'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                raw_data = json.loads(response.read().decode('utf-8'))
                
                # Pack your rich repository information into the packet
                repos_summary = [{
                    "name": repo.get("name"),
                    "visibility": repo.get("visibility"),
                    "html_url": repo.get("html_url"),
                    "updated_at": repo.get("updated_at")
                } for repo in raw_data]
                
                data_packet = {
                    "packet_type": "global_round_trip_telemetry",
                    "owner": username,
                    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                    "total_public_repositories": len(repos_summary),
                    "repositories": repos_summary
                }
                
                json_packet_string = json.dumps(data_packet, indent=2)
                
                print(f"[*] Packet packed with {len(repos_summary)} repositories. Firing across the planet...")
                
                # --- START GLOBAL STOPWATCH ---
                start_time = time.perf_counter()
                
                target_url = "https://httpbin.org/post"
                target_req = urllib.request.Request(
                    target_url,
                    data=json_packet_string.encode('utf-8'),
                    headers={'Content-Type': 'application/json', 'User-Agent': 'Global-Packet-Agent'},
                    method='POST'
                )
                
                # Send the packet out and wait for the response to fly back
                with urllib.request.urlopen(target_req, timeout=10) as target_response:
                    response_body = target_response.read().decode('utf-8')
                    response_code = target_response.status
                    
                # --- STOP GLOBAL STOPWATCH ---
                end_time = time.perf_counter()
                
                # Calculate elapsed time in milliseconds
                elapsed_ms = (end_time - start_time) * 1000
                
                # Parse the server's echo response to confirm your repo data made the trip
                response_json = json.loads(response_body)
                echoed_data = response_json.get("json", {})
                
                print(f"\n[+] Landing successful! HTTP Status: {response_code}")
                print(f"🌍 Total Round-Trip Time across the network: {elapsed_ms:.2f} milliseconds!")
                print(f"[+] Verified: Your repository data made the round trip and came back!")
                print(f"    - Owner: {echoed_data.get('owner')}")
                print(f"    - Repositories Transmitted: {echoed_data.get('total_public_repositories')}")
                
            else:
                print(f"[!] GitHub status error: {response.status}")
                
    except Exception as exc:
        print(f"[!] Transmission lost in space: {type(exc).__name__}: {exc}")

if __name__ == "__main__":
    measure_and_echo_trip("KAnoOoKAh")
