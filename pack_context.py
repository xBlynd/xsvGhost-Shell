import os

# Files to ignore
IGNORE_DIRS = {".git", "__pycache__", "_archive", "venv", ".idea", ".vscode"}
IGNORE_EXTS = {".pyc", ".png", ".jpg", ".exe", ".zip"}

output_file = "FULL_PROJECT_CONTEXT.txt"

with open(output_file, "w", encoding="utf-8") as outfile:
    # 1. Write the Folder Structure (Tree)
    outfile.write("=== PROJECT STRUCTURE ===\n")
    for root, dirs, files in os.walk("."):
        # Filter directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        level = root.replace(".", "").count(os.sep)
        indent = " " * 4 * level
        outfile.write(f"{indent}{os.path.basename(root)}/\n")
        subindent = " " * 4 * (level + 1)
        for f in files:
            if not any(f.endswith(ext) for ext in IGNORE_EXTS) and f != output_file:
                outfile.write(f"{subindent}{f}\n")
    
    outfile.write("\n\n=== FILE CONTENTS ===\n")

    # 2. Write the File Contents
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for filename in files:
            if filename == "pack_context.py" or filename == output_file:
                continue
            if any(filename.endswith(ext) for ext in IGNORE_EXTS):
                continue

            filepath = os.path.join(root, filename)
            outfile.write(f"\n\n{'='*50}\nFILE: {filepath}\n{'='*50}\n")
            
            try:
                with open(filepath, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
            except Exception as e:
                outfile.write(f"[Error reading file: {e}]")

print(f"✅ Done. Upload '{output_file}' to the chat.")