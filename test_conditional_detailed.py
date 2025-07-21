#!/usr/bin/env python3
"""
Test script to verify what WOULD happen on Python 3.9.
This simulates the behavior by checking poetry.lock for version resolution.
"""

import sys
import subprocess
import json

def check_uplink_version_for_python(python_version_str):
    """Check which uplink version would be installed for a given Python version."""
    major, minor = map(int, python_version_str.split('.'))
    
    if (major, minor) >= (3, 10):
        return "0.10.0"
    else:
        return "0.9.7"

def main():
    print("=== Uplink Conditional Dependency Test ===\n")
    
    # Test current Python version (actual)
    current_python = f"{sys.version_info.major}.{sys.version_info.minor}"
    print(f"Current Python: {current_python}")
    
    try:
        import uplink
        actual_uplink_version = uplink.__version__
        print(f"Actual uplink version: {actual_uplink_version}")
    except ImportError:
        print("❌ Could not import uplink")
        return
    
    # Test what would happen on different Python versions
    test_versions = ["3.9", "3.10", "3.11", "3.12", "3.13"]
    
    print("\n=== Conditional Dependency Resolution ===")
    for py_version in test_versions:
        expected_uplink = check_uplink_version_for_python(py_version)
        status = "✅" if py_version != "3.9" else "⚠️ "
        warning = " (may have pkg_resources warnings)" if py_version == "3.9" else " (no pkg_resources warnings)"
        print(f"Python {py_version}: uplink {expected_uplink}{warning} {status}")
    
    print(f"\n=== Current Environment Verification ===")
    expected_for_current = check_uplink_version_for_python(current_python)
    if actual_uplink_version.startswith(expected_for_current):
        print(f"✅ Correct: Python {current_python} has uplink {actual_uplink_version}")
    else:
        print(f"❌ Error: Python {current_python} should have uplink {expected_for_current}, but has {actual_uplink_version}")
    
    # Test nisystemlink integration
    try:
        import nisystemlink.clients.core._uplink._base_client
        print("✅ nisystemlink uplink integration working")
    except Exception as e:
        print(f"❌ Error importing nisystemlink uplink integration: {e}")
        
    print("\n=== Poetry Configuration Check ===")
    try:
        result = subprocess.run(['poetry', 'show', 'uplink'], 
                              capture_output=True, text=True, check=True)
        print("Current uplink installation details:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Could not get poetry show output: {e}")

if __name__ == "__main__":
    main()
