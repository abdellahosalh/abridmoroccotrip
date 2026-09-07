import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))

html_files = [f for f in os.listdir(base_dir) if f.endswith('.html') and f not in ['classic-morocco.html', 'trip-template.html', 'agent-tools.html']]

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

    # 3. Add og:url if missing
    if '<meta property="og:url"' not in content and '<meta property=\'og:url\'' not in content:
        og_url_tag = f'  <meta property="og:url" content="{canonical_url}" />\n'
        if '<meta property="og:type"' in content:
            content = content.replace('<meta property="og:type"', og_url_tag + '  <meta property="og:type"')
        else:
            content = content.replace('</head>', og_url_tag + '</head>')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        seo_updates_count += 1
        print(f"Updated SEO in: {filename}")

print(f"Done. Updated {seo_updates_count} files.")
