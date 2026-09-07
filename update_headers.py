import os
import re
from pathlib import Path

NEW_HEADER = """  <!-- ── HEADER ── -->
  <header class="site-header" id="siteHeader">
    <div class="container nav">
      <!-- Brand (left) -->
      <a href="index.html" class="brand">
        <div class="brand-logo">
          <img src="https://i.postimg.cc/fR1NNYPc/500484189-17846895132482722-1431764686690149070-n.jpg" alt="AbridMoroccoTrip Logo">
        </div>
        <div class="brand-text">
          <strong>AbridMoroccoTrip</strong>
          <span>Premium Tours</span>
        </div>
      </a>

      <!-- Navigation Links (center) -->
      <ul class="nav-links">
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="tours.html">Tours</a></li>
        <li><a href="classic-morocco.html">Classic 13-Day</a></li>
        <li><a href="packages.html">Packages</a></li>
        <li><a href="gallery.html">Gallery</a></li>
        <li><a href="blog.html">Blog</a></li>
      </ul>

      <!-- Right Side: Contact + Book Now + Language + Menu -->
      <div class="nav-actions">
        <a href="contact.html" class="contact-link">Contact</a>
        <a class="btn btn-gold" href="contact.html">✨ Book Now</a>

        <!-- Language Switcher -->
        <div id="google_translate_element" style="display:inline-block;"></div>

        <!-- Mobile Menu Toggle -->
        <button class="menu-toggle" id="menuToggle" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div class="container mobile-menu" id="mobileMenu">
      <div class="mobile-panel">
        <a href="index.html">🏠 Home</a>
        <a href="about.html">👤 About Us</a>
        <a href="tours.html">🗺️ Tours</a>
        <a href="classic-morocco.html">🗺️ Classic 13-Day Itinerary</a>
        <a href="packages.html">📦 Packages</a>
        <a href="gallery.html">🖼️ Gallery</a>
        <a href="blog.html">📰 Blog</a>
        <a href="contact.html">📋 Contact</a>
        <a href="https://wa.me/212762934488" target="_blank" style="color:#25D366;font-weight:700;">💬 WhatsApp</a>
      </div>
    </div>
  </header>"""

# Update ALL HTML files in the folder (including index.html and classic-morocco.html)
PAGES = [f for f in os.listdir('.') if f.endswith('.html') and f != 'update_headers.py']

ACTIVE_MAP = {
    'index.html': 'Home',
    'about.html': 'About',
    'tours.html': 'Tours',
    'packages.html': 'Packages',
    'gallery.html': 'Gallery',
    'blog.html': 'Blog',
    'contact.html': 'Contact',
    'classic-morocco.html': 'Classic 13-Day'
}

def add_active_class(header_html, active_text):
    pattern = r'(<a\s+href="[^"]*\.html"[^>]*>)({})(</a>)'.format(re.escape(active_text))
    def repl(m):
        opening = m.group(1)
        if 'class=' in opening:
            new_opening = re.sub(r'class="([^"]*)"', r'class="\1 active"', opening)
        else:
            new_opening = opening.replace('>', ' class="active">')
        return new_opening + m.group(2) + m.group(3)
    return re.sub(pattern, repl, header_html)

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'<header\s+class="site-header"[^>]*>.*?</header>'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        print(f"❌ No old header found in {filepath}, skipping.")
        return

    filename = os.path.basename(filepath)
    active_text = ACTIVE_MAP.get(filename)
    new_header = add_active_class(NEW_HEADER, active_text) if active_text else NEW_HEADER

    # Backup
    backup_dir = Path('backup_headers')
    backup_dir.mkdir(exist_ok=True)
    backup_path = backup_dir / filepath
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)

    new_content = content[:match.start()] + new_header + content[match.end():]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✅ Updated {filepath}")

def main():
    for page in PAGES:
        if os.path.exists(page):
            update_file(page)
        else:
            print(f"⚠️  {page} not found")
    print("\n🎉 All HTML files updated! Backups saved in 'backup_headers'")

if __name__ == '__main__':
    main()
