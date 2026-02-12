"""
cmd_docs - Read the Docs in Terminal
View Ghost Shell documentation without leaving the shell.

Usage:
  docs                    - Show docs index
  docs <section>          - View specific section
  docs search <term>      - Search documentation
  docs edit <file>        - Open doc in editor
"""
import sys
from pathlib import Path
import subprocess
import os

ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = ROOT / 'docs'

MANIFEST = {
    "name": "docs",
    "version": "1.0",
    "description": "View Ghost Shell documentation in terminal",
    "usage": "docs [section] [--edit]",
    "author": "Ghost Shell Core"
}

def run(args):
    if not args:
        show_index()
    elif args[0] == 'search' and len(args) > 1:
        search_docs(' '.join(args[1:]))
    elif args[0] == 'edit' and len(args) > 1:
        edit_doc(args[1])
    elif '--edit' in args:
        edit_doc(args[0])
    else:
        show_section(args[0])

def show_index():
    """Display docs index"""
    index_file = DOCS_DIR / 'index.md'
    
    if not index_file.exists():
        print("❌ Documentation not found. Run 'docs init' to create.")
        return
    
    render_markdown(index_file)

def show_section(section_path):
    """Display a specific doc section"""
    # Try exact path
    doc_file = DOCS_DIR / f'{section_path}.md'
    
    if not doc_file.exists():
        # Try common paths
        for subdir in ['architecture', 'guides', 'install', 'dev']:
            alt_path = DOCS_DIR / subdir / f'{section_path}.md'
            if alt_path.exists():
                doc_file = alt_path
                break
    
    if not doc_file.exists():
        print(f"❌ Documentation section '{section_path}' not found")
        print(f"   Try: docs search {section_path}")
        return
    
    render_markdown(doc_file)

def render_markdown(file_path):
    """Render markdown in terminal"""
    try:
        # Try using glow (beautiful markdown renderer)
        if has_command('glow'):
            subprocess.run(['glow', str(file_path)])
            return
        
        # Try using bat (syntax highlighting)
        if has_command('bat'):
            subprocess.run(['bat', '--style=plain', '--language=markdown', str(file_path)])
            return
        
        # Fallback: plain text with basic formatting
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic terminal formatting
        formatted = format_markdown_basic(content)
        print(formatted)
        
    except Exception as e:
        print(f"❌ Error reading docs: {e}")

def format_markdown_basic(content):
    """Basic markdown formatting for terminal"""
    lines = content.split('\n')
    output = []
    
    for line in lines:
        # Headers
        if line.startswith('# '):
            output.append('\n' + '=' * 60)
            output.append(line[2:].upper())
            output.append('=' * 60)
        elif line.startswith('## '):
            output.append('\n' + line[3:])
            output.append('-' * len(line[3:]))
        elif line.startswith('### '):
            output.append('\n' + line[4:])
        
        # Code blocks
        elif line.startswith('```'):
            output.append('\n' + '─' * 60)
        
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            output.append('  • ' + line[2:])
        elif line.startswith('  - '):
            output.append('    ◦ ' + line[4:])
        
        # Regular lines
        else:
            output.append(line)
    
    return '\n'.join(output)

def search_docs(term):
    """Search documentation for term"""
    results = []
    
    for doc_file in DOCS_DIR.rglob('*.md'):
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if term.lower() in content.lower():
                # Get context
                lines = content.split('\n')
                matches = [i for i, line in enumerate(lines) if term.lower() in line.lower()]
                
                rel_path = doc_file.relative_to(DOCS_DIR)
                results.append({
                    'file': str(rel_path),
                    'matches': len(matches),
                    'preview': lines[matches] if matches else ''
                })
        except:
            continue
    
    if not results:
        print(f"❌ No results found for '{term}'")
        return
    
    print(f"\n🔍 Found {len(results)} documents matching '{term}':\n")
    for result in results:
        print(f"📄 {result['file']} ({result['matches']} matches)")
        print(f"   {result['preview'][:80]}")
        print()

def edit_doc(doc_path):
    """Open documentation in editor"""
    doc_file = DOCS_DIR / f'{doc_path}.md'
    
    if not doc_file.exists():
        for subdir in ['architecture', 'guides', 'install', 'dev']:
            alt_path = DOCS_DIR / subdir / f'{doc_path}.md'
            if alt_path.exists():
                doc_file = alt_path
                break
    
    if not doc_file.exists():
        print(f"❌ File not found: {doc_path}")
        return
    
    # Get editor from env or use default
    editor = os.environ.get('EDITOR', 'notepad' if sys.platform == 'win32' else 'nano')
    
    try:
        subprocess.run([editor, str(doc_file)])
    except Exception as e:
        print(f"❌ Error opening editor: {e}")
        print(f"   File location: {doc_file}")

def has_command(cmd):
    """Check if command exists"""
    from shutil import which
    return which(cmd) is not None

if __name__ == "__main__":
    run(sys.argv[1:])
