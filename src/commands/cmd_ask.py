"""
Command: ask
Quick alias - routes to Eve AI engine.
Shorthand for `eve ask <question>`.
"""

DESCRIPTION = "Ask the AI (Eve)"
USAGE = "ask <your question>"
REQUIRED_ROLE = "GUEST"


def execute(kernel, args):
    """Query the AI via Eve."""
    if not args.strip():
        return "  Usage: ask <your question>\n  Example: ask Write me a bash script to backup /home"

    eve = kernel.get_engine("eve")
    if not eve:
        return "  [!] Eve engine not loaded. Use `eve setup` for installation guide."

    result = eve.ask(args.strip())

    if result.get("response"):
        tier = result.get("tier", "?")
        model = result.get("model", "?")
        return f"\n  Eve [{tier}/{model}]:\n  {result['response']}"
    
    error_msg = f"  [Eve] {result.get('error', 'No response')}"
    if result.get("hint"):
        error_msg += f"\n  Hint: {result['hint']}"
    return error_msg
