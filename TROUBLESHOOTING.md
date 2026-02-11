# Ghost Shell OS - Troubleshooting Guide

## Common Issues and Solutions

### PREFLIGHT Failures

#### "Python 3.8+ required. Found: X.Y.Z"

**Issue**: Your Python version is older than 3.8

**Solution**:
1. Download Python 3.9+ from python.org
2. Ensure python.exe is in your PATH
3. Verify with `python --version`
4. Reinstall Ghost Shell with new Python version

**Prevention**: Always check `python --version` before deploying

---

#### "Critical module missing: [module_name]"

**Issue**: Required Python package not installed

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Install specific missing module
pip install hashlib  # or missing module name
```

**Prevention**: Run PREFLIGHT before first use

---

#### "Folder structure invalid. Expected: src/core, src/commands"

**Issue**: Project structure is corrupted or incomplete

**Solution**:
1. Verify repo clone is complete: `git status`
2. If missing files, re-clone repository:
   ```bash
   git clone https://github.com/xBlynd/xsvGhost-Shell.git
   ```
3. Check git submodules: `git submodule update --init`

---

#### "Write permissions denied on data/ folder"

**Issue**: Ghost Shell can't write to data directory

**Solution**:

**Windows**:
```bash
# Run as Administrator
runas /user:Administrator cmd
cd project_folder
python src/main.py help
```

**Linux/Mac**:
```bash
chmod -R 755 data/
sudo chown -R $USER:$USER data/
```

---

### Startup Issues

#### "ModuleNotFoundError: No module named 'src.core.kernel'"

**Issue**: Python can't find Ghost Shell modules

**Solution**:
1. Ensure you're running from project root directory
2. Check Python path: `echo $PYTHONPATH`
3. Add project to path:
   ```bash
   cd /path/to/xsvGhost-Shell
   python src/main.py help
   ```
4. Verify __init__.py files exist in all src/ subdirectories

---

#### "Kernel initialization failed"

**Issue**: One or more engines failed to initialize

**Solution**:
1. Check console output for specific engine error
2. Verify all engine files exist in src/core/
3. Check data/config/ files for corruption
4. Reset configuration:
   ```bash
   rm -rf data/config/*
   python PREFLIGHT.py
   ```

---

#### "SecurityEngine: Authentication failed for user 'admin'"

**Issue**: Default credentials don't work or vault is corrupted

**Solution**:
1. Reset vault:
   ```bash
   rm data/vault/secrets.encrypted
   python src/main.py help  # Re-init with defaults
   ```
2. Change password in shell:
   ```
   > settings set admin_password "new_secure_password"
   ```
3. Check vault permissions: `ls -la data/vault/`

---

### Runtime Issues

#### "WebServer failed to start on port 8000"

**Issue**: Port already in use or permission denied

**Solution**:

**Windows**:
```bash
# Find process using port 8000
netstat -ano | findstr :8000
# Kill process (replace PID with actual PID)
taskkill /PID <PID> /F
```

**Linux/Mac**:
```bash
# Find process using port 8000
lsof -i :8000
# Kill process
kill -9 <PID>
```

**Alternative**: Change port in settings:
```
> settings set webserver_port 8001
```

---

#### "ReminderPulse thread crashed"

**Issue**: Background reminder system failed

**Solution**:
1. Check data/logs/errors.log for details
2. Restart reminder engine:
   ```
   > engine restart reminder
   ```
3. Check reminder_config.json validity:
   ```bash
   python -m json.tool data/config/reminder_config.json
   ```

---

#### "Command 'X' not found"

**Issue**: Command file missing or not auto-discovered

**Solution**:
1. Verify cmd file exists: `ls src/commands/cmd_x.py`
2. Reload commands:
   ```
   > reload
   ```
3. Check for syntax errors in cmd file:
   ```bash
   python -m py_compile src/commands/cmd_x.py
   ```

---

#### "Vault operation failed: encryption error"

**Issue**: Vault encryption/decryption failed

**Solution**:
1. Check vault key files: `ls data/vault/`
2. Verify disk space: `df -h` (need >100MB)
3. Check file permissions: `chmod 600 data/vault/secrets.encrypted`
4. Rescan vault integrity:
   ```
   > repair check vault
   ```

---

### Performance Issues

#### "Ghost Shell is slow/sluggish"

**Issue**: High CPU or memory usage

**Diagnosis**:
```
> status  # Check system resources
> engine info reminder  # Check engine metrics
```

**Solution**:

**High Memory Usage**:
- Clear old journal entries: `> journal clean --older-than 30days`
- Archive old reminders: `> reminders archive --before 2024-01-01`

**High CPU Usage**:
- Reduce reminder check interval: `> settings set reminder_check_ms 5000`
- Disable verbose logging: `> settings set log_level INFO`

---

#### "ReminderPulse consuming 100% CPU"

**Issue**: Background thread stuck in loop

**Solution**:
1. Increase check interval (default 500ms):
   ```
   > settings set reminder_pulse_interval_ms 2000
   ```
2. Restart reminder engine:
   ```
   > engine restart reminder
   ```
3. If still stuck, kill and restart:
   ```bash
   # Kill Ghost Shell process
   python src/main.py help  # Restart
   ```

---

### Connection Issues

#### "Cannot connect to remote host"

**Issue**: HostBridge can't reach target system

**Solution**:
1. Verify host is online: `ping <host_ip>`
2. Check firewall: Ensure port 22 (SSH) or 5985 (WinRM) is open
3. Test connectivity:
   ```bash
   # Linux/Mac
   ssh user@host
   
   # Windows
   winrs -r:host whoami
   ```
4. Update host config:
   ```
   > host connect <host_ip> --user <username> --password <password>
   ```

---

#### "API requests timing out"

**Issue**: WebServer unresponsive

**Solution**:
1. Check WebServer status: `> status`
2. Restart WebServer: `> engine restart webserver`
3. Increase timeout in client:
   ```python
   client = GhostShellClient(timeout=30)  # 30 seconds
   ```
4. Check network: `curl http://localhost:8000/api/v1/system/info`

---

### Data Issues

#### "Cannot find journal entry dated X"

**Issue**: Journal database corrupt or entries deleted

**Solution**:
1. Check journal integrity:
   ```
   > repair check journal
   ```
2. Restore from backup:
   ```
   > restore --from backup_date
   ```
3. View journal index:
   ```
   > journal list --verbose
   ```

---

#### "Reminder deadlines not triggering"

**Issue**: ReminderEngine not executing scheduled reminders

**Solution**:
1. Check reminder status:
   ```
   > remind --list
   ```
2. Verify system time is correct: `> status`
3. Restart reminder engine:
   ```
   > engine restart reminder
   ```
4. Test with immediate reminder:
   ```
   > remind "Test reminder" --in 10seconds
   ```

---

### Log Files Location

Ghost Shell maintains detailed logs:

```
data/logs/
├── system.log         # Core system events
├── commands.log       # Command execution
├── errors.log         # Error traces
└── security.log       # Authentication/vault operations
```

**View recent errors**:
```bash
tail -50 data/logs/errors.log
```

**Search logs**:
```bash
grep "ReminderPulse" data/logs/system.log
```

---

### Getting Help

**If issue persists after troubleshooting**:

1. **Collect diagnostic info**:
   ```
   > status > diag_report.txt
   > repair check --full > diag_full_report.txt
   ```

2. **Check GitHub Issues**: https://github.com/xBlynd/xsvGhost-Shell/issues

3. **Enable debug logging**:
   ```
   > settings set log_level DEBUG
   > reload
   ```

4. **Create issue with**:
   - Ghost Shell version: `> version`
   - Python version: `python --version`
   - OS information: `> status`
   - Diagnostic reports
   - Error logs (data/logs/errors.log)
   - Reproducible steps

---

## System Recovery

### Full System Reset

**WARNING: This deletes all data, configuration, and vaults**

```bash
# Backup first!
cp -r data data.backup

# Reset
rm -rf data/
python PREFLIGHT.py
python src/main.py help
```

### Restore from Backup

```bash
cp -r data.backup/* data/
python src/main.py help
```

### Emergency Single-Mode Boot

```bash
# Skip remote connections, WebServer
python src/main.py help  # Uses safe defaults
```

---

## Performance Tuning

### Optimize for slow systems

```
> settings set reminder_check_ms 3000       # 3s instead of 500ms
> settings set webserver_workers 2          # Reduce workers
> settings set max_concurrent_reminders 5   # Limit parallelism
> settings set log_level WARNING            # Reduce logging
```

### Optimize for high-load systems

```
> settings set reminder_check_ms 100        # More responsive
> settings set webserver_workers 8          # More workers
> settings set max_concurrent_reminders 20  # Higher parallelism
> settings set cache_size 1000              # Larger cache
```
