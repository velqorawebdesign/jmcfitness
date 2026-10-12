# JMC Fitness website

Static website for **JMC Fitness** — custom training plans and nutrition plans. Instagram: [@jmcfitness.1](https://www.instagram.com/jmcfitness.1/).

Plain HTML/CSS/JS. No frameworks, no build dependencies beyond Python 3, no cookies, no tracking.

## Editing

1. Put your real business details in the `BUSINESS` block at the top of `build.py`.
2. Edit page content in `src/pages/*.html`.
3. Run `python3 build.py` (add `--strict` to fail if any placeholder is left). It regenerates the `.html` files in the root.

Don't edit the root `.html` files directly; they are overwritten by the build.

## Before you go live (required)

`python3 build.py` lists every placeholder still to fill in. They show on the site as highlighted `[brackets]` until you do.

- [ ] **Business details** – legal name, postal address, email. Irish/EU law (E-Commerce Regulations 2003, Consumer Rights Act 2022) requires these to be shown.
- [ ] **CRO business name (RBN)** – if you trade as "JMC Fitness" rather than your own name, register the business name with the CRO and add the number. Otherwise remove that line.
- [ ] **VAT status**.
- [ ] **Your first name and qualifications** – list only qualifications you actually hold, with the awarding body.
- [ ] **Host, email provider and payment provider** – named in the Privacy Policy.
- [ ] **Have a solicitor review the legal pages.** They are written for a sole trader in Ireland selling to consumers, but they are a starting point, not legal advice.
- [ ] Send each client a written **health questionnaire with a separate explicit-consent tick** (health data is "special category" under GDPR Art. 9) before collecting injuries/medical info.
- [ ] Before starting a plan within the 14-day cancellation period, get the client's **written request and acknowledgement** (see `refunds.html`).
- [ ] Replace `assets/img/jmc-fitness-logo.*` with the original logo file if you have it (the current one is cropped from a screenshot).
- [ ] Set `SITE_URL` in `build.py` once you have a domain.

## Compliance checklist (what was checked)

| Item | Status |
|---|---|
| Colour contrast | All text pairs ≥ 5:1 (WCAG AA needs 4.5:1); input borders and focus ring ≥ 3:1. |
| Alt text | Logo has descriptive alt text; the repeated decorative logo uses `alt=""`. |
| Accessibility | axe-core (WCAG 2.2 AA + best practice): 0 violations on all 6 pages, desktop and mobile. Skip link, landmarks, visible focus, 44px+ touch targets, no horizontal scroll at 375px. |
| Keyboard-friendly form | Native inputs, visible labels, `fieldset`/`legend` for radio group, errors written in text, announced via `aria-live`, focus moves to the first error. |
| Clear button labels | Every button/link says what it does ("Send enquiry by email", "Enquire about the nutrition plan"). New-tab links say so to screen readers. |
| Animation | Kinetic headline, rotating word, scrolling marquee, scroll reveals. Marquee has a Pause button (WCAG 2.2.2); everything is off with "reduce motion". Content is fully visible without JavaScript. |
| Reviews/testimonials | None. No fake reviews. Add real ones only with the client's written permission. |
| Unsupported claims | No guaranteed results, timeframes, "best" claims or invented qualifications. Results disclaimer and "not medical advice" notices included. |
| Prices | Not invented. Site states the price is given in writing before payment. |
| Cookies / consent banner | No cookies or browser storage are used, so no banner is legally needed (ePrivacy Regs S.I. 336/2011). Verified in Chromium: 0 cookies. |
| Tracking | No analytics, pixels or tracking scripts. |
| Third-party embeds | None. Instagram is a plain link, not an embed (embeds set Meta cookies). Fonts are self-hosted, so there are no requests to Google Fonts. Verified: 0 external requests on load. A Content-Security-Policy blocks third-party scripts, frames and connections. |
| Data minimisation | Form asks only for name, email, plan and optional goal. It is not sent to any server; it opens the visitor's own email app. Health data is explicitly not requested on the form. |
| Form consent | Required tick-box confirming the Privacy Policy has been read, plus an 18+ confirmation. No marketing opt-in, because there is no marketing. |
| Image copyright | Only the JMC Fitness logo is used (your own). No stock photos. Anton font is SIL Open Font License (`assets/fonts/OFL-Anton.txt`). |
| Legal pages | Terms & Conditions, Refund & Cancellation Policy (14-day right, model form), Privacy Policy (GDPR, DPC complaints), Cookies Policy, Accessibility Statement. |
| Local law | Written for Ireland/EU: GDPR & Data Protection Act 2018, ePrivacy Regs 2011, Consumer Rights Act 2022, EU distance-selling rules. |

## Hosting

Any static host works (GitHub Pages, Netlify, Cloudflare Pages). Upload the repo root; `src/` and `build.py` don't need to be public but don't hurt.
