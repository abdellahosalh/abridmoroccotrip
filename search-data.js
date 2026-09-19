/* ═══════════════════════════════════════════════════════════════════
   ABRID MOROCCO — Client-side search index
   Lightweight local index of trips, destinations, experiences & guides.
   Used by the search overlay in site.js. No external libraries.
   ═══════════════════════════════════════════════════════════════════ */
window.ABRID_SEARCH = [
  /* ── Trips ── */
  { t: "Classic Morocco — The Grand Tour", c: "Trip", u: "classic-morocco.html", d: "13 days · Imperial cities, Sahara & Chefchaouen. Private guide & A/C vehicle." },
  { t: "Merzouga Desert Adventure", c: "Trip", u: "merzouga.html", d: "3 days · Sahara camp & camel trek. Transport Marrakech ↔ Merzouga." },
  { t: "Imilchil, Lakes & Summit", c: "Trip", u: "imilchil.html", d: "3 days · High Atlas adventure. Amazigh culture, mountain villages." },
  { t: "Across the High Atlas: Azilal to Rich", c: "Trip", u: "high-atlas-azilal-imilchil-rich.html", d: "5 days · Signature journey via Imilchil, lakes Isli & Tislit, Agoudal, Amouguer and Rich. Private driver & local guides." },
  { t: "Imperial Cities Circuit", c: "Trip", u: "imperial.html", d: "8 days · Fez, Marrakech, Rabat. History, medinas & monuments." },
  { t: "Marrakech Day Tour", c: "Trip", u: "marrakech.html", d: "1 day · Souks, palaces & gardens. City highlights and photography." },
  { t: "Atlas Mountains & Ourika Valley Day Trip", c: "Trip", u: "atlas.html", d: "1 day · Private 4x4, waterfalls, Berber lunch." },
  { t: "Essaouira Day Trip", c: "Trip", u: "essaouira.html", d: "1 day · Coastal medina & seafood. Atlantic breezes." },
  { t: "Hot Air Balloon over Marrakech", c: "Experience", u: "air-balloon.html", d: "Sunrise flight over the Palmeraie and Atlas foothills." },
  { t: "Ouzoud Camel Ride", c: "Experience", u: "ouzoud-camel-ride.html", d: "Atlas trails around the falls with mint tea stop." },
  { t: "Small Group Morocco Tour", c: "Trip", u: "small-group-tour.html", d: "11 days · Shared group journey through Morocco." },
  { t: "Private Custom Morocco Tour", c: "Trip", u: "private.html", d: "Tailor-made itinerary designed around the way you travel." },
  { t: "Chefchaouen Day Trip from Fes", c: "Trip", u: "chefchaouen.html", d: "1 day · Blue medina, kasbah square and Spanish Mosque viewpoint. Private transport & local guide." },
  { t: "Fes Medina Guided Day Tour", c: "Trip", u: "fes.html", d: "1 day · Tanneries, madrasas, Mellah and pottery quarter with a licensed local guide." },
  { t: "Ouzoud Waterfalls Day Trip", c: "Trip", u: "ouzoud.html", d: "1 day from Marrakech · Viewpoints, macaques and optional boat ride." },
  { t: "Zagora Desert in 2 Days", c: "Trip", u: "zagora.html", d: "2 days · Atlas pass, Ait Benhaddou, Draa Valley, camel trek and desert camp." },
  { t: "Mount Toubkal Trek", c: "Trip", u: "toubkal.html", d: "2 days · 4,167m summit with certified guide, mules and refuge night. From Marrakech." },
  { t: "Agafay Desert Evening", c: "Trip", u: "agafay.html", d: "Evening from Marrakech · Sunset, dinner in camp and stars. Back the same night." },
  { t: "6-Day Christmas Morocco Itinerary", c: "Trip", u: "6-day-christmas-morocco.html", d: "Winter adventure through Morocco's highlights." },

  /* ── Destinations ── */
  { t: "Marrakech", c: "Destination", u: "destination-marrakech.html", d: "The Red City — palaces, souks, gardens, Jemaa el-Fna and the gateway to the south." },
  { t: "Sahara Desert & Merzouga", c: "Destination", u: "destination-sahara.html", d: "Erg Chebbi dunes, camel treks, luxury desert camps and star-filled skies." },
  { t: "Chefchaouen", c: "Destination", u: "destination-chefchaouen.html", d: "The Blue Pearl — blue-washed lanes beneath the Rif Mountains." },
  { t: "Fes", c: "Destination", u: "destination-fes.html", d: "Morocco's spiritual and cultural capital — the oldest medina of the imperial cities." },
  { t: "Essaouira", c: "Destination", u: "destination-essaouira.html", d: "Coastal medina, surf, seafood and Atlantic sunsets." },
  { t: "Agadir", c: "Destination", u: "destination-agadir.html", d: "Beach resort city on Morocco's Atlantic coast — sun, surf and the Souss." },
  { t: "Atlas Mountains", c: "Destination", u: "destination-atlas.html", d: "Berber villages, trekking, Ourika Valley and the Imilchil lakes." },
  { t: "Todra & Dades Gorges", c: "Destination", u: "destination-todra-dades.html", d: "Canyons, climbing and switchback roads on the road south to the Sahara." },
  { t: "Rabat & Casablanca", c: "Destination", u: "destination-rabat-casablanca.html", d: "Imperial capital and ocean city — where Morocco trips begin." },
  { t: "Tangier", c: "Destination", u: "destination-tangier.html", d: "Ferry gateway from Spain — Hercules Caves, Cap Spartel and the kasbah." },
  { t: "Ouarzazate", c: "Destination", u: "destination-ouarzazate.html", d: "Film studios, kasbahs and the door of the desert." },
  { t: "Ait Ben Haddou", c: "Destination", u: "destination-ait-ben-haddou.html", d: "UNESCO mud-brick ksar on the former caravan route to the Sahara." },
  { t: "Casablanca & Rabat", c: "Destination", u: "imperial.html", d: "The imperial cities circuit — Casablanca's Hassan II Mosque, Rabat and Fes." },
  { t: "Ouarzazate & the South", c: "Destination", u: "destination-ait-ben-haddou.html", d: "The gateway to the Sahara, Morocco's film studios and the kasbah road." },

  /* ── Experiences ── */
  /* ── Guide articles ── */
  { t: "Chefchaouen Blue City Guide 2026", c: "Guide", u: "blog-chefchaouen.html", d: "Spanish Mosque viewpoint, Akchour waterfalls and the blue medina." },
  { t: "The Complete Guide to the Sahara Desert", c: "Guide", u: "blog-sahara-guide.html", d: "Merzouga, camel treks, luxury camps, weather and packing." },
  { t: "Driving in Morocco: Safety Guide", c: "Guide", u: "blog-driving-safety.html", d: "Road rules, tolls, fuel and mountain passes from a local driver." },
  { t: "What to Pack for the Sahara", c: "Guide", u: "blog-sahara-packing.html", d: "Essential packing list for desert travel in Morocco." },
  { t: "Top 10 Things to Do in Marrakech", c: "Guide", u: "blog-marrakech-top10.html", d: "The Red City's must-see sights, souks and experiences." },
  { t: "Imilchil: Berber Culture in the High Atlas", c: "Guide", u: "blog-imilchil.html", d: "The weekly souk, lakes and Amazigh traditions of Imilchil." },
  { t: "Agoudal: the Village That Fell From the Sky", c: "Guide", u: "blog-agoudal.html", d: "Iron meteorite, high village and Assif Melloul valley east of Imilchil." },
  { t: "Lakes Isli & Tislit: the Twin Lakes of Imilchil", c: "Guide", u: "blog-lakes-isli-tislit.html", d: "Twin lakes guide — legend, geology, walks and seasons." },
  { t: "Rich & the Upper Ziz: Where the High Atlas Ends", c: "Guide", u: "blog-rich-ziz.html", d: "Ksar history, Monday souk and the road to the Ziz Gorges." },
  { t: "Essaouira Travel Guide", c: "Guide", u: "blog-essaouira.html", d: "Coastal town guide — ramparts, beaches and seafood." },
  { t: "Essaouira: Bus vs Private Tour", c: "Guide", u: "blog-essaouira-bus-vs-tour.html", d: "Compare the options for visiting Essaouira from Marrakech." },
  { t: "Sahara Erg Chebbi Guide", c: "Guide", u: "blog-sahara-erg-chebbi.html", d: "Everything about the great dunes of Erg Chebbi at Merzouga." },
  { t: "What to Pack for the High Atlas", c: "Guide", u: "blog-high-atlas-packing.html", d: "Layers, footwear, sun, water and cash for mountain days above 2,000 metres." },
  { t: "How Much Does a Morocco Trip Cost?", c: "Guide", u: "guide-costs.html", d: "What drives the price — transport, guides, stays, season and group size." },
  { t: "Best Time to Visit Morocco", c: "Guide", u: "guide-best-time.html", d: "Seasons for the Sahara, Atlas, coast and cities, plus Ramadan timing." },
  { t: "Tipping in Morocco", c: "Guide", u: "guide-tipping.html", d: "Who to tip, when, and typical amounts for guides, drivers and restaurants." },

  /* ── Plan & contact ── */
  { t: "Itineraries & Sample Routes", c: "Guide", u: "itineraries.html", d: "Ready-made Morocco itineraries from 3 to 13 days — or build your own route. Desert escapes, imperial circuits, winter breaks." },
  { t: "Plan My Trip", c: "Plan", u: "plan-my-trip.html", d: "Send your dates, destinations and travel style — we reply with a private Morocco itinerary within 2 hours." },
  { t: "Contact Abrid Morocco", c: "Contact", u: "contact.html", d: "WhatsApp, email and office hours for Abrid Morocco. Response within 2 hours. No deposit required." },
  { t: "Traveller Reviews", c: "Trust", u: "reviews.html", d: "What travellers say about Abrid Morocco — Google reviews." },
  { t: "Responsible Travel", c: "Trust", u: "responsible-travel.html", d: "Local guides, family stays and cultural respect — our commitments." }
];