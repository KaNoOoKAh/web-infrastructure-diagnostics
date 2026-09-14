#!/usr/bin/env python3
"""
MOCK BASELINE DATA GENERATOR

What This Does (In Plain English):
====================================
This script creates FAKE but realistic heartbeat data for testing.

Instead of waiting for real data from 6 global regions over 24+ hours,
we generate 288 synthetic snapshots (one every 5 minutes for 24 hours)
that look exactly like real infrastructure monitoring data.

Why This Matters:
- Tests the entire pipeline WITHOUT waiting for real data
- Finds bugs in the analyzer before they hit production
- Lets us verify the anomaly detection works correctly
- Zero network dependencies, zero external APIs needed
- Fast feedback loop

What It Generates:
- 288 heartbeat snapshots (24-hour baseline)
- 6 regions: us-east, us-west, eu-west, asia-pacific, south-america, africa
- Per snapshot: latency, DNS resolution, uptime status
- Realistic patterns: normal variation + intentional anomalies
- Output: JSON files saved to data/raw/baseline/

How To Use:
    python scripts/generate_mock_baseline.py
    
Then analyze it:
    python scripts/analyze_heartbeat.py
    
Expected Output:
    - Baseline stats: mean latency per region, uptime %, DNS times
    - Anomalies: detected >2σ latency spikes (intentionally planted)
"""

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List


# ============================================================================
# CONFIGURATION: Set your baseline expectations here
# ============================================================================

REGIONAL_BASELINES = {
    "us-east": {
        "base_latency_ms": 45.0,
        "latency_variance": 5.0,      # ±5ms normal variation
        "dns_base_ms": 8.0,
        "uptime_percent": 99.8,
    },
    "us-west": {
        "base_latency_ms": 52.0,
        "latency_variance": 6.0,
        "dns_base_ms": 9.5,
        "uptime_percent": 99.7,
    },
    "eu-west": {
        "base_latency_ms": 48.0,
        "latency_variance": 5.5,
        "dns_base_ms": 10.2,
        "uptime_percent": 99.9,
    },
    "asia-pacific": {
        "base_latency_ms": 120.0,     # Longer due to distance
        "latency_variance": 15.0,
        "dns_base_ms": 25.0,
        "uptime_percent": 99.2,
    },
    "south-america": {
        "base_latency_ms": 90.0,
        "latency_variance": 10.0,
        "dns_base_ms": 15.0,
        "uptime_percent": 98.5,
    },
    "africa": {
        "base_latency_ms": 150.0,
        "latency_variance": 20.0,
        "dns_base_ms": 30.0,
        "uptime_percent": 97.0,
    },
}

# How many anomalies to intentionally inject per region
ANOMALIES_PER_REGION = 3


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_latency(baseline: Dict, inject_spike: bool = False) -> float:
    """
    Generate a realistic latency value.
    
    Args:
        baseline: Region baseline config
        inject_spike: If True, create a >2σ anomaly spike
        
    Returns:
        Latency in milliseconds
    """
    base = baseline["base_latency_ms"]
    variance = baseline["latency_variance"]
    
    if inject_spike:
        # Create a spike: 3-5 standard deviations above normal
        return base + (variance * random.uniform(3.5, 5.0))
    else:
        # Normal variation: ~68% within 1σ, ~95% within 2σ
        return base + random.gauss(0, variance)


def generate_dns_time(baseline: Dict) -> float:
    """Generate realistic DNS resolution time."""
    base = baseline["dns_base_ms"]
    return base + random.gauss(0, base * 0.15)  # ±15% variation


def is_online(baseline: Dict) -> bool:
    """Determine if region is online based on uptime percentage."""
    return random.random() < (baseline["uptime_percent"] / 100.0)


def generate_heartbeat_snapshot(
    timestamp: datetime,
    region_baselines: Dict,
    anomaly_regions: List[str]
) -> Dict:
    """
    Generate a single heartbeat snapshot for all 6 regions.
    
    Args:
        timestamp: UTC timestamp for this snapshot
        region_baselines: Configuration for all regions
        anomaly_regions: List of region names to inject anomalies into
        
    Returns:
        Dictionary matching heartbeat format
    """
    snapshot = {}
    
    for region, baseline in region_baselines.items():
        online = is_online(baseline)
        inject_spike = region in anomaly_regions
        
        snapshot[region] = {
            "timestamp": timestamp.isoformat(),
            "host": baseline.get("host", "example.com"),
            "latency_ms": generate_latency(baseline, inject_spike) if online else None,
            "dns_resolution_ms": generate_dns_time(baseline) if online else None,
            "reachable": online,
            "dns_working": online,
        }
    
    return snapshot


def generate_mock_baseline(
    num_snapshots: int = 288,
    start_time: datetime = None,
    interval_minutes: int = 5
) -> List[Dict]:
    """
    Generate a complete mock baseline dataset.
    
    Args:
        num_snapshots: How many 5-minute snapshots to generate
        start_time: Starting timestamp (default: 24 hours ago)
        interval_minutes: Minutes between snapshots
        
    Returns:
        List of heartbeat snapshots
    """
    
    if start_time is None:
        start_time = datetime.now(timezone.utc) - timedelta(hours=24)
    
    snapshots = []
    
    # Pre-select which snapshots will have anomalies
    # Spread them across the timeline
    anomaly_snapshot_indices = random.sample(
        range(num_snapshots),
        min(len(REGIONAL_BASELINES) * ANOMALIES_PER_REGION, num_snapshots // 10)
    )
    
    # Pre-select which regions get anomalies at each anomaly snapshot
    anomaly_regions_per_snapshot = {}
    for idx in anomaly_snapshot_indices:
        num_regions = random.randint(1, 3)
        anomaly_regions_per_snapshot[idx] = random.sample(
            list(REGIONAL_BASELINES.keys()),
            num_regions
        )
    
    print(f"Generating {num_snapshots} snapshots...")
    print(f"Injecting {len(anomaly_snapshot_indices)} anomaly events across regions")
    
    for i in range(num_snapshots):
        timestamp = start_time + timedelta(minutes=interval_minutes * i)
        
        # Check if this snapshot should have anomalies
        anomaly_regions = anomaly_regions_per_snapshot.get(i, [])
        
        snapshot = generate_heartbeat_snapshot(
            timestamp,
            REGIONAL_BASELINES,
            anomaly_regions
        )
        
        snapshots.append(snapshot)
        
        # Progress indicator
        if (i + 1) % 50 == 0:
            print(f"  ✓ Generated {i + 1}/{num_snapshots} snapshots")
    
    return snapshots


def save_snapshots(snapshots: List[Dict], output_dir: str = "data/raw/baseline"):
    """
    Save snapshots to individual JSON files (matching heartbeat.py format).
    
    Args:
        snapshots: List of snapshot dictionaries
        output_dir: Directory to save files
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nSaving snapshots to {output_dir}...")
    
    for i, snapshot in enumerate(snapshots):
        # Extract timestamp from first region's data
        timestamp_iso = list(snapshot.values())[0]["timestamp"]
        timestamp_obj = datetime.fromisoformat(timestamp_iso)
        
        # Format filename: heartbeat_YYYYMMDD_HHMMSS.json
        filename = timestamp_obj.strftime("heartbeat_%Y%m%d_%H%M%S.json")
        filepath = output_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        if (i + 1) % 50 == 0:
            print(f"  ✓ Saved {i + 1}/{len(snapshots)} files")
    
    print(f"\n✅ All {len(snapshots)} snapshots saved to {output_dir}/")


def print_summary(snapshots: List[Dict]):
    """Print a summary of generated data."""
    print("\n" + "=" * 70)
    print("MOCK BASELINE DATA SUMMARY")
    print("=" * 70)
    
    # Time range
    first_ts = list(snapshots[0].values())[0]["timestamp"]
    last_ts = list(snapshots[-1].values())[0]["timestamp"]
    print(f"Time range: {first_ts} to {last_ts}")
    print(f"Total snapshots: {len(snapshots)}")
    print(f"Interval: 5 minutes")
    
    # Regions
    print(f"\nRegions covered: {list(REGIONAL_BASELINES.keys())}")
    
    # Anomaly count
    total_anomalies = 0
    for region, baseline in REGIONAL_BASELINES.items():
        for snapshot in snapshots:
            if snapshot[region]["latency_ms"]:
                expected_mean = baseline["base_latency_ms"]
                expected_stdev = baseline["latency_variance"]
                actual = snapshot[region]["latency_ms"]
                z_score = (actual - expected_mean) / expected_stdev if expected_stdev > 0 else 0
                if abs(z_score) > 2.0:
                    total_anomalies += 1
    
    print(f"\nAnomaly events injected: {total_anomalies} (>2σ latency spikes)")
    
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Run the analyzer:")
    print("   python scripts/analyze_heartbeat.py")
    print("\n2. Check that it finds the anomalies we injected")
    print("\n3. Review the baseline stats (mean, stdev, uptime per region)")
    print("=" * 70 + "\n")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate realistic mock heartbeat baseline data"
    )
    parser.add_argument(
        "--snapshots",
        type=int,
        default=288,
        help="Number of snapshots to generate (default: 288 = 24 hours at 5min intervals)"
    )
    parser.add_argument(
        "--output-dir",
        default="data/raw/baseline",
        help="Directory to save snapshots"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Generate data but don't save (useful for testing)"
    )
    
    args = parser.parse_args()
    
    # Generate data
    snapshots = generate_mock_baseline(num_snapshots=args.snapshots)
    
    # Save to files
    if not args.no_save:
        save_snapshots(snapshots, args.output_dir)
    
    # Print summary
    print_summary(snapshots)
