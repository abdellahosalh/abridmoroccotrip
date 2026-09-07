import os
import re
from pathlib import Path

HEADER_FIX_CSS = '''
/* ─── FORCE ONE‑LINE HEADER ─── */
.nav {
    flex-wrap: nowrap !important;
    gap: 6px !important;
}
.nav-links {
    flex-wrap: nowrap !important;
    gap: 8px !important;
}
.nav-links a {
    font-size: 0.75rem !important;
    padding: 4px 6px !important;
    white-space: nowrap !important;
}
.nav-actions {
    flex-wrap: nowrap !important;
    gap: 4px !important;
    flex-shrink: 0 !important;
}
.nav-actions .contact-link {
    font-size: 0.75rem !important;
    padding: 4px 8px !important;
    white-space: nowrap !important;
}
.nav-actions .btn-gold {
    font-size: 0.7rem !important;
    padding: 4px 12px !important;
    white-space: nowrap !important;
}
.nav-actions .lang-selector {
    font-size: 0.65rem !important;
    padding: 3px 8px !important;
}
.brand-text strong {
    font-size: 0.9rem !important;
}
.brand-text span {
    font-size: 0.55rem !important;
}
.brand-logo {
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    min-height: 32px !important;
    max-width: 32px !important;
    max-height: 32px !important;
}

/* ─── MOBILE: hide Contact & Book Now ─── */
@media (max-width: 860px) {
    .nav-actions .contact-link,
    .nav-actions .btn-gold,
    .nav-actions .lang-wrapper {
        display: none !important;
    }
    .nav-links {
        display: none !important;
    }
    .menu-toggle {
        display: flex !important;
    }
    .brand-text strong {
        font-size: 0.75rem !important;
    }
    .brand-logo {
        width: 28px !important;
        height: 28px !important;
        min-width: 28px !important;
        min-height: 28px !important;
        max-width: 28px !important;
        max-height: 28px !important;
    }
}
@media (max-width: 480px) {
    .nav-actions .lang-selector {
        display: none !important;
    }
    .brand-text strong {
        font-size: 0.65rem !important;
    }
}
'''

def apply_fix(content):
    # Find the <style> block and insert the fix if not already present
    style_match = re.search(r'<style[^>]*>.*?</style>', content, re.DOTALL | re.IGNORECASE)
    if not style_match:
        # No style block – create one
        head_end = content.find('</head>')
        if head_end == -1:
            return content
        new_style = f'<style>\n{HEADER_FIX_CSS}\n</style>\n'
        content = content[:head_end] + new_style + content[head_end:]
        return content

    style_content = style_match.group(0)
    if 'FORCE ONE‑LINE HEADER' in style_content:
        return content  # already fixed

    # Insert the fix at the end of the style block, before </style>
    new_style = style_content[:-7] + HEADER_FIX_CSS + '\n</style>'
    return content.replace(style_content, new_style)

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    new_content = apply_fix(content)

    if new_content != content:
        # Backup
        backup_dir = Path('backup_one_line')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / os.path.basename(filepath)
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Fixed {filepath}")
        return True
    else:
        print(f"ℹ️  No changes needed in {filepath}")
        return False

def main():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if 'backup' in root.lower():
            continue
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(os.path.join(root, file))

    if not html_files:
        print("No HTML files found.")
        return

    print(f"Found {len(html_files)} HTML files.")
    any_changed = False
    for f in html_files:
        if update_file(f):
            any_changed = True

    if not any_changed:
        print("\n🎉 All pages already have the one‑line header.")
    else:
        print("\n✅ One‑line header fix applied. Backups in 'backup_one_line'.")
        print("   Upload all files and clear your browser cache.")

if __name__ == '__main__':
    main()
