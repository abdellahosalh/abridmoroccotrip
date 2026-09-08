import re
from pathlib import Path

# ─── FIND EXISTING BALLOON PAGE ───
balloon_file = None
for f in ['air-balloon.html', 'balloon.html', 'hot-air-balloon.html']:
    if Path(f).exists():
        balloon_file = f
        break

if balloon_file is None:
    print('❌ No balloon page found. Creating air-balloon.html...')
    # Create a simple balloon page
    with open('air-balloon.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head><title>Hot Air Balloon | AbridMoroccoTrip</title></head>
<body><h1>Hot Air Balloon over Marrakech</h1><p>Contact us to book.</p></body>
</html>''')
    balloon_file = 'air-balloon.html'
    print('✅ Created air-balloon.html')

print(f'📄 Using balloon page: {balloon_file}')

# ─── UPDATE TOURS.HTML ───
tours_path = Path('tours.html')
if tours_path.exists():
    with open(tours_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the balloon card and fix the href
    # Look for the card with "Balloon" and change its href
    pattern = r'(<div\s+class="tour-card"[^>]*data-category="day"[^>]*>.*?<a\s+class="btn[^"]*"\s+href=")(?:balloon\.html|air-balloon\.html|hot-air-balloon\.html|#)(".*?Balloon.*?</a>)'
    replacement = r'\1' + balloon_file + r'\2'
    new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)

    if new_content != content:
        with open(tours_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ Updated tours.html to point to {balloon_file}')
    else:
        # Try a simpler approach: just find any balloon link and replace it
        simple_pattern = r'href="(?:balloon\.html|air-balloon\.html|hot-air-balloon\.html)"'
        if re.search(simple_pattern, content, re.IGNORECASE):
            new_content = re.sub(simple_pattern, f'href="{balloon_file}"', content, flags=re.IGNORECASE)
            with open(tours_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'✅ Updated tours.html to point to {balloon_file}')
        else:
            print('ℹ️  No balloon link found in tours.html')
else:
    print('❌ tours.html not found')

print('\n🎉 Done! Upload all files and clear cache.')
