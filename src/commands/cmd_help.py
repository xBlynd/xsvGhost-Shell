"""
Help Command - List available commands
"""

HELP = "Show available commands"

def execute(kernel, args):
    """Display help"""
    
    loader = kernel.engines.get('loader')
    if not loader:
        return "Loader engine unavailable"
    
    commands = loader.list_commands()
    
    output = []
    output.append("\n=== AVAILABLE COMMANDS ===\n")
    
    for cmd in commands:
        help_text = loader.get_command_help(cmd)
        if help_text:
            # Get first line of help
            first_line = help_text.split('\n')[0].strip()
            output.append(f"  {cmd:<15} {first_line}")
        else:
            output.append(f"  {cmd}")
    
    output.append("")
    output.append("Type 'help <command>' for detailed help")
    output.append("")
    
    return "\n".join(output)
