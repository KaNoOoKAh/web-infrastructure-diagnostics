from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from real_monitor.workload import run_workload_once


class WorkloadTests(unittest.TestCase):
    def test_repeatable_checksum_for_same_inputs(self) -> None:
        first = run_workload_once(
            worker_count=2,
            batch_size=10,
            intensity=20,
            payload_size_bytes=256,
            start_index=0,
        )
        second = run_workload_once(
            worker_count=2,
            batch_size=10,
            intensity=20,
            payload_size_bytes=256,
            start_index=0,
        )

        self.assertEqual(first.operations_completed, 10)
        self.assertEqual(second.operations_completed, 10)
        self.assertEqual(first.checksum, second.checksum)
        self.assertGreater(first.operations_per_second, 0.0)


if __name__ == "__main__":
    unittest.main()
