from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_run, render_analysis, summarize_anomalies
from .config import DEFAULT_CONFIG_PATH, MonitorConfig
from .db import DatabaseManager
from .runner import run_with_overrides


def _load_config(path: str | None) -> MonitorConfig:
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    return MonitorConfig.from_file(config_path)


def _common_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="Path to JSON config")
    parser.add_argument("--db-path", help="SQLite database path override")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Real workload monitor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_db_parser = subparsers.add_parser("init-db", help="Initialize SQLite schema")
    _common_parser(init_db_parser)

    run_parser = subparsers.add_parser("run", help="Run monitoring session")
    _common_parser(run_parser)
    run_parser.add_argument("--location-id")
    run_parser.add_argument("--location-label")
    run_parser.add_argument("--location-timezone")
    run_parser.add_argument("--location-notes")
    run_parser.add_argument("--worker-count", type=int)
    run_parser.add_argument("--batch-size", type=int)
    run_parser.add_argument("--intensity", type=int)
    run_parser.add_argument("--payload-size-bytes", type=int)
    run_parser.add_argument("--sampling-interval", type=float)
    run_parser.add_argument("--duration", type=float, help="Duration in seconds")

    list_locations_parser = subparsers.add_parser(
        "list-locations", help="List location profiles from DB"
    )
    _common_parser(list_locations_parser)

    analyze_parser = subparsers.add_parser("analyze", help="Analyze run vs historical baselines")
    _common_parser(analyze_parser)
    analyze_parser.add_argument("--run-id", help="Run id to analyze (defaults to latest)")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    cfg = _load_config(args.config)
    if args.db_path:
        cfg = cfg.with_overrides(database_path=args.db_path)

    db = DatabaseManager(cfg.database_path)

    if args.command == "init-db":
        db.init_db()
        print(f"Initialized database at {cfg.database_path}")
        return 0

    if args.command == "run":
        run_id = run_with_overrides(
            cfg,
            database_path=args.db_path,
            location_id=args.location_id,
            location_label=args.location_label,
            location_timezone=args.location_timezone,
            location_notes=args.location_notes,
            worker_count=args.worker_count,
            batch_size=args.batch_size,
            intensity=args.intensity,
            payload_size_bytes=args.payload_size_bytes,
            sampling_interval_seconds=args.sampling_interval,
            duration_seconds=args.duration,
        )
        print(f"Run finished. run_id={run_id}")
        return 0

    if args.command == "list-locations":
        db.init_db()
        rows = db.list_locations()
        if not rows:
            print("No locations found.")
            return 0
        for row in rows:
            print(
                f"{row['location_id']}: {row['label']} timezone={row['timezone']} notes={row['notes']}"
            )
        return 0

    if args.command == "analyze":
        db.init_db()
        rows = analyze_run(db=db, analyzer_cfg=cfg.analyzer, run_id=args.run_id)
        print(render_analysis(rows))
        summary = summarize_anomalies(rows)
        print(
            f"Summary: total={summary['total_rows']} anomalies={summary['anomaly_rows']} insufficient_history={summary['insufficient_history_rows']}"
        )
        return 0

    parser.error("Unknown command")
    return 2
