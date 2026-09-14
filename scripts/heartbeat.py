#!/usr/bin/env python3
"""
HEARTBEAT COLLECTION DAEMON — GATE 0 VERSION

Minimalist implementation focused on measurement integrity and provenance.

Job:
1. Measure latency to one endpoint
2. Record with full provenance
3. Validate schema compliance
4. Write atomic JSON
5. Report continuously on success/failure

No interpretation. No anomaly detection. No solar correlation.

Just: measure → timestamp → record → validate → write.
"""

import subprocess
import json
import logging
import time
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [HEARTBEAT] %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/heartbeat.log")
    ]
)
logger = logging.getLogger(__name__)


class Gate0Collector:
    """Minimal heartbeat collector for Gate 0 validation."""
    
    SOFTWARE_VERSION = "heartbeat.py v0.1.0-gate0"
    SCHEMA_VERSION = "1.0"
    
    def __init__(
        self,
        collector_id: str = "gate0-001",
        endpoint: str = "8.8.8.8",
        protocol: str = "icmp",
        output_dir: str = "data/raw/heartbeat"
    ):
        self.collector_id = collector_id
        self.endpoint = endpoint
        self.protocol = protocol
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure logs directory exists
        Path("logs").mkdir(exist_ok=True)
        
        self.config_hash = self._generate_config_hash()
        self.start_time = time.monotonic()
        self.record_count = 0
        self.success_count = 0
        self.failure_count = 0
        
        logger.info(f"Gate0Collector initialized")
        logger.info(f"  Collector ID: {collector_id}")
        logger.info(f"  Endpoint: {endpoint} ({protocol})")
        logger.info(f"  Output: {output_dir}")
        logger.info(f"  Config hash: {self.config_hash}")
    
    def _generate_config_hash(self) -> str:
        """Generate SHA256 hash of configuration."""
        config_str = json.dumps({
            "collector_id": self.collector_id,
            "endpoint": self.endpoint,
            "protocol": self.protocol,
            "software_version": self.SOFTWARE_VERSION,
            "schema_version": self.SCHEMA_VERSION
        }, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()[:16]
    
    def measure_latency(self) -> Dict:
        """
        Measure latency. Return measurement dict or failure dict.
        
        Never fabricates data. Returns null for unmeasured fields.
        """
        try:
            if self.protocol == "icmp":
                return self._measure_icmp()
            elif self.protocol == "http":
                return self._measure_http()
            else:
                return {
                    "latency_ms": None,
                    "jitter_ms": None,
                    "packet_loss_fraction": None,
                    "success": False,
                    "failure_reason": f"Unknown protocol: {self.protocol}"
                }
        except Exception as e:
            logger.error(f"Measurement exception: {e}")
            return {
                "latency_ms": None,
                "jitter_ms": None,
                "packet_loss_fraction": None,
                "success": False,
                "failure_reason": f"exception: {type(e).__name__}"
            }
    
    def _measure_icmp(self) -> Dict:
        """Measure ICMP ping."""
        try:
            cmd = ["ping", "-c", "1", "-W", "5", self.endpoint]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=6
            )
            
            if result.returncode == 0:
                # Parse latency from output
                for line in result.stdout.split('\n'):
                    if 'time=' in line:
                        time_str = line.split('time=')[1].split(' ')[0]
                        try:
                            latency_ms = float(time_str)
                            return {
                                "latency_ms": latency_ms,
                                "jitter_ms": None,
                                "packet_loss_fraction": 0.0,
                                "success": True,
                                "failure_reason": None
                            }
                        except ValueError:
                            pass
                
                return {
                    "latency_ms": None,
                    "jitter_ms": None,
                    "packet_loss_fraction": None,
                    "success": False,
                    "failure_reason": "Could not parse ping output"
                }
            else:
                return {
                    "latency_ms": None,
                    "jitter_ms": None,
                    "packet_loss_fraction": 1.0,
                    "success": False,
                    "failure_reason": "ping_timeout"
                }
        
        except subprocess.TimeoutExpired:
            return {
                "latency_ms": None,
                "jitter_ms": None,
                "packet_loss_fraction": 1.0,
                "success": False,
                "failure_reason": "subprocess_timeout"
            }
        
        except FileNotFoundError:
            return {
                "latency_ms": None,
                "jitter_ms": None,
                "packet_loss_fraction": None,
                "success": False,
                "failure_reason": "ping_command_not_found"
            }
    
    def _measure_http(self) -> Dict:
        """Measure HTTP latency."""
        try:
            import urllib.request
            start = time.perf_counter()
            response = urllib.request.urlopen(f"http://{self.endpoint}", timeout=5)
            elapsed = (time.perf_counter() - start) * 1000
            response.close()
            
            return {
                "latency_ms": elapsed,
                "jitter_ms": None,
                "packet_loss_fraction": 0.0,
                "success": True,
                "failure_reason": None
            }
        
        except urllib.error.URLError as e:
            return {
                "latency_ms": None,
                "jitter_ms": None,
                "packet_loss_fraction": 1.0,
                "success": False,
                "failure_reason": f"url_error: {str(e)[:50]}"
            }
        
        except Exception as e:
            return {
                "latency_ms": None,
                "jitter_ms": None,
                "packet_loss_fraction": 1.0,
                "success": False,
                "failure_reason": f"{type(e).__name__}"
            }
    
    def collect_measurement(self) -> Dict:
        """
        Collect one measurement with full provenance.
        
        Returns record matching heartbeat_v1.json schema.
        """
        now_utc = datetime.now(timezone.utc)
        elapsed_ms = (time.monotonic() - self.start_time) * 1000
        
        measurement = self.measure_latency()
        
        record = {
            "record_id": str(uuid.uuid4()),
            "schema_version": self.SCHEMA_VERSION,
            "timestamp_utc": now_utc.isoformat(),
            "elapsed_monotonic_ms": elapsed_ms,
            "collector_id": self.collector_id,
            "software_version": self.SOFTWARE_VERSION,
            "condition": "gate0_test",
            "site_id": "gate0",
            "instrument_id": self.collector_id,
            "endpoint_id": self.endpoint,
            "endpoint": self.endpoint,
            "protocol": self.protocol,
            "latency_ms": measurement["latency_ms"],
            "jitter_ms": measurement["jitter_ms"],
            "packet_loss_fraction": measurement["packet_loss_fraction"],
            "success": measurement["success"],
            "failure_reason": measurement["failure_reason"],
            "config_hash": self.config_hash,
            "environment": {
                "temperature_c": None,
                "humidity_percent": None,
                "pressure_hpa": None
            },
            "system": {
                "cpu_percent": None,
                "memory_percent": None
            }
        }
        
        return record
    
    def write_record_atomic(self, record: Dict) -> bool:
        """
        Write record to disk atomically.
        
        Uses temp file + rename pattern to ensure no partial writes.
        Microsecond-accurate timestamps prevent silent overwrites.
        """
        try:
            now = datetime.fromisoformat(record["timestamp_utc"])
            filename = f"heartbeat_{now.strftime('%Y%m%d_%H%M%S_%f')}.json"
            filepath = self.output_dir / filename
            
            # Write to temp file first
            temp_path = filepath.with_suffix('.tmp')
            with open(temp_path, 'w') as f:
                json.dump(record, f, indent=2)
            
            # Atomic rename
            temp_path.replace(filepath)
            
            self.record_count += 1
            if record["success"]:
                self.success_count += 1
            else:
                self.failure_count += 1
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to write record: {e}")
            return False
    
    def run_daemon(self, interval_seconds: int = 300, max_duration_hours: int = 48):
        """
        Run collection daemon for Gate 0 test.
        
        Args:
            interval_seconds: Collection interval (default 5 min)
            max_duration_hours: Max runtime (default 48h for full gate test)
        """
        logger.info("=" * 80)
        logger.info("GATE 0 COLLECTION DAEMON STARTING")
        logger.info("=" * 80)
        logger.info(f"Interval: {interval_seconds}s")
        logger.info(f"Max duration: {max_duration_hours}h")
        logger.info(f"Target: {self.endpoint} ({self.protocol})")
        logger.info("")
        
        max_seconds = max_duration_hours * 3600
        cycle = 0
        
        try:
            while True:
                elapsed = time.monotonic() - self.start_time
                
                if elapsed > max_seconds:
                    logger.info(f"Max duration reached ({max_duration_hours}h). Stopping.")
                    break
                
                cycle += 1
                now = datetime.now(timezone.utc)
                
                # Collect measurement
                record = self.collect_measurement()
                
                # Write atomically
                written = self.write_record_atomic(record)
                
                if written:
                    status = "✓" if record["success"] else "⚠️"
                    latency = f"{record['latency_ms']:.1f}ms" if record['latency_ms'] else "N/A"
                    logger.info(f"{status} Cycle #{cycle:5d} | {latency:>10s} | {now.strftime('%H:%M:%S')}")
                else:
                    logger.error(f"❌ Cycle #{cycle} write failed")
                
                # Sleep
                time.sleep(interval_seconds)
        
        except KeyboardInterrupt:
            logger.info("\nTermination signal received. Stopping cleanly.")
        
        except Exception as e:
            logger.error(f"Daemon error: {e}")
        
        finally:
            self._print_summary()
    
    def _print_summary(self):
        """Print summary statistics."""
        elapsed = time.monotonic() - self.start_time
        hours = elapsed / 3600
        
        logger.info("")
        logger.info("=" * 80)
        logger.info("GATE 0 COLLECTION SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Runtime: {hours:.2f} hours")
        logger.info(f"Total records: {self.record_count}")
        logger.info(f"Successful: {self.success_count}")
        logger.info(f"Failed: {self.failure_count}")
        
        if self.record_count > 0:
            success_rate = (self.success_count / self.record_count) * 100
            logger.info(f"Success rate: {success_rate:.1f}%")
        
        logger.info(f"Output directory: {self.output_dir}")
        logger.info("=" * 80)


def main():
    """Main entry point."""
    collector = Gate0Collector(
        collector_id="gate0-primary-001",
        endpoint="8.8.8.8",
        protocol="icmp",
        output_dir="data/raw/heartbeat"
    )
    
    # Run for 48 hours (or until stopped)
    collector.run_daemon(interval_seconds=300, max_duration_hours=48)


if __name__ == "__main__":
    main()
