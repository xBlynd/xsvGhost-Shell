"""
Command: ask
Query the Cortex AI engine.
Currently a stub - will connect to Ollama/API when Cortex is operational.
"""

DESCRIPTION = "Ask the AI (Cortex)"
USAGE = "ask <your question>"
REQUIRED_ROLE = "GUEST"


def execute(kernel, args):
    """Query the AI."""
    if not args.strip():
        return "  Usage: ask <your question>\n  Example: ask Write me a bash script to backup /home"

    cortex = kernel.get_engine("cortex")
    if not cortex:
        return "  [!] Cortex engine not loaded"

    result = cortex.ask(args.strip())

    if result.get("response"):
        return f"\n  Ghost AI:\n  {result['response']}"
    elif result.get("error"):
        return f"  [Cortex] {result['error']}"
    if result.get("hint"):
        return f"  [Cortex] {result['error']}\n  Hint: {result['hint']}"
    return "  [Cortex] No response"
