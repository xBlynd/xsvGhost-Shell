"""
Shell Command - The main interactive loop
"""

HELP = "Enter interactive shell mode"

def execute(kernel, args):
    """Main shell loop"""
    
    while kernel.running:
        try:
            # Get input
            user_input = input("\nghost> ").strip()
            
            if not user_input:
                continue
            
            # Parse command and args
            parts = user_input.split()
            cmd_name = parts[0]
            cmd_args = parts[1:]
            
            # Check for exit
            if cmd_name in ['exit', 'quit', 'q']:
                break
            
            # Try to find command
            loader = kernel.engines.get('loader')
            if loader and cmd_name in loader.commands:
                try:
                    cmd_module = loader.commands[cmd_name]
                    result = cmd_module.execute(kernel, cmd_args)
                    if result:
                        print(result)
                except Exception as e:
                    print(f"[Error] Command failed: {e}")
            else:
                # Command not found - try OS passthrough
                print(f"Unknown command: {cmd_name}")
                print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n[Use 'exit' to quit]")
            continue
        except EOFError:
            break
    
    return None
