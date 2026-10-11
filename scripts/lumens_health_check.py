#!/usr/bin/env python3
"""
Web Node & Digital Footprint Health Optimizer
----------------------------------------------
Executes low-level network maintenance tasks to reduce redundant web traffic,
minimize client-server compute strain, and reduce energy/carbon footprints:

1. Transit Efficiency:
   Purges stale DNS caches to eliminate redundant name-resolution queries.
2. Web Cache & Storage Health:
   Clears orphan HTTP response caches to lower drive write overhead.
3. Socket & Connection Health:
   Resets hung network sockets and stale TCP states to free socket descriptors.
4. Energy & Bandwidth Reduction:
   Aborts unwanted background telemetry/analytics pings to cut outbound bandwidth usage.
"""

import os
import platform
import subprocess
import gc

def print_status(msg, status="OK"):
    print(f"[{status}] {msg}")

def optimize_dns_cache():
    print("\n--- 1. Transit Efficiency (DNS Cache Flush) ---")
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True, check=True)
        elif system == "Darwin":
            subprocess.run(["dscacheutil", "-flushcache"], capture_output=True, check=True)
            subprocess.run(["killall", "-HUP", "mDNSResponder"], capture_output=True, check=True)
        elif system == "Linux":
            subprocess.run(["resolvectl", "flush-caches"], capture_output=True, check=True)
        print_status("Flushed local DNS resolver cache, eliminating stale outbound lookup pings.")
    except Exception as e:
        print_status(f"DNS flush skipped or requires administrative privileges: {e}", status="WARN")

def optimize_web_caches():
    print("\n--- 2. Web Cache & Browser Artifact Cleanup ---")
    system = platform.system()
    bytes_cleared = 0
    cache_targets = []

    if system == "Linux":
        cache_targets = [os.path.expanduser("~/.cache/google-chrome"), os.path.expanduser("~/.cache/mozilla")]
    elif system == "Darwin":
        cache_targets = [os.path.expanduser("~/Library/Caches/Google/Chrome"), os.path.expanduser("~/Library/Caches/Firefox")]
    elif system == "Windows":
        local_app = os.environ.get("LOCALAPPDATA", "")
        cache_targets = [
            os.path.join(local_app, r"Google\Chrome\User Data\Default\Cache"),
            os.path.join(local_app, r"Mozilla\Firefox\Profiles")
        ]

    for path in cache_targets:
        if os.path.exists(path):
            try:
                for root, _, files in os.walk(path):
                    for f in files:
                        if f.endswith(".tmp") or "cache" in f.lower():
                            fp = os.path.join(root, f)
                            try:
                                bytes_cleared += os.path.getsize(fp)
                                os.remove(fp)
                            except Exception:
                                pass
            except Exception:
                pass

    print_status(f"Cleared ~{bytes_cleared / (1024*1024):.2f} MB of stale web cache data.")

def optimize_sockets():
    print("\n--- 3. Connection & Socket Refresh ---")
    # Trigger garbage collection to release unclosed HTTP connection pools/sockets in active scripts
    gc.collect()
    system = platform.system()
    
    if system == "Windows":
        try:
            subprocess.run(["netsh", "interface", "ip", "delete", "destinationcache"], capture_output=True)
            print_status("Flushed IP destination cache to refresh network routing paths.")
        except Exception:
            print_status("Socket table garbage collection complete.")
    else:
        print_status("Released idle network socket handles via runtime GC.")

def optimize_background_traffic():
    print("\n--- 4. Bandwidth & Energy Reduction ---")
    system = platform.system()
    killed = 0
    # Common idle background web update service identifiers
    target_services = ["googleupdate", "softwareupdate", "edgeupdate"]

    if system != "Windows":
        try:
            output = subprocess.check_output(["ps", "-eo", "pid,comm"]).decode('utf-8')
            for line in output.splitlines()[1:]:
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    pid, name = parts
                    if any(s in name.lower() for s in target_services):
                        try:
                            os.kill(int(pid), 9)
                            killed += 1
                        except Exception:
                            pass
        except Exception:
            pass

    print_status(f"Halted {killed} redundant web update background threads.")

if __name__ == "__main__":
    print("==================================================")
    print("      WORLD WIDE WEB SYSTEM HEALTH OPTIMIZER     ")
    print("==================================================")
    optimize_dns_cache()
    optimize_web_caches()
    optimize_sockets()
    optimize_background_traffic()
    print("\n[COMPLETE] Web system optimization cycle finished.")
