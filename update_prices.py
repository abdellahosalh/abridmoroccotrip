from pathlib import Path
import re

# Run this script from the website folder. It no longer changes or increases prices.
directory = Path(__file__).resolve().parent

currency_amount = re.compile(
    r"(?<![\w])(?:[$€£]\s*\d[\d,]*(?:\.\d+)?|\d[\d,]*(?:\.\d+)?\s*(?:USD|MAD|EUR|€|£))(?![\w])",
    re.IGNORECASE,
)
schema_offers = re.compile(
    r'\s*"offers"\s*:\s*\{[^{}]*\},?',
    re.IGNORECASE,
)


def hide_prices(content):
    # Remove offer blocks so search engines cannot read a hidden numeric price.
    content = schema_offers.sub("", content)
    # Replace visible and metadata currency amounts with a quote request.
    content = currency_amount.sub("Quote on request", content)
    content = re.sub(
        r"\b(?:from|starting at|only)\s+Quote on request\b",
        "Quote on request",
        content,
        flags=re.IGNORECASE,
    )
    return content


updated = 0
for filepath in directory.rglob("*"):
    if filepath.suffix.lower() not in {".html", ".js", ".xml", ".css"}:
        continue

    original = filepath.read_text(encoding="utf-8")
    revised = hide_prices(original)
    if revised != original:
        filepath.write_text(revised, encoding="utf-8")
        updated += 1
        print(f"Removed prices from {filepath.name}")

print(f"Finished scanning the website. Updated {updated} files.")
