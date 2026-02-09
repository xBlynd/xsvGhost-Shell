import sys
import os
import platform
import subprocess
from pathlib import Path

def ask_yes_no(question):
    while True:
        choice = input(f"{question} (y/n): ").lower()
        if choice == 'y': return True
        if choice == 'n': return False

def install_windows(root_path):
    print(" [*] Detected Windows System.")
    
    # 1. PATH PROMPT
    if ask_yes_no(" [?] Add 'xsv' to your User PATH?"):
        ps_command = f"""
        $target = '{root_path}'
        $current = [Environment]::GetEnvironmentVariable('Path', 'User')
        if ($current -notlike "*$target*") {{
            [Environment]::SetEnvironmentVariable('Path', $current + ';' + $target, 'User')
            Write-Output "Path Updated."
        }} else {{
            Write-Output "Already in Path."
        }}
        """
        try:
            subprocess.run(["powershell", "-Command", ps_command], check=True)
            print("     ✅ Path Updated (Restart terminal to see changes).")
        except Exception as e:
            print(f"     ❌ Failed to set PATH: {e}")

    # 2. DESKTOP SHORTCUT PROMPT
    if ask_yes_no(" [?] Create 'Ghost Shell' Shortcut on Desktop?"):
        try:
            desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
            shortcut_path = desktop / "Ghost Shell.lnk"
            
            vbs_script = f"""
            Set oWS = WScript.CreateObject("WScript.Shell")
            sLinkFile = "{shortcut_path}"
            Set oLink = oWS.CreateShortcut(sLinkFile)
            oLink.TargetPath = "{root_path}\\LAUNCH.bat"
            oLink.WorkingDirectory = "{root_path}"
            oLink.IconLocation = "%SystemRoot%\\system32\\SHELL32.dll,72"
            oLink.Save
            """
            
            vbs_file = root_path / "temp_install.vbs"
            with open(vbs_file, "w") as f:
                f.write(vbs_script)
                
            subprocess.run(["cscript", "/nologo", str(vbs_file)], check=True)
            os.remove(vbs_file)
            print("     ✅ Shortcut Created.")
            
        except Exception as e:
            print(f"     ❌ Failed to create shortcut: {e}")

def run(args):
    print("\n 📥 xsvCommandCenter SETUP")
    print(" " + "="*30)
    
    root_path = Path(__file__).parent.parent.parent.resolve()
    
    if platform.system() == "Windows":
        install_windows(root_path)
    elif platform.system() == "Linux":
        print(" [!] Linux Setup TODO: Add Alias Logic here.")
    else:
        print(f" ❌ Unsupported OS.")
    
    print("\n ✅ Setup Logic Complete.")