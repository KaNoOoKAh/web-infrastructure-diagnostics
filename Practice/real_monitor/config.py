from __future__ import annotations

from dataclasses import dataclass, replace
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LocationProfile:
    location_id: str = "default-location"
    label: str = "Default Location"
    timezone: str = "local"
    notes: str = ""


@dataclass(frozen=True)
class WorkloadConfig:
    worker_count: int = 2
    batch_size: int = 100
    intensity: int = 100
    payload_size_bytes: int = 1024


@dataclass(frozen=True)
class RunnerConfig:
    sampling_interval_seconds: float = 30.0
    duration_seconds: float | None = None


@dataclass(frozen=True)
class AnalyzerConfig:
    min_baseline_samples: int = 3
    anomaly_threshold_percent: float = 20.0


@dataclass(frozen=True)
class MonitorConfig:
    database_path: str = "./Practice/real_monitor/real_monitor.db"
    location: LocationProfile = LocationProfile()
    workload: WorkloadConfig = WorkloadConfig()
    runner: RunnerConfig = RunnerConfig()
    analyzer: AnalyzerConfig = AnalyzerConfig()

    @staticmethod
    def from_file(path: str | Path) -> "MonitorConfig":
        with Path(path).expanduser().open("r", encoding="utf-8") as fh:
            raw = json.load(fh)

        location_raw = raw.get("location", {})
        workload_raw = raw.get("workload", {})
        runner_raw = raw.get("runner", {})
        analyzer_raw = raw.get("analyzer", {})

        cfg = MonitorConfig(
            database_path=str(raw.get("database_path", MonitorConfig().database_path)),
            location=LocationProfile(
                location_id=str(location_raw.get("location_id", LocationProfile().location_id)),
                label=str(location_raw.get("label", LocationProfile().label)),
                timezone=str(location_raw.get("timezone", LocationProfile().timezone)),
                notes=str(location_raw.get("notes", LocationProfile().notes)),
            ),
            workload=WorkloadConfig(
                worker_count=int(workload_raw.get("worker_count", WorkloadConfig().worker_count)),
                batch_size=int(workload_raw.get("batch_size", WorkloadConfig().batch_size)),
                intensity=int(workload_raw.get("intensity", WorkloadConfig().intensity)),
                payload_size_bytes=int(
                    workload_raw.get("payload_size_bytes", WorkloadConfig().payload_size_bytes)
                ),
            ),
            runner=RunnerConfig(
                sampling_interval_seconds=float(
                    runner_raw.get(
                        "sampling_interval_seconds", RunnerConfig().sampling_interval_seconds
                    )
                ),
                duration_seconds=(
                    None
                    if runner_raw.get("duration_seconds") is None
                    else float(runner_raw["duration_seconds"])
                ),
            ),
            analyzer=AnalyzerConfig(
                min_baseline_samples=int(
                    analyzer_raw.get(
                        "min_baseline_samples", AnalyzerConfig().min_baseline_samples
                    )
                ),
                anomaly_threshold_percent=float(
                    analyzer_raw.get(
                        "anomaly_threshold_percent", AnalyzerConfig().anomaly_threshold_percent
                    )
                ),
            ),
        )
        cfg.validate()
        return cfg

    def with_overrides(self, **overrides: Any) -> "MonitorConfig":
        cfg = self
        if "database_path" in overrides and overrides["database_path"]:
            cfg = replace(cfg, database_path=str(overrides["database_path"]))

        location = cfg.location
        if overrides.get("location_id"):
            location = replace(location, location_id=str(overrides["location_id"]))
        if overrides.get("location_label"):
            location = replace(location, label=str(overrides["location_label"]))
        if overrides.get("location_timezone"):
            location = replace(location, timezone=str(overrides["location_timezone"]))
        if overrides.get("location_notes") is not None:
            location = replace(location, notes=str(overrides["location_notes"]))
        cfg = replace(cfg, location=location)

        workload = cfg.workload
        if overrides.get("worker_count") is not None:
            workload = replace(workload, worker_count=int(overrides["worker_count"]))
        if overrides.get("batch_size") is not None:
            workload = replace(workload, batch_size=int(overrides["batch_size"]))
        if overrides.get("intensity") is not None:
            workload = replace(workload, intensity=int(overrides["intensity"]))
        if overrides.get("payload_size_bytes") is not None:
            workload = replace(
                workload, payload_size_bytes=int(overrides["payload_size_bytes"])
            )
        cfg = replace(cfg, workload=workload)

        runner = cfg.runner
        if overrides.get("sampling_interval_seconds") is not None:
            runner = replace(
                runner,
                sampling_interval_seconds=float(overrides["sampling_interval_seconds"]),
            )
        if "duration_seconds" in overrides and overrides["duration_seconds"] is not None:
            runner = replace(runner, duration_seconds=float(overrides["duration_seconds"]))
        cfg = replace(cfg, runner=runner)

        cfg.validate()
        return cfg

    def validate(self) -> None:
        if self.workload.worker_count <= 0:
            raise ValueError("worker_count must be > 0")
        if self.workload.batch_size <= 0:
            raise ValueError("batch_size must be > 0")
        if self.workload.intensity <= 0:
            raise ValueError("intensity must be > 0")
        if self.workload.payload_size_bytes <= 0:
            raise ValueError("payload_size_bytes must be > 0")
        if self.runner.sampling_interval_seconds <= 0:
            raise ValueError("sampling_interval_seconds must be > 0")
        if (
            self.runner.duration_seconds is not None
            and self.runner.duration_seconds <= 0
        ):
            raise ValueError("duration_seconds must be > 0 when provided")
        if not self.location.location_id.strip():
            raise ValueError("location_id cannot be empty")


DEFAULT_CONFIG_PATH = Path(__file__).with_name("default_config.json")
