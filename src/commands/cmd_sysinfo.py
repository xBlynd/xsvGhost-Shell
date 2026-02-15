"""
Command: sysinfo
Display detailed system information about the host machine.
"""

DESCRIPTION = "Show host system information"
USAGE = "sysinfo"
REQUIRED_ROLE = "GUEST"


import platform
import sys
import os


def execute(kernel, args):
    """Show system information."""
    lines = [
        "\n  ┌─ SYSTEM INFO ─────────────────────────────┐",
        f"  │ OS:           {platform.system()} {platform.release()}",
        f"  │ Version:      {platform.version()}",
        f"  │ Architecture: {platform.machine()}",
        f"  │ Processor:    {platform.processor() or 'unknown'}",
        f"  │ Hostname:     {platform.node()}",
        f"  │ Python:       {sys.version.split()[0]}",
        f"  │ Working Dir:  {os.getcwd()}",
    ]

    core = kernel.get_engine("ghost_core")
    if core:
        lines.append(f"  │ Ghost Root:   {core.root_dir}")
        lines.append(f"  │ Portable:     {'Yes (USB)' if core.is_portable else 'No (Local)'}")

    # Disk usage
    try:
        if hasattr(os, 'statvfs'):
            st = os.statvfs('/')
            total_gb = (st.f_blocks * st.f_frsize) / (1024**3)
            free_gb = (st.f_bavail * st.f_frsize) / (1024**3)
            lines.append(f"  │ Disk:         {free_gb:.1f} GB free / {total_gb:.1f} GB total")
    except Exception:
        pass

    lines.append("  └─────────────────────────────────────────┘")
    return "\n".join(lines)
