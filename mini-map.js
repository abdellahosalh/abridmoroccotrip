/* ═══════════════════════════════════════════════════════════════════
   ABRID MOROCCO — Shared mini live maps (Leaflet, no API key)
   Any element with class "mini-map" and data attributes becomes a map:
     data-center="lat,lon"   map centre (required)
     data-zoom="8"           zoom level (default 8)
     data-pins='[["Label",lat,lon],["Label2",lat,lon2]]'
   Pins use pure-CSS markers — no image assets. Topographic tiles first,
   automatic fallback to a second free style if unreachable.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  var TOPO = {
    url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    opts: {
      maxZoom: 17, subdomains: "abc",
      attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org" target="_blank" rel="noopener">SRTM</a> | style: &copy; <a href="https://opentopomap.org" target="_blank" rel="noopener">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener">CC-BY-SA</a>)'
    }
  };
  var FALLBACK = {
    url: "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    opts: {
      maxZoom: 19, subdomains: "abcd",
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions" target="_blank" rel="noopener">CARTO</a>'
    }
  };

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function initOne(el) {
    if (typeof L === "undefined") {
      el.innerHTML = '<p style="padding:40px;text-align:center;color:var(--text-muted);">Map needs a connection — please reload online.</p>';
      return;
    }
    var parts = (el.getAttribute("data-center") || "31.8,-6.0").split(",");
    var center = [parseFloat(parts[0]), parseFloat(parts[1])];
    var zoom = parseInt(el.getAttribute("data-zoom") || "8", 10);
    var pins = [];
    try { pins = JSON.parse(el.getAttribute("data-pins") || "[]"); } catch (e) { pins = []; }

    var map = L.map(el, { scrollWheelZoom: false }).setView(center, zoom);
    var layer = L.tileLayer(TOPO.url, TOPO.opts).addTo(map);
    var errors = 0, switched = false;
    layer.on("tileerror", function () {
      errors++;
      if (errors > 4 && !switched) {
        switched = true;
        map.removeLayer(layer);
        layer = L.tileLayer(FALLBACK.url, FALLBACK.opts).addTo(map);
      }
    });

    pins.forEach(function (p) {
      var label = p[0], lat = p[1], lon = p[2];
      var icon = L.divIcon({
        className: "",
        html: '<div class="route-pin">' + esc(label) + "</div>",
        iconSize: null, iconAnchor: [15, 15], popupAnchor: [0, -16]
      });
      L.marker([lat, lon], { icon: icon }).bindPopup("<strong>" + esc(label) + "</strong>").addTo(map);
    });
    map.on("click", function () { map.scrollWheelZoom.enable(); });
  }

  function boot() {
    var els = document.querySelectorAll(".mini-map[data-center]");
    for (var i = 0; i < els.length; i++) initOne(els[i]);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
