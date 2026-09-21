/* ═══════════════════════════════════════════════════════════════════
   ABRID MOROCCO — Shared tour reservation cart
   On any tour page listed in TOURS below, a floating "Reserve" button
   opens a cart modal. On submit it builds a reservation PDF (tour
   picture + details + thank-you letter) and emails everything — cart,
   letter and PDF — straight to the owner for a personal reply.
   No per-page configuration needed: the tour is detected from the URL.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  var OWNER_EMAIL = "abdeosalh@gmail.com";
  var WA_NUMBER = "212762934488";
  var LANG = (document.documentElement.getAttribute("lang") || "en").slice(0, 2).toLowerCase();
  function T(en, fr, es) { return LANG === "fr" ? fr : (LANG === "es" ? es : en); }
  var FR = LANG === "fr";
  var ES = LANG === "es";

  var TOURS = {
    "marrakech.html": { name: "Marrakech Day Tour", dur: "1 Day", img: "https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=600&auto=format&fit=crop", price: "€50 pp" },
    "atlas.html": { name: "Atlas Mountains & Ourika Valley", dur: "1 Day", img: "https://i.postimg.cc/NfvKF7Rj/vincenzo-montagna-pd-Z9t-Nbpztw-unsplash.jpg", price: "€100 pp" },
    "essaouira.html": { name: "Essaouira Day Trip", dur: "1 Day", img: "https://images.unsplash.com/photo-1613057157282-cc3cbe630b26?w=600&auto=format&fit=crop", price: "€150 pp" },
    "air-balloon.html": { name: "Hot Air Balloon over Marrakech", dur: "Half Day", img: "https://i.postimg.cc/fRhRWzns/1788783065964.jpg", price: "€150 pp" },
    "ouzoud-camel-ride.html": { name: "Ouzoud Camel Ride", dur: "Half Day", img: "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?w=600&auto=format&fit=crop", price: "Quote on request" },
    "merzouga.html": { name: "Merzouga Desert Adventure", dur: "3 Days", img: "https://images.unsplash.com/photo-1593350058052-cc6636c9facd?w=600&auto=format&fit=crop", price: "€180 pp" },
    "imilchil.html": { name: "Imilchil, Lakes & Summit", dur: "3 Days", img: "https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=600&auto=format&fit=crop/YNqJlL3B9gIRgqnp/untitled-2-3-AoPepbZODoTZZDk2.jpg", price: "€1,500 pp" },
    "chefchaouen.html": { name: "Chefchaouen Day Trip", dur: "Day Trip", img: "https://i.postimg.cc/vTjVBp7p/Untitled-design.jpg", price: "€200 pp" },
    "fes.html": { name: "Fes Medina Guided Tour", dur: "Day Tour", img: "https://images.unsplash.com/photo-1512958789358-4effcbe171a0?w=600&auto=format&fit=crop", price: "€50 pp" },
    "ouzoud.html": { name: "Ouzoud Waterfalls", dur: "Day Trip", img: "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?w=600&auto=format&fit=crop", price: "€150 pp" },
    "zagora.html": { name: "Zagora Desert Express", dur: "2 Days", img: "https://images.unsplash.com/photo-1593350058052-cc6636c9facd?w=600&auto=format&fit=crop", price: "€1,000 pp" },
    "toubkal.html": { name: "Mount Toubkal Trek", dur: "2 Days", img: "images/toubkal/toubkal-massif.jpg", price: "€700 pp" },
    "agafay.html": { name: "Agafay Desert Evening", dur: "Evening", img: "images/agafay/agafay-camp.jpg", price: "€200 pp" },
    "high-atlas-azilal-imilchil-rich.html": { name: "Across the High Atlas", dur: "5 Days", img: "images/high-atlas/imilchil/imilchil-01.jpg", price: "€3,000 pp" },
    "imperial.html": { name: "Imperial Cities Circuit", dur: "8 Days", img: "https://images.unsplash.com/photo-1559925523-10de9e23cf90?w=600&auto=format&fit=crop", price: "€3,000 pp" },
    "6-day-christmas-morocco.html": { name: "6-Day Morocco Christmas Itinerary", dur: "6 Days", img: "https://i.postimg.cc/vTjVBp7p/Untitled-design.jpg", price: "€2,500 pp" },
    "classic-morocco.html": { name: "Classic Morocco Grand Tour", dur: "13 Days", img: "https://images.unsplash.com/photo-1512958789358-4effcbe171a0?w=600&auto=format&fit=crop", price: "€3,000 pp" },
    "small-group-tour.html": { name: "Small Group Morocco Tour", dur: "11 Days", img: "https://images.unsplash.com/photo-1506869640319-fe1a24fd76dc?w=600&auto=format&fit=crop", price: "€2,000 pp" },
    "private.html": { name: "Private Custom Morocco Tour", dur: "Any Length", img: "https://images.unsplash.com/photo-1526994387180-9557a434b046?w=600&auto=format&fit=crop", price: "€1,200 pp" }
  };

  var file = (location.pathname.split("/").pop() || "index.html").split("?")[0].toLowerCase();
  var tour = TOURS[file] || TOURS["private.html"];
  if (!tour) return;
  var currentTour = tour;

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function absUrl(u) {
    if (/^https?:/i.test(u)) return u;
    var a = document.createElement("a");
    a.href = u;
    return a.href;
  }

  /* Floating reserve button */
  var fab = document.createElement("button");
  fab.type = "button";
  fab.className = "cart-fab";
  fab.id = "cartFab";
  fab.setAttribute("aria-label", T("Reserve this tour", "Réserver ce circuit", "Reservar este viaje"));
  fab.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg><span>' + T("Reserve", "Réserver", "Reservar") + '</span>';
  document.body.appendChild(fab);

  /* Modal */
  var overlay = document.createElement("div");
  overlay.className = "cart-overlay";
  overlay.id = "cartOverlay";
  overlay.setAttribute("hidden", "");
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", T("Reserve this tour", "Réserver ce circuit"));
  var today = new Date().toISOString().slice(0, 10);
  overlay.innerHTML =
    '<div class="cart-box">' +
    '<button type="button" class="cart-close" id="cartClose" aria-label="' + T("Close", "Fermer", "Cerrar") + '">✕</button>' +
    '<div class="cart-tour"><img id="cartThumb" src="" alt="" loading="lazy">' +
    '<div><strong id="cartTourName"></strong><span id="cartTourMeta"></span></div></div>' +
    '<div id="cartFormWrap">' +
    '<form id="cartForm">' +
    '<div class="cart-grid">' +
    '<div><label for="cartName">' + T("Full name", "Nom complet", "Nombre completo") + '</label><input id="cartName" name="name" required autocomplete="name" placeholder="' + T("Sara", "Sara") + '"></div>' +
    '<div><label for="cartEmail">' + T("Email", "E-mail", "Correo electrónico") + '</label><input id="cartEmail" name="email" type="email" required autocomplete="email" placeholder="' + T("you@example.com", "vous@exemple.com", "tu@ejemplo.com") + '"></div>' +
    '<div><label for="cartPhone">' + T("Phone / WhatsApp", "Téléphone / WhatsApp", "Teléfono / WhatsApp") + '</label><input id="cartPhone" name="phone" autocomplete="tel" placeholder="+33 …"></div>' +
    '<div><label for="cartDate">' + T("Preferred date", "Date souhaitée", "Fecha preferida") + '</label><input id="cartDate" name="date" type="date" min="' + today + '" required></div>' +
    '<div><label for="cartPax">' + T("Travelers", "Voyageurs", "Viajeros") + '</label><input id="cartPax" name="travelers" type="number" min="1" max="30" value="2" required></div>' +
    '<div><label for="cartMsg">' + T("Anything we should know?", "Précisions ?", "¿Algo que debamos saber?") + '</label><input id="cartMsg" name="requests" placeholder="' + T("Hotel, diet, pace…", "Hôtel, régime, rythme…", "Hotel, dieta, ritmo…") + '"></div>' +
    '</div>' +
    '<button type="submit" class="btn btn-primary" id="cartSubmit" style="width:100%;">' + T("Send reservation →", "Envoyer la réservation →", "Enviar reserva →") + '</button>' +
    '<p class="fine">' + T("No payment now — Abdellah or Karim replies personally within 2 hours.", "Aucun paiement maintenant — Abdellah ou Karim répond personnellement sous 2 heures.", "Sin pago ahora — Abdellah o Karim responde personalmente en 2 horas.") + '</p>' +
    '<p class="fine"><a href="plan-my-trip.html" style="color:var(--terracotta,#E4002B);font-weight:700;">' + T("Prefer a fully custom trip? Plan it here →", "Un voyage sur mesure ? Planifiez ici →", "¿Un viaje a medida? Planifícalo aquí →") + '</a></p>' +
    '</form></div></div>';
  document.body.appendChild(overlay);

  function open() { overlay.removeAttribute("hidden"); document.body.style.overflow = "hidden"; }
  function close() { overlay.setAttribute("hidden", ""); document.body.style.overflow = ""; }
  function setTour(key) {
    var t = TOURS[key] || TOURS["private.html"] || tour;
    currentTour = t;
    document.getElementById("cartThumb").src = t.img;
    document.getElementById("cartTourName").textContent = t.name;
    document.getElementById("cartTourMeta").textContent = t.dur + " · " + (t.price || "Quote on request");
    overlay.setAttribute("aria-label", T("Reserve ", "Réserver ", "Reservar ") + t.name);
  }
  setTour(file in TOURS ? file : "private.html");
  fab.addEventListener("click", function () { setTour(file in TOURS ? file : "private.html"); open(); });
  document.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-reserve-tour]") : null;
    if (!b) return;
    e.preventDefault();
    setTour(b.getAttribute("data-reserve-tour"));
    open();
  });
  overlay.querySelector("#cartClose").addEventListener("click", close);
  overlay.addEventListener("click", function (e) { if (e.target === overlay) close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !overlay.hasAttribute("hidden")) close(); });

  /* Inline "Reserve" buttons (data-open-cart) replace the floating pill where present */
  function refreshPill() {
    var inlineVisible = document.querySelectorAll("[data-open-cart]");
    var anyVisible = false;
    inlineVisible.forEach(function (b) { if (b.offsetParent !== null) anyVisible = true; });
    fab.style.display = anyVisible ? "none" : "";
  }
  refreshPill();
  var rT = false;
  window.addEventListener("resize", function () {
    if (!rT) { rT = true; setTimeout(function () { refreshPill(); rT = false; }, 250); }
  });
  document.querySelectorAll("[data-open-cart]").forEach(function (b) { b.addEventListener("click", open); });

  function loadImageData(url) {
    return fetch(absUrl(url), { mode: "cors" }).then(function (r) {
      if (!r.ok) throw new Error("img " + r.status);
      return r.blob();
    }).then(function (blob) {
      return new Promise(function (res, rej) {
        var fr = new FileReader();
        fr.onload = function () { res({ dataUrl: fr.result, type: blob.type }); };
        fr.onerror = rej;
        fr.readAsDataURL(blob);
      });
    });
  }

  function buildPdf(img) {
    var NS = window.jspdf;
    var doc = new NS.jsPDF({ unit: "mm", format: "a4" });
    var W = 210, y = 0;
    doc.setFillColor(228, 0, 43);
    doc.rect(0, 0, W, 34, "F");
    doc.setTextColor(255, 255, 255);
    doc.setFont("helvetica", "bold");
    doc.setFontSize(20);
    doc.text("Abrid Morocco", 14, 14);
    doc.setFontSize(12);
    doc.setFont("helvetica", "normal");
    doc.text("Tour reservation", 14, 23);
    y = 44;
    if (img && img.dataUrl) {
      try {
        var fmt = img.type.indexOf("png") !== -1 ? "PNG" : "JPEG";
        doc.addImage(img.dataUrl, fmt, 14, y, 60, 40);
      } catch (e) { /* picture optional in PDF */ }
    }
    var ref = "ABR-" + Date.now().toString().slice(-6);
    doc.setTextColor(20, 20, 20);
    doc.setFontSize(16);
    doc.setFont("helvetica", "bold");
    var tx = (img && img.dataUrl) ? 80 : 14;
    var title = doc.splitTextToSize(currentTour.name, W - tx - 14);
    doc.text(title, tx, y + 8);
    doc.setFontSize(11);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(120, 120, 120);
    doc.text(currentTour.dur + "  ·  Ref " + ref, tx, y + 8 + title.length * 7);
    y = Math.max(y + 46, y + 14 + title.length * 7 + 8);
    function row(k, v) {
      doc.setFont("helvetica", "bold");
      doc.setFontSize(11);
      doc.setTextColor(20, 20, 20);
      doc.text(k + ":", 14, y);
      doc.setFont("helvetica", "normal");
      var lines = doc.splitTextToSize(String(v || "—"), W - 70);
      doc.text(lines, 62, y);
      y += Math.max(7, lines.length * 6) + 2;
    }
    var g = function (id) { var el = document.getElementById(id); return el ? el.value : ""; };
    row("Name", g("cartName"));
    row("Email", g("cartEmail"));
    row("Phone", g("cartPhone"));
    row("Date", g("cartDate"));
    row("Travelers", g("cartPax"));
    row("Price", currentTour.price || "Quote on request");
    row("Requests", g("cartMsg"));
    row("Received", new Date().toLocaleString());
    y += 6;
    doc.setDrawColor(228, 0, 43);
    doc.line(14, y, W - 14, y);
    y += 8;
    doc.setFont("helvetica", "bold");
    doc.setFontSize(12);
    doc.text("A little letter for our guest", 14, y);
    y += 7;
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10.5);
    var letterFR = "Merci d'avoir choisi Abrid Morocco ! Votre réservation pour \"" + currentTour.name + "\" (" + ref + ") est entre les mains d'Abdellah et Karim. Nous répondons personnellement sous 2 heures (9h00-21h00, heure du Maroc) pour confirmer la disponibilité et régler les derniers détails. Aucun paiement n'est dû avant le jour du départ. Nous avons hâte de vous faire découvrir notre Maroc.";
    var letterES = "Gracias por elegir Abrid Morocco. Tu reserva de \"" + currentTour.name + "\" (" + ref + ") está en manos de Abdellah y Karim. Respondemos personalmente en 2 horas (9:00-21:00, hora de Marruecos) para confirmar disponibilidad y ultimar detalles. No se debe ningún pago hasta el día de salida. Estamos deseando mostrarte nuestro Marruecos.";
    var letterEN = "Thank you for choosing Abrid Morocco! Your reservation for \"" + currentTour.name + "\" (" + ref + ") is with Abdellah and Karim now. We reply personally within 2 hours (9:00-21:00 Morocco time) to confirm availability and shape the final details. No payment is due until tour day. We cannot wait to show you our Morocco.";
    var letter = doc.splitTextToSize(FR ? letterFR : (ES ? letterES : letterEN), W - 28);
    doc.text(letter, 14, y);
    y += letter.length * 5 + 10;
    doc.setFontSize(9);
    doc.setTextColor(130, 130, 130);
    doc.text("Abrid Morocco · +212 762 934 488 · abridmorocco@gmail.com · abridmorocco.com", 14, 287);
    return { doc: doc, ref: ref };
  }

  overlay.querySelector("#cartForm").addEventListener("submit", function (ev) {
    ev.preventDefault();
    var btn = document.getElementById("cartSubmit");
    btn.disabled = true;
    btn.textContent = "Sending…";
    var g = function (id) { var el = document.getElementById(id); return el ? el.value : ""; };
    var name = g("cartName"), email = g("cartEmail");
    loadImageData(currentTour.img).catch(function () { return null; }).then(function (img) {
      var out = buildPdf(img);
      var fd = new FormData();
      fd.append("_subject", "New tour reservation – " + currentTour.name + " (" + out.ref + ")");
      fd.append("_template", "table");
      fd.append("Tour", currentTour.name);
      fd.append("Duration", currentTour.dur);
      fd.append("Price", currentTour.price || "Quote on request");
      fd.append("Reference", out.ref);
      fd.append("Name", name);
      fd.append("Email", email);
      fd.append("Phone", g("cartPhone"));
      fd.append("Preferred date", g("cartDate"));
      fd.append("Travelers", g("cartPax"));
      fd.append("Requests", g("cartMsg"));
      try {
        var pdfBlob = out.doc.output("blob");
        fd.append("attachment", pdfBlob, "reservation-" + out.ref + ".pdf");
      } catch (e) { /* email still goes without PDF */ }
      return fetch("https://formsubmit.co/ajax/" + OWNER_EMAIL, { method: "POST", body: fd });
    }).then(function (r) {
      if (!r.ok) throw new Error("send failed");
      document.getElementById("cartFormWrap").innerHTML =
        '<div class="abrid-popup-ok" style="text-align:center;padding:18px 6px;">' +
        '<div style="font-size:2.4rem;">🎉</div>' +
        "<h3>" + T("Reservation received!", "Réservation reçue !", "¡Reserva recibida!") + "</h3>" +
        "<p style=\"color:var(--muted);\">" + T("Thank you, ", "Merci, ", "Gracias, ") + esc(name.split(" ")[0]) +
        T(" — Abdellah or Karim replies personally within 2 hours. A copy of your reservation PDF was prepared with your request.", " — Abdellah ou Karim répond personnellement sous 2 heures. Une copie de votre PDF de réservation a été préparée avec votre demande.", " — Abdellah o Karim responde personalmente en 2 horas. Se ha preparado una copia de tu PDF de reserva con tu solicitud.")+ "</p>" +
        '<button type="button" class="btn btn-secondary" id="cartDone">' + T("Continue exploring", "Continuer à explorer", "Seguir explorando") + '</button></div>';
      document.getElementById("cartDone").addEventListener("click", close);
    }).catch(function () {
      var text = encodeURIComponent("Hello Abrid Morocco! I would like to reserve: " + currentTour.name +
        " (" + currentTour.dur + "). Name: " + name + ", Email: " + email);
      document.getElementById("cartFormWrap").innerHTML =
        '<div style="text-align:center;padding:18px 6px;"><h3>' + T("Sending hiccup", "Petit problème d'envoi", "Problema de envío") + '</h3>' +
        '<p style="color:var(--muted);">' + T("Please send your reservation directly:", "Veuillez envoyer votre réservation directement :", "Envía tu reserva directamente:") + '</p>' +
        '<a class="btn btn-primary" target="_blank" rel="noopener" href="https://wa.me/' + WA_NUMBER + "?text=" + text + '">' + T("Send via WhatsApp", "Envoyer via WhatsApp", "Enviar por WhatsApp") + '</a></div>';
    }).finally(function () {
      btn.disabled = false;
      btn.textContent = T("Send reservation →", "Envoyer la réservation →");
    });
  });
})();
