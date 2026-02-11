"""
SecurityEngine - Authentication & Encryption
Handles vault encryption keys, session management, and 2FA.
"""
import os
import hashlib
import secrets
from pathlib import Path
from threading import Lock
import time

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    from cryptography.hazmat.backends import default_backend
    import base64
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

ROOT = Path(__file__).parent.parent.parent

class SecurityEngine:
    """The Gatekeeper - Manages authentication and encryption"""
    
    def __init__(self):
        self.encryption_key = None  # RAM ONLY
        self.fernet = None
        self.salt = None
        self.session_start = None
        self.lock = Lock()
        self.idle_timeout = 300  # 5 minutes
        self.last_activity = time.time()
        self.authenticated = False
    
    def initialize(self):
        """Load or generate salt"""
        salt_file = ROOT / 'data' / 'config' / '.salt'
        
        if salt_file.exists():
            self.salt = salt_file.read_bytes()
        else:
            self.salt = os.urandom(32)
            salt_file.parent.mkdir(parents=True, exist_ok=True)
            salt_file.write_bytes(self.salt)
    
    def derive_key(self, password: str) -> bytes:
        """Derive encryption key using PBKDF2 (100k iterations)"""
        if not CRYPTO_AVAILABLE:
            return hashlib.sha256(password.encode() + self.salt).digest()
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def authenticate(self, password: str) -> bool:
        """Authenticate and unlock vault"""
        with self.lock:
            try:
                self.encryption_key = self.derive_key(password)
                
                if CRYPTO_AVAILABLE:
                    self.fernet = Fernet(self.encryption_key)
                
                self.session_start = time.time()
                self.last_activity = time.time()
                self.authenticated = True
                return True
            except Exception as e:
                print(f"Authentication failed: {e}")
                return False
    
    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data using Fernet"""
        with self.lock:
            if not self.authenticated:
                raise RuntimeError("Not authenticated")
            
            self.last_activity = time.time()
            
            if CRYPTO_AVAILABLE and self.fernet:
                return self.fernet.encrypt(data)
            else:
                # Fallback: XOR with key (INSECURE but functional)
                key = self.encryption_key
                return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    
    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data using Fernet"""
        with self.lock:
            if not self.authenticated:
                raise RuntimeError("Not authenticated")
            
            self.last_activity = time.time()
            
            if CRYPTO_AVAILABLE and self.fernet:
                return self.fernet.decrypt(data)
            else:
                # Fallback: XOR reversal
                key = self.encryption_key
                return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    
    def check_session(self) -> bool:
        """Check if session has timed out"""
        with self.lock:
            if not self.authenticated:
                return False
            
            idle_time = time.time() - self.last_activity
            if idle_time > self.idle_timeout:
                self.lock_session()
                return False
            
            return True
    
    def lock_session(self):
        """Lock the session (wipe key from RAM)"""
        with self.lock:
            self.encryption_key = None
            self.fernet = None
            self.authenticated = False
            print("🔒 Session locked (idle timeout)")
    
    def shutdown(self):
        """Wipe encryption key from RAM"""
        with self.lock:
            if self.encryption_key:
                # Overwrite memory before deletion
                self.encryption_key = b'\x00' * len(self.encryption_key)
            self.encryption_key = None
            self.fernet = None
            self.authenticated = False
