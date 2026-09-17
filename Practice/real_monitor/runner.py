from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
import time
import traceback
import uuid

from .config import MonitorConfig
from .db import DatabaseManager, ObservationRecord, RunRecord
from .metrics import collect_host_metrics, get_device_identity, get_sample_clock
from .workload import run_workload_once


class MonitorRunner:
    def __init__(self, db: DatabaseManager, config: MonitorConfig) -> None:
        self.db = db
        self.config = config

    def run(self) -> str:
        run_id = str(uuid.uuid4())
        device = get_device_identity()
        started_clock = get_sample_clock()

        self.db.upsert_location(
            location_id=self.config.location.location_id,
            label=self.config.location.label,
            timezone=self.config.location.timezone,
            notes=self.config.location.notes,
            created_at_utc=started_clock.timestamp_utc,
        )
        self.db.insert_run(
            RunRecord(
                run_id=run_id,
                start_time_utc=started_clock.timestamp_utc,
                location_id=self.config.location.location_id,
                device_id=device.device_id,
                hostname=device.hostname,
                platform=device.platform,
                worker_count=self.config.workload.worker_count,
                batch_size=self.config.workload.batch_size,
                intensity=self.config.workload.intensity,
                sampling_interval_seconds=self.config.runner.sampling_interval_seconds,
                duration_seconds=self.config.runner.duration_seconds,
                status="running",
                error_count=0,
            )
        )

        started = time.perf_counter()
        previous_process_seconds: float | None = None
        previous_wall_seconds: float | None = None
        error_count = 0
        status = "completed"
        next_start_index = 0

        try:
            while True:
                if (
                    self.config.runner.duration_seconds is not None
                    and (time.perf_counter() - started) >= self.config.runner.duration_seconds
                ):
                    break

                cycle_started = time.perf_counter()
                sample_clock = get_sample_clock()
                try:
                    workload_result = run_workload_once(
                        worker_count=self.config.workload.worker_count,
                        batch_size=self.config.workload.batch_size,
                        intensity=self.config.workload.intensity,
                        payload_size_bytes=self.config.workload.payload_size_bytes,
                        start_index=next_start_index,
                    )
                    next_start_index += self.config.workload.batch_size
                except Exception:
                    workload_result = None
                    error_count += 1

                host_metrics, previous_process_seconds, previous_wall_seconds = collect_host_metrics(
                    previous_process_seconds=previous_process_seconds,
                    previous_wall_seconds=previous_wall_seconds,
                )

                self.db.insert_observation(
                    ObservationRecord(
                        run_id=run_id,
                        timestamp_utc=sample_clock.timestamp_utc,
                        local_date=sample_clock.local_date,
                        local_time=sample_clock.local_time,
                        time_of_day_bucket=sample_clock.time_of_day_bucket,
                        location_id=self.config.location.location_id,
                        worker_count=self.config.workload.worker_count,
                        batch_size=self.config.workload.batch_size,
                        intensity=self.config.workload.intensity,
                        operations_completed=0
                        if workload_result is None
                        else workload_result.operations_completed,
                        elapsed_seconds=0.0
                        if workload_result is None
                        else workload_result.elapsed_seconds,
                        operations_per_second=None
                        if workload_result is None
                        else workload_result.operations_per_second,
                        process_cpu_percent=host_metrics.process_cpu_percent,
                        system_cpu_percent=host_metrics.system_cpu_percent,
                        process_memory_mb=host_metrics.process_memory_mb,
                        system_memory_percent=host_metrics.system_memory_percent,
                        disk_read_bytes=host_metrics.disk_read_bytes,
                        disk_write_bytes=host_metrics.disk_write_bytes,
                        load_avg_1m=host_metrics.load_avg_1m,
                        temperature_c=host_metrics.temperature_c,
                        error_count=error_count,
                    )
                )

                elapsed_cycle = time.perf_counter() - cycle_started
                sleep_seconds = self.config.runner.sampling_interval_seconds - elapsed_cycle
                if sleep_seconds > 0:
                    time.sleep(sleep_seconds)
        except KeyboardInterrupt:
            status = "interrupted"
        except Exception:
            status = "failed"
            error_count += 1
            traceback.print_exc()
        finally:
            self.db.update_run_end(
                run_id=run_id,
                end_time_utc=datetime.now(timezone.utc).isoformat(),
                status=status,
                error_count=error_count,
            )

        return run_id


def run_with_overrides(config: MonitorConfig, **overrides: object) -> str:
    runtime_cfg = config.with_overrides(**overrides)
    db = DatabaseManager(runtime_cfg.database_path)
    db.init_db()
    runner = MonitorRunner(db, runtime_cfg)
    return runner.run()
