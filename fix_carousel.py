import os
import re
from pathlib import Path

# ─── NEW CAROUSEL STYLES ───
CAROUSEL_CSS = '''
/* ─── TOUR CAROUSEL – ONE AT A TIME ─── */
.tour-grid {
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    gap: 16px !important;
    padding: 8px 4px 20px 4px !important;
    scroll-snap-type: x mandatory !important;
    -webkit-overflow-scrolling: touch !important;
    scroll-behavior: smooth !important;
    scrollbar-width: thin !important;
    scrollbar-color: var(--terracotta) var(--cream) !important;
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
    border-radius: 10px !important;
}
/* ─── CARD SIZES ─── */
.tour-grid .tour-card {
    flex: 0 0 85% !important;
    max-width: 400px !important;
    scroll-snap-align: center !important;
    min-height: 380px !important;
}
/* ─── TABLET ─── */
@media (min-width: 600px) {
    .tour-grid .tour-card {
        flex: 0 0 45% !important;
        max-width: 380px !important;
        min-height: 380px !important;
    }
}
/* ─── DESKTOP ─── */
@media (min-width: 1024px) {
    .tour-grid .tour-card {
        flex: 0 0 30% !important;
        max-width: 360px !important;
        min-height: 400px !important;
    }
}
/* ─── REMOVE OLD GRID STYLES ─── */
.tour-grid {
    display: flex !important;
}
'''

def inject_carousel_css(content):
    # Find the <style> block
    style_match = re.search(r'<style[^>]*>.*?</style>', content, re.DOTALL | re.IGNORECASE)
    if not style_match:
        head_end = content.find('</head>')
        if head_end != -1:
            new_style = f'<style>\n{CAROUSEL_CSS}\n</style>\n'
            return content[:head_end] + new_style + content[head_end:]
        return content

    style_content = style_match.group(0)

    # Remove any existing .tour-grid styles to avoid conflicts
    # Remove entire .tour-grid blocks
    style_content = re.sub(r'\.tour-grid\s*\{[^}]*\}', '', style_content, flags=re.DOTALL | re.IGNORECASE)
    # Remove any @media that targets .tour-grid
    style_content = re.sub(r'@media\s*\([^)]*\)\s*\{[^}]*\.tour-grid[^}]*\}', '', style_content, flags=re.DOTALL | re.IGNORECASE)
    # Remove any .tour-grid::-webkit-scrollbar blocks
    style_content = re.sub(r'\.tour-grid::-webkit-scrollbar[^{]*\{[^}]*\}', '', style_content, flags=re.DOTALL | re.IGNORECASE)

    # Insert the new carousel CSS before </style>
    new_style = style_content[:-7] + CAROUSEL_CSS + '\n</style>'
    return content.replace(style_match.group(0), new_style)

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    new_content = inject_carousel_css(content)

    if new_content != content:
        backup_dir = Path('backup_carousel')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / filepath.name
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ Updated carousel in {filepath}')
        return True
    else:
        print(f'ℹ️  No changes needed in {filepath}')
        return False

def main():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if 'backup' in root.lower():
            continue
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                # Only fix files that contain 'tour-grid'
                try:
                    with open(Path(root) / file, 'r', encoding='utf-8') as f:
                        if 'tour-grid' in f.read():
                            html_files.append(Path(root) / file)
                except:
                    pass

    if not html_files:
        print('No files with tour-grid found.')
        return

    print(f'Found {len(html_files)} files with tour-grid.')
    any_changed = False
    for f in html_files:
        if fix_file(f):
            any_changed = True

    if any_changed:
        print('\n✅ Tour carousel applied. Backups in "backup_carousel".')
        print('   Upload all files and clear your cache.')
    else:
        print('\n🎉 All files already have the carousel.')

if __name__ == '__main__':
    main()
