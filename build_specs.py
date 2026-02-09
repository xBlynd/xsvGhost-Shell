import os
from pathlib import Path

# --- CONFIGURATION ---
# We use the current directory + "specs"
SPECS_DIR = Path("specs")

def create_file(filename, content):
    # Ensure the directory exists
    SPECS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = SPECS_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {filepath}")

# --- CONTENT DEFINITIONS ---

# 1. HOST RULES (How we talk to Windows/Linux)
host_content = (
    "# Specification: Host Bridge (02_HOST.md)\n\n"
    "## 1. Objective\n"
    "This module handles all Operating System interactions. We never use 'os.system' directly in other files.\n\n"
    "## 2. Required Functions\n"
    "- get_os_type(): Returns 'windows' or 'linux'.\n"
    "- clear_screen(): Runs 'cls' (Windows) or 'clear' (Linux).\n"
    "- launch(path): Opens a file or program safely.\n"
    "- is_vm(): Checks if we are running inside Parrot OS or a VM.\n"
)

# 2. VAULT RULES (How we save data)
vault_content = (
    "# Specification: Data Vault (03_VAULT.md)\n\n"
    "## 1. Objective\n"
    "This module handles saving and loading your Journal and Notes.\n\n"
    "## 2. File Structure\n"
    "- Data lives in the 'data/vault/' folder.\n"
    "- Journal entries go into 'data/vault/journal/YYYY-MM-DD.md'.\n"
    "- Notes go into 'data/vault/notes/'.\n"
)

# 3. WEB RULES (How the server works)
web_content = (
    "# Specification: Web Interface (04_WEB.md)\n\n"
    "## 1. Objective\n"
    "A simple web page to view your notes and launch apps.\n\n"
    "## 2. Settings\n"
    "- Default Port: 8000\n"
    "- Address: localhost (127.0.0.1)\n"
    "- If Port 8000 is busy, try 8001, then 8002.\n"
)

# --- EXECUTION ---
if __name__ == "__main__":
    print("Building Specifications...")
    create_file("02_HOST.md", host_content)
    create_file("03_VAULT.md", vault_content)
    create_file("04_WEB.md", web_content)
    print("\nSuccess. The 'Law' files are created.")