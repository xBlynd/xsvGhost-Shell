"""
Ping Command - Network diagnostics with jitter analysis
"""

HELP = """Smart ping with jitter analysis
Usage:
  ping <host> [count]
  
Example:
  ping 8.8.8.8
  ping google.com 5
"""

def execute(kernel, args):
    """Execute ping with jitter analysis"""
    
    blackbox = kernel.engines.get('blackbox')
    if not blackbox:
        return "BlackBox engine unavailable"
    
    if not args:
        return HELP
    
    host = args[0]
    count = int(args[1]) if len(args) > 1 else 10
    
    print(f"\nPinging {host} with {count} packets...\n")
    
    result = blackbox.ping(host, count)
    
    if "error" in result:
        return f"Error: {result['error']}"
    
    # Format output
    output = []
    output.append("=== PING RESULTS ===")
    output.append(f"Host: {result['host']}")
    output.append(f"Packets: {result['packets']} sent, {result['received']} received ({result['loss_percent']:.1f}% loss)")
    output.append("")
    output.append("Latency:")
    output.append(f"  Min: {result['min_ms']} ms")
    output.append(f"  Avg: {result['avg_ms']} ms")
    output.append(f"  Max: {result['max_ms']} ms")
    output.append("")
    output.append(f"Jitter: {result['jitter_ms']} ms ({result['stability']})")
    output.append("")
    
    # Stability explanation
    if result['stability'] == "POOR":
        output.append("⚠ High jitter detected - connection unstable")
        output.append("  This may cause lag in games or dropped video calls")
    elif result['stability'] == "EXCELLENT":
        output.append("✓ Excellent stability - ideal for real-time applications")
    
    return "\n".join(output)
