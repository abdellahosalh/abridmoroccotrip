# -*- coding: utf-8 -*-
import re, os
BASE = r"C:\Users\abrid\OneDrive\Documents\Default Project\abridmoroccotrip-main"
SITE = "https://www.abridmorocco.com"

COMMON_FR = [
 ("Skip to main content", "Aller au contenu principal"),
 ("Abrid Morocco home", "Accueil Abrid Morocco"),
 ("Search Abrid Morocco", "Rechercher sur Abrid Morocco"),
 ("Chat with Abrid Morocco on WhatsApp", "Discuter avec Abrid Morocco sur WhatsApp"),
 ("Chat with Abrid on WhatsApp", "Discuter avec Abrid sur WhatsApp"),
 ('aria-label="Reserve a tour"', 'aria-label="Réserver un circuit"'),
 ('aria-label="Open menu"', 'aria-label="Ouvrir le menu"'),
 ("PREMIUM TOURS", "CIRCUITS PREMIUM"),
 ("Morocco travel platform", "Plateforme de voyage au Maroc"),
 ("A Morocco travel platform built by people who know Morocco. Sahara, Atlas, Imperial Cities - private guides and characterful stays since 2022.", "Plateforme de voyage au Maroc créée par des gens qui connaissent le Maroc. Sahara, Atlas, Cités impériales — guides privés et hébergements de caractère depuis 2022."),
 ("A Morocco travel platform built by people who know Morocco. Sahara, Atlas, Imperial Cities — private guides and characterful stays since 2022.", "Plateforme de voyage au Maroc créée par des gens qui connaissent le Maroc. Sahara, Atlas, Cités impériales — guides privés et hébergements de caractère depuis 2022."),
 ('<li><a href="https://www.abridmorocco.com/index.html">Home</a></li>', '<li><a href="https://www.abridmorocco.com/index.html">Accueil</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/trips.html">Trips</a></li>', '<li><a href="https://www.abridmorocco.com/trips.html">Circuits</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/destinations.html">Destinations</a></li>', '<li><a href="https://www.abridmorocco.com/destinations.html">Destinations</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/experiences.html">Experiences</a></li>', '<li><a href="https://www.abridmorocco.com/experiences.html">Expériences</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/blog.html">Morocco Guide</a></li>', '<li><a href="https://www.abridmorocco.com/blog.html">Guide du Maroc</a></li>'),
 ('class="nav-cta">Plan My Trip</a>', 'class="nav-cta">Planifier mon voyage</a>'),
 ('<li><a href="https://www.abridmorocco.com/about.html">About</a></li>', '<li><a href="https://www.abridmorocco.com/about.html">À propos</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/contact.html">Contact</a></li>', '<li><a href="https://www.abridmorocco.com/contact.html">Contact</a></li>'),
 ('>Search</a>', '>Rechercher</a>'),
 ('>Home</a>', '>Accueil</a>'),
 ('>Trips</a>', '>Circuits</a>'),
 ('>Destinations</a>', '>Destinations</a>'),
 ('>Experiences</a>', '>Expériences</a>'),
 ('>Morocco Guide</a>', '>Guide du Maroc</a>'),
 ('>Plan My Trip</a>', '>Planifier mon voyage</a>'),
 ('>About Abrid</a>', '>À propos d\u2019Abrid</a>'),
 ('>Contact</a>', '>Contact</a>'),
 ('>Chat on WhatsApp</a>', '>Discuter sur WhatsApp</a>'),
 ('>Reserve</button>', '>Réserver</button>'),
 ('>Plan My Trip</a>', '>Planifier mon voyage</a>'),
 ('placeholder="Search trips, destinations, guides..."', 'placeholder="Rechercher circuits, destinations, guides..."'),
 ('placeholder="Search trips, destinations, guides…"', 'placeholder="Rechercher circuits, destinations, guides…"'),
 ('aria-label="Search">', 'aria-label="Recherche">'),
 ('aria-label="Search Abrid Morocco"', 'aria-label="Rechercher sur Abrid Morocco"'),
 ('>Close</button>', '>Fermer</button>'),
 ('aria-label="Cookie consent"', 'aria-label="Consentement aux cookies"'),
 ('We use cookies to improve your experience and analyse site traffic. Read our <a href="https://www.abridmorocco.com/cookies.html">cookie policy</a>.', 'Nous utilisons des cookies pour améliorer votre expérience et analyser le trafic du site. Lisez notre <a href="https://www.abridmorocco.com/cookies.html">politique des cookies</a>.'),
 ('>Accept</button>', '>Accepter</button>'),
 ('>Decline</button>', '>Refuser</button>'),
 ('<h4>Booking</h4>', '<h4>Réservation</h4>'),
 ('>How Booking Works</a>', '>Comment fonctionne la réservation</a>'),
 ('>Cancellation Policy</a>', '>Politique d\u2019annulation</a>'),
 ('>Terms of Service</a>', '>Conditions d\u2019utilisation</a>'),
 ('>Airport Transfer</a>', '>Transfert aéroport</a>'),
 ('<h4>Company</h4>', '<h4>Société</h4>'),
 ('>About Us</a>', '>À propos de nous</a>'),
 ('>Gallery</a>', '>Galerie</a>'),
 ('<h4>Contact</h4>', '<h4>Contact</h4>'),
 ('>Get in Touch</a>', '>Nous contacter</a>'),
 ('>Live Chat on WhatsApp</a>', '>Chat en direct sur WhatsApp</a>'),
 ('>FAQ</a>', '>FAQ</a>'),
 ('>Email Us</a>', '>Nous écrire</a>'),
 ('<h4>Purpose</h4>', '<h4>Notre mission</h4>'),
 ('>Responsible Travel</a>', '>Voyage responsable</a>'),
 ('>Community Journey</a>', '>Voyage communautaire</a>'),
 ('>Traveller Reviews</a>', '>Avis des voyageurs</a>'),
 ('>Leave a Google Review</a>', '>Laisser un avis Google</a>'),
 ('All rights reserved.', 'Tous droits réservés.'),
 ('>Terms</a>', '>Conditions</a>'),
 ('>Privacy</a>', '>Confidentialité</a>'),
 ('>Cookies</a>', '>Cookies</a>'),
 ('>Made in Morocco</span>', '>Fait au Maroc</span>'),
 ('aria-label="Subscribe"', 'aria-label="S\u2019abonner"'),
 ('aria-label="Close">✕</button>', 'aria-label="Fermer">✕</button>'),
 ('Morocco in your inbox', 'Le Maroc dans votre boîte mail'),
 ('One short letter a month — routes, seasons, secret spots. No spam, ever.', 'Une courte lettre par mois — itinéraires, saisons, adresses secrètes. Jamais de spam.'),
 ('<label for="abridName">Your name</label>', '<label for="abridName">Votre nom</label>'),
 ('<label for="abridEmail">Email address</label>', '<label for="abridEmail">Adresse e-mail</label>'),
 ("<label for=\"abridInterest\">I'm dreaming of…</label>", '<label for="abridInterest">Je rêve de…</label>'),
 ('<option value="Anywhere in Morocco">Anywhere in Morocco</option>', '<option value="Anywhere in Morocco">Partout au Maroc</option>'),
 ('<option value="Sahara desert">Sahara desert</option>', '<option value="Sahara desert">Désert du Sahara</option>'),
 ('<option value="High Atlas">High Atlas</option>', '<option value="High Atlas">Haut Atlas</option>'),
 ('<option value="Imperial cities">Imperial cities</option>', '<option value="Imperial cities">Cités impériales</option>'),
 ('>Subscribe free</button>', '>S\u2019abonner gratuitement</button>'),
 ('Unsubscribe anytime with one click.', 'Désinscription en un clic à tout moment.'),
 ('<a href="https://www.abridmorocco.com/plan-my-trip.html" class="footer-contact-btn">Plan My Trip</a>', '<a href="https://www.abridmorocco.com/plan-my-trip.html" class="footer-contact-btn">Planifier mon voyage</a>'),
 ('<a class="btn btn-primary btn-sm" href="https://www.abridmorocco.com/plan-my-trip.html">Plan My Trip</a>', '<a class="btn btn-primary btn-sm" href="https://www.abridmorocco.com/plan-my-trip.html">Planifier mon voyage</a>'),
]

COMMON_ES = [
 ("Skip to main content", "Ir al contenido principal"),
 ("Abrid Morocco home", "Inicio de Abrid Morocco"),
 ("Search Abrid Morocco", "Buscar en Abrid Morocco"),
 ("Chat with Abrid Morocco on WhatsApp", "Chatear con Abrid Morocco por WhatsApp"),
 ("Chat with Abrid on WhatsApp", "Chatear con Abrid por WhatsApp"),
 ('aria-label="Reserve a tour"', 'aria-label="Reservar un tour"'),
 ('aria-label="Open menu"', 'aria-label="Abrir el menú"'),
 ("PREMIUM TOURS", "TOURS PREMIUM"),
 ("Morocco travel platform", "Plataforma de viajes por Marruecos"),
 ("A Morocco travel platform built by people who know Morocco. Sahara, Atlas, Imperial Cities - private guides and characterful stays since 2022.", "Plataforma de viajes por Marruecos creada por quienes conocen Marruecos. Sáhara, Atlas, Ciudades Imperiales: guías privados y alojamientos con encanto desde 2022."),
 ("A Morocco travel platform built by people who know Morocco. Sahara, Atlas, Imperial Cities — private guides and characterful stays since 2022.", "Plataforma de viajes por Marruecos creada por quienes conocen Marruecos. Sáhara, Atlas, Ciudades Imperiales: guías privados y alojamientos con encanto desde 2022."),
 ('<li><a href="https://www.abridmorocco.com/index.html">Home</a></li>', '<li><a href="https://www.abridmorocco.com/index.html">Inicio</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/trips.html">Trips</a></li>', '<li><a href="https://www.abridmorocco.com/trips.html">Viajes</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/destinations.html">Destinations</a></li>', '<li><a href="https://www.abridmorocco.com/destinations.html">Destinos</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/experiences.html">Experiences</a></li>', '<li><a href="https://www.abridmorocco.com/experiences.html">Experiencias</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/blog.html">Morocco Guide</a></li>', '<li><a href="https://www.abridmorocco.com/blog.html">Guía de Marruecos</a></li>'),
 ('class="nav-cta">Plan My Trip</a>', 'class="nav-cta">Planifica mi viaje</a>'),
 ('<li><a href="https://www.abridmorocco.com/about.html">About</a></li>', '<li><a href="https://www.abridmorocco.com/about.html">Nosotros</a></li>'),
 ('<li><a href="https://www.abridmorocco.com/contact.html">Contact</a></li>', '<li><a href="https://www.abridmorocco.com/contact.html">Contacto</a></li>'),
 ('>Search</a>', '>Buscar</a>'),
 ('>Home</a>', '>Inicio</a>'),
 ('>Trips</a>', '>Viajes</a>'),
 ('>Destinations</a>', '>Destinos</a>'),
 ('>Experiences</a>', '>Experiencias</a>'),
 ('>Morocco Guide</a>', '>Guía de Marruecos</a>'),
 ('>Plan My Trip</a>', '>Planifica mi viaje</a>'),
 ('>About Abrid</a>', '>Sobre Abrid</a>'),
 ('>Contact</a>', '>Contacto</a>'),
 ('>Chat on WhatsApp</a>', '>Chatear por WhatsApp</a>'),
 ('>Reserve</button>', '>Reservar</button>'),
 ('placeholder="Search trips, destinations, guides..."', 'placeholder="Buscar viajes, destinos, guías..."'),
 ('placeholder="Search trips, destinations, guides…"', 'placeholder="Buscar viajes, destinos, guías…"'),
 ('aria-label="Search">', 'aria-label="Búsqueda">'),
 ('aria-label="Search Abrid Morocco"', 'aria-label="Buscar en Abrid Morocco"'),
 ('>Close</button>', '>Cerrar</button>'),
 ('aria-label="Cookie consent"', 'aria-label="Consentimiento de cookies"'),
 ('We use cookies to improve your experience and analyse site traffic. Read our <a href="https://www.abridmorocco.com/cookies.html">cookie policy</a>.', 'Usamos cookies para mejorar tu experiencia y analizar el tráfico del sitio. Lee nuestra <a href="https://www.abridmorocco.com/cookies.html">política de cookies</a>.'),
 ('>Accept</button>', '>Aceptar</button>'),
 ('>Decline</button>', '>Rechazar</button>'),
 ('<h4>Booking</h4>', '<h4>Reserva</h4>'),
 ('>How Booking Works</a>', '>Cómo funciona la reserva</a>'),
 ('>Cancellation Policy</a>', '>Política de cancelación</a>'),
 ('>Terms of Service</a>', '>Términos del servicio</a>'),
 ('>Airport Transfer</a>', '>Traslado al aeropuerto</a>'),
 ('<h4>Company</h4>', '<h4>Empresa</h4>'),
 ('>About Us</a>', '>Quiénes somos</a>'),
 ('>Gallery</a>', '>Galería</a>'),
 ('<h4>Contact</h4>', '<h4>Contacto</h4>'),
 ('>Get in Touch</a>', '>Contáctanos</a>'),
 ('>Live Chat on WhatsApp</a>', '>Chat en vivo por WhatsApp</a>'),
 ('>FAQ</a>', '>Preguntas frecuentes</a>'),
 ('>Email Us</a>', '>Escríbenos</a>'),
 ('<h4>Purpose</h4>', '<h4>Nuestro propósito</h4>'),
 ('>Responsible Travel</a>', '>Viaje responsable</a>'),
 ('>Community Journey</a>', '>Viaje comunitario</a>'),
 ('>Traveller Reviews</a>', '>Opiniones de viajeros</a>'),
 ('>Leave a Google Review</a>', '>Dejar una reseña en Google</a>'),
 ('All rights reserved.', 'Todos los derechos reservados.'),
 ('>Terms</a>', '>Términos</a>'),
 ('>Privacy</a>', '>Privacidad</a>'),
 ('>Cookies</a>', '>Cookies</a>'),
 ('>Made in Morocco</span>', '>Hecho en Marruecos</span>'),
 ('aria-label="Subscribe"', 'aria-label="Suscribirse"'),
 ('aria-label="Close">✕</button>', 'aria-label="Cerrar">✕</button>'),
 ('Morocco in your inbox', 'Marruecos en tu correo'),
 ('One short letter a month — routes, seasons, secret spots. No spam, ever.', 'Una carta breve al mes: rutas, estaciones, rincones secretos. Nada de spam.'),
 ('<label for="abridName">Your name</label>', '<label for="abridName">Tu nombre</label>'),
 ('<label for="abridEmail">Email address</label>', '<label for="abridEmail">Correo electrónico</label>'),
 ("<label for=\"abridInterest\">I'm dreaming of…</label>", '<label for="abridInterest">Sueño con…</label>'),
 ('<option value="Anywhere in Morocco">Anywhere in Morocco</option>', '<option value="Anywhere in Morocco">Cualquier lugar de Marruecos</option>'),
 ('<option value="Sahara desert">Sahara desert</option>', '<option value="Sahara desert">Desierto del Sáhara</option>'),
 ('<option value="High Atlas">High Atlas</option>', '<option value="High Atlas">Alto Atlas</option>'),
 ('<option value="Imperial cities">Imperial cities</option>', '<option value="Imperial cities">Ciudades imperiales</option>'),
 ('>Subscribe free</button>', '>Suscribirme gratis</button>'),
 ('Unsubscribe anytime with one click.', 'Date de baja en un clic cuando quieras.'),
 ('<a href="https://www.abridmorocco.com/plan-my-trip.html" class="footer-contact-btn">Plan My Trip</a>', '<a href="https://www.abridmorocco.com/plan-my-trip.html" class="footer-contact-btn">Planifica mi viaje</a>'),
 ('<a class="btn btn-primary btn-sm" href="https://www.abridmorocco.com/plan-my-trip.html">Plan My Trip</a>', '<a class="btn btn-primary btn-sm" href="https://www.abridmorocco.com/plan-my-trip.html">Planifica mi viaje</a>'),
]

def mechanical(html, slug, lang):
    self_url = f"{SITE}/{lang}/{slug}"
    en_url = f"{SITE}/{slug}"
    # html lang
    html = html.replace('<html lang="en">', f'<html lang="{lang}">')
    # path fixes
    html = html.replace('href="design.css"', 'href="../design.css"')
    html = html.replace("href='design.css'", "href='../design.css'")
    html = html.replace('href="style.css"', 'href="../style.css"')
    html = html.replace('src="site.js"', 'src="../site.js"')
    html = html.replace('src="book-cart.js"', 'src="../book-cart.js"')
    html = html.replace('src="search-data.js"', 'src="../search-data.js"')
    html = html.replace('src="mini-map.js"', 'src="../mini-map.js"')
    html = re.sub(r'src="images/', 'src="../images/', html)
    html = re.sub(r'src="videos/', 'src="../videos/', html)
    # link fixes: relative .html -> absolute EN except destination-*
    def repl_link(m):
        url = m.group(1)
        if url.startswith("destination-"):
            return f'href="{url}"'
        return f'href="{SITE}/{url}"'
    html = re.sub(r'href="([A-Za-z0-9][^"#:\s]*?\.html)"', repl_link, html)
    # canonical
    html = re.sub(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{self_url}" />', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{self_url}">', html)
    # hreflang: remove existing alternate hreflang lines, insert triad after canonical
    html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*" ?/?>', '', html)
    triad = (f'\n  <link rel="alternate" hreflang="en" href="{en_url}" />'
             f'\n  <link rel="alternate" hreflang="fr" href="{SITE}/fr/{slug}" />'
             f'\n  <link rel="alternate" hreflang="es" href="{SITE}/es/{slug}" />'
             f'\n  <link rel="alternate" hreflang="x-default" href="{en_url}" />')
    html = html.replace(f'<link rel="canonical" href="{self_url}" />', f'<link rel="canonical" href="{self_url}" />' + triad, 1)
    if triad not in html:
        html = html.replace(f'<link rel="canonical" href="{self_url}">', f'<link rel="canonical" href="{self_url}"> Napoleon' + triad, 1)
    # og:url
    html = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{self_url}"', html)
    # schema TouristDestination url + Breadcrumb last item url -> self
    # TouristDestination "url"
    html = re.sub(r'"url":\s*"https://www\.abridmorocco\.com/' + re.escape(slug) + r'"', f'"url": "{self_url}"', html)
    # BreadcrumbList last item: "item":"https://...slug"
    # replace only breadcrumb item pointing to en page: pattern name + item en_url
    html = html.replace(f'"item":"{en_url}"}}]', f'"item":"{self_url}"}}]')
    # geo.placename if present
    if lang == "fr":
        html = html.replace('content="Morocco"', 'content="Maroc"')
    else:
        html = html.replace('content="Morocco"', 'content="Marruecos"')
    return html

print("mechanical ok")
