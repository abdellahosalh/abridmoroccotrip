/* ═══════════════════════════════════════════════════════════════════
   ABRID MOROCCO — Shared behaviour
   Handles: mobile menu, sticky header, footer year, search.
   Load at the end of <body> on every page.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ===== EXPLORE MOROCCO dropdown with 3s auto-hide =====
     Opens on hover/focus (CSS :hover + .open). A setTimeout(3000)
     force-hides it even while still hovered, via .drop-hide
     (override in design.css). mouseleave resets for next hover. */
  var dropItems = document.querySelectorAll('.nav-links li.drop');
  var DROP_TIMEOUT = 3000;

  dropItems.forEach(function (dropLi) {
    var dropTimer = null;

    function showDrop() {
      dropLi.classList.add('open');
      dropLi.classList.remove('drop-hide');
      clearTimeout(dropTimer);
      dropTimer = setTimeout(function () {
        dropLi.classList.remove('open');
        dropLi.classList.add('drop-hide');
      }, DROP_TIMEOUT);
    }

    function hideDrop() {
      clearTimeout(dropTimer);
      dropLi.classList.remove('open');
      dropLi.classList.remove('drop-hide');
    }

    dropLi.addEventListener('mouseenter', showDrop);
    dropLi.addEventListener('mouseleave', hideDrop);
    var trigger = dropLi.querySelector('a');
    if (trigger) {
      trigger.addEventListener('focus', showDrop);
      trigger.addEventListener('blur', hideDrop);
    }
  });


  /* ── Search overlay ── */
  var overlay = document.getElementById('searchOverlay');
  var searchInput = document.getElementById('searchInput');
  var searchResults = document.getElementById('searchResults');
  var searchOpen = document.getElementById('searchOpen');
  var searchClose = document.getElementById('searchClose');

  function runSearch(q) {
    if (!searchResults) return;
    var idx = window.ABRID_SEARCH || [];
    var query = q.toLowerCase().trim();
    if (!query) {
      searchResults.innerHTML = '<p class="search-nores">Type a destination, trip or topic…</p>';
      return;
    }
    var words = query.split(/\s+/);
    var hits = idx.filter(function (item) {
      var hay = (item.t + ' ' + item.c + ' ' + item.d).toLowerCase();
      return words.every(function (w) { return hay.indexOf(w) >= 0; });
    });
    if (!hits.length) {
      searchResults.innerHTML = '<p class="search-nores">No results for "' + q.replace(/</g,'&lt;') + '"</p>';
      return;
    }
    var html = '';
    hits.forEach(function (hit) {
      html += '<a class="search-result" href="' + hit.u + '">' +
        '<span class="search-cat">' + hit.c + '</span>' +
        '<strong>' + hit.t + '</strong>' +
        '<p>' + hit.d + '</p>' +
        '</a>';
    });
    searchResults.innerHTML = html;
  }

  function openSearch() {
    if (!overlay) return;
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    if (searchInput) {
      searchInput.value = '';
      searchInput.focus();
      runSearch('');
    }
  }
  function closeSearch() {
    if (!overlay) return;
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
  if (searchOpen) searchOpen.addEventListener('click', openSearch);
  if (searchClose) searchClose.addEventListener('click', closeSearch);
  if (overlay) {
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeSearch();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeSearch();
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openSearch();
      }
    });
  }
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      runSearch(this.value);
    });
  }

  /* ── Filter logic for trips / destinations pages ──
     Markup convention (see trips.html):
     <div class="filter-options" data-filter="dur|xp|style">
       <button class="filter-btn active" data-value="">All</button>
       <button class="filter-btn" data-value="day">Day Trip</button>
     </div>
     Cards: <article class="tour-card" data-dur="day short" data-xp="desert atlas">
     Result count: <div class="filter-results" id="filterResults"> */
  var filterBars = document.querySelectorAll('.filter-bar');
  filterBars.forEach(function (bar) {
    var options = bar.querySelectorAll('.filter-options[data-filter]');
    var cards = bar.parentNode.querySelectorAll('.tour-card, .dest-card');
    var countEl = document.getElementById('filterResults') ||
      bar.parentNode.querySelector('#filterResults');

    function applyFilters() {
      var shown = 0;
      var activeGroups = [];
      options.forEach(function (group) {
        var g = group.getAttribute('data-filter');
        var activeVal = null;
        group.querySelectorAll('.filter-btn.active').forEach(function (a) {
          activeVal = a.getAttribute('data-value') || '';
        });
        if (activeVal) activeGroups.push(g + '=' + activeVal);
      });

      cards.forEach(function (card) {
        var match = activeGroups.every(function (kv) {
          var parts = kv.split('=');
          var group = parts[0];
          var value = parts[1];
          return (card.getAttribute('data-' + group) || '').split(/\s+/).indexOf(value) >= 0;
        });
        card.classList.toggle('hidden', !match);
        if (match) shown++;
      });

      if (countEl) {
        countEl.textContent = shown + ' result' + (shown === 1 ? '' : 's') +
          (activeGroups.length ? '' : ' (showing all)');
      }
    }

    options.forEach(function (group) {
      group.querySelectorAll('.filter-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var value = btn.getAttribute('data-value') || '';
          group.querySelectorAll('.filter-btn').forEach(function (a) {
            var av = a.getAttribute('data-value') || '';
            a.classList.toggle('active', av === value);
          });
          applyFilters();
        });
      });
    });

    applyFilters();
  });
})();