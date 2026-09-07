import os
import re
from pathlib import Path

# New Instagram URL
NEW_INSTA = "https://www.instagram.com/abridmorocco/"

# List of old handles we want to replace (add more if needed)
OLD_HANDLES = [
    "abridmoroccotrip",
    "abridmorocco.trip",
    "abrid_morocco",
    "abridmorocco"
]

def get_all_html_files():
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(os.path.join(root, file))
    return html_files

def update_instagram_links(content):
    # Pattern to match any href containing instagram.com (case-insensitive)
    # We'll capture the whole href attribute value.
    pattern = r'href\s*=\s*["\']([^"\']*instagram\.com[^"\']*)["\']'
    matches = re.finditer(pattern, content, re.IGNORECASE)

    replacements = []
    for match in matches:
        full_attr = match.group(0)
        url = match.group(1)
        # Check if this URL contains any of the old handles
        should_replace = False
        for handle in OLD_HANDLES:
            if handle.lower() in url.lower():
                should_replace = True
                break
        if should_replace:
            # Build new URL: if the old URL had www or not, we just replace with new
            # But we want to keep the protocol (http or https) if present, but we'll just use https.
            # We'll replace the entire URL with NEW_INSTA
            new_attr = re.sub(r'href\s*=\s*["\']([^"\']*)["\']', f'href="{NEW_INSTA}"', full_attr, flags=re.IGNORECASE)
            replacements.append((url, NEW_INSTA))
            # Replace in content
            content = content.replace(full_attr, new_attr)
    return content, replacements

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content, changes = update_instagram_links(content)
    if changes:
        # Backup
        backup_dir = Path('backup_instagram')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / os.path.basename(filepath)
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Fixed {len(changes)} Instagram links in {filepath}:")
        for old, new in changes:
            print(f"   {old} → {new}")
        return True
    else:
        print(f"ℹ️  No old Instagram links found in {filepath}")
        return False

def main():
    html_files = get_all_html_files()
    if not html_files:
        print("No HTML files found.")
        return
    print(f"Found {len(html_files)} HTML files.")
    fixed_any = False
    for file in html_files:
        if update_file(file):
            fixed_any = True
    if not fixed_any:
        print("\n🎉 No old Instagram links found to replace.")
    else:
        print("\n✅ Instagram links updated. Backups saved in 'backup_instagram'.")
        print("   Upload all files to your server and clear cache.")

if __name__ == '__main__':
    main()
