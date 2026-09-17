from __future__ import annotations

from dataclasses import dataclass
import sqlite3
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RunRecord:
    run_id: str
    start_time_utc: str
    location_id: str
    device_id: str
    hostname: str
    platform: str
    worker_count: int
    batch_size: int
    intensity: int
    sampling_interval_seconds: float
    duration_seconds: float | None
    status: str
    error_count: int = 0


@dataclass(frozen=True)
class ObservationRecord:
    run_id: str
    timestamp_utc: str
    local_date: str
    local_time: str
    time_of_day_bucket: str
    location_id: str
    worker_count: int
    batch_size: int
    intensity: int
    operations_completed: int
    elapsed_seconds: float
    operations_per_second: float | None
    process_cpu_percent: float | None
    system_cpu_percent: float | None
    process_memory_mb: float | None
    system_memory_percent: float | None
    disk_read_bytes: int | None
    disk_write_bytes: int | None
    load_avg_1m: float | None
    temperature_c: float | None
    error_count: int


class DatabaseManager:
    def __init__(self, database_path: str) -> None:
        self.database_path = str(Path(database_path).expanduser())

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def init_db(self) -> None:
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.executescript(
                """
                PRAGMA foreign_keys = ON;

                CREATE TABLE IF NOT EXISTS locations (
                    location_id TEXT PRIMARY KEY,
                    label TEXT NOT NULL,
                    timezone TEXT,
                    notes TEXT,
                    created_at_utc TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    start_time_utc TEXT NOT NULL,
                    end_time_utc TEXT,
                    location_id TEXT NOT NULL,
                    device_id TEXT NOT NULL,
                    hostname TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    worker_count INTEGER NOT NULL,
                    batch_size INTEGER NOT NULL,
                    intensity INTEGER NOT NULL,
                    sampling_interval_seconds REAL NOT NULL,
                    duration_seconds REAL,
                    status TEXT NOT NULL,
                    error_count INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY(location_id) REFERENCES locations(location_id)
                );

                CREATE TABLE IF NOT EXISTS observations (
                    observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    timestamp_utc TEXT NOT NULL,
                    local_date TEXT NOT NULL,
                    local_time TEXT NOT NULL,
                    time_of_day_bucket TEXT NOT NULL,
                    location_id TEXT NOT NULL,
                    worker_count INTEGER NOT NULL,
                    batch_size INTEGER NOT NULL,
                    intensity INTEGER NOT NULL,
                    operations_completed INTEGER NOT NULL,
                    elapsed_seconds REAL NOT NULL,
                    operations_per_second REAL,
                    process_cpu_percent REAL,
                    system_cpu_percent REAL,
                    process_memory_mb REAL,
                    system_memory_percent REAL,
                    disk_read_bytes INTEGER,
                    disk_write_bytes INTEGER,
                    load_avg_1m REAL,
                    temperature_c REAL,
                    error_count INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY(run_id) REFERENCES runs(run_id),
                    FOREIGN KEY(location_id) REFERENCES locations(location_id)
                );

                CREATE INDEX IF NOT EXISTS idx_observations_timestamp_utc
                    ON observations(timestamp_utc);
                CREATE INDEX IF NOT EXISTS idx_observations_time_of_day
                    ON observations(time_of_day_bucket);
                CREATE INDEX IF NOT EXISTS idx_observations_location
                    ON observations(location_id);
                CREATE INDEX IF NOT EXISTS idx_observations_workload
                    ON observations(worker_count, batch_size, intensity);
                """
            )

    def upsert_location(
        self,
        location_id: str,
        label: str,
        timezone: str,
        notes: str,
        created_at_utc: str,
    ) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO locations (location_id, label, timezone, notes, created_at_utc)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(location_id) DO UPDATE SET
                    label = excluded.label,
                    timezone = excluded.timezone,
                    notes = excluded.notes
                """,
                (location_id, label, timezone, notes, created_at_utc),
            )

    def list_locations(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT location_id, label, timezone, notes, created_at_utc FROM locations ORDER BY location_id"
            ).fetchall()
        return [dict(row) for row in rows]

    def insert_run(self, run: RunRecord) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO runs (
                    run_id, start_time_utc, location_id, device_id, hostname, platform,
                    worker_count, batch_size, intensity, sampling_interval_seconds,
                    duration_seconds, status, error_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run.run_id,
                    run.start_time_utc,
                    run.location_id,
                    run.device_id,
                    run.hostname,
                    run.platform,
                    run.worker_count,
                    run.batch_size,
                    run.intensity,
                    run.sampling_interval_seconds,
                    run.duration_seconds,
                    run.status,
                    run.error_count,
                ),
            )

    def update_run_end(
        self,
        run_id: str,
        end_time_utc: str,
        status: str,
        error_count: int,
    ) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE runs
                SET end_time_utc = ?, status = ?, error_count = ?
                WHERE run_id = ?
                """,
                (end_time_utc, status, error_count, run_id),
            )

    def insert_observation(self, observation: ObservationRecord) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO observations (
                    run_id, timestamp_utc, local_date, local_time, time_of_day_bucket,
                    location_id, worker_count, batch_size, intensity,
                    operations_completed, elapsed_seconds, operations_per_second,
                    process_cpu_percent, system_cpu_percent, process_memory_mb,
                    system_memory_percent, disk_read_bytes, disk_write_bytes,
                    load_avg_1m, temperature_c, error_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    observation.run_id,
                    observation.timestamp_utc,
                    observation.local_date,
                    observation.local_time,
                    observation.time_of_day_bucket,
                    observation.location_id,
                    observation.worker_count,
                    observation.batch_size,
                    observation.intensity,
                    observation.operations_completed,
                    observation.elapsed_seconds,
                    observation.operations_per_second,
                    observation.process_cpu_percent,
                    observation.system_cpu_percent,
                    observation.process_memory_mb,
                    observation.system_memory_percent,
                    observation.disk_read_bytes,
                    observation.disk_write_bytes,
                    observation.load_avg_1m,
                    observation.temperature_c,
                    observation.error_count,
                ),
            )

    def get_latest_run_id(self) -> str | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT run_id FROM runs ORDER BY start_time_utc DESC LIMIT 1"
            ).fetchone()
        if row is None:
            return None
        return str(row["run_id"])

    def get_observation_groups_for_run(self, run_id: str) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    time_of_day_bucket,
                    location_id,
                    worker_count,
                    batch_size,
                    intensity,
                    COUNT(*) AS sample_count,
                    AVG(operations_per_second) AS avg_ops,
                    AVG(process_cpu_percent) AS avg_process_cpu,
                    AVG(system_cpu_percent) AS avg_system_cpu,
                    AVG(temperature_c) AS avg_temperature
                FROM observations
                WHERE run_id = ?
                GROUP BY time_of_day_bucket, location_id, worker_count, batch_size, intensity
                ORDER BY time_of_day_bucket
                """,
                (run_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_historical_group_baseline(
        self,
        *,
        time_of_day_bucket: str,
        location_id: str,
        worker_count: int,
        batch_size: int,
        intensity: int,
        exclude_run_id: str,
    ) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT
                    COUNT(*) AS sample_count,
                    AVG(operations_per_second) AS avg_ops,
                    AVG(process_cpu_percent) AS avg_process_cpu,
                    AVG(system_cpu_percent) AS avg_system_cpu,
                    AVG(temperature_c) AS avg_temperature
                FROM observations
                WHERE time_of_day_bucket = ?
                  AND location_id = ?
                  AND worker_count = ?
                  AND batch_size = ?
                  AND intensity = ?
                  AND run_id != ?
                """,
                (
                    time_of_day_bucket,
                    location_id,
                    worker_count,
                    batch_size,
                    intensity,
                    exclude_run_id,
                ),
            ).fetchone()
        return dict(row) if row is not None else {"sample_count": 0}
