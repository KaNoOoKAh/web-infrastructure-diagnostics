# web-infrastructure-diagnostics

Real-time monitoring and analysis of global web infrastructure health, physical system stress, and atmospheric influences on internet performance.

## True Intent: The Somatic Research Nexus

This repository is a **framework for discovering and teaching reproducible patterns across three interconnected domains: objective environment (weather, atmospheric data), subjective somatic-cognitive state (mind, body, sensory experience), and system metrics (network latency, infrastructure health).** Rather than treating these as separate concerns, the nexus demonstrates that the same scientific method—predict before testing, establish baselines, detect real deviations from noise, explain why changes occur, and store lessons for future reference—applies universally. By formalizing the **hypothesis → prediction → measurement → comparison → lesson loop**, this project enables researchers, practitioners, and individuals to move from anecdotal observation to reproducible, compounding knowledge across personal states, technical systems, and environmental factors.

---

## Project Vision

This repository serves as both a **production-ready monitoring framework** and an **experimental laboratory** for understanding how infrastructure, environment, and human state interact. It combines:
- Real CPU workload execution with authentic telemetry collection
- Historical baselines for day-over-day performance analysis
- Python 2-to-3 compatibility research and automated error education
- System-level metrics (CPU, memory, disk I/O, load, temperature)
- Location-aware profiling and anomaly detection
- Personal experiment logging and somatic-environmental correlation analysis
- Structured methods for turning observations into lessons

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
│   ├── sitecustomize.py                # Global exception hook & analysis
│   ├── Recording_Live_Data_www.md      # Notes on live data collection
│   └── Ocular Acknowledgment/          # Research notes and explorations
│
├── scripts/                            # Utility & analysis scripts
│   ├── sentinel_runner.py              # Compatibility shim + learning system
│   ├── experiment_journal.py           # Personal experiment tracking (hypothesis→prediction→result→lesson)
│   ├── personal_baseline.py            # Detect real deviations in personal metrics vs. noise
│   ├── predict_vs_actual.py            # Calibration tool for improving prediction accuracy
│   ├── ab_test.py                      # Simple A/B testing framework with baseline matching
│   ├── mistake_to_lesson.py            # Turn failures into stored, compounding lessons
│   ├── somatIC_loggEr3.py              # Somatic-cognitive environmental & status logger
│   ├── heartbeat.py                    # Network latency collection daemon
│   ├── analyze_heartbeat.py            # Heartbeat data analysis
│   ├── calcium_world.py                # Environmental data processing
│   └── other utility scripts            # Data validation, transmission, health checks
│
├── docs/                               # Documentation
│   ├── learning_loop.md                # Method guide: hypothesis→prediction→test→result→lesson
│   └── NEXUS_RESEARCH_METHOD.md        # Unified framework for somatic research
│
├── data/                               # Observation data storage
│   ├── experiment_journal.jsonl        # Personal experiment records
│   ├── raw/heartbeat/                  # Network latency measurements
│   ├── research/                       # Research datasets
│   ├── 2026-10-9-Observation_Data.md   # Example observation records
│   └── Internet_and_Ping.md            # Network connectivity analysis
│
├── observations/                       # Analysis & reports
│   ├── templates/
│   │   ├── personal_experiment_template.md    # Fill-in form for personal experiments
│   │   └── hotzone_observation_template.md    # Infrastructure observation template
│   ├── 2026-10-10-Padakun_*.md         # Detailed location-based findings
│   ├── 2026-10-10-lightbulb_observation.md   # Anomaly reports
│   ├── 2926-10-9-Interference_Report.md      # Pattern analysis
│   └── github_anomaly.md               # System-level anomalies
│
├── coding_paradigms.md                 # Theory: code syntax & paradigms
├── research_brief_markdown_escape_failures.md # Analysis of automation issues
└── README.md                           # This file

```

---

## Core Framework: The Learning Loop

At the heart of this nexus is a universal method that works for infrastructure metrics, personal habits, and somatic state:

1. **Predict first** (write it down before testing to prevent hindsight bias)
2. **Establish baselines** (historical same-time-of-day reference to distinguish signal from noise)
3. **Measure and record** (capture authentic data, never synthetic fallbacks)
4. **Compare** (calculate deviation %; is this real change or normal variation?)
5. **Capture surprise** (the gap between prediction and reality is where learning happens)
6. **Store the lesson** (write findings to JSON so knowledge compounds over time)

This loop is implemented across four domains:

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

### 2. **Sentinel Learning System** (`scripts/sentinel_runner.py` + `Practice/sitecustomize.py`)

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
- `scripts/sentinel_runner.py`: Main orchestration (~400 lines)
- `Practice/sitecustomize.py`: Global exception hook (~280 lines)
- `Practice/procciuti_corrections/`: JSON knowledge base (auto-generated)

---

### 3. **Personal Experiment & Somatic Learning Tools** (`scripts/`)

**Purpose**: Apply the learning loop to personal observation, habits, and somatic state.

#### **experiment_journal.py** — Hypothesis Tracking

Lock in predictions *before* testing, then compare with reality:

```bash
# Start: record hypothesis and prediction before testing
python scripts/experiment_journal.py start \
  "Walking 10 min after lunch improves my 3pm focus" \
  --prediction "focus rating >= 7 on 4 of 5 days" \
  --metric focus_1_to_10

# Record: add data points during testing
python scripts/experiment_journal.py record <id> --value 8 --note "felt clear"
python scripts/experiment_journal.py record <id> --value 6 --note "tired"

# Close: record surprise and lesson learned
python scripts/experiment_journal.py close <id> \
  --surprise "weekend days differed from weekdays" \
  --lesson "control for sleep quality; weekday routine matters more"

# Review: see all experiments, predictions, and lessons
python scripts/experiment_journal.py review
```

#### **personal_baseline.py** — Signal vs. Noise

Distinguish real changes in your metrics from random variation:

```bash
python scripts/personal_baseline.py --metric focus --value 8 --time-of-day 15:00
# Compares today's value against your historical 3pm average
# Flags if deviation > threshold (default 15%)
```

#### **predict_vs_actual.py** — Calibration

Train yourself to make better predictions by scoring accuracy over time:

```bash
python scripts/predict_vs_actual.py record \
  --event "morning coffee" --prediction "focus +2" --actual 1.5
# Logs deviation; helps you see if you're overconfident or underestimating
```

#### **ab_test.py** — Controlled Comparison

Change one variable, keep a control, compare objectively:

```bash
python scripts/ab_test.py analyze \
  --treatment "coffee days" --control "no-coffee days" \
  --metric energy --time-of-day 10:00
# Uses same-time-of-day baseline matching (like real_monitor does)
```

#### **mistake_to_lesson.py** — Failure as Data

Turn any failure or unexpected result into a stored lesson:

```bash
python scripts/mistake_to_lesson.py log \
  --what-happened "planned 30 min run, only did 10 min" \
  --context "rainy day, low mood" \
  --why "underestimated weather impact on motivation"
# Generates lesson JSON; patterns emerge after multiple entries
```

---

### 4. **Somatic-Environmental Monitoring** (`scripts/somatIC_loggEr3.py` + `scripts/heartbeat.py`)

**Purpose**: Capture the objective environment and subjective state simultaneously, with full provenance.

#### **somatIC_loggEr3.py** — Somatic-Cognitive Logger

Collects objective weather data and subjective state in a single packet:

```bash
python scripts/somatIC_loggEr3.py
# Queries Open-Meteo API for real weather (temperature, humidity, wind, pressure)
# Prompts user to log: mind status, body status, environmental perception
# Saves locally and optionally transmits to cloud endpoint
# Creates records suitable for correlation analysis
```

#### **heartbeat.py** — Network Latency Daemon

Minimalist collection of network latency with full measurement integrity:

```bash
python scripts/heartbeat.py
# Pings endpoint (8.8.8.8, configurable) every 5 minutes
# Records with UTC timestamp, config hash, provenance
# Writes atomically to JSON; never synthetic data
# Runs as a daemon for 48h or custom duration
```

---

### 5. **Coding Paradigms Theory** (`coding_paradigms.md`)

**Purpose**: Educational reference on how values, variables, and structures are declared across languages.

**Covers**:
- HTML attribute-value assignment
- JavaScript imperative/procedural patterns (let, const, var)
- Python dynamic typing
- Functional/declarative approaches
- Container transformations (map, filter, etc.)

---

### 6. **Research Documentation** (`docs/`)

#### **docs/learning_loop.md** — Beginner's Guide

Explains why the learning loop works and how to apply it:
- Why predicting first matters (hindsight bias prevention)
- Why baselines matter (noise vs. signal)
- Why changing one variable at a time matters (causality)
- Why recording surprises matters (mental model fixes)
- Why writing lessons down matters (vs. forgetting)

Includes a worked non-tech example (sleep → morning focus).

#### **docs/NEXUS_RESEARCH_METHOD.md** — Unified Framework

Unifies the three domains (infrastructure, environment, somatic state) under one method.

---

## Data & Observations

- **`data/`**: Raw observations from monitoring runs, network heartbeats, and personal experiments
  - `experiment_journal.jsonl` — Personal experiment records
  - `raw/heartbeat/` — Network latency measurements
  - `*.md` — Timestamped observation records
- **`observations/`**: Analysis reports, baselines, anomaly flags, and lessons
  - `templates/` — Standardized forms for consistent logging
  - `*.md` — Detailed findings by location, theme, and time period

---

## Concepts & Design

### Real vs. Synthetic Metrics

This project prioritizes **authentic execution** over fabricated data:
- CPU workload is real hash computation (not simulated load)
- Network measurements are actual pings (not fabricated latency)
- Somatic state is subjective report (not inferred or synthetic)
- Metrics are collected from actual system state
- Unavailable metrics are stored as `NULL` (never synthetic fallbacks)
- Errors are real exceptions, not constructed scenarios

### Day-over-Day & Baseline Analysis

The analyzer compares new observations against historical baselines:
```
Baseline: Same time-of-day, same location, same workload settings
Compare: Latest run's metrics vs. historical average
Report: Deviation %, anomaly flags, insufficient-history warnings
```

This enables:
- Detecting performance regressions over time
- Understanding load patterns at specific times
- Validating infrastructure changes
- Identifying real shifts in personal metrics vs. random variation
- Building predictive intuition over time

### Location & Context Profiles

Locations are manually configured (JSON) to represent:
- Physical deployment sites (office-a, datacenter-1, etc.)
- Local timezone & time-of-day buckets
- Custom metadata (network profile, hardware, region, atmospheric conditions)
- Environmental baselines for somatic correlation

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

### Quick Start: Personal Experiment Tracking

```bash
# Start an experiment with locked-in prediction
python scripts/experiment_journal.py start \
  "My hypothesis about personal behavior" \
  --prediction "Quantified prediction here" \
  --metric metric_name

# Record data points as you test
python scripts/experiment_journal.py record <id> --value 42 --note "context"

# Close with surprise and lesson
python scripts/experiment_journal.py close <id> \
  --surprise "What you didn't expect" \
  --lesson "What you learned"

# Review all experiments
python scripts/experiment_journal.py review
```

### Quick Start: Sentinel Learning System

```bash
# Run Python 2 code through Sentinel's learning system
python scripts/sentinel_runner.py

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
- [ ] Dashboard for historical baselines and anomaly visualization
- [ ] Export data to CSV/Parquet for analysis in Pandas/DuckDB
- [ ] Correlation analysis between somatic state and environmental conditions
- [ ] Multi-location heartbeat collection

### Medium-term (1-3 months)
- [ ] Hardware sensor adapters (battery, power, ambient sensors)
- [ ] Automatic location detection (network profile based)
- [ ] Rolling baseline models per metric
- [ ] Anomaly scoring using Z-scores and Isolation Forests
- [ ] Pattern discovery across multiple experiments

### Long-term (3+ months)
- [ ] Predictive models for personal habit optimization
- [ ] Atmospheric data correlation (weather, solar activity, geomagnetic indices)
- [ ] Integration with observability platforms (Prometheus, Grafana)
- [ ] Research publication tools (hypothesis testing, p-value calculations)
- [ ] Distributed observation network across multiple sites and researchers

---

## Key Learnings & Design Principles

1. **Safety First**: No hardware/voltage manipulation. Software-only workload controls.
2. **Real Data**: Authentic execution and metrics, never synthetic fallbacks.
3. **Learning-Driven**: System learns from errors and stores knowledge for future reference.
4. **Location-Aware**: Baseline analysis respects geographic and temporal context.
5. **Transparent Execution**: Code runs with minimal modification; analysis happens behind the scenes.
6. **Historical Context**: Day-over-day and time-of-day comparisons reveal trends and anomalies.
7. **Universal Method**: The hypothesis → prediction → measurement → comparison → lesson loop applies to infrastructure, environment, and personal state equally.
8. **Compounding Knowledge**: Each observation and lesson is stored and accessible, enabling pattern recognition over time.

---

## Cross-Repository Knowledge

This project integrates patterns and insights from related research:
- **Error handling strategies** from `procciuti_error_handler.py`
- **Code paradigm understanding** for architecture decisions
- **Markdown formatting lessons** from automation research
- **Infrastructure patterns** for monitoring design
- **Somatic-environmental correlation** from continuous observation experiments

Each component documents its approach so insights can be **applied to other projects and research domains**.

---

## Contributing

### Adding a New Monitoring Module

1. Create a subdirectory under `Practice/`
2. Include `README.md` with setup and usage
3. Add tests in `tests/`
4. Update this README with the new module description

### Adding a New Analysis Tool

1. Create a Python script in `scripts/`
2. Implement the learning loop: predict → measure → compare → lesson
3. Store findings to `data/` as JSON or JSONL
4. Document usage in this README
5. Add an example to `docs/learning_loop.md`

### Contributing Experiments & Observations

1. Use `scripts/experiment_journal.py` or fill in `observations/templates/personal_experiment_template.md`
2. Store findings in `data/` and `observations/`
3. Reference related experiments and lessons
4. Tag with location, time-of-day, and environmental conditions for correlation analysis

### Improving Tools

- Report bugs via [Issues](https://github.com/KaNoOoKAh/web-infrastructure-diagnostics/issues)
- Suggest new analysis modes or prediction models
- Contribute better baseline matching algorithms
- Share findings from personal experiments

---

## License

This project is published as-is for educational and research purposes.

---

## Latest Activity

- **PR #3**: Added personal learning loop tools and somatic research framework (in progress)
- **PR #2**: Added `Practice/real_monitor` MVP for real workload telemetry and day-over-day analysis (merged 2026-09-17)
- **PR #1**: Added research brief on markdown escape failures (merged 2026-09-14)

See [Pull Requests](https://github.com/KaNoOoKAh/web-infrastructure-diagnostics/pulls) for the full history.

---

## Questions?

Refer to the detailed docs:
- [`docs/learning_loop.md`](docs/learning_loop.md) – Method guide with worked examples
- [`docs/NEXUS_RESEARCH_METHOD.md`](docs/NEXUS_RESEARCH_METHOD.md) – Unified framework
- [`Practice/real_monitor/README.md`](Practice/real_monitor/README.md) – Setup, schema, CLI reference
- [`coding_paradigms.md`](coding_paradigms.md) – Code syntax & language theory
- `Practice/procciuti_corrections/` – JSON knowledge base from sentinel analysis
- `observations/templates/` – Standardized forms for logging experiments
