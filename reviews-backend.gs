/* ═══════════════════════════════════════════════════════════════════
   ABRID MOROCCO — Reviews backend (Google Sheets + Apps Script)
   Free, no new accounts. Setup (one time, ~10 minutes):

   1. sheets.google.com → new spreadsheet, rename one tab to: reviews
   2. Row 1 headers (exact order):
      timestamp | name | trip | rating | traveldate | review | approved
   3. In the approved column select the whole column:
      Insert → Checkbox (so approvals are a one-tap tick)
   4. Extensions → Apps Script → delete everything → paste THIS file
   5. Change OWNER_EMAIL below to your inbox
   6. Deploy → New deployment → type Web app →
      Execute as: Me · Who has access: Anyone → Deploy
   7. Copy the Web app URL, paste it as window.ABRID_REVIEWS_API
      at the top of site.js, redeploy/upload the site. Done.

   HOW IT WORKS:
   - Visitors submit reviews on reviews.html → stored as a new row,
     approved = unticked (never shown publicly).
   - You get an email per review with a link to the sheet.
   - Tick "approved" for genuine reviews → they appear on
     reviews.html and the homepage automatically within minutes.
   - Spam protection: nothing is public without your tick, plus a
     honeypot field, minimum fill-time check, length + duplicate
     guards below.
   ═══════════════════════════════════════════════════════════════════ */

var OWNER_EMAIL = "abridmorocco@gmail.com";
var SHEET_NAME = "reviews";
var MIN_FILL_SECONDS = 4;
var MAX_REVIEW_CHARS = 2000;

/* GET (or plain visit) → JSON list of APPROVED reviews only */
function doGet() {
  var out = [];
  try {
    var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    if (!sh) return json(out);
    var rows = sh.getDataRange().getValues();
    for (var i = 1; i < rows.length; i++) {
      if (rows[i][6] === true) {
        out.push({
          name: String(rows[i][1] || ""),
          trip: String(rows[i][2] || ""),
          rating: Number(rows[i][3]) || 5,
          date: String(rows[i][4] || ""),
          text: String(rows[i][5] || "")
        });
      }
    }
  } catch (err) { /* return whatever we have */ }
  return json(out);
}

/* POST (JSON, sent as text/plain to avoid preflight) → queue a review */
function doPost(e) {
  try {
    var d = JSON.parse((e && e.postData && e.postData.contents) || "{}");

    /* Silent bot guards — always answer OK so bots learn nothing */
    if (d.website) return json({ ok: true });                       // honeypot
    var review = String(d.review || "").trim().slice(0, MAX_REVIEW_CHARS);
    var name = String(d.name || "").trim().slice(0, 80);
    if (!name || !review) return json({ ok: true });
    var started = Number(d.started) || 0;
    if (started && (Date.now() - started) < MIN_FILL_SECONDS * 1000) return json({ ok: true });

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(SHEET_NAME);
    if (!sh) return json({ ok: true });

    /* Duplicate guard: same name + same text already queued */
    var rows = sh.getDataRange().getValues();
    var key = (name + "||" + review).toLowerCase();
    for (var i = 1; i < rows.length; i++) {
      if ((String(rows[i][1] || "") + "||" + String(rows[i][5] || "")).toLowerCase() === key) {
        return json({ ok: true });
      }
    }

    var rating = Math.max(1, Math.min(5, parseInt(d.rating, 10) || 5));
    sh.appendRow([new Date(), name, String(d.trip || "").slice(0, 120),
      rating, String(d.traveldate || "").slice(0, 20), review, false]);

    /* Email notification (failure must not break the submit) */
    try {
      MailApp.sendEmail(OWNER_EMAIL,
        "New review to approve — " + name + " (" + rating + "/5)",
        "Trip: " + (d.trip || "-") + "\nTravelled: " + (d.traveldate || "-") +
        "\n\n" + review + "\n\nApprove here: " + ss.getUrl());
    } catch (mailErr) { /* quota or permission — review is still saved */ }

    return json({ ok: true });
  } catch (err) {
    return json({ ok: true });
  }
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
