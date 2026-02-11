# Ghost Shell OS - Command Reference

## Command Index

Ghost Shell provides 25+ commands across different categories. Each command can be invoked directly from the shell.

### Usage Pattern
```
python src/main.py <command> [arguments...]
```
or from within the shell:
```
> <command> [arguments...]
```

## Core Commands

### shell
Launches the Ghost Shell interactive command prompt.
- **Status**: Phase 1 COMPLETE
- **Arguments**: Optional login credentials
- **Features**:
  - SECURE SESSION authentication
  - Background ReminderPulse thread for notifications
  - Command history
  - Exit command to shutdown gracefully

### help
Displays available commands and their descriptions.
- **Status**: Phase 1 COMPLETE
- **Arguments**: Optional specific command name
- **Examples**:
  - `help` - Lists all commands
  - `help shell` - Details for shell command

### version
Shows system version information.
- **Status**: Phase 1 COMPLETE
- **Output**: Ghost Shell version, build ID, build date

### status
Displays current system status.
- **Status**: Phase 1 COMPLETE
- **Output**: 
  - OS and platform
  - System uptime
  - Active engines
  - Resource usage

## Document Management Commands

### create
Creates new documents or configuration files.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `filename [optional_content]`
- **Features**:
  - Interactive or direct content entry
  - File type detection
  - Automatic metadata generation

### edit
Edits existing documents with syntax highlighting.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `filename`
- **Features**:
  - Line number display
  - Search and replace
  - Undo/redo support

### docs
Accesses and displays documentation.
- **Status**: Phase 1 COMPLETE
- **Arguments**: Optional search terms
- **Features**:
  - Full-text search
  - Category filtering
  - Automatic index generation

## Reminder/Journal Commands

### remind
Schedules reminders and notifications.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `message [due_time] [frequency]`
- **Examples**:
  - `remind "Check system" 14:30` - Daily at 2:30 PM
  - `remind "Backup" +7 days` - In 7 days
- **Features**:
  - ReminderEngine integration
  - Multiple notification channels
  - Recurring reminders

### journal
Manages journal entries and daily logs.
- **Status**: Phase 1 COMPLETE
- **Arguments**: Optional date or search query
- **Features**:
  - Auto-timestamped entries
  - Search functionality
  - Category tagging
  - Export to formats (JSON, TXT, CSV)

### todo
Manages TODO lists and tasks.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `add|remove|list [task_text]`
- **Examples**:
  - `todo add "Fix blocking issues"`
  - `todo list` - Shows all tasks
  - `todo remove 3` - Removes task #3

## Engine Management Commands

### engine
Manages available engines and their status.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `list|info|restart [engine_name]`
- **Examples**:
  - `engine list` - All 11 engines status
  - `engine info security` - SecurityEngine details
  - `engine restart reminder` - Restarts ReminderEngine

### repair
Diagnostics and system repair utilities.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `check|fix [system_area]`
- **Features**:
  - Automatic issue detection
  - Repair suggestions
  - Rollback capability

## Configuration Commands

### settings
Manages system configuration.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `get|set|list [key] [value]`
- **Examples**:
  - `settings list` - All configuration
  - `settings set timeout 3600` - 1 hour timeout
  - `settings get reminder_interval`

### setup
Initial system configuration wizard.
- **Status**: Phase 1 COMPLETE
- **Features**:
  - Guided setup process
  - Default value suggestions
  - Configuration validation

## Host/System Commands

### host
Host system interaction and discovery.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `info|connect|disconnect [host_id]`
- **Features**:
  - Auto-discovery of available hosts
  - Multi-host management
  - Connection pooling

### launcher
Launches programs and scripts.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `program_name [args...]`
- **Features**:
  - Background execution
  - Output capture
  - Process monitoring

## Security Commands

### alias
Manages command aliases.
- **Status**: Phase 1 COMPLETE
- **Arguments**: `add|remove|list [alias] [command]`
- **Features**:
  - Shortcut creation
  - Persistence across sessions

## Advanced Commands

### reload
Reloads modules and configuration.
- **Status**: Phase 1 COMPLETE
- **Features**:
  - Hot-reloading
  - Zero-downtime updates
  - Dependency handling

### exit
Gracefully shuts down Ghost Shell.
- **Status**: Phase 1 COMPLETE
- **Features**:
  - Session cleanup
  - ReminderPulse thread shutdown
  - Data persistence

## Command Patterns

### Error Handling
All commands implement consistent error handling:
- Exit code 0 = Success
- Exit code 1 = General error
- Exit code 2 = Usage error

### Argument Parsing
Commands support multiple argument formats:
- Positional: `command arg1 arg2`
- Named: `command --key value`
- Mixed: `command arg1 --key value arg2`

### Return Values
Commands can return:
- Status messages (stdout)
- Error messages (stderr)
- Structured data (JSON when --json flag used)

## Extending Commands

To add new commands:

1. Create `src/commands/cmd_yourcommand.py`
2. Implement `run(args=None)` function:
```python
def run(args=None):
    """Your command description"""
    kernel = get_kernel()
    # Access engines: security = kernel.get_engine('security')
    # Process arguments and execute logic
    print("Result")
    return True
```

3. Command auto-discovered by main.py
4. Use `help yourcommand` to document

## Best Practices

1. **Always validate arguments** before processing
2. **Use kernel engines** instead of direct system calls
3. **Return boolean** indicating success/failure
4. **Log important operations** via InfoEngine
5. **Handle KeyboardInterrupt** gracefully
6. **Provide helpful error messages**
7. **Support both --verbose and --quiet flags**
8. **Document with docstrings**

## Phase 2 Planned Commands

Upcoming commands scheduled for Phase 2:
- **restore**: System backup/restore utilities
- **audit**: Detailed audit logging
- **cluster**: Multi-Ghost coordination
- **benchmark**: Performance testing
- **plugin**: Third-party plugin management
- **webhook**: Event-driven integrations
- **backup**: Automated backup scheduling
- **sync**: Multi-host synchronization
