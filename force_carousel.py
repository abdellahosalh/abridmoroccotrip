import os
import re
from pathlib import Path

FORCE_CAROUSEL_CSS = '''
/* ─── FORCE HORIZONTAL CAROUSEL ─── */
.tour-grid {
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    overflow-y: visible !important;
    gap: 16px !important;
    padding: 8px 8px 20px 8px !important;
    scroll-snap-type: x mandatory !important;
    -webkit-overflow-scrolling: touch !important;
    scroll-behavior: smooth !important;
    max-width: 100% !important;
    width: 100% !important;
    flex-direction: row !important;
}
.tour-grid .tour-card {
    flex: 0 0 85% !important;
    max-width: 380px !important;
    min-width: 260px !important;
    scroll-snap-align: center !important;
    display: flex !important;
    flex-direction: column !important;
}
@media (min-width: 600px) {
    .tour-grid .tour-card {
        flex: 0 0 45% !important;
        max-width: 380px !important;
    }
}
@media (min-width: 1024px) {
    .tour-grid .tour-card {
        flex: 0 0 30% !important;
        max-width: 360px !important;
    }
}
@media (max-width: 480px) {
    .tour-grid .tour-card {
        flex: 0 0 90% !important;
        max-width: 340px !important;
        min-width: 200px !important;
    }
}
/* ─── REMOVE ANY GRID OR COLUMN LAYOUT ─── */
.tour-grid,
.tour-grid[class*="grid"],
.tour-grid[class*="column"],
.tour-grid[style*="grid"] {
    display: flex !important;
    grid-template-columns: unset !important;
    grid-template-rows: unset !important;
}
/* ─── DOTS ─── */
.tour-dots {
    display: flex !important;
    justify-content: center !important;
    gap: 8px !important;
    padding: 8px 0 10px 0 !important;
}
.tour-dots .dot {
    width: 10px !important;
    height: 10px !important;
    border-radius: 50% !important;
    background: #8a7a6a !important;
    border: none !important;
    padding: 0 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    opacity: 0.4 !important;
}
.tour-dots .dot.active {
    background: #c94f2c !important;
    opacity: 1 !important;
    transform: scale(1.3) !important;
}
'''

FIXED_JS = '''
// ─── TOUR CAROUSEL ───
(function() {
    var grid = document.querySelector('.tour-grid');
    var dotsContainer = document.getElementById('tourDots');
    if (!grid || !dotsContainer) return;

    // Force flex layout (in case CSS fails)
    grid.style.display = 'flex';
    grid.style.flexWrap = 'nowrap';
    grid.style.overflowX = 'auto';
    grid.style.scrollSnapType = 'x mandatory';
    grid.style.gap = '16px';

    var cards = grid.querySelectorAll('.tour-card');
    if (cards.length === 0) return;

    // Make each card flex-shrink 0
    cards.forEach(function(card) {
        card.style.flex = '0 0 85%';
        card.style.maxWidth = '380px';
        card.style.scrollSnapAlign = 'center';
        card.style.display = 'flex';
        card.style.flexDirection = 'column';
    });

    // Create dots
    cards.forEach(function(card, index) {
        var dot = document.createElement('button');
        dot.className = 'dot' + (index === 0 ? ' active' : '');
        dot.setAttribute('data-index', index);
        dot.addEventListener('click', function() {
            var cardWidth = cards[0].offsetWidth + 16;
            grid.scrollTo({ left: index * cardWidth, behavior: 'smooth' });
        });
        dotsContainer.appendChild(dot);
    });

    // Update dots on scroll
    var isScrolling = false;
    grid.addEventListener('scroll', function() {
        if (isScrolling) return;
        isScrolling = true;
        requestAnimationFrame(function() {
            var cardWidth = cards[0].offsetWidth + 16;
            var scrollLeft = grid.scrollLeft;
            var index = Math.round(scrollLeft / cardWidth);
            var dots = dotsContainer.querySelectorAll('.dot');
            dots.forEach(function(dot, i) {
                dot.classList.toggle('active', i === index);
            });
            isScrolling = false;
        });
    });

    // Resize handler
    var resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            var cardWidth = cards[0].offsetWidth + 16;
            var scrollLeft = grid.scrollLeft;
            var index = Math.round(scrollLeft / cardWidth);
            var dots = dotsContainer.querySelectorAll('.dot');
            dots.forEach(function(dot, i) {
                dot.classList.toggle('active', i === index);
            });
        }, 200);
    });
})();
'''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'tour-grid' not in content:
        return False

    original = content

    # Remove any existing carousel-related scripts and styles that might conflict
    content = re.sub(r'<script[^>]*>.*?(?:tourDots|carousel|pagination).*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'\.tour-grid\s*\{[^}]*\}', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'@media\s*\([^)]*\)\s*\{[^}]*\.tour-grid[^}]*\}', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'\.tour-grid::-webkit-scrollbar[^{]*\{[^}]*\}', '', content, flags=re.DOTALL | re.IGNORECASE)

    # Inject new CSS at the very end of the head, before </head>
    head_end = content.find('</head>')
    if head_end != -1:
        content = content[:head_end] + '<style>\n' + FORCE_CAROUSEL_CSS + '\n</style>\n' + content[head_end:]

    # Add dots container if missing
    if 'tour-dots' not in content:
        grid_match = re.search(r'(<div\s+class="tour-grid"[^>]*>.*?</div>)', content, re.DOTALL | re.IGNORECASE)
        if grid_match:
            dots_html = '\n    <div class="tour-dots" id="tourDots"></div>\n'
            content = content.replace(grid_match.group(0), grid_match.group(0) + dots_html)

    # Add fixed JavaScript before </body>
    body_end = content.rfind('</body>')
    if body_end != -1:
        content = content[:body_end] + '<script>\n' + FIXED_JS + '\n</script>\n' + content[body_end:]

    if content != original:
        backup_dir = Path('backup_carousel_final')
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / filepath.name
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ Fixed carousel in {filepath}')
        return True
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
        print('\n✅ Carousel forced on all pages. Backups in "backup_carousel_final".')
        print('   Upload all files and clear your cache.')
    else:
        print('\n🎉 All files are already fixed.')

if __name__ == '__main__':
    main()
