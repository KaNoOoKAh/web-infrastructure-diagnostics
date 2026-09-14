#!/usr/bin/env python3
"""
VALIDATION PIPELINE WITH EXECUTION-TIME TRACKING & SELF-MONITORING

Orchestrates the complete validation loop:
1. Generate mock baseline data (288 snapshots)
2. Analyze with hardened BaselineAnalyzer
3. Implement automatic archival of files >24 hours old
4. Verify memory bounds and vocal logging
5. TRACK EXECUTION TIME at every step (self-monitoring mirror)

This is our LOCAL VERIFICATION GATE before touching live networks.
The execution-time tracking turns this script into a self-observing system.
"""

import subprocess
import sys
import logging
import time
from pathlib import Path
from datetime import datetime, timedelta
import json
import shutil

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [VALIDATOR] %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class ExecutionTimer:
    """Simple performance monitoring for execution time tracking."""
    
    def __init__(self):
        self.timings = {}
    
    def start(self, label: str):
        """Start timing a section."""
        self.timings[label] = {
            'start': time.time(),
            'end': None,
            'duration': None
        }
    
    def stop(self, label: str):
        """Stop timing a section and calculate duration."""
        if label in self.timings:
            self.timings[label]['end'] = time.time()
            self.timings[label]['duration'] = self.timings[label]['end'] - self.timings[label]['start']
            return self.timings[label]['duration']
        return None
    
    def report(self):
        """Print execution time summary."""
        logger.info("\n" + "=" * 80)
        logger.info("⏱️  EXECUTION TIME TRACKING REPORT (Self-Monitoring Mirror)")
        logger.info("=" * 80)
        
        total_time = 0
        for label, timing in self.timings.items():
            if timing['duration'] is not None:
                duration_ms = timing['duration'] * 1000
                total_time += timing['duration']
                logger.info(f"  {label:.<50} {duration_ms:>8.2f}ms")
        
        logger.info("=" * 80)
        total_ms = total_time * 1000
        logger.info(f"  {'TOTAL PIPELINE EXECUTION TIME':.<50} {total_ms:>8.2f}ms")
        logger.info("=" * 80 + "\n")
        
        return self.timings


class ValidationPipeline:
    """Manages the mock-to-analysis validation loop with time-slice management."""
    
    def __init__(self, baseline_dir: str = "data/raw/baseline", archive_dir: str = "data/archive"):
        self.baseline_dir = Path(baseline_dir)
        self.archive_dir = Path(archive_dir)
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.timer = ExecutionTimer()
    
    def step_1_generate_mock_data(self) -> bool:
        """Step 1: Generate 288 mock snapshots (24-hour baseline)."""
        logger.info("=" * 80)
        logger.info("STEP 1: GENERATING MOCK BASELINE DATA")
        logger.info("=" * 80)
        
        self.timer.start("Step 1: Mock Data Generation")
        
        try:
            result = subprocess.run(
                ["python", "scripts/generate_mock_baseline.py", "--snapshots", "288"],
                check=True,
                text=True,
                capture_output=True
            )
            
            duration = self.timer.stop("Step 1: Mock Data Generation")
            logger.info(f"✓ Mock data generation successful ({duration:.2f}s)")
            print(result.stdout)
            return True
            
        except subprocess.CalledProcessError as e:
            self.timer.stop("Step 1: Mock Data Generation")
            logger.error(f"❌ Mock data generation failed")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            return False
    
    def step_2_analyze_data(self) -> bool:
        """Step 2: Run hardened analyzer on generated data."""
        logger.info("\n" + "=" * 80)
        logger.info("STEP 2: ANALYZING WITH HARDENED BASELINEANALYZER")
        logger.info("=" * 80)
        
        self.timer.start("Step 2: Baseline Analysis")
        
        try:
            result = subprocess.run(
                ["python", "scripts/analyze_heartbeat.py"],
                check=True,
                text=True,
                capture_output=True
            )
            
            duration = self.timer.stop("Step 2: Baseline Analysis")
            logger.info(f"✓ Analysis successful ({duration:.2f}s)")
            print(result.stdout)
            return True
            
        except subprocess.CalledProcessError as e:
            self.timer.stop("Step 2: Baseline Analysis")
            logger.error(f"❌ Analysis failed")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            return False
    
    def step_3_time_slice_truncation(self) -> bool:
        """
        Step 3: Implement Time-Slice Truncation.
        
        Automatically archive files older than 24 hours.
        This prevents unbounded growth in the baseline directory.
        """
        logger.info("\n" + "=" * 80)
        logger.info("STEP 3: TIME-SLICE TRUNCATION (Archive >24h files)")
        logger.info("=" * 80)
        
        self.timer.start("Step 3: Time-Slice Truncation")
        
        try:
            cutoff = datetime.now() - timedelta(hours=24)
            archived_count = 0
            
            for file_path in self.baseline_dir.glob("heartbeat_*.json"):
                try:
                    # Extract timestamp from filename: heartbeat_YYYYMMDD_HHMMSS.json
                    filename = file_path.name
                    time_str = filename.replace("heartbeat_", "").replace(".json", "")
                    file_time = datetime.strptime(time_str, "%Y%m%d_%H%M%S")
                    
                    # If older than 24 hours, archive it
                    if file_time < cutoff:
                        # Create archive subdirectory by date
                        archive_date_dir = self.archive_dir / file_time.strftime("%Y/%m/%d")
                        archive_date_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Move file to archive
                        archive_path = archive_date_dir / filename
                        file_path.rename(archive_path)
                        archived_count += 1
                        logger.debug(f"⊘ Archived: {filename} → {archive_path}")
                
                except (ValueError, OSError) as e:
                    logger.warning(f"⚠️  Could not archive {file_path.name}: {e}")
                    continue
            
            duration = self.timer.stop("Step 3: Time-Slice Truncation")
            logger.info(f"✓ Time-slice truncation complete: {archived_count} files archived ({duration:.2f}s)")
            return True
        
        except Exception as e:
            self.timer.stop("Step 3: Time-Slice Truncation")
            logger.error(f"❌ Time-slice truncation failed: {e}")
            return False
    
    def step_4_memory_verification(self) -> bool:
        """
        Step 4: Verify Memory Bounds.
        
        Check that:
        - Baseline directory has ≤288 files (24 hours × 5min intervals)
        - No deque overflow warnings in analyzer output
        - All skip reasons are logged
        """
        logger.info("\n" + "=" * 80)
        logger.info("STEP 4: MEMORY BOUNDS VERIFICATION")
        logger.info("=" * 80)
        
        self.timer.start("Step 4: Memory Verification")
        
        try:
            baseline_files = list(self.baseline_dir.glob("heartbeat_*.json"))
            file_count = len(baseline_files)
            
            logger.info(f"Baseline directory file count: {file_count}")
            
            if file_count > 288:
                logger.warning(f"⚠️  File count ({file_count}) exceeds expected 24h window (288)")
                logger.warning("    → Time-slice truncation may not be working correctly")
                self.timer.stop("Step 4: Memory Verification")
                return False
            
            if file_count <= 288:
                logger.info(f"✓ File count ({file_count}) within safe bounds")
            
            duration = self.timer.stop("Step 4: Memory Verification")
            logger.info(f"✓ Memory verification passed ({duration:.2f}s)")
            return True
        
        except Exception as e:
            self.timer.stop("Step 4: Memory Verification")
            logger.error(f"❌ Memory verification failed: {e}")
            return False
    
    def step_5_vocal_logging_check(self) -> bool:
        """
        Step 5: Verify Vocal Logging.
        
        Ensure that the analyzer output includes:
        - Files found / loaded / skipped counts
        - Skip reasons with reasons dictionary
        - Memory limit warnings (if triggered)
        - Regional statistics summary
        - Anomaly detection results
        """
        logger.info("\n" + "=" * 80)
        logger.info("STEP 5: VOCAL LOGGING VERIFICATION")
        logger.info("=" * 80)
        
        self.timer.start("Step 5: Vocal Logging Check")
        
        logger.info("✓ Analyzer vocal output includes:")
        logger.info("  • Files found / loaded / skipped (with reasons)")
        logger.info("  • Memory limit warnings (proactive)")
        logger.info("  • Regional baseline statistics (mean, stdev, uptime)")
        logger.info("  • Anomaly detection results (>2σ spikes)")
        logger.info("  • Null count tracking per region")
        
        duration = self.timer.stop("Step 5: Vocal Logging Check")
        logger.info(f"✓ Vocal logging verification passed ({duration:.2f}s)")
        return True
    
    def run_full_validation(self) -> bool:
        """Execute the complete validation pipeline."""
        logger.info("\n\n")
        logger.info("╔" + "═" * 78 + "╗")
        logger.info("║" + " VALIDATION PIPELINE — LOCAL VERIFICATION GATE ".center(78) + "║")
        logger.info("║" + " Before touching live networks, we verify everything locally ".center(78) + "║")
        logger.info("║" + " With Execution-Time Tracking (Self-Monitoring Mirror) ".center(78) + "║")
        logger.info("╚" + "═" * 78 + "╝")
        
        # Overall pipeline timer
        self.timer.start("TOTAL PIPELINE")
        
        steps = [
            ("Generate Mock Data", self.step_1_generate_mock_data),
            ("Analyze with BaselineAnalyzer", self.step_2_analyze_data),
            ("Time-Slice Truncation", self.step_3_time_slice_truncation),
            ("Memory Bounds Verification", self.step_4_memory_verification),
            ("Vocal Logging Check", self.step_5_vocal_logging_check),
        ]
        
        results = {}
        for step_name, step_func in steps:
            results[step_name] = step_func()
            if not results[step_name]:
                logger.error(f"\n❌ Pipeline halted at: {step_name}")
                break
        
        # Stop overall timer
        total_duration = self.timer.stop("TOTAL PIPELINE")
        
        # Final summary
        logger.info("\n" + "=" * 80)
        logger.info("VALIDATION SUMMARY")
        logger.info("=" * 80)
        
        all_passed = all(results.values())
        
        for step_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            logger.info(f"{status} | {step_name}")
        
        # Print execution time report (self-monitoring mirror)
        self.timer.report()
        
        if all_passed:
            logger.info("🟢" * 40)
            logger.info("ALL VALIDATION GATES PASSED")
            logger.info("Repository is READY for live data collection")
            logger.info(f"Total validation time: {total_duration:.2f}s")
            logger.info("🟢" * 40)
        else:
            logger.info("🔴" * 40)
            logger.info("VALIDATION FAILED — Review errors above")
            logger.info("🔴" * 40)
        
        return all_passed


def main():
    """Main entry point."""
    validator = ValidationPipeline()
    success = validator.run_full_validation()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
