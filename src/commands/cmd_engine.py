"""
cmd_engine - Control Ghost Shell engines
Usage:
  engine status              - Show all engines
  engine enable <name>       - Enable an engine
  engine disable <name>      - Disable an engine
  engine restart <name>      - Restart an engine
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT))

from src.core.kernel import get_kernel

MANIFEST = {
    "name": "engine",
    "version": "1.0",
    "description": "Control Ghost Shell engines",
    "usage": "engine <status|enable|disable|restart> [engine_name]",
    "author": "Ghost Shell Core"
}

def run(args):
    kernel = get_kernel()
    if not kernel:
        print("❌ Kernel not initialized")
        return
    
    if not args:
        show_status(kernel)
        return
    
    command = args[0].lower()
    
    if command == "status":
        show_status(kernel)
    elif command == "enable" and len(args) > 1:
        kernel.enable_engine(args[1])
    elif command == "disable" and len(args) > 1:
        kernel.disable_engine(args[1])
    elif command == "restart" and len(args) > 1:
        restart_engine(kernel, args[1])
    else:
        print(MANIFEST['usage'])

def show_status(kernel):
    """Show all engine states"""
    health = kernel.monitor_health()
    
    print("\n🔧 Ghost Shell Engine Status\n")
    print(f"{'Engine':<15} {'State':<12} {'Restarts':<10} {'Errors':<8}")
    print("=" * 50)
    
    for name, data in health.items():
        state = data['state']
        restarts = data['restarts']
        errors = data['errors']
        
        # Color coding
        if state == 'running':
            icon = "✓"
        elif state == 'disabled':
            icon = "○"
        elif state == 'failed':
            icon = "❌"
        else:
            icon = "⚠"
        
        print(f"{icon} {name:<13} {state:<12} {restarts:<10} {errors:<8}")
    
    print()

def restart_engine(kernel, name):
    """Restart an engine"""
    wrapper = kernel.engines.get(name)
    if not wrapper:
        print(f"❌ Engine '{name}' not found")
        return
    
    if wrapper.state.value == 'running':
        wrapper.shutdown()
    
    if wrapper.load():
        print(f"✓ {name} restarted")
    else:
        print(f"❌ {name} failed to restart")

if __name__ == "__main__":
    run(sys.argv[1:])
