import os
import re
from pathlib import Path

CSS = '''
/* ─── HORIZONTAL CAROUSEL ─── */
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
    .tour-grid .tour-card { flex: 0 0 45% !important; max-width: 380px !important; }
}
@media (min-width: 1024px) {
    .tour-grid .tour-card { flex: 0 0 30% !important; max-width: 360px !important; }
}
@media (max-width: 480px) {
    .tour-grid .tour-card { flex: 0 0 90% !important; max-width: 340px !important; min-width: 200px !important; }
}
.tour-dots {
    display: flex !important;
    justify-content: center !important;
    gap: 8px !important;
    padding: 8px 0 10px 0 !important;
}
.tour-dots .dot {
    width: 10px !important; height: 10px !important; border-radius: 50% !important;
    background: #8a7a6a !important; border: none !important; padding: 0 !important;
    cursor: pointer !important; transition: all 0.3s ease !important; opacity: 0.4 !important;
}
.tour-dots .dot.active {
    background: #c94f2c !important; opacity: 1 !important; transform: scale(1.3) !important;
}
'''

JS = '''
(function() {
    var grid = document.querySelector('.tour-grid');
    var dotsContainer = document.getElementById('tourDots');
    if (!grid || !dotsContainer) return;
    var cards = grid.querySelectorAll('.tour-card');
    if (cards.length === 0) return;
    cards.forEach(function(card) {
        card.style.flex = '0 0 85%';
        card.style.maxWidth = '380px';
        card.style.scrollSnapAlign = 'center';
    });
    cards.forEach(function(card, index) {
        var dot = document.createElement('button');
        dot.className = 'dot' + (index === 0 ? ' active' : '');
        dot.setAttribute('data-index', index);
        dot.addEventListener('click', function() {
            var w = cards[0].offsetWidth + 16;
            grid.scrollTo({ left: index * w, behavior: 'smooth' });
        });
        dotsContainer.appendChild(dot);
    });
    var isScrolling = false;
    grid.addEventListener('scroll', function() {
        if (isScrolling) return;
        isScrolling = true;
        requestAnimationFrame(function() {
            var w = cards[0].offsetWidth + 16;
            var idx = Math.round(grid.scrollLeft / w);
            var dots = dotsContainer.querySelectorAll('.dot');
            dots.forEach(function(d, i) { d.classList.toggle('active', i === idx); });
            isScrolling = false;
        });
    });
    var resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            var w = cards[0].offsetWidth + 16;
            var idx = Math.round(grid.scrollLeft / w);
            var dots = dotsContainer.querySelectorAll('.dot');
            dots.forEach(function(d, i) { d.classList.toggle('active', i === idx); });
        }, 200);
    });
})();
'''

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'tour-grid' not in c:
        return False
    orig = c
    # Remove old carousel scripts
    c = re.sub(r'<script[^>]*>.*?(?:tourDots|carousel|pagination).*?</script>', '', c, flags=re.DOTALL | re.IGNORECASE)
    # Remove old .tour-grid styles
    c = re.sub(r'\.tour-grid\s*\{[^}]*\}', '', c, flags=re.DOTALL | re.IGNORECASE)
    c = re.sub(r'@media\s*\([^)]*\)\s*\{[^}]*\.tour-grid[^}]*\}', '', c, flags=re.DOTALL | re.IGNORECASE)
    c = re.sub(r'\.tour-grid::-webkit-scrollbar[^{]*\{[^}]*\}', '', c, flags=re.DOTALL | re.IGNORECASE)
    # Inject new CSS
    head_end = c.find('</head>')
    if head_end != -1:
        c = c[:head_end] + '<style>\n' + CSS + '\n</style>\n' + c[head_end:]
    # Add dots container
    if 'tour-dots' not in c:
        m = re.search(r'(<div\s+class="tour-grid"[^>]*>.*?</div>)', c, re.DOTALL | re.IGNORECASE)
        if m:
            c = c.replace(m.group(0), m.group(0) + '\n    <div class="tour-dots" id="tourDots"></div>\n')
    # Add JS
    body_end = c.rfind('</body>')
    if body_end != -1:
        c = c[:body_end] + '<script>\n' + JS + '\n</script>\n' + c[body_end:]
    if c != orig:
        backup_dir = Path('backup_carousel_final')
        backup_dir.mkdir(exist_ok=True)
        with open(backup_dir / path.name, 'w', encoding='utf-8') as f:
            f.write(orig)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'✅ {path.name}')
        return True
    return False

for root, dirs, files in os.walk('.'):
    if 'backup' in root.lower(): continue
    for f in files:
        if f.endswith('.html') and not f.startswith('.'):
            process_file(Path(root) / f)
print('\n✅ Done! Upload all HTML files and clear cache.')
