from __future__ import annotations

from datetime import datetime, timezone
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from real_monitor.analyzer import analyze_run
from real_monitor.config import AnalyzerConfig
from real_monitor.db import DatabaseManager, ObservationRecord, RunRecord


class AnalyzerTests(unittest.TestCase):
    def _seed_run(
        self,
        db: DatabaseManager,
        *,
        run_id: str,
        ops: float,
        location_id: str = "loc-1",
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        db.insert_run(
            RunRecord(
                run_id=run_id,
                start_time_utc=now,
                location_id=location_id,
                device_id="device-1",
                hostname="host-1",
                platform="Linux",
                worker_count=2,
                batch_size=10,
                intensity=5,
                sampling_interval_seconds=1.0,
                duration_seconds=5.0,
                status="completed",
            )
        )
        db.insert_observation(
            ObservationRecord(
                run_id=run_id,
                timestamp_utc=now,
                local_date="2026-09-17",
                local_time="10:00:00",
                time_of_day_bucket="10:00",
                location_id=location_id,
                worker_count=2,
                batch_size=10,
                intensity=5,
                operations_completed=10,
                elapsed_seconds=1.0,
                operations_per_second=ops,
                process_cpu_percent=40.0,
                system_cpu_percent=20.0,
                process_memory_mb=100.0,
                system_memory_percent=55.0,
                disk_read_bytes=1,
                disk_write_bytes=1,
                load_avg_1m=0.1,
                temperature_c=None,
                error_count=0,
            )
        )

    def test_insufficient_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            db = DatabaseManager(str(Path(tmp_dir) / "monitor.db"))
            db.init_db()
            now = datetime.now(timezone.utc).isoformat()
            db.upsert_location("loc-1", "Location 1", "UTC", "", now)
            self._seed_run(db, run_id="run-current", ops=100.0)

            rows = analyze_run(db, AnalyzerConfig(min_baseline_samples=2), run_id="run-current")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0].note, "insufficient_history")

    def test_anomaly_when_deviation_exceeds_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            db = DatabaseManager(str(Path(tmp_dir) / "monitor.db"))
            db.init_db()
            now = datetime.now(timezone.utc).isoformat()
            db.upsert_location("loc-1", "Location 1", "UTC", "", now)
            self._seed_run(db, run_id="run-baseline", ops=100.0)
            self._seed_run(db, run_id="run-current", ops=150.0)

            rows = analyze_run(
                db,
                AnalyzerConfig(min_baseline_samples=1, anomaly_threshold_percent=20.0),
                run_id="run-current",
            )
            self.assertEqual(len(rows), 1)
            self.assertTrue(rows[0].anomaly)
            self.assertEqual(rows[0].note, "anomaly")


if __name__ == "__main__":
    unittest.main()
