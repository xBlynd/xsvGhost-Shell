from getpass import getpass
from typing import Any


class SecurityEngine:
    """The Gatekeeper.

    Phoenix v0: requires a password if configured, otherwise dev-pass.
    """

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel
        self.authenticated = False

    def authenticate(self) -> None:
        settings = self.kernel.load_settings()
        required_password = settings.get("login_password")

        if not required_password:
            # Dev mode: no password configured
            self.authenticated = True
            print("[Security] No login_password set. Dev mode: authenticated.")
            return

        for attempt in range(3):
            entered = getpass("Ghost Shell password: ")
            if entered == required_password:
                self.authenticated = True
                print("[Security] Authentication successful.")
                return
            else:
                print("[Security] Invalid password.")

        print("[Security] Too many failed attempts. Locking out.")
        self.authenticated = False
