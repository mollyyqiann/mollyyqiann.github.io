# Infinite Exploration — Website Exploration

Design exploration and build-out for the Infinite Exploration marketing site (AI-coordinated lunar power/hydrogen/oxygen/water infrastructure). Source brief: `Infinite_Exploration_Website_Brief_1.docx`.

## Current deliverable: repo root (live on GitHub Pages)

This repo is `mollyyqiann.github.io`, so whatever sits at the repo root is served at `https://mollyyqiann.github.io/`. The multi-page site lives at root, one HTML file per page from the brief's "Planned Site Structure":

| Page | URL |
|---|---|
| Home | `https://mollyyqiann.github.io/` (`index.html`) |
| Technology / Platform | `technology.html` |
| About | `about.html` |
| News | `news.html` |
| Contact | `contact.html` |

Shared code lives in `assets/`:
- `style.css` — all page styling (Option 2 palette: cool black + blue, `--bg:#06080b`, `--accent:#3d8bfd`), reveal/parallax/Ken Burns effects, `.soft-bg-section`/`.float-img` background-photo + floating-accent patterns.
- `script.js` — scroll-reveal (IntersectionObserver), parallax scroll handler, contact form submit handler (static — see Open Items below).

Pages reference their imagery via `images/d6-*` (root-level `images/` folder — copies of the same files that live in `designs/images/`, kept in sync manually since `designs/design-6-turion-inspired.html` still references the `designs/images/` copies).

### Preview locally
```
cd "/Users/mollyqian/Desktop/infinite exploration" && python3 -m http.server 4173
```
then open `http://localhost:4173/index.html`.

## `designs/*.html` — single-page concept rounds (superseded)

Six standalone one-page explorations, built and refined in sequence before the multi-page build:

1. `design-1-dark-cinematic.html`
2. `design-2-premium-minimal.html`
3. `design-3-bold-technical.html`
4. `design-4-corporate-investor.html`
5. `design-5-modern-saas.html`
6. `design-6-turion-inspired.html` — final direction (Option 2 palette, Turion Space–inspired layout). This is the file the current multi-page root site was built from.

`design-2-about.html`, `design-2-contact.html`, `design-2-news.html`, `design-2-technology.html` are a **stale early multi-page attempt** on the old cream/tan palette, from before the black+blue direction was chosen. Not part of the current site — kept for reference only.

Root-level `design-*-screenshot.png` files are preview captures from the early comparison round (designs 1–5).

## `designs/images/`

Generated imagery (OpenAI `gpt-image-1`, DALL·E 3 fallback). `d1`–`d5` prefixes are per-concept images used only by the superseded single-page rounds. `d6-*` are the current site's imagery:
- `d6-hero-orbital.jpg`, `d6-stats-arrayfield.jpg`, `d6-ops-control.jpg`, `d6-ops-lunarnight.jpg` — hero/section backgrounds
- `d6-product-array.png`, `d6-product-relay.png`, `d6-product-rover.png` — product renders
- `d6-whoweare-bg.jpg`, `d6-outputs-bg.jpg` — Home page "Who We Are" / "Four Core Outputs" section backgrounds
- `d6-float-module.png`, `d6-float-tank.png`, `d6-float-panel.png` — small floating accent renders on the Home page

## `designs/scripts/`

- `generate_images.py` — original image batch (7 `d6-*` core images)
- `generate_images_round2.py` — second batch (Home page background + floating accents)

Both call the OpenAI Images API (`gpt-image-1`, falling back to `dall-e-3` on 403/404) and require `OPENAI_API_KEY` passed as an environment variable at invocation — the key is never written to a file in this repo:
```
OPENAI_API_KEY="sk-..." python3 generate_images_round2.py
```

## `.claude/launch.json`

Preview-tool server config, serves the repo root on port 4173.

## Open items (from the brief, currently placeholders in the root-level pages)

These are explicitly unresolved in the brief and stubbed out rather than fabricated:
- **Contact form** (`contact.html`) — static only, no backend wired up; needs Formspree/Netlify Forms or similar before launch.
- **Team members** — no names/titles/bios/headshots in the brief; About page has no fabricated team section.
- **News items** — placeholder dates/entries on Home and News pages; no real announcements existed to use.
- **Partner logos, office address, legal/company details** — marked TBD/placeholder in `contact.html` and elsewhere.
