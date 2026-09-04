import os
import re

# Analytics script to inject
analytics_script = '''  <!-- Vercel Web Analytics -->
  <script>
    window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
  </script>
  <script defer src="/_vercel/insights/script.js"></script>
'''

# Get all HTML files
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print(f"Found {len(html_files)} HTML files")

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if analytics is already added
        if '/_vercel/insights/script.js' in content or 'window.va' in content:
            print(f"✓ {html_file} - Already has analytics, skipping")
            continue
        
        # Find the </head> tag and insert before it
        if '</head>' in content:
            content = content.replace('</head>', f'{analytics_script}</head>', 1)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ {html_file} - Analytics added")
        else:
            print(f"✗ {html_file} - No </head> tag found")
    
    except Exception as e:
        print(f"✗ {html_file} - Error: {e}")

print("\nDone! Analytics script added to all HTML files.")
