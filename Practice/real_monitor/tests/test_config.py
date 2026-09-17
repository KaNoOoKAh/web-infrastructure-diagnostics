from __future__ import annotations

import json
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from real_monitor.config import MonitorConfig


class ConfigTests(unittest.TestCase):
    def test_parse_file_and_override(self) -> None:
        data = {
            "database_path": "./x.db",
            "location": {"location_id": "loc-a", "label": "Loc A"},
            "workload": {"worker_count": 3, "batch_size": 12, "intensity": 15},
            "runner": {"sampling_interval_seconds": 3, "duration_seconds": 20},
            "analyzer": {"min_baseline_samples": 2, "anomaly_threshold_percent": 15},
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            cfg_path = Path(tmp_dir) / "cfg.json"
            cfg_path.write_text(json.dumps(data), encoding="utf-8")

            cfg = MonitorConfig.from_file(cfg_path)
            self.assertEqual(cfg.location.location_id, "loc-a")
            self.assertEqual(cfg.workload.worker_count, 3)
            self.assertEqual(cfg.runner.duration_seconds, 20)

            overridden = cfg.with_overrides(worker_count=5, batch_size=20)
            self.assertEqual(overridden.workload.worker_count, 5)
            self.assertEqual(overridden.workload.batch_size, 20)

    def test_invalid_values_raise(self) -> None:
        cfg = MonitorConfig()
        with self.assertRaises(ValueError):
            cfg.with_overrides(worker_count=0)


if __name__ == "__main__":
    unittest.main()
