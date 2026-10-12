#!/usr/bin/env python3
"""Build the JMC Fitness static site.

Edit BUSINESS below (your real details), then run:  python3 build.py
Pages are written from src/pages/*.html into the project root.

Any value still wrapped in [square brackets] is treated as a placeholder:
it is highlighted on the page and listed when you build, so nothing goes
live with made-up details by accident.
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent

# ---------------------------------------------------------------------------
# Your real business details. Replace every [PLACEHOLDER].
# ---------------------------------------------------------------------------
BUSINESS = {
    "BRAND": "JMC Fitness",
    "OWNER": "[Your full legal name or company name]",
    "FIRST_NAME": "[Your first name]",
    "EMAIL": "[your-email@example.com]",
    "ADDRESS": "[Business postal address, Ireland]",
    # Registered Business Name number from the CRO, if you trade under a name
    # other than your own. Delete the line in the footer if not applicable.
    "RBN": "[CRO business name number, or remove]",
    "VAT": "[VAT number, or 'Not VAT registered']",
    "QUALIFICATIONS": "[Your coaching / nutrition qualifications and awarding body — only list ones you actually hold]",
    # Services that handle client data — named in the Privacy Policy.
    "HOST": "[Website host, e.g. Netlify / GitHub Pages]",
    "EMAIL_PROVIDER": "[Email provider, e.g. Google Workspace / Outlook]",
    "PAYMENT_PROVIDER": "[Payment provider, e.g. Stripe / Revolut Business / Square]",
    "IG_HANDLE": "jmcfitness.1",
    "IG_URL": "https://www.instagram.com/jmcfitness.1/",
    "IG_DM_URL": "https://ig.me/m/jmcfitness.1",
    "UPDATED": "12 October 2026",
    "SITE_URL": "",  # e.g. https://www.jmcfitness.ie — used for canonical links once you have a domain
}

PAGES = [
    # (source file, output file, nav label or None)
    ("index.html", "index.html", None),
    ("terms.html", "terms.html", "Terms & Conditions"),
    ("refunds.html", "refunds.html", "Refund & Cancellation Policy"),
    ("privacy.html", "privacy.html", "Privacy Policy"),
    ("cookies.html", "cookies.html", "Cookies Policy"),
    ("accessibility.html", "accessibility.html", "Accessibility Statement"),
]

IG_ICON = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/>'
    '<circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
)


def is_placeholder(v):
    return v.startswith("[") and v.endswith("]")


def render_value(v):
    if is_placeholder(v):
        return f'<mark class="todo">{html.escape(v)}</mark>'
    return html.escape(v)


def fill(text):
    # {{KEY_RAW}} -> plain value for attributes (href, data-*)
    # {{KEY}}     -> escaped value, highlighted if it is still a placeholder
    def raw(m):
        return html.escape(BUSINESS[m.group(1)].strip("[]"), quote=True)

    text = re.sub(r"\{\{(\w+)_RAW\}\}", raw, text)
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: render_value(BUSINESS[m.group(1)]), text)
    return text


def header(current):
    links = [
        ("index.html#plans", "Plans"),
        ("index.html#how-it-works", "How it works"),
        ("index.html#about", "About"),
        ("index.html#faq", "FAQ"),
        ("index.html#contact", "Get started"),
    ]
    items = "\n".join(
        f'          <li><a href="{href}">{label}</a></li>' for href, label in links
    )
    return f"""<a class="skip-link" href="#main">Skip to main content</a>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="index.html">
        <img src="assets/img/favicon.png" width="44" height="44" alt="">
        <span>JMC <b>Fitness</b><span class="visually-hidden"> – home</span></span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav id="site-nav" class="site-nav" aria-label="Main">
        <ul>
{items}
          <li><a href="{{{{IG_URL_RAW}}}}" rel="noopener" target="_blank">Instagram<span class="visually-hidden"> (opens in a new tab)</span></a></li>
        </ul>
      </nav>
    </div>
  </header>"""


def footer(current):
    current_attr = ' aria-current="page"'
    legal = "\n".join(
        f'            <li><a href="{out}"{current_attr if out == current else ""}>{label}</a></li>'
        for _, out, label in PAGES
        if label
    )
    return f"""<footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h2>JMC Fitness</h2>
          <p>Custom training and nutrition plans. Building a better you.</p>
          <address>
            {{{{BRAND}}}} is a trading name of {{{{OWNER}}}}.<br>
            {{{{ADDRESS}}}}<br>
            Email: <a href="mailto:{{{{EMAIL_RAW}}}}">{{{{EMAIL}}}}</a><br>
            Business name no.: {{{{RBN}}}}<br>
            VAT: {{{{VAT}}}}
          </address>
        </div>
        <div>
          <h2>Legal</h2>
          <ul>
{legal}
          </ul>
        </div>
        <div>
          <h2>Follow</h2>
          <ul>
            <li><a href="{{{{IG_URL_RAW}}}}" rel="noopener" target="_blank">Instagram @{{{{IG_HANDLE}}}}<span class="visually-hidden"> (opens in a new tab)</span></a></li>
            <li><a href="{{{{IG_DM_URL_RAW}}}}" rel="noopener" target="_blank">Message “COACH” on Instagram<span class="visually-hidden"> (opens in a new tab)</span></a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© <span data-year>2026</span> {{{{OWNER}}}} trading as JMC Fitness. All rights reserved. The JMC Fitness name and logo belong to JMC Fitness.</p>
        <p>This website does not use cookies, analytics or tracking. The plans and information here are general fitness guidance, not medical advice.</p>
      </div>
    </div>
  </footer>"""


def page(src, out):
    raw = (ROOT / "src" / "pages" / src).read_text(encoding="utf-8")
    meta, body = raw.split("\n---\n", 1)
    info = dict(line.split(":", 1) for line in meta.strip().splitlines())
    title = info["title"].strip()
    desc = info["description"].strip()
    canonical = ""
    if BUSINESS["SITE_URL"]:
        url = BUSINESS["SITE_URL"].rstrip("/") + "/" + ("" if out == "index.html" else out)
        canonical = f'\n  <link rel="canonical" href="{url}">'
    doc = f"""<!doctype html>
<html lang="en-IE">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc, quote=True)}">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self'; style-src 'self'; script-src 'self'; connect-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'self'">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="theme-color" content="#0b0e1a">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(desc, quote=True)}">
  <meta property="og:image" content="assets/img/jmc-fitness-logo.png">
  <meta property="og:type" content="website">{canonical}
  <link rel="icon" type="image/png" href="assets/img/favicon.png">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="assets/css/styles.css">
  <script src="assets/js/main.js" defer></script>
</head>
<body>
  {header(out)}

  <main id="main" tabindex="-1">
{body.rstrip()}
  </main>

  {footer(out)}
</body>
</html>
"""
    doc = fill(doc)
    (ROOT / out).write_text(doc, encoding="utf-8")
    return doc


def main():
    missing = sorted(k for k, v in BUSINESS.items() if v and is_placeholder(v))
    for src, out, _ in PAGES:
        page(src, out)
        print(f"built {out}")
    if missing:
        print("\nPlaceholders still to replace in build.py before launch:")
        for k in missing:
            print(f"  - {k}: {BUSINESS[k]}")
        if "--strict" in sys.argv:
            sys.exit(1)


if __name__ == "__main__":
    main()
