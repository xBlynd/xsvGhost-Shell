import sys
import importlib
from pathlib import Path

# CONFIGURATION
APP_NAME = "xsvCommandCenter"
VERSION = "v6.0-Ghost-Kernel"
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

def main():
    # Run preflight checks
    from PREFLIGHT import PreflightCheck
    checker = PreflightCheck()
    if not checker.run():
        sys.exit(1)
    
    print()  # Blank line for readability
    
    # Boot the kernel
    from src.core.kernel import initialize, get_kernel
    if not initialize():
        sys.exit(1)
    
    print()  # Blank line
    
    kernel = get_kernel()
    
    # Get engines (these might be None if engines not implemented yet)
    security = kernel.get_engine('security')
    vault = kernel.get_engine('vault')
    
    # If no arguments, run the HELP command
    if len(sys.argv) < 2:
        from src.commands import cmd_help
        cmd_help.run([])
        kernel.shutdown()
        return
    
    # Otherwise, run the requested command
    cmd_name = sys.argv[1].lower()
    cmd_args = sys.argv[2:]
    
    try:
        # 1. Try to find a Module (src/commands/cmd_*.py)
        try:
            module_path = f"src.commands.cmd_{cmd_name}"
            module = importlib.import_module(module_path)
            module.run(cmd_args)
        except ModuleNotFoundError:
            pass  # Not a module, try Magic Launcher
        
        # 2. Try Magic Launcher (commands.json)
        try:
            from src.commands import cmd_launcher
            launcher = cmd_launcher.Launcher()
            if launcher.run(cmd_name):
                return
        except:
            pass
        
        # 3. If neither found
        print(f"❌ Unknown command: '{cmd_name}'")
        print("   Type 'xsv help' to see available tools.")
    
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
    finally:
        kernel.shutdown()

if __name__ == "__main__":
    main()
