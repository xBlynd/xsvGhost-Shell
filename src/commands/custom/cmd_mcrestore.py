"""
Command: mcrestore
Restores a Minecraft instance config from a ZIP created by mcbackup.
Usage: mcrestore vault         → finds latest ZIP in data/vault/mc_backups/
       mcrestore <path>        → restores from a specific ZIP file
"""

import os
import zipfile
import platform
from pathlib import Path

DESCRIPTION = "Restore a Minecraft instance config from an mcbackup ZIP"
USAGE = "mcrestore vault|<zip_path>"
REQUIRED_ROLE = "GUEST"
ENGINE_DEPS = ["vault"]

MANIFEST = {
    "name": "mcrestore",
    "description": DESCRIPTION,
    "usage": USAGE,
    "required_role": REQUIRED_ROLE,
    "engine_deps": ENGINE_DEPS,
}

# Files included in the ZIP that are documentation, not game files
_DOC_FILES = {"MOD_LIST.txt", "RESTORE_INSTRUCTIONS.txt", "JAVA_ARGS.txt", "instance.cfg"}


def _find_latest_vault_zip(vault_engine):
    """Return Path to most recent .zip in vault/mc_backups/, or None."""
    mc_backups = Path(vault_engine.vault_dir) / "mc_backups"
    if not mc_backups.exists():
        return None
    zips = [f for f in mc_backups.iterdir() if f.suffix == ".zip" and f.is_file()]
    if not zips:
        return None
    return max(zips, key=lambda f: f.stat().st_mtime)


def _detect_instance_name(zf):
    """Read instance.cfg from inside the ZIP and return the instance name, or None."""
    try:
        with zf.open("instance.cfg") as cfg:
            for line in cfg.read().decode("utf-8", errors="replace").splitlines():
                if line.startswith("name="):
                    return line.split("=", 1)[1].strip()
    except (KeyError, Exception):
        pass
    return None


def _get_prism_instances_dir():
    """Return the Prism Launcher instances directory or None."""
    appdata = os.environ.get("APPDATA", "")
    if not appdata:
        return None
    path = Path(appdata) / "PrismLauncher" / "instances"
    return path if path.exists() else None


def execute(kernel, args):
    if platform.system() != "Windows":
        return "[!] mcrestore is Windows-only (Prism Launcher path detection)."

    if not args:
        return f"Usage: {USAGE}\n  vault     → latest ZIP from data/vault/mc_backups/\n  <path>    → path to a specific ZIP file"

    vault_engine = kernel.get_engine("vault")
    dest_arg = args[0]

    # --- Resolve ZIP path ---
    if dest_arg.lower() in ("vault", "latest"):
        zip_path = _find_latest_vault_zip(vault_engine)
        if zip_path is None:
            vault_mc = Path(vault_engine.vault_dir) / "mc_backups"
            return (
                f"[!] No backups found in vault.\n"
                f"    Expected: {vault_mc}\n"
                f"    Run 'mcbackup vault' on your source machine first."
            )
        print(f"[i] Using latest vault backup: {zip_path.name}")
    else:
        zip_path = Path(dest_arg)
        if not zip_path.exists():
            return f"[!] File not found: {zip_path}"

    # --- Validate ZIP ---
    if not zipfile.is_zipfile(str(zip_path)):
        return f"[!] Not a valid ZIP file: {zip_path}"

    with zipfile.ZipFile(str(zip_path), "r") as zf:
        all_names = zf.namelist()

        # Verify it looks like an mcbackup archive
        top_names = {n.split("/")[0] for n in all_names}
        if "MOD_LIST.txt" not in top_names and "instance.cfg" not in top_names:
            return (
                "[!] This doesn't look like an mcbackup archive (no MOD_LIST.txt or instance.cfg).\n"
                "    Only ZIPs created by 'mcbackup' can be restored with this command."
            )

        # --- Check Prism is installed ---
        prism_dir = _get_prism_instances_dir()
        if prism_dir is None:
            return (
                "[!] Prism Launcher not found at %APPDATA%\\PrismLauncher\\instances\\\n"
                "    1. Install Prism Launcher: https://prismlauncher.org\n"
                "    2. Create a new instance\n"
                "    3. Launch it once to generate the minecraft/ folder\n"
                "    4. Run mcrestore again"
            )

        # --- Detect target instance name ---
        instance_name = _detect_instance_name(zf)
        if instance_name is None:
            instance_name = "Minecraft PVP"
            print(f"[i] Could not detect instance name from backup. Defaulting to: {instance_name}")
        else:
            print(f"[i] Target instance: {instance_name}")

        # --- Check instance folder exists ---
        instance_path = prism_dir / instance_name
        if not instance_path.exists():
            return (
                f"[!] Instance folder not found: {instance_path}\n"
                f"    1. Open Prism Launcher\n"
                f"    2. Create a new instance named exactly: {instance_name}\n"
                f"    3. Launch it once to generate the .minecraft folder, then close\n"
                f"    4. Run mcrestore again"
            )

        minecraft_path = instance_path / "minecraft"
        if not minecraft_path.exists():
            print(f"[i] minecraft/ not found — creating: {minecraft_path}")
            minecraft_path.mkdir(parents=True, exist_ok=True)

        # --- Extract game files (skip doc files) ---
        print(f"[1/3] Extracting files to {minecraft_path} ...")
        restored = 0
        skipped_docs = 0

        for member in zf.infolist():
            # Skip directories
            if member.filename.endswith("/"):
                continue

            top = member.filename.split("/")[0]

            # Skip documentation files at root of ZIP
            if top in _DOC_FILES:
                skipped_docs += 1
                continue

            dest_file = minecraft_path / member.filename
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            with zf.open(member) as src, open(str(dest_file), "wb") as dst:
                dst.write(src.read())
            restored += 1

        # --- Display mod list ---
        print("[2/3] Mod list (you must download these manually):")
        mod_list_text = None
        try:
            with zf.open("MOD_LIST.txt") as f:
                mod_list_text = f.read().decode("utf-8", errors="replace")
        except KeyError:
            pass

        if mod_list_text:
            print("")
            for line in mod_list_text.splitlines():
                print(f"  {line}")
            print("")
        else:
            print("  (No MOD_LIST.txt in backup)")

        # --- Display Java args reminder ---
        print("[3/3] Java args reminder:")
        java_args_text = None
        try:
            with zf.open("JAVA_ARGS.txt") as f:
                java_args_text = f.read().decode("utf-8", errors="replace")
        except KeyError:
            pass

        if java_args_text:
            print("")
            for line in java_args_text.splitlines():
                print(f"  {line}")
            print("")
        else:
            print("  (No JAVA_ARGS.txt in backup)")

    # --- Summary ---
    lines = [
        "",
        "  Restore complete!",
        f"  Source:          {zip_path.name}",
        f"  Instance:        {instance_name}",
        f"  Location:        {minecraft_path}",
        f"  Files restored:  {restored}",
        "",
        "  Next steps:",
        "    1. Download mods listed above into your instance's mods folder",
        "    2. Apply Java args in Prism: right-click instance → Edit → Java",
        "    3. Launch and enjoy",
    ]
    return "\n".join(lines)
