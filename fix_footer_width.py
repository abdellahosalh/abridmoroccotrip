import os
import re
from pathlib import Path

FOOTER_FIX_CSS = '''
/* ─── FIX FOOTER OVERFLOW ─── */
footer {
    overflow-x: hidden !important;
    max-width: 100% !important;
    width: 100% !important;
}
footer .container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 0 16px !important;
    overflow-x: hidden !important;
}
footer .container > div {
    flex-wrap: wrap !important;
    gap: 20px !important;
}
footer .container > div > div {
    min-width: 140px !important;
    flex: 1 1 180px !important;
}
footer .container ul {
    padding: 0 !important;
    margin: 0 !important;
    list-style: none !important;
}
footer .container ul li {
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    max-width: 100% !important;
}
footer .footer-contact-btn {
    max-width: 100% !important;
    box-sizing: border-box !important;
}
footer .footer-bottom {
    flex-wrap: wrap !important;
    gap: 8px !important;
}
@media (max-width: 860px) {
    footer .container > div {
        grid-template-columns: 1fr 1fr !important;
        gap: 16px !important;
    }
    footer .container > div > div {
        flex: 1 1 100% !important;
        min-width: unset !important;
    }
    footer .container ul li {
        white-space: normal !important;
        word-break: break-word !important;
    }
}
@media (max-width: 480px) {
    footer .container {
        padding: 0 12px !important;
    }
    footer .container > div {
        grid-template-columns: 1fr !important;
        gap: 12px !important;
    }
}
'''

def inject_css(content):
    # Look for <style> block
    style_match = re.search(r'<style[^>]*>.*?</style>', content, re.DOTALL | re.IGNORECASE)
    if not style_match:
        # Create style block before </head>
        head_end = content.find('</head>')
        if head_end != -1:
            new_style = f'<style>\n{FOOTER_FIX_CSS}\n</style>\n'
            return content[:head_end] + new_style + content[head_end:]
        return content

    style_content = style_match.group(0)
    # Check if fix already present
    if 'FIX FOOTER OVERFLOW' in style_content:
        return content

    # Insert before </style>
    new_style = style_content[:-7] + FOOTER_FIX_CSS + '\n</style>'
    return content.replace(style_content, new_style)

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    new_content = inject_css(content)

    if new_content != content:
        backup_dir = Path('backup_footer_width')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / filepath.name
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ Fixed footer width in {filepath}')
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
                html_files.append(Path(root) / file)

    if not html_files:
        print('No HTML files found.')
        return

    print(f'Found {len(html_files)} HTML files.')
    any_changed = False
    for f in html_files:
        if fix_file(f):
            any_changed = True

    if any_changed:
        print('\n✅ Footer width fix applied to all pages. Backups in "backup_footer_width".')
        print('   Upload all files and clear your cache.')
    else:
        print('\n🎉 All pages already have the fix.')

if __name__ == '__main__':
    main()
