import os
import re

base_dir = r"C:\Users\LENOVO THINKPAD\Documents\Nouveau dossier\abridmoroccotrip-main"

html_files = [f for f in os.listdir(base_dir) if f.endswith('.html')]

seo_updates_count = 0

for filename in html_files:
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Ensure meta robots
    if '<meta name="robots"' not in content and "<meta name='robots'" not in content:
        content = content.replace('<head>', '<head>\n  <meta name="robots" content="index, follow">')

    # 2. Ensure canonical tag
    canonical_url = f"https://www.abridmorocco.com/{filename}"
    if '<link rel="canonical"' not in content:
        content = content.replace('</head>', f'  <link rel="canonical" href="{canonical_url}" />\n</head>')

    # 3. Upgrade fonts link if Playfair Display is found
    if 'Playfair+Display' in content:
        content = content.replace(
            'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600;700;800&display=swap',
            'https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap'
        )

    # 4. Add og:url if missing
    if '<meta property="og:url"' not in content and '<meta property=\'og:url\'' not in content:
        og_url_tag = f'  <meta property="og:url" content="{canonical_url}" />\n'
        if '<meta property="og:type"' in content:
            content = content.replace('<meta property="og:type"', og_url_tag + '  <meta property="og:type"')
        else:
            content = content.replace('</head>', og_url_tag + '</head>')

    # 5. Add full twitter cards if only card type exists
    if '<meta name="twitter:card"' in content and '<meta name="twitter:title"' not in content:
        # Extract title and description
        title_match = re.search(r'<title>(.*?)</title>', content)
        title_val = title_match.group(1) if title_match else "AbridMoroccoTrip"
        
        desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
        desc_val = desc_match.group(1) if desc_match else "Authentic Morocco Tours & Experiences"

        img_match = re.search(r'<meta property="og:image" content="(.*?)"', content)
        img_val = img_match.group(1) if img_match else "https://images.unsplash.com/photo-1539020140153-e479b8c22e70?q=80&w=1200&auto=format&fit=crop"

        twitter_block = (
            f'  <meta name="twitter:title" content="{title_val}" />\n'
            f'  <meta name="twitter:description" content="{desc_val}" />\n'
            f'  <meta name="twitter:image" content="{img_val}" />\n'
        )
        content = content.replace('<meta name="twitter:card" content="summary_large_image" />', 
                                  '<meta name="twitter:card" content="summary_large_image" />\n' + twitter_block)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        seo_updates_count += 1
        print(f"Updated SEO tags in: {filename}")

print(f"Total HTML files updated with SEO enhancements: {seo_updates_count}")
