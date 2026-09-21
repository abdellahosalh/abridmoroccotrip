# -*- coding: utf-8 -*-
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_common import COMMON_FR, NAV_FR, COMMON_ES, NAV_ES
from gen_fr1 import mechanical, apply_pairs, TANGIER_FR, TETOUAN_FR
from gen_fr2 import ASILAH_FR, CHEF_FR, MARRA_FR
from gen_es1 import TANGIER_ES, TETOUAN_ES
from gen_es2 import ASILAH_ES, CHEF_ES, MARRA_ES

BASE = r"C:\Users\abrid\OneDrive\Documents\Default Project\abridmoroccotrip-main"
SITE = "https://www.abridmorocco.com"

EXTRA_FR = [
 ("A Morocco travel platform built by people who know Morocco. Sahara, Atlas, Imperial Cities - private guides and characterful stays since 2022.",
  "Plateforme de voyage au Maroc cr\u00e9\u00e9e par des gens qui connaissent le Maroc. Sahara, Atlas, Cit\u00e9s imp\u00e9riales \u2014 guides priv\u00e9s et h\u00e9bergements de caract\u00e8re depuis 2022."),
 ("A Morocco travel platform built by people who know Morocco. Sahara, Atlas, Imperial Cities \u2014 private guides and characterful stays since 2022.",
  "Plateforme de voyage au Maroc cr\u00e9\u00e9e par des gens qui connaissent le Maroc. Sahara, Atlas, Cit\u00e9s imp\u00e9riales \u2014 guides priv\u00e9s et h\u00e9bergements de caract\u00e8re depuis 2022."),
 ('>Plan My Trip</a>', '>Planifier mon voyage</a>'),
 ('"name": "Morocco"}', '"name": "Maroc"}'),
 ('"touristType": "Morocco traveller"', '"touristType": "Voyageur au Maroc"'),
 ('>Fes</a>', '>F\u00e8s</a>'),
 ('>Tangier</a>', '>Tanger</a>'),
 ('>Rabat and Casablanca</a>', '>Rabat et Casablanca</a>'),
 ('</a> and <a href="destination-rabat-casablanca.html"', '</a> et <a href="destination-rabat-casablanca.html"'),
 ('"isPartOf": {"@type": "Country", "name": "Morocco"}', '"isPartOf": {"@type": "Country", "name": "Maroc"}'),
]
EXTRA_ES = [
 ("A Morocco travel platform built by people who know Morocco. Sahara, Atlas, Imperial Cities - private guides and characterful stays since 2022.",
  "Plataforma de viajes por Marruecos creada por quienes conocen Marruecos. S\u00e1hara, Atlas, Ciudades Imperiales: gu\u00edas privados y alojamientos con encanto desde 2022."),
 ("A Morocco travel platform built by people who know Morocco. Sahara, Atlas, Imperial Cities \u2014 private guides and characterful stays since 2022.",
  "Plataforma de viajes por Marruecos creada por quienes conocen Marruecos. S\u00e1hara, Atlas, Ciudades Imperiales: gu\u00edas privados y alojamientos con encanto desde 2022."),
 ('>Plan My Trip</a>', '>Planifica mi viaje</a>'),
 ('"name": "Morocco"}', '"name": "Marruecos"}'),
 ('"touristType": "Morocco traveller"', '"touristType": "Viajero por Marruecos"'),
 ('>Fes</a>', '>Fez</a>'),
 ('>Tangier</a>', '>T\u00e1nger</a>'),
 ('>Rabat and Casablanca</a>', '>Rabat y Casablanca</a>'),
 ('</a> and <a href="destination-rabat-casablanca.html"', '</a> y <a href="destination-rabat-casablanca.html"'),
 ('"isPartOf": {"@type": "Country", "name": "Morocco"}', '"isPartOf": {"@type": "Country", "name": "Marruecos"}'),
]

PAGES = {
 "destination-tangier.html": (TANGIER_FR, TANGIER_ES),
 "destination-tetouan.html": (TETOUAN_FR, TETOUAN_ES),
 "destination-asilah.html": (ASILAH_FR, ASILAH_ES),
 "destination-chefchaouen.html": (CHEF_FR, CHEF_ES),
 "destination-marrakech.html": (MARRA_FR, MARRA_ES),
}

os.makedirs(os.path.join(BASE, "fr"), exist_ok=True)
os.makedirs(os.path.join(BASE, "es"), exist_ok=True)

report = []
for slug, (fr_pairs, es_pairs) in PAGES.items():
    with open(os.path.join(BASE, slug), encoding="utf-8") as f:
        en = f.read()
    en_imgs = len(re.findall(r'images/photos/', en))
    for lang, pairs, common, nav, extra in (("fr", fr_pairs, COMMON_FR, NAV_FR, EXTRA_FR),
                                            ("es", es_pairs, COMMON_ES, NAV_ES, EXTRA_ES)):
        html = mechanical(en, slug, lang)
        html = apply_pairs(html, nav + common + pairs + extra)
        outdir = os.path.join(BASE, lang)
        with open(os.path.join(outdir, slug), "w", encoding="utf-8") as f:
            f.write(html)
        # verify
        opens = len(re.findall(r"<div[\s>]", html))
        closes = html.count("</div>")
        balanced = (opens == closes)
        self_url = f"{SITE}/{lang}/{slug}"
        en_url = f"{SITE}/{slug}"
        checks = {
            "lang": f'<html lang="{lang}">' in html,
            "canonical": f'<link rel="canonical" href="{self_url}" />' in html,
            "hreflang_en": f'hreflang="en" href="{en_url}"' in html,
            "hreflang_fr": f'hreflang="fr" href="{SITE}/fr/{slug}"' in html,
            "hreflang_es": f'hreflang="es" href="{SITE}/es/{slug}"' in html,
            "xdefault": f'hreflang="x-default" href="{en_url}"' in html,
            "ogurl": f'<meta property="og:url" content="{self_url}"' in html,
            "css": 'href="../design.css"' in html,
            "js": 'src="../site.js"' in html or 'src="../mini-map.js"' in html,
        }
        imgs = len(re.findall(r'\.\./images/photos/', html))
        leftover_morocco = html.count("Morocco") - html.count("Abrid Morocco")
        leftover_moroccan = len(re.findall(r"Moroccan", html))
        # relative destination links still relative?
        rel_dest = len(re.findall(r'href="destination-[^"]+\.html"', html))
        abs_other = len(re.findall(r'href="https://www\.abridmorocco\.com/[a-z0-9\-]+\.html"', html))
        report.append((lang, slug, opens, closes, balanced, checks, en_imgs, imgs, rel_dest, abs_other, leftover_morocco, leftover_moroccan))

for (lang, slug, opens, closes, balanced, checks, en_imgs, imgs, rel_dest, abs_other, lo_m, lo_mn) in report:
    bad = [k for k, v in checks.items() if not v]
    print(f"{lang}/{slug}: div {opens}/{closes} balanced={balanced} imgs EN={en_imgs} OUT={imgs} relDest={rel_dest} absOther={abs_other} leftoverMorocco={lo_m} leftoverMoroccan={lo_mn} bad={bad}")
print("DONE")
