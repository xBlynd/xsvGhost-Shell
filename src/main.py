#!/usr/bin/env python3
"""
Ghost Shell Phoenix - Main Entry Point
"One Stick, Any Computer, Surgical Precision"

Usage:
    python src/main.py
    python src/main.py --headless    (no banner, no shell - for automation)
    python src/main.py --debug       (verbose boot logging)
"""

import sys
import os

# === UTF-8 FIX ===
# Windows consoles default to cp1252. Force UTF-8 so emoji and box-drawing
# characters in banners and output render correctly on all platforms.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# === THE ANCHOR ===
# This single line makes the ENTIRE system portable.
# No matter where Ghost Shell lives (USB, C:\Dev, /home/user, Android storage),
# ROOT_DIR always points to the project root.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from src.core.kernel import GhostKernel


def main():
    """Boot Ghost Shell Phoenix."""
    headless = "--headless" in sys.argv
    debug = "--debug" in sys.argv

    try:
        kernel = GhostKernel(root_dir=ROOT_DIR, debug=debug)
        boot_success = kernel.boot()

        if not boot_success:
            print("\n[!] Kernel boot failed. Check errors above.")
            sys.exit(1)

                if headless:
                    # Headless mode - kernel is up, engines are loaded
                    # Future: accept commands via stdin pipe or API
                    print("[Ghost] Running in headless mode. Press Ctrl+C to exit.")
                    try:
                        import time
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        pass
                else:
                    # Ghost Shell Pre-Boot Prompt
                    authenticated = False
                    while not authenticated:
                        try:
                            choice = input("\nGhost Shell v6.5 > ").strip().lower()
                            
                            if choice == "login":
                                from src.tui.inline_login import show_login_challenge
                                authenticated = show_login_challenge(kernel)
                            elif choice in ("exit", "quit"):
                                print("[Ghost] Shutdown requested.")
                                sys.exit(0)
                            elif choice == "help":
                                print("\nAvailable Pre-Boot Commands:")
                                print("  login      - Initiate authentication sequence")
                                print("  exit       - Shutdown the system")
                            elif not choice:
                                continue
                            else:
                                print(f"Unknown command: '{choice}'. Type 'login' to begin.")
                        except KeyboardInterrupt:
                            print("\n[Ghost] Shutdown requested.")
                            sys.exit(0)
        
                    # Interactive mode - drop into shell
                    kernel.run_shell()
                    except KeyboardInterrupt:
        print("\n[Ghost] Interrupted. Shutting down...")
    except Exception as e:
        print(f"\n[FATAL] Unrecoverable error: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup runs no matter what
        try:
            kernel.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    main()
