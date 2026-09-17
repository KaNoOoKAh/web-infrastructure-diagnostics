from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import hashlib
import time


@dataclass(frozen=True)
class WorkloadResult:
    operations_completed: int
    elapsed_seconds: float
    operations_per_second: float
    checksum: str


def _make_payload(op_index: int, payload_size_bytes: int) -> bytes:
    seed = f"real-monitor|{op_index}|{payload_size_bytes}".encode("utf-8")
    payload = hashlib.sha256(seed).digest()
    repeat_count = (payload_size_bytes // len(payload)) + 1
    return (payload * repeat_count)[:payload_size_bytes]


def _hash_operation(op_index: int, intensity: int, payload_size_bytes: int) -> str:
    data = _make_payload(op_index=op_index, payload_size_bytes=payload_size_bytes)
    digest = hashlib.sha256(data).digest()
    for _ in range(intensity - 1):
        digest = hashlib.sha256(digest + data).digest()
    return digest.hex()


def run_workload_once(
    worker_count: int,
    batch_size: int,
    intensity: int,
    payload_size_bytes: int,
    start_index: int = 0,
) -> WorkloadResult:
    if worker_count <= 0:
        raise ValueError("worker_count must be > 0")
    if batch_size <= 0:
        raise ValueError("batch_size must be > 0")
    if intensity <= 0:
        raise ValueError("intensity must be > 0")
    if payload_size_bytes <= 0:
        raise ValueError("payload_size_bytes must be > 0")

    operation_indices = list(range(start_index, start_index + batch_size))
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=worker_count) as pool:
        checksums = list(
            pool.map(
                lambda idx: _hash_operation(
                    op_index=idx,
                    intensity=intensity,
                    payload_size_bytes=payload_size_bytes,
                ),
                operation_indices,
            )
        )
    elapsed = max(time.perf_counter() - started, 1e-9)

    combined = hashlib.sha256("|".join(checksums).encode("utf-8")).hexdigest()
    return WorkloadResult(
        operations_completed=batch_size,
        elapsed_seconds=elapsed,
        operations_per_second=batch_size / elapsed,
        checksum=combined,
    )
