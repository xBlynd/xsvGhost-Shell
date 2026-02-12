import os
from typing import Any


class VaultEngine:
    """The Librarian: simple text file CRUD under data/vault."""

    def __init__(self, kernel: Any) -> None:
        self.kernel = kernel

    def _ns_dir(self, namespace: str) -> str:
        path = os.path.join(self.kernel.vault_dir, namespace)
        os.makedirs(path, exist_ok=True)
        return path

    def save_text(self, namespace: str, name: str, content: str) -> str:
        path = os.path.join(self._ns_dir(namespace), f"{name}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
