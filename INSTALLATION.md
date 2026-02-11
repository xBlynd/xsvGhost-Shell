# 📦 INSTALLATION.md - xsvGhost-Shell v6.0 Setup Guide

## Quick Start (Windows)

### Prerequisites
- USB Drive (8GB+ recommended for full vault)
- Windows 7 / Windows 10 / Windows 11
- Python 3.9+ (will be auto-detected)
- Admin rights (for certain commands)

### Installation Steps

1. **Clone/Download the repository** to your USB drive
   ```bash
   git clone https://github.com/xBlynd/xsvGhost-Shell.git D:\ghost-shell
   # OR download ZIP and extract to USB
   ```

2. **Navigate to the directory**
   ```bash
   cd D:\ghost-shell
   ```

3. **Run PREFLIGHT checks**
   ```bash
   python PREFLIGHT.py
   ```
   This verifies:
   - Python version compatibility
   - Required dependencies
   - Vault folder structure
   - File permissions

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Launch Ghost Shell**
   ```bash
   LAUNCH.bat
   # OR directly: python src/main.py
   ```

6. **First-time setup**
   ```
   xsv> setup
   # Creates config, initializes vault, sets password
   ```

## Linux / ParrotOS Installation

### Prerequisites
- Linux distribution (Ubuntu 20.04+ recommended)
- Python 3.9+
- libnotify-bin (for toasts)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/xBlynd/xsvGhost-Shell.git ~/ghost-shell
   cd ~/ghost-shell
   ```

2. **Install system dependencies**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install -y python3.9 python3-pip libnotify-bin

   # Arch
   sudo pacman -S python python-pip libnotify
   ```

3. **Run PREFLIGHT**
   ```bash
   python3 PREFLIGHT.py
   ```

4. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Create launcher script**
   ```bash
   chmod +x launch.sh
   ./launch.sh  # Creates ghost shell
   ```

6. **Initial setup**
   ```
   xsv> setup
   ```

## Troubleshooting

### "PREFLIGHT.py not found"
Download PREFLIGHT.py from the repo or create it (see CRITICAL ISSUE section above)

### "ModuleNotFoundError: No module named 'src'"
Ensure you're running from the root directory:
```bash
cd /path/to/xsvGhost-Shell
python src/main.py
```

### Toast notifications not working (Linux)
```bash
sudo apt install libnotify-bin  # Ubuntu/Debian
sudo pacman -S libnotify        # Arch
```

### Permission denied on LAUNCH.bat
```bash
chmod +x LAUNCH.bat  # Make executable
```

## Vault Structure Setup

After installation, your vault will be:
```
data/vault/
├── config/
│   └── settings.json          # User preferences
├── notes/                     # Personal notes
├── journals/                  # Daily logs
├── loot/                      # Sensitive data (encrypted)
└── library/                   # Installed scripts
```

All vault contents are encrypted with Fernet (256-bit).

## Post-Installation Configuration

### 1. Set Master Password
```
xsv> settings password --set
Enter new master password: ***
Confirm: ***
```

### 2. Configure Preferences
```
xsv> settings theme --set blue  # Work mode
# OR
xsv> settings theme --set red   # Hacking mode
```

### 3. Test Core Engines
```
xsv> status            # Check all engines
xsv> info              # System information
xsv> help              # View all commands
```

## Updates

### Update from GitHub
```bash
git pull origin main
# Then re-run PREFLIGHT to verify integrity
python PREFLIGHT.py
```

### Backup Before Update
```bash
xsv> vault backup
# Creates timestamped backup in data/backups/
```

## First Commands to Try

```bash
# Add a task
xsv> todo add "Learn Ghost Shell" --due 10m

# Set a reminder
xsv> remind "Check email" 30m

# View system health
xsv> status

# Check available commands
xsv> help

# Open the interactive shell
xsv> shell
```

## Need Help?

- Check `docs/` for detailed documentation
- Run `xsv> help <command>` for command-specific help
- Review `TROUBLESHOOTING.md` for common issues

---

**Version:** v6.0-Ghost-Kernel  
**Status:** Alpha / Active Development  
**Last Updated:** February 11, 2026
