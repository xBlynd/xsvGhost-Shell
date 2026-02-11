# 📄 SECURITY.md - Vault & Encryption Architecture

## Overview

Ghost Shell implements a **split-brain security model**:
- **Public Brain (GitHub):** Logic, commands, and documentation
- **Private Soul (USB/Cloud):** Encrypted vault with personal data

This document details vault encryption, authentication, and security controls.

## Vault Encryption Architecture

### Encryption Method: Fernet (Symmetric)

**Algorithm:** AES-128-CBC with HMAC authentication  
**Key Size:** 128-bit (cryptographically secure)  
**Implementation:** Python `cryptography.Fernet`  
**Standard:** RFC 7539  

```python
from cryptography.fernet import Fernet

# Master key stored in RAM during session
master_key = Fernet.generate_key()  # 44-byte URL-safe base64
cipher = Fernet(master_key)

# Encrypt sensitive data
encrypted_data = cipher.encrypt(b"sensitive data")

# Decrypt (requires master key)
plaintext = cipher.decrypt(encrypted_data)
```

### Vault File Structure

```
data/vault/                              # .gitignore'd - Never syncs to GitHub
├── .vault_key                        # Master encryption key (NOT INCLUDED in repo)
├── config/
│   └── settings.json                # User preferences (ENCRYPTED)
├── notes/
│   └── *.md                         # Personal notes (ENCRYPTED)
├─┐ journals/
│   └─┐ 2026-02-11.json             # Daily logs (ENCRYPTED)
├── loot/
│   └── passwords.json             # Password vault (ENCRYPTED + COMPRESSED)
└── backups/
    └── vault_2026-02-11_010000.bak # Timestamped backups
```

### Master Key Management

**Location:** Stored in RAM only (never on disk)  
**Lifetime:** Created at session start, destroyed on `kernel.shutdown()`  
**Derivation:** PBKDF2 from user password

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import os

# User password + salt -> master key
password = b"user_password"
salt = os.urandom(16)  # Random salt

kdf = PBKDF2(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,  # NIST recommended (2024)
)
master_key = kdf.derive(password)
```

## Authentication

### 1. Startup Authentication

When Ghost Shell boots:

1. **GhostCoreEngine** initializes
2. **SecurityEngine** prompts for master password
3. PBKDF2 derives master key from password
4. Key is validated against stored hash
5. On success: Master key stays in RAM; On failure: Exit

```
Ghost Shell v6.0 - "One Stick, Any Computer, Surgical Precision"

Enter Master Password: **
✅ Authentication successful. Welcome back.

xsv>
```

### 2. Session Security

- **Idle Timeout:** Auto-lock after 5 minutes (SecurityEngine)
- **Lock Command:** `xsv> lock` - Clears master key from RAM
- **Unlock:** Re-authentication required
- **Crash Handling:** Kernel shutdown clears key automatically

## Vault Protection Mechanisms

### 1. File-Level Encryption

Each vault file is encrypted independently:

```python
# Writing to vault
def write_vault(filename, data, master_key):
    cipher = Fernet(master_key)
    encrypted = cipher.encrypt(data.encode())
    with open(f"data/vault/{filename}", "wb") as f:
        f.write(encrypted)

# Reading from vault
def read_vault(filename, master_key):
    cipher = Fernet(master_key)
    with open(f"data/vault/{filename}", "rb") as f:
        encrypted = f.read()
    return cipher.decrypt(encrypted).decode()
```

### 2. Integrity Verification

**HeartbeatEngine** monitors vault integrity:

```
xsv> vault integrity
✅ vault_key: OK (hash matches)
✅ settings.json: OK
✅ journals/: OK (4 files)
✅ loot/passwords.json: OK
✅ All files encrypted and tamper-free
```

### 3. Backup & Recovery

**Automatic backups** before vault modifications:

```bash
# Create backup
xsv> vault backup
Created: data/backups/vault_2026-02-11_010000.bak

# Restore from backup
xsv> vault restore vault_2026-02-11_010000.bak
Restored vault from backup. 4 files recovered.
```

## The SecurityEngine (The Gatekeeper)

Responsibilities:

| Function | Implementation |
|----------|----------------|
| **Login System** | PBKDF2 password hashing + master key derivation |
| **Vault Key Management** | Keep Fernet key in RAM, destroy on shutdown |
| **Session Monitoring** | 5-minute idle timeout, auto-lock |
| **2FA (Future)** | Keyfile check + password (planned for v7.0) |
| **Encryption/Decryption** | All vault reads/writes pass through SecurityEngine |

## The GhostEngine (The Phantom) - Anti-Forensics

When exiting, Ghost Shell performs:

1. **Timestamp Wiping** - Reset file modification times
2. **Clipboard Scrubbing** - Clear Windows clipboard
3. **Temp File Removal** - Delete temporary config copies
4. **Memory Wipe** - Overwrite master key with zeros

```python
# On shutdown
def kernel_shutdown():
    # Clear master key from RAM
    self.security_engine.master_key = b'\x00' * len(self.master_key)
    
    # Wipe temp files
    for temp_file in temp_vault_copies:
        secure_delete(temp_file)  # Overwrite with random data
    
    # Clear clipboard
    if IS_WINDOWS:
        run_powershell("Clear-Clipboard")
```

## Threat Model

### Protected Against

✅ **Disk-Level Attacks:** All vault files encrypted; unreadable without master key  
✅ **Passive Monitoring:** No plaintext files; no temporary unencrypted copies  
✅ **USB Theft:** Without password, vault is inaccessible  
✅ **Session Hijacking:** 5-minute timeout + memory key destruction  
✅ **Forensic Recovery:** Anti-forensics wipes temps/clipboard on exit  

### NOT Protected Against

⚠️ **Active Physical Access:** If someone has USB + admin access + your password  
⚠️ **Memory Dumps:** If attacker dumps RAM while Ghost Shell is running, key is visible  
⚠️ **Keylogging:** Passwords typed can be intercepted (mitigated by using keyfiles)  
⚠️ **Shoulder Surfing:** Always shield your password input  

## Best Practices

### 1. Master Password

✅ Use **minimum 16 characters**  
✅ Mix **uppercase, lowercase, numbers, symbols**  
✅ **Never reuse** passwords from other services  
⚠️ Don't write it down or share it  

### 2. USB Security

✅ Use **hardware encryption** (BitLocker, LUKS)
✅ **Physically secure** the USB  
✅ **Backup vault** regularly
✅ Test **recovery process** quarterly  

### 3. Session Hygiene

✅ **Lock** the shell before stepping away (`xsv> lock`)  
✅ **Exit** Ghost Shell when done (`xsv> exit`)  
✅ **Clear clipboard** after sensitive ops  
✅ Use **private browsing** for web tools  

### 4. Regular Audits

```bash
# Monthly security check
xsv> vault integrity
xsv> engine status    # Check all engines
xsv> logs error      # Review any errors
```

## Known Limitations

1. **No Remote Sync Encryption (v6.0)** - Cloud sync planned for v7.0
2. **Single-Factor Authentication** - 2FA in development
3. **No Hardware Security Module** - Future integration possible
4. **Python-Level Vulnerability** - No protection against Python code injection

## Security Roadmap

| Version | Feature |
|---------|----------|
| **v6.0** (Current) | Fernet encryption, PBKDF2, 5-min timeout |
| **v6.5** | Hardware keyfile support, HMAC verification |
| **v7.0** | 2FA, cloud encryption, remote backup |
| **v8.0** | Hardware security module support (optional) |

## Reporting Security Issues

**DO NOT** open public GitHub issues for security vulnerabilities.

1. Email: [Your secure contact here]
2. Include: Vulnerability type, reproduction steps, impact
3. **Embargo:** Wait for patch before public disclosure

---

**Last Updated:** February 11, 2026  
**Threat Model Reviewed:** February 11, 2026  
**Next Audit:** May 11, 2026
