#!/usr/bin/env python3
"""
Ghost Shell Phoenix v7.0 - Main Entry Point
One Stick, Any Computer, Surgical Precision
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.kernel import GhostKernel

def main():
    """Boot Ghost Shell Phoenix"""
    try:
        kernel = GhostKernel()
        kernel.boot()
        kernel.run()
    except KeyboardInterrupt:
        print("\n\n[Ghost] Shutdown requested...")
    except Exception as e:
        print(f"\n[FATAL] Kernel panic: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
