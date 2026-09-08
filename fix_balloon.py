import os
import re
from pathlib import Path

# ─── FIND EXISTING BALLOON PAGE ───
balloon_file = None
for f in ['balloon.html', 'air-balloon.html', 'hot-air-balloon.html']:
    if Path(f).exists():
        balloon_file = f
        break

if balloon_file is None:
    print('ℹ️  No balloon page found. Creating air-balloon.html...')
    with open('air-balloon.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Hot Air Balloon over Marrakech | AbridMoroccoTrip</title>
  <link rel="icon" href="https://i.postimg.cc/fR1NNYPc/500484189-17846895132482722-1431764686690149070-n.jpg" type="image/jpeg" />
  <meta name="description" content="Sunrise hot air balloon flight over Marrakech. Float above palm groves and the Atlas Mountains. Includes breakfast, hotel pickup, and flight certificate." />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700;14..32,800&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">

  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    :root { --terracotta: #c94f2c; --terracotta-dark: #a63d1f; --gold: #f4b942; --gold-light: #fce8c8; --cream: #fef9f0; --brown: #3d2a1e; --brown-light: #5a4a3a; --muted: #8a7a6a; --bg: #fcf8f2; --shadow: 0 8px 30px rgba(0,0,0,.06); --shadow-hover: 0 16px 48px rgba(0,0,0,.10); --radius: 20px; --radius-sm: 12px; --transition: .35s cubic-bezier(.175,.885,.32,1.275); --font: 'Inter',-apple-system,sans-serif; --font-serif: 'Playfair Display',serif; }
    html { scroll-behavior: smooth; }
    body { font-family: var(--font); background: var(--bg); color: var(--brown); line-height: 1.6; }
    img { max-width:100%; height:auto; display:block; }
    a { text-decoration:none; color:inherit; }
    .container { max-width:1200px; margin:0 auto; padding:0 24px; }
    .btn { display:inline-flex; align-items:center; justify-content:center; gap:10px; padding:14px 32px; border-radius:60px; font-weight:700; font-size:.95rem; border:none; cursor:pointer; transition:all .35s; text-align:center; }
    .btn-primary { background:linear-gradient(135deg,var(--terracotta),var(--terracotta-dark)); color:#fff; box-shadow:0 8px 28px rgba(201,79,44,.35); }
    .btn-primary:hover { transform:translateY(-3px) scale(1.02); box-shadow:0 14px 40px rgba(201,79,44,.45); }
    .btn-secondary { background:rgba(255,255,255,.92); color:var(--brown); border:2px solid rgba(61,42,30,.12); backdrop-filter:blur(10px); }
    .btn-secondary:hover { transform:translateY(-3px); border-color:var(--terracotta); box-shadow:0 8px 28px rgba(0,0,0,.08); background:#fff; }
    .btn-gold { background:linear-gradient(135deg,var(--gold),#e8a820); color:var(--brown); box-shadow:0 8px 28px rgba(244,185,66,.35); }
    .btn-gold:hover { transform:translateY(-3px) scale(1.02); box-shadow:0 14px 40px rgba(244,185,66,.5); }
    .scroll-progress { position:fixed; top:0; left:0; height:4px; background:linear-gradient(90deg,var(--terracotta),var(--gold)); z-index:999; width:0%; transition:width .1s; }
    .promo-banner { background:linear-gradient(90deg,var(--brown) 0%,var(--terracotta) 50%,var(--brown) 100%); background-size:200% 100%; animation:bannerSlide 6s linear infinite; color:#fff; text-align:center; padding:12px 20px; font-weight:600; font-size:.9rem; letter-spacing:.04em; position:relative; z-index:999; }
    @keyframes bannerSlide { 0% { background-position:0 0; } 100% { background-position:200% 0; } }
    .promo-banner span { color:var(--gold); font-weight:800; }
    .site-header { background:rgba(255,255,255,.92); backdrop-filter:blur(12px); position:sticky; top:0; z-index:100; border-bottom:1px solid rgba(0,0,0,.05); padding:10px 0; }
    .site-header.scrolled { box-shadow:0 4px 20px rgba(0,0,0,.06); }
    .nav { display:flex; align-items:center; justify-content:space-between; gap:20px; flex-wrap:nowrap; }
    .brand { display:flex; align-items:center; gap:12px; flex-shrink:0; }
    .brand-logo { width:38px; height:38px; min-width:38px; min-height:38px; max-width:38px; max-height:38px; overflow:hidden; flex-shrink:0; border-radius:10px; border:2px solid rgba(255,255,255,0.6); box-shadow:0 4px 14px rgba(192,82,46,0.25); }
    .brand-logo img { width:100%; height:100%; object-fit:cover; }
    .brand-text strong { font-size:0.9rem; color:var(--brown); white-space:nowrap; }
    .brand-text span { font-size:.55rem; color:var(--muted); display:block; margin-top:-2px; white-space:nowrap; }
    .nav-links { display:flex; list-style:none; gap:8px; font-size:.75rem; font-weight:500; align-items:center; flex-wrap:nowrap; }
    .nav-links a { color:var(--brown-light); transition:color var(--transition); white-space:nowrap; padding:4px 6px; }
    .nav-links a:hover, .nav-links a.active { color:var(--terracotta); }
    .nav-actions { display:flex; align-items:center; gap:4px; flex-shrink:0; flex-wrap:nowrap; }
    .nav-actions .contact-link { font-weight:600; color:var(--brown-light); padding:4px 8px; border-radius:60px; font-size:.75rem; white-space:nowrap; }
    .nav-actions .contact-link:hover { color:var(--terracotta); background:rgba(201,79,44,.06); }
    .nav-actions .btn-gold { padding:4px 12px; font-size:.7rem; }
    .lang-wrapper { position:relative; display:inline-block; flex-shrink:0; }
    .lang-selector { display:flex; align-items:center; gap:4px; background:none; border:1px solid rgba(44,26,18,.12); border-radius:60px; padding:3px 8px; cursor:pointer; font-weight:600; font-size:.65rem; color:var(--brown); transition:all .3s; }
    .lang-selector:hover { border-color:var(--terracotta); background:rgba(201,79,44,.06); }
    .lang-selector .arrow { font-size:.5rem; transition:transform .3s; }
    .lang-selector.open .arrow { transform:rotate(180deg); }
    .lang-dropdown { display:none; position:absolute; top:calc(100% + 4px); right:0; background:#fff; border-radius:12px; box-shadow:0 16px 40px rgba(0,0,0,.15); padding:4px 0; min-width:130px; border:1px solid rgba(0,0,0,.06); z-index:100; overflow:hidden; }
    .lang-dropdown.show { display:block; }
    .lang-dropdown a { display:flex; align-items:center; gap:8px; padding:8px 16px; color:var(--brown); text-decoration:none; font-weight:500; font-size:.8rem; transition:background .2s; }
    .lang-dropdown a:hover { background:#f5ede6; }
    .lang-dropdown a .flag { font-size:1.1rem; }
    .menu-toggle { display:none; flex-direction:column; gap:4px; background:none; border:none; cursor:pointer; padding:4px; flex-shrink:0; }
    .menu-toggle span { display:block; width:24px; height:2.5px; background:var(--brown); border-radius:4px; transition:var(--transition); }
    .skiptranslate iframe { display:none !important; }
    .goog-te-banner-frame.skiptranslate { display:none !important; }
    body { top:0px !important; }
    .mobile-menu { display:none; padding:16px 0; }
    .mobile-menu.open { display:block; }
    .mobile-panel { display:flex; flex-direction:column; gap:12px; background:#fff; border-radius:var(--radius-sm); padding:20px; box-shadow:var(--shadow); }
    .mobile-panel a { font-weight:500; padding:8px 0; border-bottom:1px solid rgba(0,0,0,.05); }

    @media (max-width: 860px) {
      .nav-links { display:none; }
      .menu-toggle { display:flex; }
      .nav-actions .contact-link { display:none; }
      .nav-actions .btn-gold { display:none; }
      .nav-actions .lang-wrapper { display:none; }
      .brand-text strong { font-size:.75rem; }
      .brand-logo { width:28px; height:28px; min-width:28px; min-height:28px; max-width:28px; max-height:28px; }
      .brand-text span { display:none; }
    }

    .page-hero { padding:80px 0 60px; text-align:center; position:relative; overflow:hidden; }
    .page-hero::before { content:''; position:absolute; inset:0; background:radial-gradient(ellipse 60% 50% at 50% 20%, rgba(244,185,66,.15) 0%, transparent 65%), linear-gradient(180deg,#fff9f4 0%,var(--bg) 100%); z-index:0; }
    .page-hero > * { position:relative; z-index:1; }
    .page-hero h1 { font-family:var(--font-serif); font-size:clamp(2.5rem,6vw,4rem); color:var(--brown); margin-bottom:16px; }
    .page-hero .highlight { background:linear-gradient(135deg,var(--terracotta),#e88a4a,var(--gold)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
    .page-hero p { font-size:1.15rem; color:var(--muted); max-width:600px; margin:0 auto; line-height:1.75; }
    .page-hero .badge { display:inline-block; background:rgba(255,255,255,.85); backdrop-filter:blur(8px); padding:8px 20px; border-radius:60px; font-weight:600; font-size:.9rem; border:1px solid rgba(61,42,30,.06); margin-top:12px; }

    .info-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:24px; margin:48px 0; }
    .info-card { background:#fff; border-radius:var(--radius); padding:24px; box-shadow:var(--shadow); border:1px solid rgba(0,0,0,.04); transition:transform .3s ease; }
    .info-card:hover { transform:translateY(-4px); box-shadow:var(--shadow-hover); }
    .info-card .icon { font-size:2.5rem; margin-bottom:12px; display:block; }
    .info-card h3 { font-family:var(--font-serif); font-size:1.3rem; margin-bottom:8px; color:var(--brown); }
    .info-card p { color:var(--brown-light); font-size:.95rem; line-height:1.7; }

    .step-list { display:grid; grid-template-columns:1fr 1fr; gap:20px; margin:30px 0; }
    .step-item { background:var(--cream); border-radius:var(--radius-sm); padding:20px; text-align:center; }
    .step-item .num { display:inline-block; background:var(--terracotta); color:#fff; width:40px; height:40px; border-radius:50%; line-height:40px; font-weight:700; margin-bottom:8px; }
    .step-item h4 { font-weight:700; color:var(--brown); margin-bottom:4px; }
    .step-item p { font-size:.9rem; color:var(--muted); }

    .cta-box { background:var(--cream); border-radius:var(--radius); padding:40px; text-align:center; margin-top:40px; }
    .cta-box h2 { font-family:var(--font-serif); font-size:2rem; margin-bottom:8px; }
    .cta-box p { color:var(--muted); max-width:600px; margin:0 auto 20px; }
    .contact-details { background:#fff; border-radius:var(--radius-sm); padding:20px; display:flex; flex-wrap:wrap; justify-content:center; gap:24px; margin-top:20px; }
    .contact-details .item { display:flex; align-items:center; gap:10px; font-weight:600; }

    footer { background:var(--brown); color:rgba(255,255,255,.7); padding:48px 0 24px; margin-top:40px; border-top:1px solid rgba(255,255,255,.06); overflow-x:hidden; max-width:100%; width:100%; }
    footer .container { max-width:1200px; margin:0 auto; padding:0 16px; overflow-x:hidden; }
    .footer-grid { display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:40px; margin-bottom:40px; }
    .footer-brand { display:flex; align-items:center; gap:12px; margin-bottom:14px; }
    .footer-brand img { width:44px; height:44px; border-radius:10px; object-fit:cover; border:2px solid rgba(255,255,255,.1); }
    .footer-brand strong { font-size:1.1rem; color:#fff; display:block; }
    .footer-brand span { font-size:0.7rem; color:rgba(255,255,255,.4); }
    .footer-desc { font-size:0.85rem; color:rgba(255,255,255,.5); line-height:1.7; max-width:280px; }
    .footer-heading { color:#fff; font-size:0.85rem; font-weight:700; margin-bottom:14px; }
    .footer-links { list-style:none; padding:0; font-size:0.85rem; line-height:2.2; color:rgba(255,255,255,.5); }
    .footer-links a { color:rgba(255,255,255,.5); transition:color .2s; }
    .footer-links a:hover { color:#fff; }
    .footer-bottom { border-top:1px solid rgba(255,255,255,.06); padding-top:20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; font-size:0.75rem; color:rgba(255,255,255,.3); }

    @media (max-width: 860px) { .footer-grid { grid-template-columns:1fr 1fr; gap:24px; } }
    @media (max-width: 480px) { .footer-grid { grid-template-columns:1fr; gap:16px; } .step-list { grid-template-columns:1fr; } }

    .wa-float { position:fixed; bottom:24px; right:24px; background:#25D366; color:#fff; width:60px; height:60px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:2rem; box-shadow:0 8px 28px rgba(37,211,102,.4); z-index:50; transition:var(--transition); }
    .wa-float:hover { transform:scale(1.1) rotate(-5deg); }
  </style>
</head>
<body>

  <div class="scroll-progress" id="scrollProgress"></div>
  <div class="promo-banner">SUMMER 2026 EXCLUSIVE: <span>Luxury &amp; Sustainable Routes</span> — Book Your Bespoke Authentic Journey Today!</div>

  <header class="site-header" id="siteHeader">
    <div class="container nav">
      <a href="index.html" class="brand">
        <div class="brand-logo">
          <img src="https://i.postimg.cc/fR1NNYPc/500484189-17846895132482722-1431764686690149070-n.jpg" alt="Logo">
        </div>
        <div class="brand-text">
          <strong>AbridMoroccoTrip</strong>
          <span>Premium Tours</span>
        </div>
      </a>
      <ul class="nav-links">
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="tours.html" class="active">Tours</a></li>
        <li><a href="classic-morocco.html">Classic 13-Day</a></li>
        <li><a href="packages.html">Packages</a></li>
        <li><a href="gallery.html">Gallery</a></li>
        <li><a href="blog.html">Blog</a></li>
        <li><a href="airport-transfer.html">✈️ Transfer</a></li>
      </ul>
      <div class="nav-actions">
        <a href="contact.html" class="contact-link">Contact</a>
        <a class="btn btn-gold" href="contact.html">✨ Book Now</a>
        <div id="google_translate_element" style="display:inline-block;"></div>
        <button class="menu-toggle" id="menuToggle" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
    <div class="container mobile-menu" id="mobileMenu">
      <div class="mobile-panel">
        <a href="index.html">🏠 Home</a>
        <a href="about.html">👤 About Us</a>
        <a href="tours.html">🗺️ Tours</a>
        <a href="classic-morocco.html">🗺️ Classic 13-Day</a>
        <a href="packages.html">📦 Packages</a>
        <a href="gallery.html">🖼️ Gallery</a>
        <a href="blog.html">📰 Blog</a>
        <a href="airport-transfer.html">✈️ Transfer</a>
        <a href="contact.html">📋 Contact</a>
        <a href="https://wa.me/212762934488" target="_blank" style="color:#25D366;font-weight:700;">💬 WhatsApp</a>
        <a href="contact.html" class="btn-gold" style="display:block;text-align:center;margin-top:8px;">✨ Book Now</a>
      </div>
    </div>
  </header>

  <section class="page-hero">
    <div class="container">
      <span class="badge">🎈 Bucket List Experience</span>
      <h1>Sunrise <span class="highlight">Balloon</span> over Marrakech</h1>
      <p>Float above palm groves, ancient medinas, and the majestic Atlas Mountains as the sun rises over Morocco.</p>
    </div>
  </section>

  <div class="container">
    <div class="info-grid">
      <div class="info-card">
        <span class="icon">🎈</span>
        <h3>1‑Hour Flight</h3>
        <p>Drift peacefully over the Marrakech palm grove and enjoy panoramic views of the city and the High Atlas Mountains.</p>
      </div>
      <div class="info-card">
        <span class="icon">🌅</span>
        <h3>Sunrise Departure</h3>
        <p>Early morning pickup, just before dawn – witness the golden glow as the sun rises over the desert landscape.</p>
      </div>
      <div class="info-card">
        <span class="icon">🧺</span>
        <h3>Berber Breakfast</h3>
        <p>After landing, enjoy a traditional Berber breakfast with tea, pastries, and fresh bread in a desert camp.</p>
      </div>
    </div>

    <h2 style="font-family:var(--font-serif); font-size:2rem; text-align:center; margin:40px 0 20px;">How It Works</h2>
    <div class="step-list">
      <div class="step-item"><div class="num">1</div><h4>Hotel Pickup</h4><p>We collect you from your riad or hotel before sunrise.</p></div>
      <div class="step-item"><div class="num">2</div><h4>Balloon Launch</h4><p>Watch the balloon inflate and lift off as the sun rises.</p></div>
      <div class="step-item"><div class="num">3</div><h4>Soar &amp; Explore</h4><p>Float for approximately 1 hour over the palm grove.</p></div>
      <div class="step-item"><div class="num">4</div><h4>Breakfast &amp; Return</h4><p>Enjoy a Berber breakfast, get your certificate, and return.</p></div>
    </div>

    <div style="background:var(--cream); border-radius:var(--radius); padding:30px; margin:40px 0; border-left:5px solid var(--terracotta);">
      <h3 style="font-family:var(--font-serif); font-size:1.5rem; margin-bottom:12px;">✅ What's Included</h3>
      <ul style="list-style:none; padding:0; display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <li style="display:flex; gap:10px; align-items:center; font-size:.95rem; color:var(--brown-light);"><span style="color:var(--terracotta); font-weight:700;">✓</span> Hotel pickup &amp; drop‑off</li>
        <li style="display:flex; gap:10px; align-items:center; font-size:.95rem; color:var(--brown-light);"><span style="color:var(--terracotta); font-weight:700;">✓</span> 1‑hour hot air balloon flight</li>
        <li style="display:flex; gap:10px; align-items:center; font-size:.95rem; color:var(--brown-light);"><span style="color:var(--terracotta); font-weight:700;">✓</span> Berber breakfast with tea &amp; pastries</li>
        <li style="display:flex; gap:10px; align-items:center; font-size:.95rem; color:var(--brown-light);"><span style="color:var(--terracotta); font-weight:700;">✓</span> Flight certificate</li>
        <li style="display:flex; gap:10px; align-items:center; font-size:.95rem; color:var(--brown-light);"><span style="color:var(--terracotta); font-weight:700;">✓</span> Professional pilot &amp; crew</li>
        <li style="display:flex; gap:10px; align-items:center; font-size:.95rem; color:var(--brown-light);"><span style="color:var(--terracotta); font-weight:700;">✓</span> Insurance included</li>
      </ul>
    </div>

    <div class="cta-box">
      <h2>Ready to float above Marrakech?</h2>
      <p>Contact us to book your sunrise balloon experience. Group and private flights available.</p>
      <div class="contact-details">
        <div class="item">📞 <a href="tel:+212762934488">+212 762 934 488</a></div>
        <div class="item">💬 <a href="https://wa.me/212762934488" target="_blank">WhatsApp</a></div>
        <div class="item">✉️ <a href="mailto:abridmorocco@gmail.com">abridmorocco@gmail.com</a></div>
      </div>
      <a href="contact.html" class="btn btn-primary" style="margin-top:20px;">📝 Book Your Balloon Flight</a>
    </div>
    <p style="text-align:center;font-size:.8rem;color:var(--muted);margin-top:20px;">* Prices vary by season and group size. Contact us for an accurate quote.</p>
  </div>

  <footer>
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand"><img src="https://i.postimg.cc/fR1NNYPc/500484189-17846895132482722-1431764686690149070-n.jpg" alt="Logo"><div><strong>AbridMoroccoTrip</strong><span>Premium Morocco Tours</span></div></div>
          <p class="footer-desc">Authentic Morocco tours with local expert Abdellah. Sahara, Atlas, Imperial Cities — private guides and luxury camps.</p>
        </div>
        <div><h4 class="footer-heading">Pages</h4><ul class="footer-links"><li><a href="index.html">Home</a></li><li><a href="about.html">About</a></li><li><a href="tours.html">Tours</a></li><li><a href="packages.html">Packages</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="blog.html">Blog</a></li></ul></div>
        <div><h4 class="footer-heading">Support</h4><ul class="footer-links"><li><a href="faq.html">FAQ</a></li><li><a href="contact.html">Booking</a></li><li><a href="cancellation-policy.html">Cancellation Policy</a></li><li><a href="privacy.html">Privacy Policy</a></li><li><a href="terms.html">Terms of Service</a></li></ul></div>
        <div>
          <h4 class="footer-heading">Contact</h4>
          <a href="contact.html" style="display:inline-block;background:var(--gold);color:var(--brown);padding:8px 20px;border-radius:60px;font-weight:700;text-decoration:none;font-size:0.85rem;margin-bottom:12px;">📋 Contact Us</a>
          <div style="display:flex; gap:10px; margin-top:8px;">
            <a href="https://wa.me/212762934488" target="_blank" style="background:#25D366; color:#fff; padding:6px 16px; border-radius:30px; font-size:0.75rem; font-weight:600; text-decoration:none;">WhatsApp</a>
            <a href="https://www.instagram.com/abridmorocco/" target="_blank" style="background:linear-gradient(135deg,#E1306C,#833AB4); color:#fff; padding:6px 16px; border-radius:30px; font-size:0.75rem; font-weight:600; text-decoration:none;">Instagram</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© <span id="year"></span> AbridMoroccoTrip. All rights reserved.</div>
        <div style="display:flex; gap:20px; flex-wrap:wrap;">
          <a href="terms.html">Terms</a>
          <a href="privacy.html">Privacy</a>
          <a href="cookies.html">Cookies</a>
          <span style="color:rgba(255,255,255,.15);">|</span>
          <span style="color:rgba(255,255,255,.15);">🇲🇦 Made in Morocco</span>
        </div>
      </div>
    </div>
  </footer>

  <a href="https://wa.me/212762934488" class="wa-float" target="_blank" aria-label="Chat on WhatsApp">💬</a>

  <script>
    document.getElementById('year').textContent = new Date().getFullYear();
    document.getElementById('menuToggle').addEventListener('click', function() {
      document.getElementById('mobileMenu').classList.toggle('open');
    });
    window.addEventListener('scroll', function() {
      var scrollTop = window.pageYOffset;
      var docHeight = document.documentElement.scrollHeight - window.innerHeight;
      document.getElementById('scrollProgress').style.width = (scrollTop / docHeight * 100) + '%';
      document.getElementById('siteHeader').classList.toggle('scrolled', scrollTop > 60);
    });
    function googleTranslateElementInit() {
      new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,fr,es,de,it,pt,ru,ja,ar,zh-CN',
        layout: google.translate.TranslateElement.InlineLayout.HORIZONTAL,
        autoDisplay: false
      }, 'google_translate_element');
    }
  </script>
  <script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>
</html>''')
    print('✅ Created air-balloon.html')
    balloon_file = 'air-balloon.html'

# ─── UPDATE TOURS.HTML LINK ───
if Path('tours.html').exists():
    with open('tours.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace any balloon link with the correct file
    pattern = r'(<a\s+class="btn[^"]*"\s+href=")(?:balloon\.html|air-balloon\.html|hot-air-balloon\.html)(".*?Balloon.*?</a>)'
    replacement = r'\1' + balloon_file + r'\2'
    new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE | re.DOTALL)

    if new_content != content:
        with open('tours.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ Updated tours.html to point to {balloon_file}')
    else:
        print('ℹ️  No balloon link found in tours.html – it may already point to the correct page.')
else:
    print('⚠️  tours.html not found. Can\'t update link.')

print('\n🎉 Done! Upload all files and clear cache.')
