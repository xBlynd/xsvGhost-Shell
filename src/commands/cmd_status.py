"""
Status Command - Show system health
"""

HELP = "Show Ghost Shell system status"

def execute(kernel, args):
    """Display system status"""
    
    output = []
    output.append("\n=== GHOST SHELL STATUS ===\n")
    
    # Heartbeat info
    heartbeat = kernel.engines.get('heartbeat')
    if heartbeat:
        health = heartbeat.get_health()
        output.append(f"Status: {health['status']}")
        output.append(f"Memory: {health['memory_mb']:.1f} MB")
        output.append(f"Threads: {health['threads']}")
        output.append(f"Uptime: {health['uptime']}")
        output.append("")
    
    # Engines
    output.append("Engines:")
    for name, engine in kernel.engines.items():
        status = "✓" if engine else "✗"
        output.append(f"  {status} {name}")
    output.append("")
    
    # Commands
    loader = kernel.engines.get('loader')
    if loader:
        output.append(f"Commands: {len(loader.commands)}")
        output.append("")
    
    # Security
    security = kernel.engines.get('security')
    if security:
        output.append(f"Role: {security.get_role_name()}")
        output.append("")
    
    # Sync status
    sync = kernel.engines.get('sync')
    if sync:
        sync_status = sync.get_sync_status()
        output.append(f"Location: {sync_status['status']}")
        output.append("")
    
    return "\n".join(output)
