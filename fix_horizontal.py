import os
import re
from pathlib import Path

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the desktop media query that reverts to grid
    content = re.sub(
        r'@media\s*\(\s*min-width\s*:\s*860px\s*\)\s*\{[^}]*\.tour-grid[^}]*\}[^}]*\}',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    # Ensure .tour-grid has horizontal styles
    if '.tour-grid' in content and 'flex-wrap: nowrap' not in content:
        # Inject the horizontal styles
        inject = '''
.tour-grid {
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    gap: 20px !important;
    padding: 4px 0 20px 0 !important;
    scroll-snap-type: x mandatory !important;
    -webkit-overflow-scrolling: touch !important;
}
.tour-grid .tour-card {
    flex: 0 0 300px !important;
    scroll-snap-align: start !important;
}
.tour-grid::-webkit-scrollbar {
    height: 6px !important;
}
.tour-grid::-webkit-scrollbar-thumb {
    background: var(--terracotta) !important;
    border-radius: 10px !important;
}
.tour-grid::-webkit-scrollbar-track {
    background: var(--cream) !important;
}
'''
        # Insert before the last </style>
        style_end = content.rfind('</style>')
        if style_end != -1:
            content = content[:style_end] + inject + '\n' + content[style_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✅ Fixed {filepath}')

# Fix tours.html and any other page with tour-grid
for html in Path('.').glob('*.html'):
    with open(html, 'r', encoding='utf-8') as f:
        if 'tour-grid' in f.read():
            fix_file(html)
