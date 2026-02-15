"""
Engine 09: Interface Engine - The Face
========================================
ASCII banners, theme management, output formatting.

Architecture Note:
- This engine returns STRINGS, it does not print directly.
- All visual presentation flows through here.
- Future: This becomes the adapter layer for GUI/Web/Mobile.
  Terminal output is just one "renderer". A web dashboard would
  be another renderer consuming the same data structures.

Compartmentalization:
- ONLY handles visual output
- NEVER performs business logic
"""


class InterfaceEngine:
    """The Face - visual presentation and theming."""

    ENGINE_NAME = "interface"
    ENGINE_VERSION = "1.0.0"

    # === ASCII BANNERS ===
    BANNER_GOD = r"""
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║     ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗       ║
    ║    ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝       ║
    ║    ██║  ███╗███████║██║   ██║███████╗   ██║          ║
    ║    ██║   ██║██╔══██║██║   ██║╚════██║   ██║          ║
    ║    ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║          ║
    ║     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝          ║
    ║                                                      ║
    ║           S H E L L   P H O E N I X                  ║
    ║              ⚡ G O D   M O D E ⚡                    ║
    ║                  v6.0 Phoenix                        ║
    ╚══════════════════════════════════════════════════════╝
    """

    BANNER_GUEST = r"""
    ╔══════════════════════════════════════════════════════╗
    ║          👻 GHOST SHELL PHOENIX v6.0                 ║
    ║              Guest Mode (Read-Only)                  ║
    ╚══════════════════════════════════════════════════════╝
    """

    BANNER_ADMIN = r"""
    ╔══════════════════════════════════════════════════════╗
    ║          👻 GHOST SHELL PHOENIX v6.0                 ║
    ║              ◆ Admin Mode                            ║
    ╚══════════════════════════════════════════════════════╝
    """

    def __init__(self, kernel):
        self.kernel = kernel
        # Future: load theme from config
        self.theme = "default"

    def get_banner(self, role=None):
        """Get the appropriate banner for current role."""
        if role == "GOD":
            return self.BANNER_GOD
        elif role == "ADMIN":
            return self.BANNER_ADMIN
        else:
            return self.BANNER_GUEST

    # =========================================================================
    # OUTPUT FORMATTING
    # =========================================================================
    # These methods return formatted strings. The shell loop prints them.
    # Future GUI/Web renders would consume the same data but render differently.

    def format_table(self, headers, rows, title=None):
        """Format data as a text table."""
        if not rows:
            return "  (no data)"

        # Calculate column widths
        col_widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

        # Build table
        lines = []
        if title:
            lines.append(f"\n  {title}")
            lines.append("  " + "─" * (sum(col_widths) + len(col_widths) * 3))

        # Header
        header_line = "  "
        for i, h in enumerate(headers):
            header_line += f" {str(h):<{col_widths[i]}} │"
        lines.append(header_line)
        lines.append("  " + "─" * (sum(col_widths) + len(col_widths) * 3))

        # Rows
        for row in rows:
            row_line = "  "
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    row_line += f" {str(cell):<{col_widths[i]}} │"
            lines.append(row_line)

        return "\n".join(lines)

    def format_status_block(self, title, items):
        """Format a status block with key-value pairs."""
        lines = [f"\n  ┌─ {title} ─┐"]
        max_key = max(len(k) for k, v in items) if items else 0
        for key, value in items:
            lines.append(f"  │ {key:<{max_key}} : {value}")
        lines.append(f"  └{'─' * (max_key + 20)}┘")
        return "\n".join(lines)

    def format_ping_result(self, data):
        """Format ping results for display."""
        if data.get("status") == "UNREACHABLE":
            return f"  ✗ {data['host']} - UNREACHABLE ({data['packets_lost']}/{data['packets_sent']} lost)"

        status_icon = "✓" if data["status"] == "STABLE" else "⚠"
        lines = [
            f"  {status_icon} Ping {data['host']} - {data['status']}",
            f"    avg: {data['average_ms']}ms  min: {data['min_ms']}ms  max: {data['max_ms']}ms",
            f"    jitter: {data['jitter_ms']}ms  loss: {data['loss_pct']}%",
        ]
        return "\n".join(lines)

    def format_todo_list(self, items):
        """Format todo list for display."""
        if not items:
            return "  No active todos. 🎉"

        lines = ["\n  ┌─ TODO ─┐"]
        for item in items:
            check = "✓" if item["done"] else "○"
            priority = ""
            if item.get("priority") == "high":
                priority = " [!]"
            elif item.get("priority") == "critical":
                priority = " [!!]"
            lines.append(f"  │ {check} #{item['id']}{priority} {item['text']}")
        lines.append(f"  └─────────┘")
        return "\n".join(lines)

    def format_help(self, commands):
        """Format the help menu."""
        lines = [
            "\n  ┌─ GHOST SHELL COMMANDS ─┐",
            "  │",
        ]

        # Group by category if available
        for name, module in sorted(commands.items()):
            desc = getattr(module, 'DESCRIPTION', 'No description')
            role = getattr(module, 'REQUIRED_ROLE', 'GUEST')
            lines.append(f"  │  {name:<14} {desc:<40} [{role}]")

        lines.extend([
            "  │",
            "  │  Any other input passes through to host OS",
            "  └──────────────────────┘",
        ])
        return "\n".join(lines)
