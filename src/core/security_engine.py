"""
Security Engine - The Gatekeeper
Handles authentication, authorization, RBAC
"""

import os
import hashlib
from enum import Enum
from pathlib import Path

class Role(Enum):
    """User roles"""
    GOD = "GOD"          # Full access
    ADMIN = "ADMIN"      # Standard diagnostics
    GUEST = "GUEST"      # Read-only

class SecurityEngine:
    """
    Manages authentication and authorization.
    Silent by default - only prompts if needed.
    """
    
    def __init__(self, kernel):
        self.kernel = kernel
        self.name = "security"
        self.current_role = None
        
        # Paths
        core = kernel.engines.get('ghost_core')
        if core:
            self.keys_dir = core.get_path("data", "keys")
        else:
            # Fallback if core not available
            self.keys_dir = Path(__file__).parent.parent.parent / "data" / "keys"
        
        # Authenticate immediately
        self._authenticate()
    
    def _authenticate(self):
        """
        Silent authentication.
        Only prompts if no god key found.
        """
        god_key_file = self.keys_dir / "god.key"
        
        if god_key_file.exists():
            # Silent auth - god key exists
            self.current_role = Role.GOD
            return
        
        # No god key - check for guest key
        guest_key_file = self.keys_dir / "guest.key"
        if guest_key_file.exists():
            self.current_role = Role.GUEST
            return
        
        # First boot - create god key
        print("\n[Security] First boot detected - Creating god key...")
        passphrase = input("Enter god passphrase (or press Enter for auto-generate): ").strip()
        
        if not passphrase:
            import secrets
            passphrase = secrets.token_hex(16)
            print(f"[Security] Auto-generated passphrase: {passphrase}")
            print("[Security] SAVE THIS - You'll need it to regain god access!")
        
        self._create_god_key(passphrase)
        self.current_role = Role.GOD
    
    def _create_god_key(self, passphrase):
        """Create god key from passphrase"""
        self.keys_dir.mkdir(parents=True, exist_ok=True)
        
        # Hash passphrase
        key_hash = hashlib.sha256(passphrase.encode()).hexdigest()
        
        god_key_file = self.keys_dir / "god.key"
        god_key_file.write_text(key_hash)
        
        print(f"[Security] God key created at: {god_key_file}")
    
    def has_permission(self, required_role):
        """Check if current role has permission"""
        role_hierarchy = {
            Role.GOD: 3,
            Role.ADMIN: 2,
            Role.GUEST: 1
        }
        
        current_level = role_hierarchy.get(self.current_role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return current_level >= required_level
    
    def get_role_name(self):
        """Get current role as string"""
        return self.current_role.value if self.current_role else "UNKNOWN"
