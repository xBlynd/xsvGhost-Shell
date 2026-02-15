"""
Command: keys
Key management for authentication and access control.
Issue, list, revoke, and inspect keys.

Key Types:
  GOD:   Full access. Only one God key exists.
  ADMIN: Standard access. Issued by God.
  GUEST: Read-only. Can be time-limited (great for lending USB).
"""

DESCRIPTION = "Manage authentication keys"
USAGE = "keys list | keys issue <role> [label] | keys revoke <id> | keys info <id>"
REQUIRED_ROLE = "ADMIN"


def execute(kernel, args):
    """Manage authentication keys."""
    sec = kernel.get_engine("security")
    if not sec:
        return "  [!] Security engine not available"

    parts = args.strip().split()
    if not parts:
        return _show_usage()

    action = parts[0].lower()

    if action == "list":
        return _list_keys(sec, kernel)

    elif action == "issue":
        return _issue_key(sec, parts[1:])

    elif action == "revoke":
        if len(parts) < 2:
            return "  Usage: keys revoke <key_id>"
        return _revoke_key(sec, parts[1])

    elif action == "info":
        if len(parts) < 2:
            return "  Usage: keys info <key_id>"
        return _key_info(sec, parts[1])

    elif action == "whoami":
        return _whoami(sec)

    else:
        return _show_usage()


def _show_usage():
    return (
        "  Key Management:\n"
        "    keys list                    List all keys\n"
        "    keys issue admin [label]     Issue an admin key\n"
        "    keys issue guest [label]     Issue a guest key\n"
        "    keys issue guest 24h [label] Issue a 24-hour guest key\n"
        "    keys revoke <key_id>         Revoke a key\n"
        "    keys info <key_id>           Show key details\n"
        "    keys whoami                  Show current identity"
    )


def _list_keys(sec, kernel):
    keys = sec.list_keys()
    if not keys:
        return "  No keys in keyring."

    iface = kernel.get_engine("interface")
    if iface:
        headers = ["Key ID", "Role", "Label", "Active", "Expires"]
        rows = []
        for k in keys:
            active = "✓" if k["active"] else "✗"
            expires = k.get("expires", "never")
            if expires and expires != "never":
                expires = expires[:10]  # Just the date
            rows.append([k["key_id"], k["role"], k["label"], active, expires])
        return iface.format_table(headers, rows, title="KEYRING")

    # Fallback
    lines = ["\n  Keys:"]
    for k in keys:
        status = "active" if k["active"] else "revoked"
        lines.append(f"    {k['key_id']} [{k['role']}] ({status}) - {k['label']}")
    return "\n".join(lines)


def _issue_key(sec, parts):
    if not parts:
        return "  Usage: keys issue <admin|guest> [duration] [label]"

    role_str = parts[0].upper()
    if role_str not in ("ADMIN", "GUEST"):
        return "  Can only issue ADMIN or GUEST keys. (God key is unique.)"

    # Parse optional duration and label
    expires_hours = None
    label = None

    remaining = parts[1:]
    if remaining:
        # Check for duration like "24h", "48h", "7d"
        first = remaining[0].lower()
        if first.endswith('h'):
            try:
                expires_hours = int(first[:-1])
                remaining = remaining[1:]
            except ValueError:
                pass
        elif first.endswith('d'):
            try:
                expires_hours = int(first[:-1]) * 24
                remaining = remaining[1:]
            except ValueError:
                pass

        if remaining:
            label = " ".join(remaining)

    key_data, error = sec.issue_key(role_str, label=label, expires_hours=expires_hours)

    if error:
        return f"  [!] {error}"

    lines = [
        f"\n  ✓ Key issued successfully!",
        f"    Key ID:  {key_data['key_id']}",
        f"    Role:    {key_data['role']}",
        f"    Label:   {key_data['label']}",
        f"    Expires: {key_data['expires'] or 'never'}",
        f"    File:    data/keys/{key_data['key_id']}.key",
        f"",
        f"    Copy the .key file to grant access to another Ghost Shell instance.",
    ]
    return "\n".join(lines)


def _revoke_key(sec, key_id):
    success, msg = sec.revoke_key(key_id)
    if success:
        return f"  ✓ {msg}"
    return f"  [!] {msg}"


def _key_info(sec, key_id):
    keys = sec.list_keys()
    for k in keys:
        if k["key_id"] == key_id:
            lines = [
                f"\n  Key: {k['key_id']}",
                f"    Role:    {k['role']}",
                f"    Label:   {k['label']}",
                f"    Created: {k['created']}",
                f"    Expires: {k.get('expires', 'never')}",
                f"    Active:  {'Yes' if k['active'] else 'No'}",
                f"    Creator: {k.get('creator', 'unknown')}",
            ]
            return "\n".join(lines)
    return f"  [!] Key '{key_id}' not found"


def _whoami(sec):
    lines = [
        f"\n  Current Identity:",
        f"    Role:    {sec.current_role}",
        f"    Key ID:  {sec.current_key_id}",
        f"    Auth:    {'Authenticated' if sec.authenticated else 'Not authenticated'}",
    ]
    return "\n".join(lines)
