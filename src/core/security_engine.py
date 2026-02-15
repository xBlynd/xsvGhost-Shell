"""
Engine 02: Security Engine - The Gatekeeper
=============================================
Authentication, authorization, and key management.
Supports silent auth (if key exists, no prompt) and RBAC.

Key System:
- God Key:   Full access. Generated on first boot or via `keys generate god`.
- Admin Key: Standard access. Can be issued by God.
- Guest Key: Read-only. Can be time-limited. Great for lending USB.

Key Storage:
  data/keys/
  ├── god.key           (the master key file)
  ├── keyring.json      (tracks all issued keys with metadata)
  └── guest_*.key       (temporary guest keys)

Compartmentalization:
- MUST NOT handle file operations (VaultEngine)
- MUST NOT execute system commands (RootEngine)
- ONLY validates identity and permissions
"""

import os
import json
import hashlib
import secrets
import getpass
from datetime import datetime, timedelta


# === ROLE DEFINITIONS ===
class Role:
    GOD = "GOD"
    ADMIN = "ADMIN"
    GUEST = "GUEST"

    # Permission hierarchy
    HIERARCHY = {
        "GOD": 3,
        "ADMIN": 2,
        "GUEST": 1,
    }

    @staticmethod
    def has_permission(current_role, required_role):
        """Check if current role meets or exceeds required role."""
        current_level = Role.HIERARCHY.get(current_role, 0)
        required_level = Role.HIERARCHY.get(required_role, 99)
        return current_level >= required_level


class SecurityEngine:
    """
    The Gatekeeper - manages authentication and authorization.
    """

    ENGINE_NAME = "security"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel
        self.root_dir = kernel.root_dir
        self.keys_dir = os.path.join(self.root_dir, "data", "keys")
        self.current_role = Role.GUEST  # Default until authenticated
        self.current_key_id = None
        self.authenticated = False

        os.makedirs(self.keys_dir, exist_ok=True)

        # Authenticate on init (silent if key exists)
        self._authenticate()

    # =========================================================================
    # AUTHENTICATION
    # =========================================================================

    def _authenticate(self):
        """
        Silent Authentication Pattern:
        1. Check for god.key -> instant GOD access
        2. Check for any valid admin/guest key -> appropriate access
        3. If no key found -> first boot experience (generate god key)
        """
        god_key_path = os.path.join(self.keys_dir, "god.key")

        if os.path.exists(god_key_path):
            # Silent auth - God Key detected
            try:
                with open(god_key_path, 'r') as f:
                    key_data = json.load(f)
                self.current_role = Role.GOD
                self.current_key_id = key_data.get("key_id", "god-master")
                self.authenticated = True
                return
            except Exception:
                pass

        # Check for admin/guest keys
        keyring = self._load_keyring()
        for key_id, key_info in keyring.items():
            key_file = os.path.join(self.keys_dir, f"{key_id}.key")
            if os.path.exists(key_file):
                # Check expiry
                if key_info.get("expires"):
                    exp = datetime.fromisoformat(key_info["expires"])
                    if datetime.now() > exp:
                        continue  # Key expired

                self.current_role = key_info.get("role", Role.GUEST)
                self.current_key_id = key_id
                self.authenticated = True
                return

        # No valid key found - First Boot Experience
        self._first_boot_setup()

    def _first_boot_setup(self):
        """
        First time running Ghost Shell. Generate the God Key.
        This is the ONLY time we prompt the user during auth.
        """
        print()
        print("   ╔════════════════════════════════════════════╗")
        print("   ║     👻 GHOST SHELL - FIRST BOOT SETUP     ║")
        print("   ╠════════════════════════════════════════════╣")
        print("   ║  No God Key detected.                     ║")
        print("   ║  Generating your master key now...         ║")
        print("   ╚════════════════════════════════════════════╝")
        print()

        # Generate passphrase-protected God Key
        while True:
            passphrase = getpass.getpass("   Set your God Key passphrase: ")
            if len(passphrase) < 4:
                print("   [!] Passphrase must be at least 4 characters.")
                continue
            confirm = getpass.getpass("   Confirm passphrase: ")
            if passphrase != confirm:
                print("   [!] Passphrases don't match. Try again.")
                continue
            break

        key_data = self.generate_key("god-master", Role.GOD, passphrase=passphrase)

        # Save as god.key
        god_key_path = os.path.join(self.keys_dir, "god.key")
        with open(god_key_path, 'w') as f:
            json.dump(key_data, f, indent=2)

        self.current_role = Role.GOD
        self.current_key_id = "god-master"
        self.authenticated = True

        print()
        print("   ⚡ God Key generated. You are now authenticated.")
        print(f"   🔑 Key ID: {key_data['key_id']}")
        print(f"   📁 Stored: {god_key_path}")
        print()

    # =========================================================================
    # KEY MANAGEMENT
    # =========================================================================

    def generate_key(self, key_id=None, role=Role.GUEST, passphrase=None, 
                     expires_hours=None, label=None):
        """
        Generate a new authentication key.
        
        Args:
            key_id: Unique identifier (auto-generated if None)
            role: Role level (GOD, ADMIN, GUEST)
            passphrase: Optional passphrase for the key
            expires_hours: Hours until key expires (None = never)
            label: Human-readable label (e.g., "Dad's Laptop", "Lab PC #3")
        
        Returns:
            Key data dict
        """
        if not key_id:
            key_id = f"{role.lower()}-{secrets.token_hex(6)}"

        # Generate the actual secret
        key_secret = secrets.token_hex(32)

        # Hash the passphrase if provided
        passphrase_hash = None
        if passphrase:
            salt = secrets.token_hex(16)
            passphrase_hash = hashlib.sha256(
                (passphrase + salt).encode()
            ).hexdigest()
        else:
            salt = None

        # Calculate expiry
        expires = None
        if expires_hours:
            expires = (datetime.now() + timedelta(hours=expires_hours)).isoformat()

        key_data = {
            "key_id": key_id,
            "role": role,
            "secret": key_secret,
            "passphrase_hash": passphrase_hash,
            "salt": salt,
            "created": datetime.now().isoformat(),
            "expires": expires,
            "label": label or key_id,
            "creator": self.current_key_id or "system",
            "active": True,
        }

        # Save to keyring
        self._save_to_keyring(key_data)

        return key_data

    def issue_key(self, role, label=None, expires_hours=None):
        """
        Issue a new key (wrapper for generate_key with file creation).
        Only God can issue keys.
        """
        if self.current_role != Role.GOD:
            return None, "Only God role can issue keys"

        if role == Role.GOD:
            return None, "Cannot issue additional God keys. There can be only one."

        key_data = self.generate_key(
            role=role,
            expires_hours=expires_hours,
            label=label,
        )

        # Write key file
        key_file = os.path.join(self.keys_dir, f"{key_data['key_id']}.key")
        with open(key_file, 'w') as f:
            json.dump(key_data, f, indent=2)

        return key_data, None

    def revoke_key(self, key_id):
        """Revoke a key by ID."""
        if self.current_role != Role.GOD:
            return False, "Only God role can revoke keys"

        if key_id == "god-master":
            return False, "Cannot revoke the God Key"

        keyring = self._load_keyring()
        if key_id in keyring:
            keyring[key_id]["active"] = False
            keyring[key_id]["revoked"] = datetime.now().isoformat()
            self._save_keyring(keyring)

            # Remove key file
            key_file = os.path.join(self.keys_dir, f"{key_id}.key")
            if os.path.exists(key_file):
                os.remove(key_file)

            return True, f"Key '{key_id}' revoked"

        return False, f"Key '{key_id}' not found"

    def list_keys(self):
        """List all keys in the keyring."""
        keyring = self._load_keyring()
        keys = []
        for key_id, info in keyring.items():
            # Check if expired
            expired = False
            if info.get("expires"):
                expired = datetime.now() > datetime.fromisoformat(info["expires"])

            keys.append({
                "key_id": key_id,
                "role": info.get("role", "UNKNOWN"),
                "label": info.get("label", key_id),
                "created": info.get("created", "unknown"),
                "expires": info.get("expires", "never"),
                "active": info.get("active", True) and not expired,
                "creator": info.get("creator", "unknown"),
            })

        return keys

    def validate_passphrase(self, passphrase, key_data):
        """Validate a passphrase against a key's stored hash."""
        if not key_data.get("passphrase_hash"):
            return True  # No passphrase set

        salt = key_data.get("salt", "")
        check_hash = hashlib.sha256(
            (passphrase + salt).encode()
        ).hexdigest()

        return check_hash == key_data["passphrase_hash"]

    # =========================================================================
    # AUTHORIZATION
    # =========================================================================

    def has_permission(self, required_role):
        """Check if current session has the required role."""
        if not self.authenticated:
            return False
        return Role.has_permission(self.current_role, required_role)

    def require_role(self, role):
        """Decorator-style check. Returns (allowed, message)."""
        if self.has_permission(role):
            return True, None
        return False, f"Access Denied. Required: {role}, Current: {self.current_role}"

    # =========================================================================
    # KEYRING PERSISTENCE
    # =========================================================================

    def _load_keyring(self):
        """Load the keyring (metadata about all issued keys)."""
        keyring_path = os.path.join(self.keys_dir, "keyring.json")
        if os.path.exists(keyring_path):
            try:
                with open(keyring_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_keyring(self, keyring):
        """Save the keyring."""
        keyring_path = os.path.join(self.keys_dir, "keyring.json")
        with open(keyring_path, 'w') as f:
            json.dump(keyring, f, indent=2)

    def _save_to_keyring(self, key_data):
        """Add a key's metadata to the keyring."""
        keyring = self._load_keyring()
        keyring[key_data["key_id"]] = {
            "role": key_data["role"],
            "label": key_data["label"],
            "created": key_data["created"],
            "expires": key_data["expires"],
            "active": key_data["active"],
            "creator": key_data["creator"],
        }
        self._save_keyring(keyring)
