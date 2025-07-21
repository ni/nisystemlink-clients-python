#!/usr/bin/env python3
"""
Demonstration script showing uplink version selection based on Python version.
This script shows how the conditional dependency resolution works.
"""

import sys
import uplink

def main():
    print(f"Python version: {sys.version}")
    print(f"Uplink version: {uplink.__version__}")
    
    if sys.version_info >= (3, 10):
        expected_version = "0.10.0"
        print("✅ Running Python 3.10+ - should have uplink 0.10.0 (no pkg_resources warnings)")
    else:
        expected_version = "0.9.7"  
        print("⚠️  Running Python 3.9 - should have uplink 0.9.7 (may have pkg_resources warnings)")
    
    if uplink.__version__.startswith(expected_version):
        print(f"✅ Correct uplink version for Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print(f"❌ Unexpected uplink version {uplink.__version__} for Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Test basic functionality
    try:
        import nisystemlink.clients.core._uplink._base_client
        print("✅ nisystemlink uplink integration working")
    except Exception as e:
        print(f"❌ Error importing nisystemlink uplink integration: {e}")

if __name__ == "__main__":
    main()
