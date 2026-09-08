# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os 
import re 
from pathlib import Path 
 
BASE_DIR = Path('.') 
FILES_TO_UPDATE = ['index.html', 'about.html', 'tours.html', 'packages.html', 'gallery.html', 'blog.html', 'contact.html', 'faq.html', 'air-balloon.html', 'airport-transfer.html', 'classic-morocco.html', 'cancellation-policy.html', 'cookies.html', 'essaouira.html', 'imilchil.html', 'imperial.html', 'marrakech.html', 'merzouga.html', 'privacy.html', 'private.html', 'terms.html', 'landing_page.html', 'blog-marrakech-top10.html', 'blog-imilchil.html', 'blog-chefchaouen.html', 'blog-sahara-erg-chebbi.html', 'blog-sahara-guide.html', 'blog-sahara-packing.html', 'blog-driving-safety.html', 'blog-essaouira-bus-vs-tour.html', 'blog-essaouira.html'] 
import csv
import re
from pathlib import Path

# Read issues from the CSV
issues_file = Path('audit-issues.csv')
if not issues_file.exists():
    print("❌ audit-issues.csv not found! Make sure it's in the same folder.")
    exit()

with open(issues_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    issues = list(reader)

# Helper to fix the broken email link
BAD_EMAIL_LINK = '/cdn-cgi/l/email-protection'
GOOD_EMAIL_LINK = 'mailto:abridmorocco@gmail.com'

def fix_title(content, filename, new_title):
    pattern = r'<title>.*?</title>'
    return re.sub(pattern, f'<title>{new_title}</title>', content, flags=re.DOTALL)

def fix_description(content, filename, new_desc):
    pattern = r'<meta name="description" content=".*?"\s*/?>'
    return re.sub(pattern, f'<meta name="description" content="{new_desc}" />', content, flags=re.DOTALL)

def fix_heading_structure(content):
    if '<h2' in content and '<h1' not in content:
        h2_match = re.search(r'<h2[^>]*>.*?</h2>', content, re.DOTALL)
        if h2_match:
            h2_content = h2_match.group(0)
            h2_text = re.sub(r'<[^>]+>', '', h2_content).strip()
            h1_tag = f'<h1>{h2_text}</h1>'
            content = content.replace(h2_content, h1_tag + h2_content, 1)
    return content

def fix_broken_email(content):
    if BAD_EMAIL_LINK in content:
        content = content.replace(BAD_EMAIL_LINK, GOOD_EMAIL_LINK)
    return content

# Process issues
print("🚀 Starting SEO fixes based on audit-issues.csv...\n")
success_count = 0
error_count = 0

for issue in issues:
    url = issue.get('URL', '')
    filename = url.split('/')[-1]
    if not filename:
        filename = 'index.html'

    filepath = Path(filename)
    if not filepath.exists():
        print(f"⚠️  File not found: {filename}")
        error_count += 1
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix specific issues based on the audit
        issue_type = issue.get('Issue', '')
        
        if 'Title too long' in issue_type:
            title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
            if title_match:
                base_title = title_match.group(1).strip()
                if len(base_title) > 60:
                    parts = base_title.split(' | ')
                    new_title = parts[0][:60]
                else:
                    new_title = base_title
                content = fix_title(content, filename, new_title)

        elif 'Meta description too long' in issue_type:
            desc_match = re.search(r'<meta name="description" content="(.*?)"', content, re.DOTALL)
            if desc_match:
                base_desc = desc_match.group(1).strip()
                if len(base_desc) > 160:
                    base_desc = base_desc[:157] + '...'
                content = fix_description(content, filename, base_desc)

        elif 'Heading levels skip' in issue_type:
            content = fix_heading_structure(content)

        elif 'Broken internal link' in issue_type or 'Page returns an error' in issue_type:
            content = fix_broken_email(content)

        # Write back the fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed: {filename} ({issue_type})")
        success_count += 1
        
    except Exception as e:
        error_msg = f"Error processing {filename}: {str(e)}"
        print(error_msg)
        with open("error_log.txt", "a", encoding="utf-8") as log:
            log.write(error_msg + "\n")
        error_count += 1

print(f"\n📊 Summary:")
print(f"   ✅ Successfully fixed: {success_count} files")
print(f"   ❌ Errors: {error_count} files")
print("\n✨ SEO fixes based on audit applied successfully!")