import os
import sys
import time
import subprocess
import json

class SentinelPassiveSidecar:
    """
    Watches environment physics completely from the outside.
    Zero interference with ongoing 48-hour Python executions.
    """
    def __init__(self, log_file="sentinel_48hr_environmental_physics.json", interval_seconds=10):
        self.log_file = log_file
        self.interval = interval_seconds

    def grab_system_physics(self):
        metrics = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_load_percent": 0.0,
            "memory_available_mb": 0,
            "network_latency_ms": None,
            "network_health": "Nominal"
        }
        try:
            # 1. CPU Load Metrics (External polling)
            if sys.platform != "win32":
                load = os.getloadavg()[0] * 100 / (os.cpu_count() or 1)
                metrics["cpu_load_percent"] = round(load, 2)
            else:
                out = subprocess.check_output("wmic cpu get loadpercentage", shell=True)
                metrics["cpu_load_percent"] = float(out.decode().split()[1])
            
            # 2. Network Latency & Traffic Congestion
            ping_flag = "-c 1" if sys.platform != "win32" else "-n 1"
            start = time.time()
            res = subprocess.call(f"ping {ping_flag} 1.1.1.1", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if res == 0:
                metrics["network_latency_ms"] = round((time.time() - start) * 1000, 2)
                if metrics["network_latency_ms"] > 150:
                    metrics["network_health"] = "High Traffic / Network Jitter"
            else:
                metrics["network_health"] = "Packet Loss / Heavy Network Contention"

        except Exception as e:
            metrics["network_health"] = f"Telemetry hardware polling issue: {e}"
            
        return metrics

    def monitor_loop(self):
        print("🛡️ SENTINEL SIDECAR: Passive Environmental Monitor Activated.")
        print(f"Tracking system physics every {self.interval}s for the 48-hour run...")
        print("Safely decoupled from your running script. Press Ctrl+C to stop.")
        print("-" * 60)

        while True:
            metrics = self.grab_system_physics()
            
            # Print snapshot to console
            print(f"[{metrics['timestamp']}] CPU: {metrics['cpu_load_percent']}% | Net: {metrics['network_health']} ({metrics['network_latency_ms']}ms)")
            
            # Append to persistent local file immediately to protect against sudden power/heat loss
            with open(self.log_file, "a") as f:
                f.write(json.dumps(metrics) + "\n")
                
            time.sleep(self.interval)

if __name__ == "__main__":
    # Scrapes system metrics every 10 seconds without interfering with your 48-hour process
    sidecar = SentinelPassiveSidecar(interval_seconds=10)
    try:
        sidecar.monitor_loop()
    except KeyboardInterrupt:
        print("\n🛡️ Sentinel Sidecar stopped safely. Main process remains untouched.")
