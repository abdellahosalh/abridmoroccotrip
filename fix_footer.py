import os
import re
from pathlib import Path

def fix_footer(content):
    # Find the "Contact" section in the footer
    # Look for <h4>Contact</h4> or <h4 style=...>Contact</h4>
    # Then find the <ul> that follows it and replace with a single button/link
    
    # Pattern to find the Contact heading
    heading_pattern = r'(<h4[^>]*>Contact</h4>)'
    heading_match = re.search(heading_pattern, content, re.IGNORECASE)
    if not heading_match:
        return content
    
    # Find the <ul> that comes after this heading
    # We need to find the <ul> that is the next sibling or within the same parent
    # We'll find the position of the heading, then find the next </ul> after it
    start_pos = heading_match.end()
    # Find the <ul> that starts after the heading
    ul_match = re.search(r'<ul[^>]*>.*?</ul>', content[start_pos:], re.DOTALL | re.IGNORECASE)
    if not ul_match:
        # Try a different approach: find the parent div and replace its content
        # Look for the div that contains Contact heading
        div_pattern = r'(<div[^>]*>.*?<h4[^>]*>Contact</h4>.*?)</div>'
        div_match = re.search(div_pattern, content, re.DOTALL | re.IGNORECASE)
        if div_match:
            div_content = div_match.group(1)
            # Remove all <li> items and replace with a single link
            # Keep the heading, remove the ul and its contents
            new_div = re.sub(r'<ul[^>]*>.*?</ul>', '', div_content, flags=re.DOTALL | re.IGNORECASE)
            # Now add a button/link after the heading
            new_div = re.sub(
                r'(<h4[^>]*>Contact</h4>)',
                r'\1\n          <a href="contact.html" class="footer-contact-btn" style="display:inline-block;background:var(--gold);color:var(--brown);padding:8px 20px;border-radius:60px;font-weight:700;text-decoration:none;margin-top:8px;font-size:0.85rem;">📋 Contact Us</a>',
                new_div,
                flags=re.IGNORECASE
            )
            # Also remove any leftover phone/email/address lines
            # Remove any <li> that might still be there
            new_div = re.sub(r'<li[^>]*>.*?</li>', '', new_div, flags=re.DOTALL | re.IGNORECASE)
            # Clean up extra whitespace and empty lines
            new_div = re.sub(r'\s*\n\s*\n\s*', '\n', new_div)
            # Replace the old div with the new one
            content = content.replace(div_match.group(0), new_div + '</div>')
            return content
    
    # If we found the ul, replace it
    if ul_match:
        ul_content = ul_match.group(0)
        # Replace the ul with a single link
        new_ul = '''          <a href="contact.html" class="footer-contact-btn" style="display:inline-block;background:var(--gold);color:var(--brown);padding:8px 20px;border-radius:60px;font-weight:700;text-decoration:none;margin-top:8px;font-size:0.85rem;">📋 Contact Us</a>'''
        # Replace the entire ul with the button
        content = content[:start_pos + ul_match.start()] + new_ul + content[start_pos + ul_match.end():]
        return content
    
    return content

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    new_content = fix_footer(content)
    
    if new_content != content:
        backup_dir = Path('backup_footer_fix')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / filepath.name
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ Fixed footer in {filepath}')
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
        print('\n✅ Footer fixed on all pages. Backups saved in "backup_footer_fix".')
        print('   Upload all files to your server and clear cache.')
    else:
        print('\n🎉 All files already have the fixed footer.')

if __name__ == '__main__':
    main()
