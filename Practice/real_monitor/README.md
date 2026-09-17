# real_monitor MVP

Safe real-workload monitor for day-over-day comparisons in `Practice/real_monitor`.

## Safety notes
- This tool performs **software-only** workload controls (worker count, batch size, intensity).
- It does **not** control voltage or unsafe hardware settings.
- Runs without root/admin privileges.

## What is recorded
Every observation stores:
- UTC timestamp (`timestamp_utc`)
- local date/time and `time_of_day_bucket` (`HH:MM`)
- run/session id and location id
- device identity (hostname/platform)
- workload settings (worker_count, batch_size, intensity)
- operations completed, elapsed seconds, operations/sec
- process/system CPU and memory metrics
- disk I/O (if available)
- load average (if available)
- temperature (if available)
- cumulative error count

Unavailable metrics are stored as `NULL` (never fabricated).

## Database schema
- `locations`: manual location profiles
- `runs`: run/session metadata
- `observations`: periodic samples

Indexes are included for:
- UTC timestamp
- time-of-day bucket
- location id
- workload settings (worker_count, batch_size, intensity)

## Setup
From repository root:

### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
# optional richer metrics
python -m pip install -r /home/runner/work/web-infrastructure-diagnostics/web-infrastructure-diagnostics/Practice/real_monitor/requirements.txt
```

### Windows (PowerShell)
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
# optional richer metrics
python -m pip install -r C:\path\to\web-infrastructure-diagnostics\Practice\real_monitor\requirements.txt
```

## CLI usage
Default config file:
`/home/runner/work/web-infrastructure-diagnostics/web-infrastructure-diagnostics/Practice/real_monitor/default_config.json`

Initialize DB:
```bash
python -m Practice.real_monitor init-db
```

Run continuously:
```bash
python -m Practice.real_monitor run --location-id office-a --worker-count 4 --batch-size 200 --intensity 150 --sampling-interval 20
```

Run for 15 minutes:
```bash
python -m Practice.real_monitor run --location-id office-a --duration 900
```

List location profiles:
```bash
python -m Practice.real_monitor list-locations
```

Analyze latest run against historical same-time/same-location/same-settings baseline:
```bash
python -m Practice.real_monitor analyze
```

Analyze specific run:
```bash
python -m Practice.real_monitor analyze --run-id <RUN_ID>
```

## Configuration file
Use JSON values in `default_config.json`:
- `database_path`
- `location.location_id`, `label`, `timezone`, `notes`
- `workload.worker_count`, `batch_size`, `intensity`, `payload_size_bytes`
- `runner.sampling_interval_seconds`, `duration_seconds`
- `analyzer.min_baseline_samples`, `anomaly_threshold_percent`

CLI flags can override these values.

## Roadmap
- Add optional hardware sensor adapters (battery/power, external ambient sensors)
- Add safe automatic location detection (for example network profile based)
- Add richer anomaly models per metric and rolling baselines
