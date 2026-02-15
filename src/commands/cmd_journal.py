"""
Command: journal
Personal journal management. Add entries, list, search.
"""

DESCRIPTION = "Manage journal entries"
USAGE = "journal add <text> | journal list [date] | journal search <query>"
REQUIRED_ROLE = "GUEST"


def execute(kernel, args):
    """Manage journal entries."""
    vault = kernel.get_engine("vault")
    if not vault:
        return "  [!] Vault engine not available"

    parts = args.strip().split(None, 1)
    if not parts:
        return (
            "  Usage:\n"
            "    journal add <entry text>\n"
            "    journal list [YYYY-MM-DD]\n"
            "    journal search <query>"
        )

    action = parts[0].lower()
    rest = parts[1] if len(parts) > 1 else ""

    if action == "add":
        if not rest:
            return "  Usage: journal add <your entry text>"
        result = vault.journal_add(rest)
        return f"  ✓ Journal entry added ({result['date']} {result['timestamp']})"

    elif action == "list":
        result = vault.journal_list(date=rest.strip() if rest.strip() else None)
        if "content" in result:
            if result["content"]:
                return result["content"]
            else:
                return f"  No journal entries for {result['date']}"
        else:
            entries = result.get("entries", [])
            if not entries:
                return "  No journal entries yet. Try: journal add Hello world!"
            lines = [f"\n  Recent journal files ({result.get('total_files', 0)} total):"]
            for e in entries:
                lines.append(f"    {e['date']}  ({e['size_bytes']} bytes)")
            return "\n".join(lines)

    elif action == "search":
        if not rest:
            return "  Usage: journal search <query>"
        result = vault.journal_search(rest)
        if not result["results"]:
            return f"  No matches for '{rest}'"
        lines = [f"\n  Found {result['total_matches']} matches for '{rest}':"]
        for r in result["results"]:
            lines.append(f"    {r['date']}:")
            for preview in r.get("preview", []):
                lines.append(f"      {preview}")
        return "\n".join(lines)

    else:
        return f"  Unknown journal action: {action}\n  Try: journal add, list, or search"
