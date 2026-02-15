"""
Command: help
Shows all available Ghost Shell commands.
"""

DESCRIPTION = "Show available commands"
USAGE = "help [command]"
REQUIRED_ROLE = "GUEST"


def execute(kernel, args):
    """Display help information."""
    if args.strip():
        # Help for specific command
        cmd_name = args.strip().lower()
        loader = kernel.get_engine("loader")
        if loader:
            info = loader.get_command_info(cmd_name)
            if info:
                lines = [
                    f"\n  Command: {info['name']}",
                    f"  Description: {info['description']}",
                    f"  Role Required: {info['required_role'] or 'GUEST'}",
                ]
                if info.get('usage'):
                    lines.append(f"  Usage: {info['usage']}")
                return "\n".join(lines)
            else:
                return f"  Unknown command: {cmd_name}"

    # Show all commands
    iface = kernel.get_engine("interface")
    if iface:
        return iface.format_help(kernel.commands)

    # Fallback if interface engine not loaded
    lines = ["\n  Available commands:"]
    for name, module in sorted(kernel.commands.items()):
        desc = getattr(module, 'DESCRIPTION', '')
        lines.append(f"    {name:<14} {desc}")
    lines.append("\n  Any other input is passed to the host OS.")
    return "\n".join(lines)
