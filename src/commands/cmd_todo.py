"""
Command: todo
Task management with priorities.
"""

DESCRIPTION = "Manage todo items"
USAGE = "todo add <text> | todo list | todo done <id> | todo rm <id>"
REQUIRED_ROLE = "GUEST"


def execute(kernel, args):
    """Manage todos."""
    vault = kernel.get_engine("vault")
    if not vault:
        return "  [!] Vault engine not available"

    parts = args.strip().split(None, 1)
    if not parts:
        # Show todo list by default
        result = vault.todo_list()
        iface = kernel.get_engine("interface")
        if iface:
            return iface.format_todo_list(result["items"])
        return str(result)

    action = parts[0].lower()
    rest = parts[1] if len(parts) > 1 else ""

    if action == "add":
        if not rest:
            return "  Usage: todo add <task description>"

        # Check for priority flag
        priority = "normal"
        if rest.startswith("!!! "):
            priority = "critical"
            rest = rest[4:]
        elif rest.startswith("!! "):
            priority = "high"
            rest = rest[3:]
        elif rest.startswith("! "):
            priority = "low"
            rest = rest[2:]

        item = vault.todo_add(rest, priority=priority)
        return f"  ✓ Todo #{item['id']} added ({priority}): {rest}"

    elif action == "list":
        show_done = rest.strip().lower() == "all"
        result = vault.todo_list(show_done=show_done)
        iface = kernel.get_engine("interface")
        if iface:
            return iface.format_todo_list(result["items"])
        return str(result)

    elif action == "done":
        try:
            todo_id = int(rest.strip())
        except ValueError:
            return "  Usage: todo done <id>"
        item = vault.todo_complete(todo_id)
        if item:
            return f"  ✓ Todo #{todo_id} completed!"
        return f"  [!] Todo #{todo_id} not found"

    elif action in ("rm", "remove", "delete"):
        try:
            todo_id = int(rest.strip())
        except ValueError:
            return "  Usage: todo rm <id>"
        if vault.todo_remove(todo_id):
            return f"  ✓ Todo #{todo_id} removed"
        return f"  [!] Todo #{todo_id} not found"

    else:
        return f"  Unknown todo action: {action}\n  Try: todo add, list, done, rm"
