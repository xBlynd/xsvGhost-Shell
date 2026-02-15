"""
Journal Command - Manage journal entries
"""

HELP = """Journal operations
Usage:
  j add <entry>     - Add entry to today's journal
  j list           - List recent journal files
  j read [date]    - Read journal (today or specific date)
"""

def execute(kernel, args):
    """Execute journal command"""
    
    vault = kernel.engines.get('vault')
    if not vault:
        return "Vault engine unavailable"
    
    if not args:
        return HELP
    
    action = args[0]
    
    if action == "add":
        if len(args) < 2:
            return "Usage: j add <entry>"
        
        entry = " ".join(args[1:])
        success, msg = vault.journal_add(entry)
        return msg
    
    elif action == "list":
        entries = vault.journal_list()
        
        if not entries:
            return "No journal entries found"
        
        output = ["\n=== RECENT JOURNALS ===\n"]
        for e in entries:
            output.append(f"  {e['date']} ({e['size']} bytes)")
        
        return "\n".join(output)
    
    elif action == "read":
        date = args[1] if len(args) > 1 else None
        content = vault.journal_read(date)
        
        if content is None:
            date_str = date or "today"
            return f"No journal found for {date_str}"
        
        return f"\n=== JOURNAL ===\n\n{content}"
    
    else:
        return f"Unknown action: {action}\n\n{HELP}"
