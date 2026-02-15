"""
Reload Command - Hot reload commands without restart
"""

HELP = """Hot reload commands
Usage:
  reload <command>  - Reload specific command
  reload all        - Reload all commands
"""

def execute(kernel, args):
    """Hot reload commands"""
    
    loader = kernel.engines.get('loader')
    if not loader:
        return "Loader engine unavailable"
    
    if not args:
        return HELP
    
    cmd_name = args[0]
    
    if cmd_name == "all":
        # Rediscover all commands
        loader._discover_commands()
        return f"Reloaded all commands ({len(loader.commands)} found)"
    else:
        success, msg = loader.reload_command(cmd_name)
        return msg
