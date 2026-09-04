#!/usr/bin/env python3
"""
Script to add Vercel Speed Insights to all HTML files in the project.
This adds the Speed Insights script tag to the <head> section of each HTML file.
"""

import os
import re
from pathlib import Path

# Speed Insights script to be added
SPEED_INSIGHTS_SCRIPT = """
  <!-- Vercel Speed Insights -->
  <script>
    window.si = window.si || function () { (window.siq = window.siq || []).push(arguments); };
  </script>
  <script defer src="/_vercel/speed-insights/script.js"></script>
"""

def add_speed_insights_to_html(file_path):
    """Add Speed Insights script to an HTML file if not already present."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if Speed Insights is already present
    if 'speed-insights' in content.lower() or '/_vercel/speed-insights' in content:
        print(f"⏭️  Skipping {file_path} - Speed Insights already present")
        return False
    
    # Find the closing </head> tag and insert before it
    if '</head>' in content:
        # Insert the script before </head>
        updated_content = content.replace('</head>', f'{SPEED_INSIGHTS_SCRIPT}\n</head>', 1)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Added Speed Insights to {file_path}")
        return True
    else:
        print(f"⚠️  Warning: No </head> tag found in {file_path}")
        return False

def main():
    """Process all HTML files in the current directory."""
    html_files = list(Path('.').glob('*.html'))
    
    if not html_files:
        print("No HTML files found in the current directory")
        return
    
    print(f"Found {len(html_files)} HTML files")
    print("-" * 60)
    
    updated_count = 0
    for html_file in sorted(html_files):
        if add_speed_insights_to_html(html_file):
            updated_count += 1
    
    print("-" * 60)
    print(f"\n✨ Complete! Updated {updated_count} out of {len(html_files)} HTML files")

if __name__ == '__main__':
    main()
