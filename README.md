# web-infrastructure-diagnostics

Real-time monitoring and analysis of global web infrastructure health, physical system stress, and atmospheric influences on internet performance.

## Project Vision

This repository serves as both a **production-ready monitoring framework** and an **experimental laboratory** for understanding infrastructure dynamics. It combines:
- Real CPU workload execution with authentic telemetry collection
- Historical baselines for day-over-day performance analysis
- Python 2-to-3 compatibility research and automation
- System-level metrics (CPU, memory, disk I/O, load, temperature)
- Location-aware profiling and anomaly detection

---

## Repository Structure

```
web-infrastructure-diagnostics/
├── Practice/                           # Experimental modules & research
│   ├── real_monitor/                   # MVP: Real workload telemetry framework
│   │   ├── __main__.py                 # CLI entry point
│   │   ├── cli.py                      # Command-line interface
│   │   ├── config.py                   # Configuration parsing & validation
│   │   ├── workload.py                 # Repeatable CPU workload generator
│   │   ├── metrics.py                  # Host/process metrics collection
│   │   ├── db.py                       # SQLite schema & persistence
│   │   ├── runner.py                   # Execution orchestration
│   │   ├── analyzer.py                 # Historical baseline analysis
│   │   ├── default_config.json         # Default CLI configuration
│   │   ├── requirements.txt            # Optional dependencies (richer metrics)
│   │   ├── README.md                   # Complete setup & usage guide
│   │   └── tests/                      # pytest fixtures for workload/config/db
│   │
│   ├── Procciuti.py                    # Legacy Python 2 reference script
│   ├── procciuti_error_handler.py      # Comprehensive error handling patterns
│   ├── procciuti_corrections/          # Knowledge base (JSON reports)
│   ├── Recording_Live_Data_www.md      # Notes on live data collection
│   └── Procciuti.py                    # Usage reference
│
├── sentine_runner.py                   # Compatibility shim + learning system
├── sitecustomize.py                    # Global exception hook & analysis
├── coding_paradigms.md                 # Theory: code syntax & paradigms
├── research_brief_markdown_escape_failures.md # Analysis of automation issues
├── data/                               # Observation data storage
├── observations/                       # Analysis & reports
├── scripts/                            # Utility scripts
└── README.md                           # This file

```

---

## Key Components

### 1. **real_monitor MVP** (`Practice/real_monitor/`)

**Purpose**: A production-safe monitoring framework for real workload telemetry and historical analysis.

**Features**:
- **Real CPU workload**: Hash-based repeatable computation (no synthetic data)
- **Comprehensive metrics**: CPU, memory, disk I/O, load average, temperature (when available)
- **SQLite persistence**: Schema with indexes for fast time-of-day & location queries
- **Day-over-day analysis**: Compare runs against historical baselines for same time/location/workload
- **Config-driven**: JSON defaults with CLI overrides
- **Safety-first**: Software-only controls (worker count, batch size, intensity) — no hardware/voltage manipulation

**Setup** (5 minutes):
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
# Optional: install psutil/dataclasses-json for richer metrics
python -m pip install -r Practice/real_monitor/requirements.txt
```

**Usage**:
```bash
# Initialize database
python -m Practice.real_monitor init-db

# Run a 15-minute workload test
python -m Practice.real_monitor run --location-id office-a --duration 900

# Analyze the latest run
python -m Practice.real_monitor analyze

# List configured locations
python -m Practice.real_monitor list-locations
```

See [`Practice/real_monitor/README.md`](Practice/real_monitor/README.md) for detailed documentation.

---

### 2. **Sentinel Learning System** (`sentinel_runner.py` + `sitecustomize.py`)

**Purpose**: Automated compatibility analysis and error education for Python 2 ↔ 3 migration.

**How it works**:
- **Pre-scan**: Detects deprecated patterns before execution (e.g., `.has_key()`)
- **Compatibility shim**: Dynamically restores Python 2 methods (`.has_key()` via `in` operator)
- **Exception interception**: Global hook catches unhandled errors and analyzes them
- **Learning storage**: Saves findings to JSON for future reference
- **Transparent execution**: Legacy scripts run unmodified; learning happens in background

**Why this approach**:
- Original code (Procciuti.py) remains untouched
- Processor learns WHY changes were needed, not just THAT they were needed
- Knowledge is automatically stored for pattern recognition
- Bridges Python 2 → 3 migration without hand-editing

**Key Files**:
- `sentinel_runner.py`: Main orchestration (9 KB, ~400 lines)
- `sitecustomize.py`: Global exception hook (11 KB, ~280 lines)
- `Practice/procciuti_corrections/`: JSON knowledge base (auto-generated)

---

### 3. **Coding Paradigms Theory** (`coding_paradigms.md`)

**Purpose**: Educational reference on how values, variables, and structures are declared across languages.

**Covers**:
- HTML attribute-value assignment
- JavaScript imperative/procedural patterns (let, const, var)
- Python dynamic typing
- Functional/declarative approaches
- Container transformations (map, filter, etc.)

---

### 4. **Research Brief** (`research_brief_markdown_escape_failures.md`)

**Purpose**: Analysis of markdown escape failures in automated prompting systems.

**Topics**:
- Environmental influences on text formatting
- Root causes of escape sequence mishandling
- Engineering recommendations for GitHub and Copilot UI

---

## Data & Observations

- **`data/`**: Raw observations from monitoring runs (SQLite DB or CSV exports)
- **`observations/`**: Analysis reports, baselines, anomaly flags
- **`scripts/`**: Utility scripts for data import/export, visualization

---

## Concepts & Design

### Real vs. Synthetic Metrics

This project prioritizes **authentic execution** over fabricated data:
- CPU workload is real hash computation (not simulated load)
- Metrics are collected from actual process/system state
- Unavailable metrics are stored as `NULL` (never synthetic fallbacks)
- Errors are real exceptions, not constructed scenarios

### Day-over-Day Analysis

The analyzer compares new runs against historical baselines:
```
Baseline: Same time-of-day, same location, same workload settings
Compare: Latest run's metrics vs. historical average
Report: Deviation %, anomaly flags, insufficient-history warnings
```

This enables:
- Detecting performance regressions over time
- Understanding load patterns at specific times
- Validating infrastructure changes

### Location Profiles

Locations are manually configured (JSON) to represent:
- Physical deployment sites (office-a, datacenter-1, etc.)
- Local timezone & time-of-day buckets
- Custom metadata (network profile, hardware, region)

---

## Getting Started

### Quick Start: Real Monitoring

```bash
# 1. Clone & setup
git clone https://github.com/KaNoOoKAh/web-infrastructure-diagnostics.git
cd web-infrastructure-diagnostics
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip

# 2. Install optional metrics dependencies
pip install -r Practice/real_monitor/requirements.txt

# 3. Initialize database
python -m Practice.real_monitor init-db

# 4. Run a monitoring session
python -m Practice.real_monitor run --location-id office-a --duration 300

# 5. Analyze results
python -m Practice.real_monitor analyze
```

### Understanding Legacy Code & Migrations

```bash
# Run Python 2 code through Sentinel's learning system
python sentinel_runner.py

# This will:
# 1. Inject .has_key() compatibility
# 2. Pre-scan for deprecated patterns
# 3. Execute the legacy script
# 4. Generate comprehensive analysis report
# 5. Store findings in Practice/procciuti_corrections/
```

---

## Configuration

### real_monitor Configuration

Default config: `Practice/real_monitor/default_config.json`

```json
{
  "database_path": "observations/real_monitor.db",
  "location": {
    "location_id": "office-a",
    "timezone": "US/Hawaii"
  },
  "workload": {
    "worker_count": 4,
    "batch_size": 200,
    "intensity": 150
  },
  "runner": {
    "sampling_interval_seconds": 20,
    "duration_seconds": 900
  },
  "analyzer": {
    "min_baseline_samples": 5,
    "anomaly_threshold_percent": 15
  }
}
```

Override via CLI:
```bash
python -m Practice.real_monitor run \
  --location-id datacenter-1 \
  --worker-count 8 \
  --batch-size 500 \
  --intensity 200 \
  --duration 1800
```

---

## Testing

```bash
cd Practice/real_monitor
python -m pytest tests/ -v

# Test categories:
# - workload: repeatability, valid output
# - config: parsing, validation, CLI overrides
# - db: schema, indexing, write/read grouping
# - analyzer: baseline matching, anomaly detection
```

---

## Roadmap

### Short-term (0-1 month)
- [ ] Add GitHub Actions CI workflow for scheduled monitoring
- [ ] Export data to CSV/Parquet for analysis in Pandas/DuckDB
- [ ] Dashboard for historical baselines and anomaly visualization

### Medium-term (1-3 months)
- [ ] Multi-location distributed monitoring
- [ ] Hardware sensor adapters (battery, power, ambient sensors)
- [ ] Automatic location detection (network profile based)
- [ ] Rolling baseline models per metric
- [ ] Anomaly scoring using Z-scores and Isolation Forests

### Long-term (3+ months)
- [ ] Correlation analysis with external events (deploys, config changes)
- [ ] Predictive models for capacity planning
- [ ] Integration with observability platforms (Prometheus, Grafana)
- [ ] Real-world atmospheric data correlation (weather, solar activity)

---

## Key Learnings & Design Principles

1. **Safety First**: No hardware/voltage manipulation. Software-only workload controls.
2. **Real Data**: Authentic execution and metrics, never synthetic fallbacks.
3. **Learning-Driven**: System learns from errors and stores knowledge for future reference.
4. **Location-Aware**: Baseline analysis respects geographic and temporal context.
5. **Transparent Execution**: Legacy code runs unmodified; analysis happens behind the scenes.
6. **Historical Context**: Day-over-day comparisons reveal trends and anomalies.

---

## Cross-Repository Knowledge

This project integrates patterns and insights from related repositories:
- **Error handling strategies** from `procciuti_error_handler.py`
- **Code paradigm understanding** for architecture decisions
- **Markdown formatting lessons** from automation research
- **Infrastructure patterns** for monitoring design

Each component documents its approach so insights can be **applied to other projects**.

---

## Contributing

### Adding a New Monitoring Module

1. Create a subdirectory under `Practice/`
2. Include `README.md` with setup and usage
3. Add tests in `tests/`
4. Update this README with the new module description

### Improving real_monitor

- Report bugs via [Issues](https://github.com/KaNoOoKAh/web-infrastructure-diagnostics/issues)
- Contribute new metric collectors (via `metrics.py` extension)
- Suggest analyzer improvements (anomaly models, baselines)

---

## License

This project is published as-is for educational and research purposes.

---

## Latest Activity

- **PR #2**: Added `Practice/real_monitor` MVP for real workload telemetry and day-over-day analysis (merged 2026-09-17)
- **PR #1**: Added research brief on markdown escape failures (merged 2026-09-14)

See [Pull Requests](https://github.com/KaNoOoKAh/web-infrastructure-diagnostics/pulls) for the full history.

---

## Questions?

Refer to the detailed docs:
- [`Practice/real_monitor/README.md`](Practice/real_monitor/README.md) – Setup, schema, CLI reference
- [`coding_paradigms.md`](coding_paradigms.md) – Code syntax & language theory
- `Practice/procciuti_corrections/` – JSON knowledge base from sentinel analysis
