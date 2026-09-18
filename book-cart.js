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

  var TOURS = {
    "marrakech.html": { name: "Marrakech Day Tour", dur: "1 Day", img: "https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=600&auto=format&fit=crop" },
    "atlas.html": { name: "Atlas Mountains & Ourika Valley", dur: "1 Day", img: "https://i.postimg.cc/NfvKF7Rj/vincenzo-montagna-pd-Z9t-Nbpztw-unsplash.jpg" },
    "essaouira.html": { name: "Essaouira Day Trip", dur: "1 Day", img: "https://images.unsplash.com/photo-1613057157282-cc3cbe630b26?w=600&auto=format&fit=crop" },
    "air-balloon.html": { name: "Hot Air Balloon over Marrakech", dur: "Half Day", img: "https://i.postimg.cc/fRhRWzns/1788783065964.jpg" },
    "ouzoud-quad-tour.html": { name: "Ouzoud Quad Tour", dur: "Half Day", img: "https://images.unsplash.com/photo-1758622159686-7f61d8a81aa5?w=600&auto=format&fit=crop" },
    "merzouga.html": { name: "Merzouga Desert Adventure", dur: "3 Days", img: "https://images.unsplash.com/photo-1593350058052-cc6636c9facd?w=600&auto=format&fit=crop" },
    "imilchil.html": { name: "Imilchil, Lakes & Summit", dur: "3 Days", img: "https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=600&auto=format&fit=crop/YNqJlL3B9gIRgqnp/untitled-2-3-AoPepbZODoTZZDk2.jpg" },
    "chefchaouen.html": { name: "Chefchaouen Day Trip", dur: "Day Trip", img: "https://i.postimg.cc/vTjVBp7p/Untitled-design.jpg" },
    "fes.html": { name: "Fes Medina Guided Tour", dur: "Day Tour", img: "https://images.unsplash.com/photo-1512958789358-4effcbe171a0?w=600&auto=format&fit=crop" },
    "ouzoud.html": { name: "Ouzoud Waterfalls", dur: "Day Trip", img: "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?w=600&auto=format&fit=crop" },
    "zagora.html": { name: "Zagora Desert Express", dur: "2 Days", img: "https://images.unsplash.com/photo-1593350058052-cc6636c9facd?w=600&auto=format&fit=crop" },
    "toubkal.html": { name: "Mount Toubkal Trek", dur: "2 Days", img: "images/toubkal/toubkal-massif.jpg" },
    "agafay.html": { name: "Agafay Desert Evening", dur: "Evening", img: "images/agafay/agafay-camp.jpg" },
    "high-atlas-azilal-imilchil-rich.html": { name: "Across the High Atlas", dur: "5 Days", img: "images/high-atlas/imilchil/imilchil-01.jpg" },
    "imperial.html": { name: "Imperial Cities Circuit", dur: "8 Days", img: "https://images.unsplash.com/photo-1559925523-10de9e23cf90?w=600&auto=format&fit=crop" },
    "6-day-christmas-morocco.html": { name: "6-Day Morocco Christmas Itinerary", dur: "6 Days", img: "https://i.postimg.cc/vTjVBp7p/Untitled-design.jpg" },
    "classic-morocco.html": { name: "Classic Morocco Grand Tour", dur: "13 Days", img: "https://images.unsplash.com/photo-1512958789358-4effcbe171a0?w=600&auto=format&fit=crop" },
    "small-group-tour.html": { name: "Small Group Morocco Tour", dur: "11 Days", img: "https://images.unsplash.com/photo-1506869640319-fe1a24fd76dc?w=600&auto=format&fit=crop" },
    "private.html": { name: "Private Custom Morocco Tour", dur: "Any Length", img: "https://images.unsplash.com/photo-1526994387180-9557a434b046?w=600&auto=format&fit=crop" }
  };

  var file = (location.pathname.split("/").pop() || "index.html").split("?")[0].toLowerCase();
  var tour = TOURS[file] || TOURS["private.html"];
  if (!tour) return;

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
  fab.setAttribute("aria-label", "Reserve this tour");
  fab.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg><span>Reserve</span>';
  document.body.appendChild(fab);

  /* Modal */
  var overlay = document.createElement("div");
  overlay.className = "cart-overlay";
  overlay.id = "cartOverlay";
  overlay.setAttribute("hidden", "");
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", "Reserve " + tour.name);
  var today = new Date().toISOString().slice(0, 10);
  overlay.innerHTML =
    '<div class="cart-box">' +
    '<button type="button" class="cart-close" id="cartClose" aria-label="Close">✕</button>' +
    '<div class="cart-tour"><img id="cartThumb" src="' + esc(tour.img) + '" alt="" loading="lazy">' +
    '<div><strong>' + esc(tour.name) + '</strong><span>' + esc(tour.dur) + ' · Private · Quote on request</span></div></div>' +
    '<div id="cartFormWrap">' +
    '<form id="cartForm">' +
    '<div class="cart-grid">' +
    '<div><label for="cartName">Full name</label><input id="cartName" name="name" required autocomplete="name" placeholder="Sara"></div>' +
    '<div><label for="cartEmail">Email</label><input id="cartEmail" name="email" type="email" required autocomplete="email" placeholder="you@example.com"></div>' +
    '<div><label for="cartPhone">Phone / WhatsApp</label><input id="cartPhone" name="phone" autocomplete="tel" placeholder="+33 …"></div>' +
    '<div><label for="cartDate">Preferred date</label><input id="cartDate" name="date" type="date" min="' + today + '" required></div>' +
    '<div><label for="cartPax">Travelers</label><input id="cartPax" name="travelers" type="number" min="1" max="30" value="2" required></div>' +
    '<div><label for="cartMsg">Anything we should know?</label><input id="cartMsg" name="requests" placeholder="Hotel, diet, pace…"></div>' +
    '</div>' +
    '<button type="submit" class="btn btn-primary" id="cartSubmit" style="width:100%;">Send reservation →</button>' +
    '<p class="fine">No payment now — Abdellah or Karim replies personally within 2 hours.</p>' +
    '</form></div></div>';
  document.body.appendChild(overlay);

  function open() { overlay.removeAttribute("hidden"); document.body.style.overflow = "hidden"; }
  function close() { overlay.setAttribute("hidden", ""); document.body.style.overflow = ""; }
  fab.addEventListener("click", open);
  overlay.querySelector("#cartClose").addEventListener("click", close);
  overlay.addEventListener("click", function (e) { if (e.target === overlay) close(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !overlay.hasAttribute("hidden")) close(); });

  /* Inline "Reserve" buttons (data-open-cart) replace the floating pill where present */
  var inlineBtns = document.querySelectorAll("[data-open-cart]");
  if (inlineBtns.length) fab.style.display = "none";
  inlineBtns.forEach(function (b) { b.addEventListener("click", open); });

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
    var title = doc.splitTextToSize(tour.name, W - tx - 14);
    doc.text(title, tx, y + 8);
    doc.setFontSize(11);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(120, 120, 120);
    doc.text(tour.dur + "  ·  Ref " + ref, tx, y + 8 + title.length * 7);
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
    var letter = doc.splitTextToSize(
      "Thank you for choosing Abrid Morocco! Your reservation for \"" + tour.name +
      "\" (" + ref + ") is with Abdellah and Karim now. We reply personally within " +
      "2 hours (9:00-21:00 Morocco time) to confirm availability and shape the final details. " +
      "No payment is due until tour day. We cannot wait to show you our Morocco.", W - 28);
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
    loadImageData(tour.img).catch(function () { return null; }).then(function (img) {
      var out = buildPdf(img);
      var fd = new FormData();
      fd.append("_subject", "New tour reservation – " + tour.name + " (" + out.ref + ")");
      fd.append("_template", "table");
      fd.append("Tour", tour.name);
      fd.append("Duration", tour.dur);
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
        "<h3>Reservation received!</h3>" +
        "<p style=\"color:var(--muted);\">Thank you, " + esc(name.split(" ")[0]) +
        " — Abdellah or Karim replies personally within 2 hours. A copy of your reservation PDF was prepared with your request.</p>" +
        '<button type="button" class="btn btn-secondary" id="cartDone">Continue exploring</button></div>';
      document.getElementById("cartDone").addEventListener("click", close);
    }).catch(function () {
      var text = encodeURIComponent("Hello Abrid Morocco! I would like to reserve: " + tour.name +
        " (" + tour.dur + "). Name: " + name + ", Email: " + email);
      document.getElementById("cartFormWrap").innerHTML =
        '<div style="text-align:center;padding:18px 6px;"><h3>Sending hiccup</h3>' +
        '<p style="color:var(--muted);">Please send your reservation directly:</p>' +
        '<a class="btn btn-primary" target="_blank" rel="noopener" href="https://wa.me/' + WA_NUMBER + "?text=" + text + '">Send via WhatsApp</a></div>';
    }).finally(function () {
      btn.disabled = false;
      btn.textContent = "Send reservation →";
    });
  });
})();
