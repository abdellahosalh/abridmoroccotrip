import os
import re
import shutil
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
FOLDER = os.path.dirname(os.path.abspath(__file__))
BACKUP_FOLDER = os.path.join(FOLDER, "backup_before_update")

# Files that you've already manually updated – we skip these
SKIP_FILES = [
    "index.html",
    "about.html",
    "tours.html",
    "packages.html",
    "contact.html",
    "gallery.html",
    "blog.html",
    "marrakech.html",
    "merzouga.html",
    "atlas.html",
    "classic-morocco.html",
    "trip-template.html",
    "agent-tools.html",
    "full_update.py",
]

# ============================================================
# TEMPLATE: NEW HEADER
# ============================================================
NEW_HEADER = '''<header class="site-header" id="siteHeader">
  <div class="container nav">
    <a href="index.html" class="brand">
      <div class="brand-logo"><img src="https://i.postimg.cc/fR1NNYPc/500484189-17846895132482722-1431764686690149070-n.jpg" alt="Logo"></div>
      <div class="brand-text"><strong>AbridMoroccoTrip</strong><span>Premium Morocco Tours</span></div>
    </a>
    <ul class="nav-links">
      <li><a href="index.html">Home</a></li>
      <li><a href="about.html">About</a></li>
      <li><a href="tours.html">Tours</a></li>
      <li><a href="packages.html">Packages</a></li>
      <li><a href="gallery.html">Gallery</a></li>
      <li><a href="blog.html">Blog</a></li>
      <li><a href="contact.html">Contact</a></li>
    </ul>
    <div class="nav-actions">
      <a class="mini-contact" href="tel:+212762934488">📞 +212 762 934 488</a>
      <div id="google_translate_element" style="display:inline-block;"></div>
      <a class="btn btn-primary" href="contact.html">Book Now</a>
      <button class="menu-toggle" id="menuToggle"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="container mobile-menu" id="mobileMenu">
    <div class="mobile-panel">
      <a href="index.html">Home</a>
      <a href="about.html">About</a>
      <a href="tours.html">Tours</a>
      <a href="packages.html">Packages</a>
      <a href="gallery.html">Gallery</a>
      <a href="blog.html">Blog</a>
      <a href="contact.html">Contact</a>
      <a href="https://wa.me/212762934488" target="_blank" style="color:#25D366;font-weight:700;">💬 WhatsApp</a>
    </div>
  </div>
</header>'''

# ============================================================
# TEMPLATE: NEW FOOTER
# ============================================================
NEW_FOOTER = '''<footer style="background:var(--brown);color:rgba(255,255,255,.7);padding:48px 0 24px;margin-top:40px;border-top:1px solid rgba(255,255,255,.06);"><div class="container"><div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px;margin-bottom:40px;"><div><div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;"><img src="https://i.postimg.cc/fR1NNYPc/500484189-17846895132482722-1431764686690149070-n.jpg" alt="Logo" style="width:44px;height:44px;border-radius:10px;object-fit:cover;border:2px solid rgba(255,255,255,.1);"><div><strong style="font-size:1.1rem;color:#fff;display:block;">AbridMoroccoTrip</strong><span style="font-size:0.7rem;color:rgba(255,255,255,.4);">Premium Morocco Tours</span></div></div><p style="font-size:0.85rem;color:rgba(255,255,255,.5);line-height:1.7;max-width:280px;">Authentic Morocco tours with local experts Abdellah & Karim. Sahara, Atlas, Imperial Cities — private guides, luxury camps, fair prices.</p></div><div><h4 style="color:#fff;font-size:0.85rem;font-weight:700;margin-bottom:14px;letter-spacing:0.3px;">Pages</h4><ul style="list-style:none;padding:0;font-size:0.85rem;line-height:2.2;color:rgba(255,255,255,.5);"><li><a href="index.html" style="color:rgba(255,255,255,.5);">Home</a></li><li><a href="about.html" style="color:rgba(255,255,255,.5);">About</a></li><li><a href="tours.html" style="color:rgba(255,255,255,.5);">Tours</a></li><li><a href="packages.html" style="color:rgba(255,255,255,.5);">Packages</a></li><li><a href="gallery.html" style="color:rgba(255,255,255,.5);">Gallery</a></li><li><a href="blog.html" style="color:rgba(255,255,255,.5);">Blog</a></li><li><a href="contact.html" style="color:rgba(255,255,255,.5);">Contact</a></li></ul></div><div><h4 style="color:#fff;font-size:0.85rem;font-weight:700;margin-bottom:14px;letter-spacing:0.3px;">Support</h4><ul style="list-style:none;padding:0;font-size:0.85rem;line-height:2.2;color:rgba(255,255,255,.5);"><li><a href="faq.html" style="color:rgba(255,255,255,.5);">FAQ</a></li><li><a href="contact.html" style="color:rgba(255,255,255,.5);">Booking</a></li><li><a href="cancellation-policy.html" style="color:rgba(255,255,255,.5);">Cancellation Policy</a></li><li><a href="privacy.html" style="color:rgba(255,255,255,.5);">Privacy Policy</a></li><li><a href="terms.html" style="color:rgba(255,255,255,.5);">Terms of Service</a></li><li><a href="cookies.html" style="color:rgba(255,255,255,.5);">Cookies</a></li></ul></div><div><h4 style="color:#fff;font-size:0.85rem;font-weight:700;margin-bottom:14px;letter-spacing:0.3px;">Contact</h4><ul style="list-style:none;padding:0;font-size:0.85rem;line-height:2.2;color:rgba(255,255,255,.5);"><li style="display:flex;align-items:center;gap:8px;color:rgba(255,255,255,.6);">📞 Abdellah: <a href="tel:+212762934488" style="color:rgba(255,255,255,.6);white-space:nowrap;">+212 762 934 488</a></li><li style="display:flex;align-items:center;gap:8px;color:rgba(255,255,255,.6);">📞 Karim: <a href="tel:+212609282538" style="color:rgba(255,255,255,.6);white-space:nowrap;">+212 609 282 538</a></li><li style="display:flex;align-items:center;gap:8px;color:rgba(255,255,255,.6);">✉️ <a href="mailto:abridmorocco@gmail.com" style="color:rgba(255,255,255,.6);">abridmorocco@gmail.com</a></li><li style="display:flex;align-items:center;gap:8px;color:rgba(255,255,255,.4);font-size:0.8rem;">⏰ 9:00–21:00 (GMT+1)</li><li style="display:flex;align-items:center;gap:8px;color:rgba(255,255,255,.4);font-size:0.8rem;">📍 Casablanca, Morocco</li></ul><div style="display:flex;gap:10px;margin-top:12px;"><a href="https://wa.me/212762934488" target="_blank" style="background:#25D366;color:#fff;padding:6px 16px;border-radius:30px;font-size:0.75rem;font-weight:600;text-decoration:none;">WhatsApp</a><a href="https://www.instagram.com/abridmoroccotrip/" target="_blank" style="background:linear-gradient(135deg,#E1306C,#833AB4);color:#fff;padding:6px 16px;border-radius:30px;font-size:0.75rem;font-weight:600;text-decoration:none;">Instagram</a></div></div></div><div style="border-top:1px solid rgba(255,255,255,.06);padding-top:20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;font-size:0.75rem;color:rgba(255,255,255,.3);"><div>© <span id="year"></span> AbridMoroccoTrip. All rights reserved.</div><div style="display:flex;gap:20px;flex-wrap:wrap;"><a href="terms.html" style="color:rgba(255,255,255,.3);">Terms</a><a href="privacy.html" style="color:rgba(255,255,255,.3);">Privacy</a><a href="cookies.html" style="color:rgba(255,255,255,.3);">Cookies</a><span style="color:rgba(255,255,255,.15);">|</span><span style="color:rgba(255,255,255,.15);">🇲🇦 Made in Morocco</span></div></div></div></footer>'''

def update_head(content):
    if 'Syne' not in content:
        head_start = content.find('<head>')
        head_end = content.find('</head>')
        if head_start != -1 and head_end != -1:
            head_content = content[head_start:head_end+7]
            new_head = head_content
            if 'fonts.googleapis.com' not in head_content:
                new_head = new_head.replace('<head>', '<head>\n  <link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">')
            if 'style.css' not in head_content:
                new_head = new_head.replace('</head>', '  <link rel="stylesheet" href="style.css">\n</head>')
            content = content.replace(head_content, new_head)
    return content

def replace_header_footer(content):
    header_pattern = re.compile(r'<header\s+class="site-header"[^>]*>.*?</header>', re.DOTALL)
    content = header_pattern.sub(NEW_HEADER, content)
    start = content.rfind('<footer')
    if start != -1:
        end = content.rfind('</footer>') + 9
        content = content[:start] + NEW_FOOTER + content[end:]
    return content

def remove_prices(content):
    currency_pattern = re.compile(r'(?<![\w])(?:[$€£]\s*\d[\d,.]*(?:\.\d+)?|\d[\d,.]*(?:\.\d+)?\s*(?:USD|MAD|EUR|€|£))(?![\w])', re.IGNORECASE)
    content = currency_pattern.sub('Contact for pricing', content)
    content = re.sub(r'\s*"offers"\s*:\s*\{[^{}]*\},?', '', content, flags=re.IGNORECASE)
    return content

def add_seo_tags(content, filename):
    canonical = f'https://www.abridmorocco.com/{filename}'
    if '<link rel="canonical"' not in content:
        content = content.replace('</head>', f'  <link rel="canonical" href="{canonical}" />\n</head>')
    if '<meta name="robots"' not in content:
        content = content.replace('<head>', '<head>\n  <meta name="robots" content="index, follow">')
    if '<meta property="og:url"' not in content:
        og_tag = f'  <meta property="og:url" content="{canonical}" />\n'
        content = content.replace('</head>', og_tag + '</head>')
    return content

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    content = update_head(content)
    content = replace_header_footer(content)
    content = remove_prices(content)
    content = add_seo_tags(content, os.path.basename(filepath))
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

print("🚀 Starting full update of all HTML files...")
if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)
    print(f"📁 Created backup folder: {BACKUP_FOLDER}")
updated_count = 0
skipped_count = 0
for filename in os.listdir(FOLDER):
    if not filename.endswith('.html'):
        continue
    if filename in SKIP_FILES:
        skipped_count += 1
        continue
    filepath = os.path.join(FOLDER, filename)
    backup_path = os.path.join(BACKUP_FOLDER, filename)
    shutil.copy2(filepath, backup_path)
    if process_file(filepath):
        updated_count += 1
        print(f"✅ Updated: {filename}")
    else:
        print(f"⏭️ No changes needed: {filename}")
print(f"\n✅ Done! Updated {updated_count} files. Skipped {skipped_count} manually updated files.")
print(f"📂 Backups saved in: {BACKUP_FOLDER}")
print("\n🌟 Now upload all HTML files to your server and clear your browser cache.")
