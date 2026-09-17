from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import AnalyzerConfig
from .db import DatabaseManager


@dataclass(frozen=True)
class AnalysisRow:
    run_id: str
    time_of_day_bucket: str
    location_id: str
    worker_count: int
    batch_size: int
    intensity: int
    current_avg_ops: float | None
    baseline_avg_ops: float | None
    ops_deviation_percent: float | None
    baseline_samples: int
    anomaly: bool
    note: str


def _deviation_percent(current: float | None, baseline: float | None) -> float | None:
    if current is None or baseline is None or baseline == 0:
        return None
    return ((current - baseline) / baseline) * 100.0


def analyze_run(
    db: DatabaseManager,
    analyzer_cfg: AnalyzerConfig,
    run_id: str | None = None,
) -> list[AnalysisRow]:
    selected_run_id = run_id or db.get_latest_run_id()
    if selected_run_id is None:
        return []

    current_groups = db.get_observation_groups_for_run(selected_run_id)
    rows: list[AnalysisRow] = []

    for current in current_groups:
        baseline = db.get_historical_group_baseline(
            time_of_day_bucket=str(current["time_of_day_bucket"]),
            location_id=str(current["location_id"]),
            worker_count=int(current["worker_count"]),
            batch_size=int(current["batch_size"]),
            intensity=int(current["intensity"]),
            exclude_run_id=selected_run_id,
        )

        current_avg_ops = (
            None if current.get("avg_ops") is None else float(current["avg_ops"])
        )
        baseline_avg_ops = (
            None if baseline.get("avg_ops") is None else float(baseline["avg_ops"])
        )
        baseline_samples = int(baseline.get("sample_count") or 0)
        deviation = _deviation_percent(current_avg_ops, baseline_avg_ops)

        anomaly = False
        note = "ok"
        if baseline_samples < analyzer_cfg.min_baseline_samples:
            note = "insufficient_history"
        else:
            if deviation is not None and abs(deviation) >= analyzer_cfg.anomaly_threshold_percent:
                anomaly = True
                note = "anomaly"

        rows.append(
            AnalysisRow(
                run_id=selected_run_id,
                time_of_day_bucket=str(current["time_of_day_bucket"]),
                location_id=str(current["location_id"]),
                worker_count=int(current["worker_count"]),
                batch_size=int(current["batch_size"]),
                intensity=int(current["intensity"]),
                current_avg_ops=current_avg_ops,
                baseline_avg_ops=baseline_avg_ops,
                ops_deviation_percent=deviation,
                baseline_samples=baseline_samples,
                anomaly=anomaly,
                note=note,
            )
        )

    return rows


def render_analysis(rows: list[AnalysisRow]) -> str:
    if not rows:
        return "No runs or observations found."

    lines = [
        "time_bucket location settings current_ops baseline_ops deviation% baseline_samples flag",
    ]
    for row in rows:
        settings = f"w{row.worker_count}/b{row.batch_size}/i{row.intensity}"
        current_ops = "null" if row.current_avg_ops is None else f"{row.current_avg_ops:.2f}"
        baseline_ops = "null" if row.baseline_avg_ops is None else f"{row.baseline_avg_ops:.2f}"
        deviation = "null" if row.ops_deviation_percent is None else f"{row.ops_deviation_percent:.2f}"
        flag = "ANOMALY" if row.anomaly else row.note
        lines.append(
            f"{row.time_of_day_bucket} {row.location_id} {settings} {current_ops} {baseline_ops} {deviation} {row.baseline_samples} {flag}"
        )
    return "\n".join(lines)


def summarize_anomalies(rows: list[AnalysisRow]) -> dict[str, Any]:
    return {
        "total_rows": len(rows),
        "anomaly_rows": sum(1 for row in rows if row.anomaly),
        "insufficient_history_rows": sum(1 for row in rows if row.note == "insufficient_history"),
    }
