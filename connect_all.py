import os
import re
from pathlib import Path

# --- NEW NAV LINKS TO ADD ---
# We'll add a new <li> for airport-transfer.html after the blog link (or at the end).
# The desktop nav is a <ul class="nav-links"> with <li> items.
# The mobile nav is a <div class="mobile-panel"> with <a> items.

# --- CLIMATE NOTE HTML ---
CLIMATE_NOTE = '''
    <!-- ─── CLIMATE COMMITMENT NOTE ─── -->
    <div class="climate-note" style="background:var(--gold-light); border-radius:var(--radius-sm); padding:18px 24px; margin:30px 0; text-align:center; font-size:0.95rem; color:var(--brown-light); border-left:4px solid var(--gold);">
      🌍 <strong>We're in the process of figuring out how much CO₂‑e this trip generates.</strong> In the meantime, learn more about our climate commitment.<br>
      When you travel with us, <strong>AbridMoroccoTrip</strong> gives you more opportunities to support important causes in the destinations you visit.
    </div>
'''

# --- Helper: check if climate note already exists ---
def has_climate_note(content):
    return 'CO₂‑e' in content or 'climate commitment' in content.lower()

# --- Helper: check if airport-transfer is in nav ---
def has_airport_link(content):
    return 'airport-transfer.html' in content

# --- Helper: insert climate note before footer ---
def insert_climate_note(content):
    # Find the <footer> tag. We'll insert right before it.
    footer_match = re.search(r'<footer', content, re.IGNORECASE)
    if not footer_match:
        return content  # no footer, skip
    # Insert climate note before the <footer> opening tag
    insert_pos = footer_match.start()
    # But we want to put it inside the container, so we might want to put after the main content.
    # Actually, it's safer to put it before the footer but after the container closing.
    # We can look for </main> or the last </div> before footer, but we'll just put before <footer>
    # with a container div.
    # However, the note needs to be inside a container to look good.
    # We'll wrap it in a <div class="container"> if not already.
    # Since we don't know if the page has a container, we'll just insert the note as is.
    # The note has its own styles, but it will look better if inside a container.
    # We'll check if there's a container right before footer, but we'll just insert it right before footer.
    # Most pages have a container wrapping content. We'll insert before footer, but we'll wrap the note in <div class="container"> if needed.
    # Let's just insert the note as a standalone div inside the container before footer.
    # We'll find the last </div> before footer and insert after it? Or better, find the </div> that closes the main container.
    # For simplicity, we'll insert right before <footer> and add a container div around the note.
    wrapped_note = f'<div class="container">{CLIMATE_NOTE}</div>'
    return content[:insert_pos] + wrapped_note + content[insert_pos:]

# --- Helper: add airport-transfer to desktop nav ---
def add_airport_to_desktop_nav(content):
    # Look for <ul class="nav-links"> and insert a new <li> before the last <li> or after blog.
    # We'll find the nav-links ul.
    ul_match = re.search(r'<ul\s+class="nav-links"[^>]*>.*?</ul>', content, re.DOTALL | re.IGNORECASE)
    if not ul_match:
        return content
    ul_content = ul_match.group(0)
    # Check if airport link already exists
    if 'airport-transfer.html' in ul_content:
        return content
    # Find the last <li> inside and insert before it, or after blog.
    # We'll insert after the blog link if exists.
    blog_li = re.search(r'<li><a\s+href="blog\.html"[^>]*>.*?</a></li>', ul_content, re.IGNORECASE)
    if blog_li:
        # Insert after blog
        insert_pos = ul_content.find(blog_li.group(0)) + len(blog_li.group(0))
        new_li = '\n        <li><a href="airport-transfer.html">✈️ Airport Transfer</a></li>'
        new_ul = ul_content[:insert_pos] + new_li + ul_content[insert_pos:]
        return content.replace(ul_content, new_ul)
    else:
        # If no blog, insert before the last </li> (or at end)
        # We'll find the last </li> and insert before it.
        last_li_end = ul_content.rfind('</li>')
        if last_li_end != -1:
            new_li = '\n        <li><a href="airport-transfer.html">✈️ Airport Transfer</a></li>'
            new_ul = ul_content[:last_li_end] + new_li + ul_content[last_li_end:]
            return content.replace(ul_content, new_ul)
    return content

# --- Helper: add airport-transfer to mobile nav ---
def add_airport_to_mobile_nav(content):
    # Look for <div class="mobile-panel"> and insert a new <a> before the last <a> or after blog.
    panel_match = re.search(r'<div\s+class="mobile-panel"[^>]*>.*?</div>', content, re.DOTALL | re.IGNORECASE)
    if not panel_match:
        return content
    panel_content = panel_match.group(0)
    if 'airport-transfer.html' in panel_content:
        return content
    # Find the blog link if exists
    blog_a = re.search(r'<a\s+href="blog\.html"[^>]*>.*?</a>', panel_content, re.IGNORECASE)
    if blog_a:
        insert_pos = panel_content.find(blog_a.group(0)) + len(blog_a.group(0))
        new_a = '\n        <a href="airport-transfer.html">✈️ Airport Transfer</a>'
        new_panel = panel_content[:insert_pos] + new_a + panel_content[insert_pos:]
        return content.replace(panel_content, new_panel)
    else:
        # Insert before last </a> or at end
        last_a_end = panel_content.rfind('</a>')
        if last_a_end != -1:
            new_a = '\n        <a href="airport-transfer.html">✈️ Airport Transfer</a>'
            new_panel = panel_content[:last_a_end] + new_a + panel_content[last_a_end:]
            return content.replace(panel_content, new_panel)
    return content

# --- Main update function ---
def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    original = content

    # 1. Add airport-transfer link to nav (desktop and mobile)
    if not has_airport_link(content):
        content = add_airport_to_desktop_nav(content)
        content = add_airport_to_mobile_nav(content)
        changed = True

    # 2. Add climate note if not present
    if not has_climate_note(content):
        content = insert_climate_note(content)
        changed = True

    if changed:
        # Backup
        backup_dir = Path('backup_connect_all')
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

# --- Main ---
def main():
    # Get all .html files in current directory and subdirectories (excluding backups)
    html_files = []
    for root, dirs, files in os.walk('.'):
        # skip backup folders
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
        print("\n🎉 All files are already up to date.")
    else:
        print("\n✅ All pages updated. Backups saved in 'backup_connect_all'.")
        print("   Upload all files to your server and clear cache.")

if __name__ == '__main__':
    main()
