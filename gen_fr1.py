# -*- coding: utf-8 -*-
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import COMMON_FR, NAV_FR
BASE = r"C:\Users\abrid\OneDrive\Documents\Default Project\abridmoroccotrip-main"
SITE = "https://www.abridmorocco.com"

def mechanical(html, slug, lang):
    self_url = f"{SITE}/{lang}/{slug}"
    en_url = f"{SITE}/{slug}"
    html = html.replace('<html lang="en">', f'<html lang="{lang}">')
    html = html.replace('href="design.css"', 'href="../design.css"')
    html = html.replace('href="style.css"', 'href="../style.css"')
    html = html.replace('src="site.js"', 'src="../site.js"')
    html = html.replace('src="book-cart.js"', 'src="../book-cart.js"')
    html = html.replace('src="search-data.js"', 'src="../search-data.js"')
    html = html.replace('src="mini-map.js"', 'src="../mini-map.js"')
    html = re.sub(r'src="images/', 'src="../images/', html)
    html = re.sub(r'src="videos/', 'src="../videos/', html)
    def repl_link(m):
        url = m.group(1)
        if url.startswith("destination-"):
            return f'href="{url}"'
        return f'href="{SITE}/{url}"'
    html = re.sub(r'href="([A-Za-z0-9][^"#:\s]*?\.html)"', repl_link, html)
    html = re.sub(r'<link rel="canonical" href="[^"]*" ?/?>', f'<link rel="canonical" href="{self_url}" />', html)
    html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*" ?/?>', '', html)
    triad = (f'\n  <link rel="alternate" hreflang="en" href="{en_url}" />'
             f'\n  <link rel="alternate" hreflang="fr" href="{SITE}/fr/{slug}" />'
             f'\n  <link rel="alternate" hreflang="es" href="{SITE}/es/{slug}" />'
             f'\n  <link rel="alternate" hreflang="x-default" href="{en_url}" />')
    html = html.replace(f'<link rel="canonical" href="{self_url}" />', f'<link rel="canonical" href="{self_url}" />' + triad, 1)
    html = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{self_url}"', html)
    html = re.sub(r'"url":\s*"https://www\.abridmorocco\.com/' + re.escape(slug) + r'"', f'"url": "{self_url}"', html)
    html = html.replace(f'"item":"{en_url}"}}]', f'"item":"{self_url}"}}]')
    return html

def apply_pairs(html, pairs):
    for old, new in sorted(pairs, key=lambda x: -len(x[0])):
        if old and old in html:
            html = html.replace(old, new)
    return html

# ---------------- TANGIER FR ----------------
TANGIER_FR = [
 ("<title>Tangier: Gateway Between Two Continents | Abrid Morocco</title>", "<title>Tanger : Porte d\u2019entr\u00e9e entre deux continents | Abrid Morocco</title>"),
 ('content="Tangier guide: Hercules Caves, Cap Spartel, the kasbah and medina — arriving by ferry from Spain and continuing to Chefchaouen and Fes."', 'content="Guide de Tanger : grottes d\u2019Hercule, cap Spartel, kasbah et m\u00e9dina — arriv\u00e9e en ferry depuis l\u2019Espagne et continuation vers Chefchaouen et F\u00e8s."'),
 ('content="Tangier: Gateway Between Two Continents | Abrid Morocco"', 'content="Tanger : Porte d\u2019entr\u00e9e entre deux continents | Abrid Morocco"'),
 ('content="Where the Atlantic meets the Mediterranean — caves, capes and kasbahs at Morocco\'s northern door."', 'content="L\u00e0 o\u00f9 l\u2019Atlantique rencontre la M\u00e9diterran\u00e9e — grottes, caps et kasbahs \u00e0 la porte nord du Maroc."'),
 ('content="Tangier: Gateway Between Two Continents"', 'content="Tanger : Porte d\u2019entr\u00e9e entre deux continents"'),
 ('content="Hercules Caves, Cap Spartel and the old kasbah — starting Morocco in Tangier."', 'content="Grottes d\u2019Hercule, cap Spartel et vieille kasbah — commencer le Maroc \u00e0 Tanger."'),
 ('"name":"Tangier","description":"Northern Moroccan port city where the Atlantic meets the Mediterranean, arrival point for ferries from Spain."', '"name":"Tanger","description":"Ville portuaire du nord du Maroc o\u00f9 l\u2019Atlantique rencontre la M\u00e9diterran\u00e9e, point d\u2019arriv\u00e9e des ferries depuis l\u2019Espagne."'),
 ('"name":"Tangier","item":"https://www.abridmorocco.com/fr/destination-tangier.html"', '"name":"Tanger","item":"https://www.abridmorocco.com/fr/destination-tangier.html"'),
 ('"name":"Home","item":"https://www.abridmorocco.com/"},{"@type":"ListItem","position":2,"name":"Destinations"', '"name":"Accueil","item":"https://www.abridmorocco.com/"},{"@type":"ListItem","position":2,"name":"Destinations"'),
 ('<span class="eyebrow">Destination · The North</span>', '<span class="eyebrow">Destination · Le Nord</span>'),
 ('<h1>Tangier: <span class="highlight">Gateway Between Continents</span></h1>', '<h1>Tanger : <span class="highlight">Porte entre les continents</span></h1>'),
 ("<p>Where the Atlantic meets the Mediterranean — caves, capes and kasbahs at Morocco's northern door, a short sail from Spain.</p>", "<p>L\u00e0 o\u00f9 l\u2019Atlantique rencontre la M\u00e9diterran\u00e9e — grottes, caps et kasbahs \u00e0 la porte nord du Maroc, \u00e0 quelques milles de l\u2019Espagne.</p>"),
 ("<span class=\"meta-item\">⛴️ Ferry port from Spain</span>", "<span class=\"meta-item\">⛴️ Port de ferry depuis l\u2019Espagne</span>"),
 ("<span class=\"meta-item\">🕳️ Hercules Caves</span>", "<span class=\"meta-item\">🕳️ Grottes d\u2019Hercule</span>"),
 ("<span class=\"meta-item\">🏰 Kasbah &amp; medina</span>", "<span class=\"meta-item\">🏰 Kasbah et m\u00e9dina</span>"),
 ("<span class=\"meta-item\">🔵 Near Chefchaouen</span>", "<span class=\"meta-item\">🔵 Pr\u00e8s de Chefchaouen</span>"),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Africa begins here</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">L\u2019Afrique commence ici</h2>'),
 ("Most travellers meet Tangier from the sea: ferries from Tarifa and Algeciras dock at Tanger Med and Tangier Ville, and on clear days you can see two continents at once. The city has always been a meeting point — Phoenician, Roman, Portuguese, British and international-zone pasts layered into one port town.",
  "La plupart des voyageurs d\u00e9couvrent Tanger depuis la mer : les ferries de Tarifa et d\u2019Alg\u00e9siras accostent \u00e0 Tanger Med et \u00e0 Tanger Ville, et par temps clair on peut voir deux continents \u00e0 la fois. La ville a toujours \u00e9t\u00e9 un lieu de rencontre — pass\u00e9s ph\u00e9nicien, romain, portugais, britannique et de zone internationale superpos\u00e9s dans une seule ville portuaire."),
 ("The essentials fit in a day: the <strong>Caves of Hercules</strong> just west of the city, with their famous sea-shaped opening; nearby <strong>Cap Spartel</strong>, the headland where Atlantic and Mediterranean waters meet; then back into town for the <strong>kasbah</strong> — its small museum, panoramic terrace cafés — and the medina spilling down to the port.",
  "L\u2019essentiel tient en une journ\u00e9e : les <strong>grottes d\u2019Hercule</strong> juste \u00e0 l\u2019ouest de la ville, avec leur c\u00e9l\u00e8bre ouverture en forme de carte d\u2019Afrique ; le <strong>cap Spartel</strong> tout proche, le promontoire o\u00f9 se rencontrent Atlantique et M\u00e9diterran\u00e9e ; puis retour en ville pour la <strong>kasbah</strong> — son petit mus\u00e9e, ses caf\u00e9s-terrasses panoramiques — et la m\u00e9dina qui descend vers le port."),
 ("Tangier pairs naturally with", "Tanger se combine naturellement avec"),
 ("in the Rif and the road south to", "dans le Rif et la route vers le sud jusqu\u2019\u00e0"),
 (". Starting your Morocco trip here instead of Marrakech means crowds thin out and prices drop from day one — tell us your ferry arrival and we meet you at the port.",
  ". Commencer votre voyage au Maroc ici plut\u00f4t qu\u2019\u00e0 Marrakech, c\u2019est moins de foule et des prix plus doux d\u00e8s le premier jour — indiquez-nous votre arriv\u00e9e en ferry et nous vous accueillerons au port."),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Highlights</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Points forts</h2>'),
 ("<li><strong>Caves of Hercules</strong> — sea caves with the celebrated Africa-shaped opening.</li>", "<li><strong>Grottes d\u2019Hercule</strong> — grottes marines avec la c\u00e9l\u00e8bre ouverture en forme d\u2019Afrique.</li>"),
 ("<li><strong>Cap Spartel</strong> — lighthouse headland at the meeting of two seas.</li>", "<li><strong>Cap Spartel</strong> — promontoire du phare \u00e0 la rencontre des deux mers.</li>"),
 ("<li><strong>The kasbah</strong> — museum, terrace cafés and strait views.</li>", "<li><strong>La kasbah</strong> — mus\u00e9e, caf\u00e9s-terrasses et vues sur le d\u00e9troit.</li>"),
 ("<li><strong>Grand and Petit Socco</strong> — the old squares between medina and modern town.</li>", "<li><strong>Grand et Petit Socco</strong> — les vieilles places entre m\u00e9dina et ville moderne.</li>"),
 ("<li><strong>Onward to Chefchaouen</strong> — the Blue Pearl is a half-day south through the Rif.</li>", "<li><strong>Cap sur Chefchaouen</strong> — la Perle Bleue est \u00e0 une demi-journ\u00e9e au sud \u00e0 travers le Rif.</li>"),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:6px;">Where it is</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:6px;">O\u00f9 cela se trouve</h2>'),
 ("<p style=\"color:var(--text-muted);margin-bottom:14px;\">Morocco's northern tip, across the strait from Spain. Drag to explore.</p>", "<p style=\"color:var(--text-muted);margin-bottom:14px;\">La pointe nord du Maroc, face \u00e0 l\u2019Espagne de l\u2019autre c\u00f4t\u00e9 du d\u00e9troit. Faites glisser pour explorer.</p>"),
 ('aria-label="Map of Tangier"', 'aria-label="Carte de Tanger"'),
 ('<h2 class="day-title" style="font-size:1.8rem;margin-bottom:10px;">Arriving by ferry?</h2>', '<h2 class="day-title" style="font-size:1.8rem;margin-bottom:10px;">Vous arrivez en ferry ?</h2>'),
 ("<p style=\"color:var(--text-muted);max-width:640px;margin:0 auto 22px;\">Send your ferry details — we meet you at the port and your northern Morocco route starts immediately.</p>", "<p style=\"color:var(--text-muted);max-width:640px;margin:0 auto 22px;\">Envoyez-nous les d\u00e9tails de votre ferry — nous vous accueillons au port et votre itin\u00e9raire dans le nord du Maroc commence aussit\u00f4t.</p>"),
 ('>Plan My Trip</a>', '>Planifier mon voyage</a>'),
 ('>Chefchaouen Day Trip</a>', '>Excursion \u00e0 Chefchaouen</a>'),
 ("<h2>Tangier in photos</h2>", "<h2>Tanger en photos</h2>"),
 ("<p>Real shots from our routes around Tangier. All photos from the Abrid Morocco local library.</p>", "<p>Photos r\u00e9elles de nos itin\u00e9raires autour de Tanger. Toutes les photos viennent de la phototh\u00e8que locale d\u2019Abrid Morocco.</p>"),
 ('alt="Tangier Strait of Gibraltar ferry port north Morocco"', 'alt="Port de ferry du d\u00e9troit de Gibraltar \u00e0 Tanger, nord du Maroc"'),
 ('alt="Cap Spartel lighthouse where Atlantic meets Mediterranean Morocco"', 'alt="Phare du cap Spartel o\u00f9 l\u2019Atlantique rencontre la M\u00e9diterran\u00e9e, Maroc"'),
 ('alt="Caves of Hercules sea opening near Tangier Morocco"', 'alt="Ouverture marine des grottes d\u2019Hercule pr\u00e8s de Tanger, Maroc"'),
 ('alt="Tangier kasbah terrace cafes overlooking the Strait Morocco"', 'alt="Caf\u00e9s-terrasses de la kasbah de Tanger surplombant le d\u00e9troit, Maroc"'),
 ('alt="Grand Socco medina gateway in Tangier Morocco"', 'alt="Porte de la m\u00e9dina au Grand Socco \u00e0 Tanger, Maroc"'),
 ('alt="Tangier old port fishing boats at sunset Morocco"', 'alt="Bateaux de p\u00eache du vieux port de Tanger au coucher du soleil, Maroc"'),
 ('<img src="https://i.postimg.cc/C5cbTcxk/abrid-logo-transparent.png" alt="Abrid Morocco logo"', '<img src="https://i.postimg.cc/C5cbTcxk/abrid-logo-transparent.png" alt="Logo Abrid Morocco"'),
 ("A Morocco travel platform built by people who know Morocco.", "Plateforme de voyage au Maroc cr\u00e9\u00e9e par des gens qui connaissent le Maroc."),
]

# ---------------- TETOUAN FR ----------------
TETOUAN_FR = [
 ("<title>Tetouan: The White Dove of the North | Abrid Morocco</title>", "<title>T\u00e9touan : la Colombe blanche du Nord | Abrid Morocco</title>"),
 ('content="Tetouan guide: UNESCO-listed medina, Andalusian quarter and Spanish-Moroccan history between Tangier and Chefchaouen. Visit with Abrid Morocco."', 'content="Guide de T\u00e9touan : m\u00e9dina class\u00e9e UNESCO, quartier andalou et histoire hispano-marocaine entre Tanger et Chefchaouen. Visitez avec Abrid Morocco."'),
 ('content="Tetouan: The White Dove of the North | Abrid Morocco"', 'content="T\u00e9touan : la Colombe blanche du Nord | Abrid Morocco"'),
 ('content="A whitewashed UNESCO medina with Andalusian soul — between Tangier and Chefchaouen."', 'content="Une m\u00e9dina UNESCO blanchie \u00e0 la chaux \u00e0 l\u2019\u00e2me andalouse — entre Tanger et Chefchaouen."'),
 ('content="Tetouan: The White Dove of the North"', 'content="T\u00e9touan : la Colombe blanche du Nord"'),
 ('content="UNESCO medina, Andalusian heritage and the Rif foothills — visiting Tetouan."', 'content="M\u00e9dina UNESCO, h\u00e9ritage andalou et contreforts du Rif — visiter T\u00e9touan."'),
 ('"name":"Tetouan","description":"Northern Moroccan city with a UNESCO-listed medina and Andalusian heritage, between Tangier and Chefchaouen."', '"name":"T\u00e9touan","description":"Ville du nord du Maroc avec une m\u00e9dina class\u00e9e UNESCO et un h\u00e9ritage andalou, entre Tanger et Chefchaouen."'),
 ('"name":"Tetouan","item":"https://www.abridmorocco.com/fr/destination-tetouan.html"', '"name":"T\u00e9touan","item":"https://www.abridmorocco.com/fr/destination-tetouan.html"'),
 ('"name":"Home","item":"https://www.abridmorocco.com/"},{"@type":"ListItem","position":2,"name":"Destinations"', '"name":"Accueil","item":"https://www.abridmorocco.com/"},{"@type":"ListItem","position":2,"name":"Destinations"'),
 ('<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="https://www.abridmorocco.com/index.html">Home</a><span>/</span><a href="https://www.abridmorocco.com/destinations.html">Destinations</a><span>/</span><span>Tetouan</span></nav>',
  '<nav class="breadcrumbs" aria-label="Fil d\u2019Ariane"><a href="https://www.abridmorocco.com/index.html">Accueil</a><span>/</span><a href="https://www.abridmorocco.com/destinations.html">Destinations</a><span>/</span><span>T\u00e9touan</span></nav>'),
 ('aria-label="Breadcrumb"', 'aria-label="Fil d\u2019Ariane"'),
 ('<span class="eyebrow">Destination · North Morocco</span>', '<span class="eyebrow">Destination · Nord du Maroc</span>'),
 ('<h1>Tetouan: <span class="highlight">The White Dove</span></h1>', '<h1>T\u00e9touan : <span class="highlight">la Colombe blanche</span></h1>'),
 ("<p>A whitewashed UNESCO medina with Andalusian soul — Tetouan sits between Tangier and Chefchaouen, and most travellers pass it by. Don't.</p>",
  "<p>Une m\u00e9dina UNESCO blanchie \u00e0 la chaux \u00e0 l\u2019\u00e2me andalouse — T\u00e9touan se trouve entre Tanger et Chefchaouen, et la plupart des voyageurs passent sans s\u2019arr\u00eater. Ne faites pas cette erreur.</p>"),
 ("<span class=\"meta-item\">🏛️ UNESCO medina</span>", "<span class=\"meta-item\">🏛️ M\u00e9dina UNESCO</span>"),
 ("<span class=\"meta-item\">🎭 Andalusian heritage</span>", "<span class=\"meta-item\">🎭 H\u00e9ritage andalou</span>"),
 ("<span class=\"meta-item\">⛰️ Rif foothills</span>", "<span class=\"meta-item\">⛰️ Contreforts du Rif</span>"),
 ("<span class=\"meta-item\">🔵 Near Chefchaouen</span>", "<span class=\"meta-item\">🔵 Pr\u00e8s de Chefchaouen</span>"),
 ('alt="Painted lanes in a northern Moroccan medina"', 'alt="Ruelles peintes d\u2019une m\u00e9dina du nord du Maroc"'),
 ('alt="Blue doors and lanes in a northern Moroccan medina"', 'alt="Portes bleues et ruelles d\u2019une m\u00e9dina du nord du Maroc"'),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">The medina nobody crowds</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">La m\u00e9dina sans la foule</h2>'),
 ("Rebuilt by Andalusian refugees and later capital of the Spanish protectorate, Tetouan carries a Spanish-Moroccan character found nowhere else in the country. Its medina — listed by UNESCO — is considered one of the most complete and least altered in Morocco, and you will often have its lanes almost to yourself.",
  "Reconstruite par des r\u00e9fugi\u00e9s andalous puis capitale du protectorat espagnol, T\u00e9touan poss\u00e8de un caract\u00e8re hispano-marocain unique dans le pays. Sa m\u00e9dina — class\u00e9e \u00e0 l\u2019UNESCO — est consid\u00e9r\u00e9e comme l\u2019une des plus compl\u00e8tes et des moins d\u00e9natur\u00e9es du Maroc, et vous aurez souvent ses ruelles presque pour vous seul."),
 ("Tetouan works best as part of a northern loop:", "T\u00e9touan s\u2019appr\u00e9cie id\u00e9alement dans une boucle du nord :"),
 ("for arrival, Tetouan for the medina morning, then up into the Rif to", "pour l\u2019arriv\u00e9e, T\u00e9touan pour la matin\u00e9e dans la m\u00e9dina, puis mont\u00e9e dans le Rif jusqu\u2019\u00e0"),
 (". Tell us your ferry or flight arrival and we sequence the north around it.", ". Indiquez-nous votre arriv\u00e9e en ferry ou en avion et nous organiserons le nord en cons\u00e9quence."),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Highlights</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Points forts</h2>'),
 ("<li><strong>UNESCO medina</strong> — whitewashed lanes, seven gates and artisan quarters.</li>", "<li><strong>M\u00e9dina UNESCO</strong> — ruelles blanchies \u00e0 la chaux, sept portes et quartiers d\u2019artisans.</li>"),
 ("<li><strong>Place Hassan II (El Feddan)</strong> — the grand square facing the Royal Palace.</li>", "<li><strong>Place Hassan II (El Feddan)</strong> — la grande place face au Palais royal.</li>"),
 ("<li><strong>Archaeological Museum</strong> — Roman mosaics from Lixus and Volubilis.</li>", "<li><strong>Mus\u00e9e arch\u00e9ologique</strong> — mosa\u00efques romaines de Lixus et Volubilis.</li>"),
 ("<li><strong>Andalusian crafts</strong> — zellige tilework, embroidery and painted wood.</li>", "<li><strong>Artisanat andalou</strong> — zellige, broderie et bois peint.</li>"),
 ("<li><strong>Martil beach</strong> — the town beach, minutes from the medina.</li>", "<li><strong>Plage de Martil</strong> — la plage de la ville, \u00e0 quelques minutes de la m\u00e9dina.</li>"),
 ("<strong>How we recommend experiencing Tetouan.</strong> Arrive mid-morning from Tangier, walk the medina with a local guide, visit the museum, lunch in the new town — then continue to Chefchaouen for sunset. Travellers often miss the museum; don't. <strong>How long:</strong> half a day is enough, a full day with the beach. <strong>How we connect it:</strong> Tangier → Tetouan → Chefchaouen →",
  "<strong>Notre fa\u00e7on recommand\u00e9e de d\u00e9couvrir T\u00e9touan.</strong> Arriv\u00e9e en milieu de matin\u00e9e depuis Tanger, visite de la m\u00e9dina avec un guide local, mus\u00e9e, d\u00e9jeuner en ville nouvelle — puis continuation vers Chefchaouen pour le coucher du soleil. Les voyageurs ratent souvent le mus\u00e9e ; ne le manquez pas. <strong>Dur\u00e9e :</strong> une demi-journ\u00e9e suffit, une journ\u00e9e compl\u00e8te avec la plage. <strong>Notre liaison :</strong> Tanger → T\u00e9touan → Chefchaouen →"),
 ("is our classic northern route.", "est notre itin\u00e9raire classique du nord."),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Good to know</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Bon \u00e0 savoir</h2>'),
 ('<h3 style="font-weight:500;font-size:1.1rem;margin:0 0 6px;">How to get there</h3>', '<h3 style="font-weight:500;font-size:1.1rem;margin:0 0 6px;">Comment y aller</h3>'),
 ("Tetouan has no train station — it is reached by road. Expect about an hour from Tangier and a similar drive from Chefchaouen by grand taxi or bus; the nearest airports are Tangier and Fes. With Abrid, your driver meets you and the route simply flows through.",
  "T\u00e9touan n\u2019a pas de gare — on y acc\u00e8de par la route. Comptez environ une heure depuis Tanger et un trajet similaire depuis Chefchaouen en grand taxi ou en bus ; les a\u00e9roports les plus proches sont Tanger et F\u00e8s. Avec Abrid, votre chauffeur vous accueille et l\u2019itin\u00e9raire se d\u00e9roule simplement."),
 ('<h3 style="font-weight:500;font-size:1.1rem;margin:18px 0 6px;">How long to stay</h3>', '<h3 style="font-weight:500;font-size:1.1rem;margin:18px 0 6px;">Combien de temps rester</h3>'),
 ("We recommend half a day for the medina and museum, a full day if you want the beach too. Most travellers sleep in Tangier or Chefchaouen.",
  "Nous recommandons une demi-journ\u00e9e pour la m\u00e9dina et le mus\u00e9e, une journ\u00e9e compl\u00e8te si vous voulez aussi la plage. La plupart des voyageurs dorment \u00e0 Tanger ou \u00e0 Chefchaouen."),
 ('<h3 style="font-weight:500;font-size:1.1rem;margin:18px 0 6px;">Best time to visit</h3>', '<h3 style="font-weight:500;font-size:1.1rem;margin:18px 0 6px;">Meilleure p\u00e9riode</h3>'),
 ("Spring (March–May) and autumn (September–November) are generally the most pleasant. Summer works well here thanks to the northern breeze.",
  "Le printemps (mars–mai) et l\u2019automne (septembre–novembre) sont g\u00e9n\u00e9ralement les plus agr\u00e9ables. L\u2019\u00e9t\u00e9 convient bien ici gr\u00e2ce \u00e0 la brise du nord."),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:6px;">Best areas to visit in Tetouan</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:6px;">Meilleurs quartiers \u00e0 visiter \u00e0 T\u00e9touan</h2>'),
 ("<p style=\"color:var(--text-muted);margin-bottom:14px;\">Three pockets cover the city — medina, Spanish quarter and sea.</p>", "<p style=\"color:var(--text-muted);margin-bottom:14px;\">Trois poches couvrent la ville — m\u00e9dina, quartier espagnol et mer.</p>"),
 ("<span class=\"discover-src\">UNESCO MEDINA</span><h4>Old lanes &amp; gates</h4><p>Whitewashed alleys, seven gates and artisan quarters — the essential walk.</p>",
  "<span class=\"discover-src\">M\u00c9DINA UNESCO</span><h4>Vieilles ruelles et portes</h4><p>Ruelles blanchies \u00e0 la chaux, sept portes et quartiers d\u2019artisans — la promenade essentielle.</p>"),
 ("<span class=\"discover-src\">SPANISH QUARTER</span><h4>Feddan &amp; Ensanche</h4><p>Grand square, Royal Palace exterior and café-lined avenues.</p>",
  "<span class=\"discover-src\">QUARTIER ESPAGNOL</span><h4>Feddan et Ensanche</h4><p>Grande place, ext\u00e9rieur du Palais royal et avenues bord\u00e9es de caf\u00e9s.</p>"),
 ("<span class=\"discover-src\">COAST</span><h4>Martil beach</h4><p>Town beach minutes away for a sea breather after the medina.</p>",
  "<span class=\"discover-src\">C\u00d4TE</span><h4>Plage de Martil</h4><p>Plage de la ville \u00e0 quelques minutes pour respirer la mer apr\u00e8s la m\u00e9dina.</p>"),
 ('aria-label="Map of Tetouan areas"', 'aria-label="Carte des quartiers de T\u00e9touan"'),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Trips visiting Tetouan</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Circuits passant par T\u00e9touan</h2>'),
 ("<div class=\"dest-tour\"><h3>Private Custom Trips</h3><p>Northern Morocco built around you — Tangier, Tetouan, Chefchaouen and beyond.</p>", "<div class=\"dest-tour\"><h3>Circuits priv\u00e9s sur mesure</h3><p>Le nord du Maroc construit autour de vous — Tanger, T\u00e9touan, Chefchaouen et au-del\u00e0.</p>"),
 ('>View tour</a>', '>Voir le circuit</a>'),
 ("No fixed Tetouan trip yet?", "Pas encore de circuit fixe \u00e0 T\u00e9touan ?"),
 ("and we build it into a northern route.", "et nous l\u2019int\u00e9grerons \u00e0 un itin\u00e9raire du nord."),
 ('>Tell us your dates</a>', '>Indiquez-nous vos dates</a>'),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Morocco guides</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Guides du Maroc</h2>'),
 ("<a class=\"related-card\" href=\"https://www.abridmorocco.com/guide-destinations.html\"><h3>Destinations Guide</h3><p>Marrakech to Chefchaouen →</p></a>", "<a class=\"related-card\" href=\"https://www.abridmorocco.com/guide-destinations.html\"><h3>Guide des destinations</h3><p>De Marrakech \u00e0 Chefchaouen →</p></a>"),
 ("<a class=\"related-card\" href=\"https://www.abridmorocco.com/guide-best-time.html\"><h3>Best Time to Visit</h3><p>Seasons by region →</p></a>", "<a class=\"related-card\" href=\"https://www.abridmorocco.com/guide-best-time.html\"><h3>Meilleure p\u00e9riode</h3><p>Les saisons par r\u00e9gion →</p></a>"),
 ("<a class=\"related-card\" href=\"https://www.abridmorocco.com/guide-transport.html\"><h3>Transport Guide</h3><p>Trains, buses &amp; cars →</p></a>", "<a class=\"related-card\" href=\"https://www.abridmorocco.com/guide-transport.html\"><h3>Guide des transports</h3><p>Trains, bus et voitures →</p></a>"),
 ("<a class=\"related-card\" href=\"https://www.abridmorocco.com/blog-chefchaouen.html\"><h3>Chefchaouen Guide</h3><p>The Blue Pearl →</p></a>", "<a class=\"related-card\" href=\"https://www.abridmorocco.com/blog-chefchaouen.html\"><h3>Guide de Chefchaouen</h3><p>La Perle Bleue →</p></a>"),
 ('<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Tetouan questions</h2>', '<h2 class="day-title" style="font-size:1.6rem;margin-bottom:14px;">Questions sur T\u00e9touan</h2>'),
 ("<summary>Is Tetouan worth visiting?</summary><p>Yes if you are passing through the north — its UNESCO medina is among Morocco's best preserved and far less crowded than Fes or Marrakech. As a half-day stop between Tangier and Chefchaouen it is excellent.</p>",
  "<summary>T\u00e9touan vaut-elle la visite ?</summary><p>Oui si vous traversez le nord — sa m\u00e9dina UNESCO compte parmi les mieux pr\u00e9serv\u00e9es du Maroc et est bien moins fr\u00e9quent\u00e9e que F\u00e8s ou Marrakech. En escale d\u2019une demi-journ\u00e9e entre Tanger et Chefchaouen, elle est excellente.</p>"),
 ("<summary>How do I combine Tetouan with Chefchaouen?</summary><p>Easily: the two are about an hour apart by road. Our classic northern route runs Tangier → Tetouan → Chefchaouen → Fes.",
  "<summary>Comment combiner T\u00e9touan avec Chefchaouen ?</summary><p>Facilement : les deux sont \u00e0 environ une heure de route. Notre itin\u00e9raire classique du nord relie Tanger → T\u00e9touan → Chefchaouen → F\u00e8s."),
 ('>Plan it with us</a>.', '>Planifiez-le avec nous</a>.'),
 ("<summary>Can I get there by train?</summary><p>No — Tetouan has no train station. You arrive by road from Tangier, Chefchaouen or Fes. With Abrid, private transport is already part of your itinerary.</p>",
  "<summary>Puis-je y aller en train ?</summary><p>Non — T\u00e9touan n\u2019a pas de gare. On y arrive par la route depuis Tanger, Chefchaouen ou F\u00e8s. Avec Abrid, le transport priv\u00e9 fait d\u00e9j\u00e0 partie de votre itin\u00e9raire.</p>"),
 ("<h2>Tetouan in photos</h2>", "<h2>T\u00e9touan en photos</h2>"),
 ("<p>Real shots from our routes around Tetouan. All photos from the Abrid Morocco local library.</p>", "<p>Photos r\u00e9elles de nos itin\u00e9raires autour de T\u00e9touan. Toutes les photos viennent de la phototh\u00e8que locale d\u2019Abrid Morocco.</p>"),
 ('alt="Tetouan UNESCO whitewashed medina lanes north Morocco"', 'alt="Ruelles blanchies de la m\u00e9dina UNESCO de T\u00e9touan, nord du Maroc"'),
 ('alt="Place Hassan II Feddan square Royal Palace Tetouan Morocco"', 'alt="Place Hassan II, square du Feddan et Palais royal de T\u00e9touan, Maroc"'),
 ('alt="Andalusian zellige tilework artisan quarter Tetouan Morocco"', 'alt="Zellige andalou du quartier des artisans de T\u00e9touan, Maroc"'),
 ('alt="Tetouan medina historic seven gates old walls Morocco"', 'alt="Sept portes historiques et vieux remparts de la m\u00e9dina de T\u00e9touan, Maroc"'),
 ('alt="Archaeological Museum Roman mosaics Tetouan Morocco"', 'alt="Mosa\u00efques romaines du mus\u00e9e arch\u00e9ologique de T\u00e9touan, Maroc"'),
 ('alt="Spanish quarter Ensanche avenues Tetouan Morocco"', 'alt="Avenues du quartier espagnol Ensanche de T\u00e9touan, Maroc"'),
 ('alt="Martil beach coastline near Tetouan Morocco"', 'alt="Littoral de la plage de Martil pr\u00e8s de T\u00e9touan, Maroc"'),
 ('alt="Rif foothills panorama over Tetouan Morocco"', 'alt="Panorama des contreforts du Rif sur T\u00e9touan, Maroc"'),
 ("<h2>Want to include Tetouan in your Morocco trip?</h2>", "<h2>Envie d\u2019inclure T\u00e9touan dans votre voyage au Maroc ?</h2>"),
 ("<p>Tell us your dates and interests — we fit Tetouan into a northern Morocco route with transport, stays and guides handled.</p>", "<p>Indiquez-nous vos dates et vos envies — nous int\u00e9grerons T\u00e9touan \u00e0 un itin\u00e9raire du nord du Maroc avec transport, h\u00e9bergements et guides pris en charge.</p>"),
 ('>Plan My Morocco Trip</a>', '>Planifier mon voyage au Maroc</a>'),
 ('>Explore Trips</a>', '>Explorer les circuits</a>'),
 ('<img src="https://i.postimg.cc/C5cbTcxk/abrid-logo-transparent.png" alt="Abrid Morocco logo"', '<img src="https://i.postimg.cc/C5cbTcxk/abrid-logo-transparent.png" alt="Logo Abrid Morocco"'),
]
