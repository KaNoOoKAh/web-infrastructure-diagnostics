from __future__ import annotations

from datetime import datetime, timezone
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from real_monitor.db import DatabaseManager, ObservationRecord, RunRecord


class DatabaseTests(unittest.TestCase):
    def test_insert_and_query(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = str(Path(tmp_dir) / "monitor.db")
            db = DatabaseManager(db_path)
            db.init_db()

            now = datetime.now(timezone.utc).isoformat()
            db.upsert_location("loc-1", "Location 1", "UTC", "notes", now)

            run = RunRecord(
                run_id="run-1",
                start_time_utc=now,
                location_id="loc-1",
                device_id="device-1",
                hostname="host-1",
                platform="Linux",
                worker_count=2,
                batch_size=10,
                intensity=5,
                sampling_interval_seconds=1.0,
                duration_seconds=10.0,
                status="running",
            )
            db.insert_run(run)
            db.insert_observation(
                ObservationRecord(
                    run_id="run-1",
                    timestamp_utc=now,
                    local_date="2026-09-17",
                    local_time="10:00:00",
                    time_of_day_bucket="10:00",
                    location_id="loc-1",
                    worker_count=2,
                    batch_size=10,
                    intensity=5,
                    operations_completed=10,
                    elapsed_seconds=1.0,
                    operations_per_second=10.0,
                    process_cpu_percent=None,
                    system_cpu_percent=None,
                    process_memory_mb=100.0,
                    system_memory_percent=None,
                    disk_read_bytes=None,
                    disk_write_bytes=None,
                    load_avg_1m=None,
                    temperature_c=None,
                    error_count=0,
                )
            )

            self.assertEqual(db.get_latest_run_id(), "run-1")
            groups = db.get_observation_groups_for_run("run-1")
            self.assertEqual(len(groups), 1)
            self.assertEqual(groups[0]["sample_count"], 1)


if __name__ == "__main__":
    unittest.main()
