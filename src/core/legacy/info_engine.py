import importlib
import py_compile
import sys
from pathlib import Path

class InfoEngine:
    # ... keep your existing get_cloud_paths and scan_windows_deep ...

    @staticmethod
    def verify_all_commands(verbose_callback=None):
        import py_compile
        root = Path(__file__).parent.parent
        cmd_dir = root / "commands"
        custom_dir = cmd_dir / "custom"
        # Adjusted path to ensure 'library' is found in the project root
        lib_dir = root.parent / "library"
        
        results = {"SYSTEM": [], "CUSTOM": [], "LIBRARY": []}
        
        def check_syntax(file_path, cat):
            name = file_path.stem.replace("cmd_", "")
            # Send immediate feedback to the terminal if callback exists
            if verbose_callback:
                verbose_callback(f"  [TESTING] {cat:<7} -> {name:<12}")
            
            try:
                py_compile.compile(str(file_path), doraise=True)
                return (name, "✅ OK")
            except Exception as e:
                return (name, f"❌ BROKEN: {str(e).split(':')[-1].strip()}")

        # 1. System Commands
        for f in cmd_dir.glob("cmd_*.py"):
            results["SYSTEM"].append(check_syntax(f, "SYSTEM"))
            
        # 2. Custom Commands
        if custom_dir.exists():
            for f in custom_dir.glob("cmd_*.py"):
                results["CUSTOM"].append(check_syntax(f, "CUSTOM"))

        # 3. Library Items (Restoring Library Visibility)
        if lib_dir.exists():
            for f in lib_dir.glob("*.*"):
                if verbose_callback:
                    verbose_callback(f"  [CHECK]   LIBRARY -> {f.name:<12}")
                results["LIBRARY"].append((f.name, "✅ FOUND"))
                
        return results