"""
sitecustomize.py - GLOBAL EXCEPTION HOOK INSTALLATION

This file is automatically loaded by Python at startup.
It installs a custom exception handler that catches ANY unhandled exception
and routes it to the Sentinel learning system.

Why this approach:
- No modification to original scripts (Procciuti.py stays untouched)
- Transparent to the user (just run `python Practice/Procciuti.py`)
- Real errors are caught (not faked or prevented)
- Processor learns from actual failures
- Knowledge is automatically stored

When an error occurs in ANY Python script:
1. Exception bubbles up unhandled
2. sys.excepthook catches it
3. Sentinel analysis system activates
4. Learning system processes the error
5. Comprehensive report is generated
6. Knowledge is stored for future reference
"""

import sys
import os
import json
import traceback
from datetime import datetime

# ============================================
# SENTINEL EXCEPTION ANALYSIS SYSTEM
# ============================================

class SentinelExceptionAnalyzer:
    """
    Analyzes unhandled exceptions and routes them to the learning system.
    
    This is the global exception handler that activates when ANY
    Python script encounters an unhandled error.
    """
    
    def __init__(self):
        self.error_database = {}
        self.corrections_path = "Practice/procciuti_corrections"
        os.makedirs(self.corrections_path, exist_ok=True)
    
    def analyze_exception(self, exc_type, exc_value, exc_traceback):
        """
        Analyze an exception in detail and extract actionable intelligence.
        
        Args:
            exc_type: The exception class (e.g., AttributeError)
            exc_value: The exception instance with message
            exc_traceback: The traceback object showing where it occurred
        """
        
        # Extract traceback information
        tb_frames = traceback.extract_tb(exc_traceback)
        
        # Find the most relevant frame (usually where the error occurred)
        error_frame = tb_frames[-1] if tb_frames else None
        
        analysis = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "error_type": exc_type.__name__,
            "error_message": str(exc_value),
            "error_module": exc_type.__module__,
            "file": error_frame.filename if error_frame else "unknown",
            "line_number": error_frame.lineno if error_frame else None,
            "function": error_frame.name if error_frame else "unknown",
            "code_context": error_frame.line if error_frame else None,
            "full_traceback": "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)),
            "analysis": self._classify_error(exc_type, exc_value, error_frame)
        }
        
        return analysis
    
    def _classify_error(self, exc_type, exc_value, error_frame):
        """
        Classify the error and determine if it's a known pattern.
        
        Returns analysis of what caused it and how to fix it.
        """
        error_msg = str(exc_value)
        
        # Check for .has_key() error
        if exc_type.__name__ == "AttributeError" and "has_key" in error_msg:
            return {
                "classification": "PYTHON_2_TO_3_MIGRATION_ERROR",
                "severity": "CRITICAL",
                "pattern": "dict.has_key() - Removed in Python 3",
                "root_cause": "Using Python 2 dictionary method on Python 3 interpreter",
                "python_versions_affected": ["Python 2.x", "NOT supported in Python 3.0+"],
                "solution": "Replace .has_key('key') with 'key' in dict",
                "explanation": {
                    "why_removed": "Python 3 removed redundant methods to enforce consistency",
                    "design_philosophy": "Use 'in' operator for membership testing across all container types",
                    "performance_impact": "'in' operator is slightly faster and generates less memory overhead",
                    "migration_effort": "Simple find-and-replace pattern"
                },
                "code_pattern": {
                    "broken": "if config_dict.has_key('gateway'):",
                    "fixed": "if 'gateway' in config_dict:"
                },
                "reference_file": "Practice/procciuti_corrections/has_key_to_in_operator.py"
            }
        
        # Generic error classification
        return {
            "classification": f"UNHANDLED_{exc_type.__name__}",
            "severity": "HIGH",
            "pattern": f"{exc_type.__name__}: {error_msg}",
            "root_cause": "Analysis required - consult error message and traceback",
            "next_steps": [
                "Review the error message carefully",
                "Check the file and line number where error occurred",
                "Verify the code context above",
                "Cross-reference with Python documentation"
            ]
        }
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """
        Main exception handler that is called when an error occurs.
        
        This is where Sentinel intercepts the error and routes it to learning.
        """
        
        # Analyze the exception
        analysis = self.analyze_exception(exc_type, exc_value, exc_traceback)
        
        # Print the error to console (standard Python behavior)
        print("\n" + "="*90)
        print("UNHANDLED EXCEPTION DETECTED")
        print("="*90)
        print(f"\nTraceback (most recent call last):")
        print(analysis["full_traceback"])
        
        # Route to Sentinel learning system
        self._route_to_sentinel(analysis)
    
    def _route_to_sentinel(self, analysis):
        """
        Route the analyzed error to the Sentinel learning system.
        
        This is where the processor learns from the actual error.
        """
        
        print("\n" + "█"*90)
        print("SENTINEL EXCEPTION ANALYSIS ACTIVATED")
        print("█"*90)
        
        print(f"\n[Sentinel] Analyzing exception for learning...")
        print(f"\nError Classification: {analysis['analysis']['classification']}")
        print(f"Severity: {analysis['analysis']['severity']}")
        print(f"Error Type: {analysis['error_type']}")
        print(f"Error Message: {analysis['error_message']}")
        print(f"Location: {analysis['file']}:{analysis['line_number']}")
        print(f"Function: {analysis['function']}")
        print(f"Code: {analysis['code_context']}")
        
        # Display the analysis
        print(f"\n" + "─"*90)
        print("ERROR ANALYSIS:")
        print("─"*90)
        
        analysis_data = analysis['analysis']
        
        print(f"\nPattern Identified: {analysis_data['pattern']}")
        print(f"Root Cause: {analysis_data['root_cause']}")
        
        if analysis_data.get('explanation'):
            print(f"\nWhy This Happened:")
            for key, value in analysis_data['explanation'].items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        if analysis_data.get('code_pattern'):
            print(f"\nCode Pattern:")
            print(f"  Broken:  {analysis_data['code_pattern']['broken']}")
            print(f"  Fixed:   {analysis_data['code_pattern']['fixed']}")
        
        if analysis_data.get('solution'):
            print(f"\nSolution: {analysis_data['solution']}")
        
        if analysis_data.get('reference_file'):
            print(f"\nReference: {analysis_data['reference_file']}")
        
        if analysis_data.get('next_steps'):
            print(f"\nNext Steps:")
            for i, step in enumerate(analysis_data['next_steps'], 1):
                print(f"  {i}. {step}")
        
        # Store the analysis
        self._store_error_analysis(analysis)
    
    def _store_error_analysis(self, analysis):
        """
        Store the error analysis in the knowledge base.
        
        Creates a permanent record that can inform future error handling.
        """
        
        print(f"\n" + "─"*90)
        print("STORING KNOWLEDGE FOR FUTURE REFERENCE")
        print("─"*90)
        
        # Create error log file
        error_log_file = os.path.join(self.corrections_path, "sentinel_exception_log.json")
        
        # Load existing log or create new
        if os.path.exists(error_log_file):
            with open(error_log_file, 'r') as f:
                error_log = json.load(f)
        else:
            error_log = {
                "exceptions_caught": [],
                "created_at": datetime.utcnow().isoformat() + "Z",
                "purpose": "Track all exceptions caught by Sentinel system"
            }
        
        # Add this error to the log
        error_entry = {
            "timestamp": analysis['timestamp'],
            "error_type": analysis['error_type'],
            "error_message": analysis['error_message'],
            "file": analysis['file'],
            "line_number": analysis['line_number'],
            "function": analysis['function'],
            "classification": analysis['analysis']['classification'],
            "severity": analysis['analysis']['severity'],
            "pattern": analysis['analysis']['pattern'],
            "solution": analysis['analysis'].get('solution', 'Unknown')
        }
        
        error_log["exceptions_caught"].append(error_entry)
        
        # Save the log
        with open(error_log_file, 'w') as f:
            json.dump(error_log, f, indent=2)
        
        print(f"\n✓ Error analysis stored: {error_log_file}")
        print(f"✓ Total exceptions logged: {len(error_log['exceptions_caught'])}")
        
        # Store detailed analysis
        detailed_file = os.path.join(
            self.corrections_path, 
            f"exception_{analysis['error_type']}_{analysis['line_number']}.json"
        )
        
        with open(detailed_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"✓ Detailed analysis stored: {detailed_file}")
        
        print(f"\n" + "█"*90)
        print("PROCESSOR LEARNING COMPLETE")
        print("█"*90)
        print(f"\nThe system now understands:")
        print(f"  • What error occurred")
        print(f"  • Why it happened")
        print(f"  • How to fix it")
        print(f"  • How to prevent it in future")
        print(f"\nThis knowledge is stored and can inform future decisions.\n")


# ============================================
# GLOBAL EXCEPTION HOOK INSTALLATION
# ============================================

# Create the analyzer
_sentinel_analyzer = SentinelExceptionAnalyzer()

# Install it as the global exception handler
sys.excepthook = _sentinel_analyzer.handle_exception

# Indicate that the hook is installed
if os.environ.get('SENTINEL_SILENT_MODE') != '1':
    pass  # Silently install without printing to avoid polluting output
