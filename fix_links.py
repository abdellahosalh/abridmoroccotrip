import os
import re
from pathlib import Path
from urllib.parse import urlparse

# Get all HTML files in the current directory (and subdirectories)
html_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html') and not file.startswith('.'):
            html_files.append(os.path.join(root, file))

print(f"Found {len(html_files)} HTML files to scan.")

# Build a set of all existing files (relative paths) for quick lookup
existing_files = set()
for root, dirs, files in os.walk('.'):
    for file in files:
        if not file.startswith('.'):
            rel_path = os.path.relpath(os.path.join(root, file), '.').replace('\\', '/')
            existing_files.add(rel_path.lower())  # case-insensitive on Windows
            # Also add without .html for potential references
            if file.endswith('.html'):
                existing_files.add(rel_path.lower()[:-5])  # without .html

def normalize_path(href):
    """Clean up href and return a normalized relative path."""
    # Remove query parameters and fragments
    parsed = urlparse(href)
    path = parsed.path
    if not path:
        return None
    # If it starts with /, remove leading slash to make relative
    if path.startswith('/'):
        path = path[1:]
    # If it's an external URL (http, https), skip
    if path.startswith('http://') or path.startswith('https://'):
        return None
    # If it's a mailto:, javascript:, #, etc., skip
    if path.startswith('#') or path.startswith('mailto:') or path.startswith('javascript:'):
        return None
    # If it's an absolute path (starts with /), we treat as relative to root
    # But we'll just remove leading slash
    return path

def find_matching_file(original_path, existing_files):
    """
    Try to find a matching existing file for a given relative path.
    Returns the corrected href or None if not found.
    """
    # Remove any leading ./ or .\
    if original_path.startswith('./') or original_path.startswith('.\\'):
        original_path = original_path[2:]
    # Remove trailing slashes
    original_path = original_path.rstrip('/')
    # If empty, skip
    if not original_path:
        return None

    # 1. Exact match (case-insensitive)
    if original_path.lower() in existing_files:
        return original_path

    # 2. Try adding .html
    if not original_path.endswith('.html') and not original_path.endswith('.htm'):
        test_path = original_path + '.html'
        if test_path.lower() in existing_files:
            return test_path

    # 3. Try replacing .htm with .html
    if original_path.endswith('.htm'):
        test_path = original_path[:-4] + '.html'
        if test_path.lower() in existing_files:
            return test_path

    # 4. Try removing .html if present (for links like "about" that point to "about.html")
    if original_path.endswith('.html'):
        test_path = original_path[:-5]
        if test_path.lower() in existing_files:
            return test_path

    # 5. Try lowercase version of original
    if original_path != original_path.lower():
        test_path = original_path.lower()
        if test_path in existing_files:
            return test_path

    return None

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all href="..." and href='...'
    pattern = r'href\s*=\s*["\']([^"\']*)["\']'
    matches = re.finditer(pattern, content, re.IGNORECASE)

    changes = []
    for match in matches:
        full_match = match.group(0)
        href = match.group(1)
        if not href:
            continue
        normalized = normalize_path(href)
        if normalized is None:
            continue  # external or special link

        # Check if the file exists
        # We'll try to locate the file relative to the current HTML file's directory
        # But we can simplify: just check relative to the project root.
        # However, sometimes links are relative to the page location.
        # We'll try both: absolute from root and relative to current file's dir.
        # For safety, we'll resolve against the current file's directory.
        current_dir = os.path.dirname(filepath)
        if current_dir == '':
            current_dir = '.'
        # Resolve the absolute path of the link target
        target_path = os.path.normpath(os.path.join(current_dir, normalized))
        # Convert to relative path from project root
        rel_target = os.path.relpath(target_path, '.').replace('\\', '/')
        # Check if it exists (case-insensitive)
        if rel_target.lower() not in existing_files:
            # Try to find a match
            corrected = find_matching_file(rel_target, existing_files)
            if corrected and corrected != rel_target:
                changes.append((href, corrected))
                # Update the href in the content
                # We need to be careful: we should replace only the href value, not the whole attribute
                # We'll use regex replace for that specific match
                # Use the full match and replace the value inside quotes
                new_attr = re.sub(r'href\s*=\s*["\']([^"\']*)["\']', f'href="{corrected}"', full_match, flags=re.IGNORECASE)
                content = content.replace(full_match, new_attr)

    if changes:
        # Backup
        backup_dir = Path('backup_link_fix')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / os.path.basename(filepath)
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {len(changes)} links in {filepath}:")
        for old, new in changes:
            print(f"   {old} → {new}")
        return True
    else:
        print(f"ℹ️  No broken links found in {filepath}")
        return False

# Main loop
fixed_any = False
for file in html_files:
    if update_file(file):
        fixed_any = True

if not fixed_any:
    print("\n🎉 No broken internal links detected.")
else:
    print("\n✅ Fixes applied. Backups saved in 'backup_link_fix' folder.")
    print("   Verify the changes and upload the updated files to your server.")
