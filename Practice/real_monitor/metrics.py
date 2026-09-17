from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os
import platform
import resource
import time
from typing import Optional

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover
    psutil = None


@dataclass(frozen=True)
class DeviceIdentity:
    device_id: str
    hostname: str
    platform: str


@dataclass(frozen=True)
class HostMetrics:
    process_cpu_percent: Optional[float]
    system_cpu_percent: Optional[float]
    process_memory_mb: Optional[float]
    system_memory_percent: Optional[float]
    disk_read_bytes: Optional[int]
    disk_write_bytes: Optional[int]
    load_avg_1m: Optional[float]
    temperature_c: Optional[float]


@dataclass(frozen=True)
class SampleClock:
    timestamp_utc: str
    local_date: str
    local_time: str
    time_of_day_bucket: str


def get_device_identity() -> DeviceIdentity:
    hostname = platform.node() or "unknown-host"
    return DeviceIdentity(
        device_id=f"{hostname}-{platform.machine() or 'unknown-machine'}",
        hostname=hostname,
        platform=f"{platform.system()} {platform.release()}",
    )


def get_sample_clock() -> SampleClock:
    utc_now = datetime.now(timezone.utc)
    local_now = datetime.now().astimezone()
    return SampleClock(
        timestamp_utc=utc_now.isoformat(),
        local_date=local_now.strftime("%Y-%m-%d"),
        local_time=local_now.strftime("%H:%M:%S"),
        time_of_day_bucket=local_now.strftime("%H:%M"),
    )


def _first_temperature_c() -> Optional[float]:
    if psutil is None or not hasattr(psutil, "sensors_temperatures"):
        return None
    try:
        temps = psutil.sensors_temperatures(fahrenheit=False)
    except Exception:
        return None
    for _, entries in temps.items():
        for entry in entries:
            current = getattr(entry, "current", None)
            if current is not None:
                return float(current)
    return None


def collect_host_metrics(
    previous_process_seconds: Optional[float],
    previous_wall_seconds: Optional[float],
) -> tuple[HostMetrics, float, float]:
    current_process_seconds = time.process_time()
    current_wall_seconds = time.perf_counter()

    process_cpu_percent: Optional[float] = None
    if (
        previous_process_seconds is not None
        and previous_wall_seconds is not None
    ):
        process_delta = current_process_seconds - previous_process_seconds
        wall_delta = current_wall_seconds - previous_wall_seconds
        if wall_delta > 0:
            process_cpu_percent = max((process_delta / wall_delta) * 100.0, 0.0)

    system_cpu_percent: Optional[float] = None
    process_memory_mb: Optional[float] = None
    system_memory_percent: Optional[float] = None
    disk_read_bytes: Optional[int] = None
    disk_write_bytes: Optional[int] = None

    if psutil is not None:
        try:
            system_cpu_percent = float(psutil.cpu_percent(interval=None))
        except Exception:
            system_cpu_percent = None
        try:
            process_memory_mb = float(psutil.Process().memory_info().rss) / (1024 * 1024)
        except Exception:
            process_memory_mb = None
        try:
            system_memory_percent = float(psutil.virtual_memory().percent)
        except Exception:
            system_memory_percent = None
        try:
            disk = psutil.disk_io_counters()
            if disk is not None:
                disk_read_bytes = int(disk.read_bytes)
                disk_write_bytes = int(disk.write_bytes)
        except Exception:
            disk_read_bytes = None
            disk_write_bytes = None
    else:
        try:
            process_memory_mb = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
            if platform.system().lower() != "darwin":
                process_memory_mb = process_memory_mb / 1024.0
            process_memory_mb = process_memory_mb / 1024.0
        except Exception:
            process_memory_mb = None

    load_avg_1m: Optional[float] = None
    if hasattr(os, "getloadavg"):
        try:
            load_avg_1m = float(os.getloadavg()[0])
        except Exception:
            load_avg_1m = None

    metrics = HostMetrics(
        process_cpu_percent=process_cpu_percent,
        system_cpu_percent=system_cpu_percent,
        process_memory_mb=process_memory_mb,
        system_memory_percent=system_memory_percent,
        disk_read_bytes=disk_read_bytes,
        disk_write_bytes=disk_write_bytes,
        load_avg_1m=load_avg_1m,
        temperature_c=_first_temperature_c(),
    )
    return metrics, current_process_seconds, current_wall_seconds
