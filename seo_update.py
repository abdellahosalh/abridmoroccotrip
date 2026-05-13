import os
import re

directory = r"c:\Users\LENOVO THINKPAD\Documents\Nouveau dossier\abridmoroccotrip\abridmoroccotrip-main"

# 1. Update CSS
css_additions = """
/* 2026 Premium Updates & Trends */
.badge-trend {
    position: absolute;
    top: 15px;
    right: 15px;
    background: linear-gradient(135deg, #FF6A00 0%, #FF2600 100%);
    color: white;
    padding: 8px 18px;
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 1px;
    box-shadow: 0 8px 20px rgba(255, 38, 0, 0.4);
    z-index: 10;
    animation: pulseTrend 2s infinite alternate;
    text-transform: uppercase;
}

@keyframes pulseTrend {
    0% { transform: scale(1); box-shadow: 0 8px 20px rgba(255, 38, 0, 0.4); }
    100% { transform: scale(1.05); box-shadow: 0 12px 30px rgba(255, 38, 0, 0.6); }
}

.promo-banner {
    background: linear-gradient(90deg, #130a06 0%, #b8623b 50%, #130a06 100%);
    color: white;
    text-align: center;
    padding: 14px 20px;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 1px;
    position: relative;
    z-index: 999;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.promo-banner span {
    color: #ffcc00;
    font-weight: 800;
}

/* Glassmorphism & Premium card interactions */
.tour-card, .package-card {
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    position: relative;
    border: 1px solid rgba(0,0,0,0.05);
    background: rgba(255, 255, 255, 0.98);
}
.tour-card:hover, .package-card:hover {
    transform: translateY(-12px) !important;
    box-shadow: 0 25px 50px rgba(0,0,0,0.15) !important;
    border-color: var(--primary) !important;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary) 0%, #8c4222 100%) !important;
    box-shadow: 0 8px 25px rgba(184, 98, 59, 0.3) !important;
    border: none !important;
}
.btn-primary:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 12px 30px rgba(184, 98, 59, 0.5) !important;
}
"""

css_path = os.path.join(directory, 'style.css')
with open(css_path, 'a', encoding='utf-8') as f:
    f.write(css_additions)
print("Updated style.css with premium 2026 aesthetics.")

# 2. Update HTML SEO and Banners
for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = content
            
            # Update Titles for 2026
            new_content = re.sub(
                r'<title>AbridMoroccoTrip \| The #1 Best Morocco Tours & Desert Trips</title>',
                r'<title>AbridMoroccoTrip | Luxury & Sustainable Morocco Tours 2026 | Bespoke Desert Trips</title>',
                new_content
            )
            
            # General SEO Updates for keywords
            new_content = new_content.replace(
                'content="Morocco tours, best Marrakech tours, Sahara desert trips, luxury Morocco travel, Morocco itinerary, guided tours in Morocco, Merzouga desert camp, local travel agency Morocco"',
                'content="Morocco tours 2026, sustainable Morocco travel, bespoke desert camps, slow travel Morocco, luxury Morocco travel, authentic riad stays, Morocco itinerary, guided tours in Morocco"'
            )
            
            # Update Descriptions
            new_content = re.sub(
                r'<meta name="description" content="Book the absolute best, authentic Morocco tours with local expert Abdellah\.[^"]+" />',
                r'<meta name="description" content="Experience Morocco\'s top travel trends in 2026. Book bespoke luxury desert camps, sustainable slow travel, and immersive cultural tours with expert guide Abdellah." />',
                new_content
            )

            # Insert Promo Banner after <body>
            if "promo-banner" not in new_content:
                new_content = new_content.replace(
                    '<body>',
                    '<body>\n  <div class="promo-banner">SUMMER 2026 EXCLUSIVE: <span>Luxury & Sustainable Routes</span> — Book Your Bespoke Authentic Journey Today!</div>'
                )

            # Insert 2026 TOP TREND badge in package images
            if "badge-trend" not in new_content:
                new_content = new_content.replace(
                    '<div class="package-image">',
                    '<div class="package-image">\n              <div class="badge-trend">2026 TRENDING</div>'
                )
                new_content = new_content.replace(
                    '<div class="tour-image">',
                    '<div class="tour-image">\n              <div class="badge-trend">2026 TOP PICK</div>'
                )

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated SEO & Graphics for {file}")

print("All SEO and graphic updates applied!")
