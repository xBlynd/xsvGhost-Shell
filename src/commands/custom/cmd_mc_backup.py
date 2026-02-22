"""
Command: mcbackup
Backs up Prism Launcher Minecraft instance configs to ZIP archives.
Destination: Desktop (default), 'vault' (SyncThing-synced), or any path.

Usage:
  mcbackup                        → ALL instances, Desktop
  mcbackup vault                  → ALL instances, Vault
  mcbackup "Minecraft PVP"        → single instance, Desktop
  mcbackup "Minecraft PVP" vault  → single instance, Vault
"""

import os
import shutil
import zipfile
import platform
import tempfile
from datetime import datetime
from pathlib import Path

DESCRIPTION = "Backup Prism Launcher Minecraft instance config(s) to ZIP archive(s)"
USAGE = "mcbackup [vault|<path>]  OR  mcbackup <instance_name> [vault|<path>]"
REQUIRED_ROLE = "GUEST"
ENGINE_DEPS = ["vault"]

MANIFEST = {
    "name": "mcbackup",
    "description": DESCRIPTION,
    "usage": USAGE,
    "required_role": REQUIRED_ROLE,
    "engine_deps": ENGINE_DEPS,
}

_DEST_KEYWORDS = {"vault"}


def _get_prism_instances_dir():
    """Return the Prism Launcher instances directory path or None."""
    appdata = os.environ.get("APPDATA", "")
    if not appdata:
        return None
    path = Path(appdata) / "PrismLauncher" / "instances"
    return path if path.exists() else None


def _list_instances(instances_dir):
    """Return list of instance folder names that contain a minecraft dir."""
    results = []
    for item in instances_dir.iterdir():
        if item.is_dir() and (item / "minecraft").exists():
            results.append(item.name)
    return sorted(results)


def _backup_instance(instance_name, prism_dir, output_dir, timestamp):
    """
    Back up a single instance to output_dir.
    Returns (zip_path, copied_count, mod_count) on success, or raises.
    """
    instance_path = prism_dir / instance_name
    minecraft_path = instance_path / "minecraft"

    archive_name = f"MC-Config-Backup-{instance_name}-{timestamp}"
    staging_dir = Path(tempfile.mkdtemp()) / archive_name
    staging_dir.mkdir(parents=True, exist_ok=True)

    # --- Copy configs ---
    config_targets = [
        "config",
        "options.txt",
        "servers.dat",
        "shaderpacks",
        "resourcepacks",
        "saves",
    ]
    copied = 0
    for target in config_targets:
        src = minecraft_path / target
        if src.exists():
            dst = staging_dir / target
            try:
                if src.is_dir():
                    shutil.copytree(str(src), str(dst))
                else:
                    shutil.copy2(str(src), str(dst))
                copied += 1
            except Exception as e:
                print(f"    [!] Could not copy {target}: {e}")

    # --- Build mod list ---
    mod_list_lines = [f"Mod List for instance: {instance_name}", f"Backup date: {timestamp}", ""]
    mod_count = 0
    mc_mods = minecraft_path / "mods"
    mods_source = mc_mods if mc_mods.exists() else None
    if mods_source:
        for f in sorted(mods_source.iterdir()):
            if f.suffix in (".jar", ".zip") and f.is_file():
                mod_list_lines.append(f"  {f.name}")
                mod_count += 1
        mod_list_lines.append(f"\nTotal: {mod_count} mods")
    else:
        mod_list_lines.append("(No mods directory found)")
    (staging_dir / "MOD_LIST.txt").write_text("\n".join(mod_list_lines), encoding="utf-8")

    # --- Copy instance.cfg ---
    instance_cfg = instance_path / "instance.cfg"
    if instance_cfg.exists():
        shutil.copy2(str(instance_cfg), str(staging_dir / "instance.cfg"))

    # --- Capture Java args ---
    instance_cfg_text = instance_cfg.read_text(encoding="utf-8", errors="replace") if instance_cfg.exists() else ""
    java_args_lines = [f"Java Args for instance: {instance_name}", ""]
    java_args_written = False
    for line in instance_cfg_text.splitlines():
        if "JvmArgs" in line or "MaxMemAlloc" in line or "MinMemAlloc" in line:
            java_args_lines.append(line.strip())
            java_args_written = True
    if not java_args_written:
        java_args_lines.append("(No Java args found in instance.cfg)")
    java_args_lines.append("\nTo restore: Prism Launcher → right-click instance → Edit → Java → paste above")
    (staging_dir / "JAVA_ARGS.txt").write_text("\n".join(java_args_lines), encoding="utf-8")

    # --- Restore instructions ---
    restore_instructions = [
        "RESTORE INSTRUCTIONS",
        "====================",
        f"Instance: {instance_name}",
        "",
        "1. Install Prism Launcher on the target machine",
        f"2. Create a new instance named exactly: {instance_name}",
        "3. Launch it once to generate the minecraft/ folder, then close",
        "4. Run: mcrestore <path_to_this_zip>",
        "   OR:  mcrestore vault  (if you backed up to vault and SyncThing synced)",
        "5. Download all mods listed in MOD_LIST.txt",
        "6. Set Java args from JAVA_ARGS.txt in Prism → Edit Instance → Java",
    ]
    (staging_dir / "RESTORE_INSTRUCTIONS.txt").write_text("\n".join(restore_instructions), encoding="utf-8")

    # --- ZIP it ---
    zip_path = output_dir / f"{archive_name}.zip"
    with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in staging_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(staging_dir)
                zf.write(str(file_path), str(arcname))

    # --- Clean up staging ---
    try:
        shutil.rmtree(str(staging_dir.parent))
    except Exception:
        pass

    return zip_path, copied, mod_count


def execute(kernel, args):
    if platform.system() != "Windows":
        return "[!] mcbackup is Windows-only (Prism Launcher path detection)."

    # args arrives as a string from the kernel — split into tokens.
    # Respect quoted instance names: "Minecraft PVP" vault
    import shlex
    try:
        parts = shlex.split(args) if args.strip() else []
    except ValueError:
        parts = args.strip().split()

    # --- Parse args ---
    # First token is a dest keyword/path if it's "vault" or an absolute path.
    # Otherwise it's an instance name, with optional second token as dest.
    instance_name = None
    dest_arg = None

    if len(parts) >= 1:
        first = parts[0]
        if first.lower() in _DEST_KEYWORDS or Path(first).is_absolute():
            dest_arg = first
        else:
            instance_name = first
            if len(parts) >= 2:
                dest_arg = parts[1]

    # --- Locate Prism instances ---
    prism_dir = _get_prism_instances_dir()
    if prism_dir is None:
        return (
            "[!] Prism Launcher not found at %APPDATA%\\PrismLauncher\\instances\\\n"
            "    Install Prism Launcher first: https://prismlauncher.org"
        )

    available = _list_instances(prism_dir)
    if not available:
        return "[!] No Minecraft instances found in Prism Launcher (need minecraft/ folder inside instance)."

    # --- Decide which instances to back up ---
    if instance_name is None:
        to_backup = available
        print(f"[i] Backing up all {len(to_backup)} instance(s): {', '.join(to_backup)}")
    else:
        if instance_name not in available:
            lines = [f"[!] Instance '{instance_name}' not found in Prism Launcher."]
            lines.append(f"    Available instances: {', '.join(available)}")
            return "\n".join(lines)
        to_backup = [instance_name]

    # --- Resolve output directory ---
    if dest_arg is None:
        output_dir = Path(os.environ.get("USERPROFILE", "~")) / "Desktop"
    elif dest_arg.lower() == "vault":
        vault_engine = kernel.get_engine("vault")
        output_dir = Path(vault_engine.vault_dir) / "mc_backups"
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = Path(dest_arg)
        if not output_dir.exists():
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                return f"[!] Cannot create output directory '{output_dir}': {e}"

    if not output_dir.exists():
        return f"[!] Output directory does not exist: {output_dir}"

    # --- Back up each instance ---
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    results = []
    total_mods = 0

    for i, name in enumerate(to_backup, 1):
        print(f"[{i}/{len(to_backup)}] Backing up: {name}")
        try:
            zip_path, copied, mod_count = _backup_instance(name, prism_dir, output_dir, timestamp)
            total_mods += mod_count
            results.append((name, zip_path, copied, mod_count, None))
            print(f"    Done → {zip_path.name}")
        except Exception as e:
            results.append((name, None, 0, 0, str(e)))
            print(f"    [!] Failed: {e}")

    # --- Summary ---
    succeeded = [r for r in results if r[4] is None]
    failed = [r for r in results if r[4] is not None]

    lines = ["", f"  Backup complete — {len(succeeded)}/{len(to_backup)} instance(s)", f"  Saved to: {output_dir}", ""]

    for name, zip_path, copied, mod_count, err in results:
        if err:
            lines.append(f"  [!] {name}: FAILED — {err}")
        else:
            lines.append(f"  [OK] {name}")
            lines.append(f"       {zip_path.name}")
            lines.append(f"       configs: {copied}  |  mods cataloged: {mod_count}")

    if dest_arg and dest_arg.lower() == "vault":
        lines.append("")
        lines.append("  SyncThing will carry these to your other machines automatically.")
        lines.append("  On laptop: mcrestore vault")
    elif succeeded:
        lines.append("")
        lines.append("  Transfer the ZIP(s) to your laptop, then: mcrestore \"<path_to_zip>\"")

    return "\n".join(lines)
