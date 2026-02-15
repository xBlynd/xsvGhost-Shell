"""
Engine 03: Ghost Engine - The Shadow
======================================
Stealth and anti-forensics. Cleans up temp files on shutdown.
Maintains minimal process footprint.

Compartmentalization:
- Runs primarily during kernel shutdown
- Does NOT interfere with running operations
"""

import os
import shutil


class GhostEngine:
    """The Shadow - cleanup, stealth, minimal footprint."""

    ENGINE_NAME = "ghost"
    ENGINE_VERSION = "1.0.0"

    def __init__(self, kernel):
        self.kernel = kernel
        self.root_dir = kernel.root_dir
        self.cleanup_targets = [
            "__pycache__",
        ]
        self.cleanup_extensions = [
            ".pyc", ".pyo",
        ]
        # Register for shutdown event
        kernel.on("shutdown", lambda data: self.cleanup())

    def cleanup(self):
        """Clean up temp files and caches. Called on shutdown."""
        removed_dirs = 0
        removed_files = 0

        for root, dirs, files in os.walk(self.root_dir):
            # Skip .git directory
            if ".git" in root:
                continue

            # Remove __pycache__ directories
            for d in dirs:
                if d in self.cleanup_targets:
                    target = os.path.join(root, d)
                    try:
                        shutil.rmtree(target)
                        removed_dirs += 1
                    except Exception:
                        pass

            # Remove .pyc files
            for f in files:
                if any(f.endswith(ext) for ext in self.cleanup_extensions):
                    target = os.path.join(root, f)
                    try:
                        os.remove(target)
                        removed_files += 1
                    except Exception:
                        pass

        return {
            "dirs_removed": removed_dirs,
            "files_removed": removed_files,
        }

    def get_footprint(self):
        """Calculate current disk footprint of Ghost Shell."""
        total_size = 0
        file_count = 0

        for root, dirs, files in os.walk(self.root_dir):
            if ".git" in root:
                continue
            for f in files:
                fp = os.path.join(root, f)
                try:
                    total_size += os.path.getsize(fp)
                    file_count += 1
                except Exception:
                    pass

        return {
            "total_bytes": total_size,
            "total_mb": round(total_size / (1024 * 1024), 2),
            "file_count": file_count,
        }
