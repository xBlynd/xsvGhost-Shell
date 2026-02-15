"""
Todo Command - Task management
"""

HELP = """Todo management
Usage:
  todo add <task>       - Add new todo
  todo list            - List active todos
  todo done <id>       - Mark todo as complete
  todo delete <id>     - Delete todo
"""

def execute(kernel, args):
    """Execute todo command"""
    
    vault = kernel.engines.get('vault')
    if not vault:
        return "Vault engine unavailable"
    
    if not args:
        return HELP
    
    action = args[0]
    
    if action == "add":
        if len(args) < 2:
            return "Usage: todo add <task>"
        
        task = " ".join(args[1:])
        success, msg = vault.todo_add(task)
        return msg
    
    elif action == "list":
        todos = vault.todo_list()
        
        if not todos:
            return "No active todos"
        
        output = ["\n=== ACTIVE TODOS ===\n"]
        for todo in todos:
            status = "✓" if todo.get("completed") else "○"
            output.append(f"  {status} #{todo['id']}: {todo['task']}")
        
        return "\n".join(output)
    
    elif action in ["done", "complete"]:
        if len(args) < 2:
            return "Usage: todo done <id>"
        
        try:
            todo_id = int(args[1])
            success, msg = vault.todo_complete(todo_id)
            return msg
        except ValueError:
            return "Invalid todo ID"
    
    elif action in ["delete", "del", "rm"]:
        if len(args) < 2:
            return "Usage: todo delete <id>"
        
        try:
            todo_id = int(args[1])
            success, msg = vault.todo_delete(todo_id)
            return msg
        except ValueError:
            return "Invalid todo ID"
    
    else:
        return f"Unknown action: {action}\n\n{HELP}"
