import os
import re
from pathlib import Path

def get_all_html_files():
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(os.path.join(root, file))
    return html_files

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # 1. Hide .contact-link, .btn-gold, .lang-wrapper, .mini-contact on mobile
    style_start = content.find('<style')
    style_end = content.find('</style>')
    if style_start != -1 and style_end != -1:
        style_content = content[style_start:style_end]
        # Check if the rule already exists
        if '@media (max-width:860px)' in style_content:
            # Check if we already have the rule hiding these elements
            if '.nav-actions .contact-link' not in style_content and '.nav-actions .btn-gold' not in style_content:
                # Find the existing media query block and append the selectors
                # We'll use a simpler approach: add a new media query at the end
                new_rule = '''
@media (max-width:860px) {
    .nav-actions .contact-link,
    .nav-actions .btn-gold,
    .nav-actions .lang-wrapper,
    .nav-actions .mini-contact {
        display: none !important;
    }
}'''
                # Insert before </style>
                content = content[:style_end] + new_rule + content[style_end:]
                changed = True
        else:
            # No media query exists, add a new one
            new_rule = '''
@media (max-width:860px) {
    .nav-actions .contact-link,
    .nav-actions .btn-gold,
    .nav-actions .lang-wrapper,
    .nav-actions .mini-contact {
        display: none !important;
    }
}'''
            content = content[:style_end] + new_rule + content[style_end:]
            changed = True

    # 2. Find the mobile panel and add Book Now and Contact if missing
    mobile_panel_start = content.find('<div class="mobile-panel">')
    if mobile_panel_start != -1:
        # Find the closing </div> of the panel (we need to find the matching one)
        # We'll use a simple approach: find the next </div> after the panel start
        # But careful: there might be nested divs. We'll find the last </div> before the mobile-menu ends.
        mobile_menu_start = content.rfind('<div class="container mobile-menu"', 0, mobile_panel_start)
        if mobile_menu_start != -1:
            mobile_menu_end = content.find('</div>', mobile_menu_start)
            if mobile_menu_end != -1:
                panel_content = content[mobile_panel_start:mobile_menu_end]
                # Check if Book Now already exists
                if 'book now' not in panel_content.lower():
                    # Insert Book Now before the closing </div> of the panel
                    new_link = '        <a href="contact.html" class="btn-gold" style="display:block;text-align:center;margin-top:8px;">✨ Book Now</a>\n'
                    # Find the last </div> in the panel content
                    last_div = panel_content.rfind('</div>')
                    if last_div != -1:
                        insert_pos = mobile_panel_start + last_div
                        content = content[:insert_pos] + new_link + content[insert_pos:]
                        changed = True

                # Check if Contact already exists
                if '📋 Contact' not in panel_content and '>Contact<' not in panel_content:
                    # Add Contact link before the closing </div>
                    contact_link = '        <a href="contact.html">📋 Contact</a>\n'
                    last_div = panel_content.rfind('</div>')
                    if last_div != -1:
                        insert_pos = mobile_panel_start + last_div
                        content = content[:insert_pos] + contact_link + content[insert_pos:]
                        changed = True

    if changed:
        # Backup
        backup_dir = Path('backup_mobile_menu')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / os.path.basename(filepath)
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated {filepath}")
        return True
    else:
        print(f"ℹ️  No changes needed in {filepath}")
        return False

def main():
    files = get_all_html_files()
    if not files:
        print("No HTML files found.")
        return
    print(f"Found {len(files)} HTML files.")
    any_changed = False
    for f in files:
        if update_file(f):
            any_changed = True
    if not any_changed:
        print("\n🎉 All files already have the mobile menu configured.")
    else:
        print("\n✅ Mobile menu updated. Backups saved in 'backup_mobile_menu'.")
        print("   Upload all files to your server and clear cache.")

if __name__ == '__main__':
    main()
