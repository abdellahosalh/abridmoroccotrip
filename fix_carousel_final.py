import os
import re
from pathlib import Path

NEW_CAROUSEL_CSS = '''
/* ─── TOUR CAROUSEL ─── */
.tour-grid {
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    gap: 16px !important;
    padding: 8px 8px 20px 8px !important;
    scroll-snap-type: x mandatory !important;
    -webkit-overflow-scrolling: touch !important;
    scroll-behavior: smooth !important;
    scrollbar-width: thin !important;
    scrollbar-color: var(--terracotta) var(--cream) !important;
}
.tour-grid::-webkit-scrollbar {
    height: 4px !important;
}
.tour-grid::-webkit-scrollbar-thumb {
    background: var(--terracotta) !important;
    border-radius: 10px !important;
}
.tour-grid::-webkit-scrollbar-track {
    background: var(--cream) !important;
    border-radius: 10px !important;
}
/* ─── CARD SIZES ─── */
.tour-grid .tour-card {
    flex: 0 0 85% !important;
    max-width: 380px !important;
    scroll-snap-align: center !important;
    min-height: 380px !important;
}
/* ─── TABLET ─── */
@media (min-width: 600px) {
    .tour-grid .tour-card {
        flex: 0 0 45% !important;
        max-width: 380px !important;
    }
}
/* ─── DESKTOP ─── */
@media (min-width: 1024px) {
    .tour-grid .tour-card {
        flex: 0 0 30% !important;
        max-width: 360px !important;
    }
}
/* ─── CARD CONTENT FIXES ─── */
.tour-card .tour-top {
    flex-wrap: wrap !important;
}
.tour-card .tour-top h3 {
    font-size: 1rem !important;
    line-height: 1.3 !important;
}
.tour-card .price {
    font-size: 1.1rem !important;
}
.tour-card .inclusions {
    font-size: 0.8rem !important;
}
.tour-card .tour-meta {
    flex-wrap: wrap !important;
}
.tour-card .tour-meta span {
    font-size: 0.7rem !important;
    padding: 2px 10px !important;
}
@media (max-width: 480px) {
    .tour-grid .tour-card {
        flex: 0 0 90% !important;
        max-width: 340px !important;
        min-height: 350px !important;
    }
    .tour-card .tour-image {
        height: 150px !important;
    }
    .tour-card .tour-body {
        padding: 14px !important;
    }
    .tour-card .tour-top h3 {
        font-size: 0.9rem !important;
    }
}
/* ─── PAGINATION DOTS ─── */
.tour-dots {
    display: flex !important;
    justify-content: center !important;
    gap: 8px !important;
    padding: 8px 0 20px 0 !important;
    margin: 0 !important;
}
.tour-dots .dot {
    width: 10px !important;
    height: 10px !important;
    border-radius: 50% !important;
    background: var(--muted) !important;
    border: none !important;
    padding: 0 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    display: inline-block !important;
    opacity: 0.4 !important;
}
.tour-dots .dot.active {
    background: var(--terracotta) !important;
    opacity: 1 !important;
    transform: scale(1.2) !important;
}
'''

def add_carousel_and_dots(content):
    # 1. Remove old .tour-grid styles
    content = re.sub(r'\.tour-grid\s*\{[^}]*\}', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'@media\s*\([^)]*\)\s*\{[^}]*\.tour-grid[^}]*\}', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'\.tour-grid::-webkit-scrollbar[^{]*\{[^}]*\}', '', content, flags=re.DOTALL | re.IGNORECASE)

    # 2. Inject new carousel CSS
    style_end = content.rfind('</style>')
    if style_end != -1:
        content = content[:style_end] + NEW_CAROUSEL_CSS + '\n' + content[style_end:]

    # 3. Find tour-grid and add dots container after it
    tour_grid_pattern = r'(<div\s+class="tour-grid"[^>]*>.*?</div>)'
    def add_dots(match):
        grid_html = match.group(1)
        # Check if dots already exist
        if 'tour-dots' in content:
            return match.group(0)
        # Add dots container after the grid
        dots_html = '''
    <!-- ─── PAGINATION DOTS ─── -->
    <div class="tour-dots" id="tourDots"></div>
    '''
        return grid_html + dots_html
    content = re.sub(tour_grid_pattern, add_dots, content, flags=re.DOTALL | re.IGNORECASE)

    # 4. Add JavaScript for dots
    js_pattern = r'(<script[^>]*>.*?</script>)'
    js_code = '''
    // ─── TOUR CAROUSEL PAGINATION DOTS ───
    (function() {
        const grid = document.querySelector('.tour-grid');
        const dotsContainer = document.getElementById('tourDots');
        if (!grid || !dotsContainer) return;

        const cards = grid.querySelectorAll('.tour-card');
        if (cards.length === 0) return;

        // Create dots
        cards.forEach((card, index) => {
            const dot = document.createElement('button');
            dot.className = 'dot' + (index === 0 ? ' active' : '');
            dot.setAttribute('data-index', index);
            dot.addEventListener('click', function() {
                const cardWidth = cards[0].offsetWidth + 16; // card width + gap
                grid.scrollTo({ left: index * cardWidth, behavior: 'smooth' });
            });
            dotsContainer.appendChild(dot);
        });

        // Update dots on scroll
        let isScrolling = false;
        grid.addEventListener('scroll', function() {
            if (isScrolling) return;
            isScrolling = true;
            requestAnimationFrame(() => {
                const cardWidth = cards[0].offsetWidth + 16;
                const scrollLeft = grid.scrollLeft;
                const index = Math.round(scrollLeft / cardWidth);
                const dots = dotsContainer.querySelectorAll('.dot');
                dots.forEach((dot, i) => {
                    dot.classList.toggle('active', i === index);
                });
                isScrolling = false;
            });
        });

        // Update on resize
        let resizeTimeout;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                const cardWidth = cards[0].offsetWidth + 16;
                const scrollLeft = grid.scrollLeft;
                const index = Math.round(scrollLeft / cardWidth);
                const dots = dotsContainer.querySelectorAll('.dot');
                dots.forEach((dot, i) => {
                    dot.classList.toggle('active', i === index);
                });
            }, 200);
        });
    })();
'''
    # Insert JS before the first </script> or before </body>
    script_match = re.search(js_pattern, content, re.DOTALL | re.IGNORECASE)
    if script_match:
        content = content[:script_match.end()] + js_code + content[script_match.end():]
    else:
        # If no script, add before </body>
        body_end = content.rfind('</body>')
        if body_end != -1:
            content = content[:body_end] + f'<script>{js_code}</script>\n' + content[body_end:]

    return content

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'tour-grid' not in content:
        print(f'ℹ️  No tour-grid in {filepath}, skipping')
        return False

    original = content
    new_content = add_carousel_and_dots(content)

    if new_content != content:
        backup_dir = Path('backup_carousel_final')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / filepath.name
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ Fixed carousel in {filepath}')
        return True
    else:
        print(f'ℹ️  No changes needed in {filepath}')
        return False

def main():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if 'backup' in root.lower():
            continue
        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(Path(root) / file)

    if not html_files:
        print('No HTML files found.')
        return

    print(f'Found {len(html_files)} HTML files.')
    any_changed = False
    for f in html_files:
        if fix_file(f):
            any_changed = True

    if any_changed:
        print('\n✅ Tour carousel with pagination dots applied to all pages.')
        print('   Backups saved in "backup_carousel_final".')
        print('   Upload all files and clear your cache.')
    else:
        print('\n🎉 All files are already updated.')

if __name__ == '__main__':
    main()
