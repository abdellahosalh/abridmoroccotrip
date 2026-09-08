import re
from pathlib import Path

# --- CSS to make tour grid horizontal ---
HORIZONTAL_GRID_CSS = '''
/* ─── HORIZONTAL TOUR GRID ─── */
.tour-grid {
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    gap: 20px !important;
    padding: 4px 0 20px 0 !important;
    scroll-snap-type: x mandatory !important;
    -webkit-overflow-scrolling: touch !important;
}
.tour-grid .tour-card {
    flex: 0 0 300px !important;
    scroll-snap-align: start !important;
}
/* Hide scrollbar on Firefox and IE */
.tour-grid {
    scrollbar-width: thin !important;
}
.tour-grid::-webkit-scrollbar {
    height: 6px !important;
}
.tour-grid::-webkit-scrollbar-thumb {
    background: var(--terracotta) !important;
    border-radius: 10px !important;
}
.tour-grid::-webkit-scrollbar-track {
    background: var(--cream) !important;
}
/* On desktop, revert to grid if you prefer, or keep horizontal */
@media (min-width: 860px) {
    .tour-grid {
        flex-wrap: wrap !important;
        overflow-x: visible !important;
        scroll-snap-type: none !important;
        display: grid !important;
        grid-template-columns: repeat(auto-fill, minmax(320px,1fr)) !important;
    }
    .tour-grid .tour-card {
        flex: unset !important;
        scroll-snap-align: unset !important;
    }
}
'''

def apply_fix(content):
    # Find the <style> block
    style_match = re.search(r'<style[^>]*>.*?</style>', content, re.DOTALL | re.IGNORECASE)
    if not style_match:
        return content

    style_content = style_match.group(0)
    # Check if already fixed
    if 'HORIZONTAL TOUR GRID' in style_content:
        return content

    # Insert the new CSS before </style>
    new_style = style_content[:-7] + HORIZONTAL_GRID_CSS + '\n</style>'
    return content.replace(style_content, new_style)

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    new_content = apply_fix(content)

    if new_content != content:
        backup_dir = Path('backup_horizontal_tours')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / filepath.name
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Updated {filepath}")
        return True
    else:
        print(f"ℹ️  No changes needed in {filepath}")
        return False

def main():
    # Target tours.html specifically, or any HTML with tour-grid
    files_to_fix = []
    for html in Path('.').glob('*.html'):
        if html.name in ['tours.html', 'index.html', 'classic-morocco.html']:  # add others if needed
            files_to_fix.append(html)
        else:
            # If the file contains 'tour-grid', we'll also fix it
            with open(html, 'r', encoding='utf-8') as f:
                if 'tour-grid' in f.read():
                    files_to_fix.append(html)

    if not files_to_fix:
        print("No files with tour-grid found.")
        return

    print(f"Found {len(files_to_fix)} files to update.")
    any_changed = False
    for f in files_to_fix:
        if update_file(f):
            any_changed = True

    if any_changed:
        print("\n✅ Horizontal tour grid applied. Backups in 'backup_horizontal_tours'.")
        print("   Upload all changed files and clear your cache.")
    else:
        print("\n🎉 All files already have the horizontal tour grid.")

if __name__ == '__main__':
    main()
