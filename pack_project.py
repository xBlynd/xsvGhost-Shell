# This file is designed to pull the ENTIRE project into a markdown file to assist in investigations into any potential issues. This isn't just a developer tool for us to fix code. It is an Intelligence Gathering Tool.

#If you are on a client's machine (or a target's machine) and you need to understand their messy project, or grab their specific config folder to analyze later:
# Ghost Way: pack C:\Users\Target\Documents\ProjectX --output loot/project_x_dump.md

# We've just turned a "debugger" into an Exfiltration & Recon Weapon.

# 🔮 Future Tuning (The Options)
# When we build the "Pro" version of this command later (Phase 3), we will add these flags:

# --no-code: Just grab text/PDFs (for document theft).

# --secrets: Regex scan for "API_KEY", "password", "token" inside the files as it packs them.

# --encrypt: Encrypt the output file immediately so it's safe in the Vault.


import os

# CONFIGURATION
OUTPUT_FILE = "GHOST_FULL_SOURCE.md"
IGNORE_DIRS = {'.git', '__pycache__', 'venv', 'env', '.idea', '.vscode', 'dist', 'build', 'node_modules'}
IGNORE_FILES = {'.DS_Store', 'Thumbs.db', OUTPUT_FILE, 'pack_project.py', 'package-lock.json'}
ALLOWED_EXTENSIONS = {'.py', '.md', '.json', '.bat', '.sh', '.txt', '.yml', '.yaml'}

def get_file_type(filename):
    return filename.split('.')[-1] if '.' in filename else 'text'

def generate_tree(startpath):
    tree = ["# 📦 Project Map", "```text"]
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        if level == 0:
            tree.append(os.path.basename(root))
        else:
            tree.append(f"{indent}{os.path.basename(root)}/")
        
        subindent = '│   ' * level + '├── '
        for f in files:
            if f not in IGNORE_FILES and any(f.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                tree.append(f"{subindent}{f}")
    tree.append("```\n")
    return "\n".join(tree)

def pack_files(startpath):
    content = []
    toc = ["# 📖 Table of Contents"]
    
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if file in IGNORE_FILES or not any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                continue
            
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, startpath).replace("\\", "/")
            
            # Add to TOC
            toc.append(f"- [{relpath}](#file-{relpath.replace('/', '-').replace('.', '-').lower()})")
            
            # Add Content
            anchor = f"file-{relpath.replace('/', '-').replace('.', '-').lower()}"
            content.append(f"<a id='{anchor}'></a>")
            content.append(f"## 📄 {relpath}")
            content.append(f"> **Location:** `{relpath}`")
            content.append(f"```{get_file_type(file)}")
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content.append(f.read())
            except Exception as e:
                content.append(f"# ERROR READING FILE: {e}")
                
            content.append("```\n")
            content.append("---") # Horizontal Rule Separator

    return "\n".join(toc) + "\n\n" + "\n".join(content)

if __name__ == "__main__":
    print("📦 Packing Ghost Shell Source...")
    cwd = os.getcwd()
    
    final_output = f"# 👻 Ghost Shell Source Dump\n**Generated:** {os.path.basename(cwd)}\n\n"
    final_output += generate_tree(cwd)
    final_output += "\n"
    final_output += pack_files(cwd)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_output)
        
    print(f"✅ Done! Open '{OUTPUT_FILE}' in VS Code and use the Outline view.")