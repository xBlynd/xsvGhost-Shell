"""
Interface Engine - The Face
Visual presentation, banners, themes
"""

from datetime import datetime

class InterfaceEngine:
    """
    Handles all visual output and theming.
    Returns strings - doesn't print directly.
    """
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "interface"
        
        # Get user role for theming
        security = kernel.engines.get('security')
        self.role = security.current_role if security else None
    
    def show_banner(self):
        """Display startup banner"""
        banner = self.get_banner()
        print(banner)
    
    def get_banner(self):
        """Generate banner based on role"""
        
        # ASCII Art
        art = r"""
    ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗
   ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝
   ██║  ███╗███████║██║   ██║███████╗   ██║   
   ██║   ██║██╔══██║██║   ██║╚════██║   ██║   
   ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   
    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   
        """
        
        # Role-based theming
        if self.role:
            role_name = self.role.value
            if role_name == "GOD":
                color = "🔴"
                subtitle = "GOD MODE ACTIVE"
            elif role_name == "ADMIN":
                color = "🟡"
                subtitle = "ADMIN MODE"
            else:
                color = "🟢"
                subtitle = "GUEST MODE"
        else:
            color = "⚪"
            subtitle = "SYSTEM READY"
        
        # System info
        core = self.kernel.engines.get('ghost_core')
        if core:
            os_info = f"{core.os_name} | Node: {core.node_id[:16]}"
        else:
            os_info = "System Unknown"
        
        # Commands count
        loader = self.kernel.engines.get('loader')
        cmd_count = len(loader.commands) if loader else 0
        
        banner_text = f"""
{art}
    {color} {subtitle}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {os_info}
    Commands: {cmd_count} | Type 'help' for commands
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        return banner_text
    
    def format_table(self, headers, rows):
        """Format data as table"""
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Build table
        lines = []
        
        # Header
        header_line = " | ".join(
            h.ljust(w) for h, w in zip(headers, col_widths)
        )
        lines.append(header_line)
        lines.append("-" * len(header_line))
        
        # Rows
        for row in rows:
            row_line = " | ".join(
                str(cell).ljust(w) for cell, w in zip(row, col_widths)
            )
            lines.append(row_line)
        
        return "\n".join(lines)
    
    def format_list(self, items, bullet="•"):
        """Format items as bullet list"""
        return "\n".join(f"{bullet} {item}" for item in items)
    
    def format_status(self, key, value, status="info"):
        """Format key-value status line"""
        symbols = {
            "ok": "✓",
            "error": "✗",
            "warning": "⚠",
            "info": "ℹ"
        }
        symbol = symbols.get(status, "•")
        return f"{symbol} {key}: {value}"
