# WoodenYears — Session Handoff / Context

_Last updated: 2026-06-01. Written so work can resume after a computer restart._

## What this project is
A password-protected, Portuguese (pt-PT) single-page documentation site for **WoodenYears**,
a Portugal-based business selling premium wooden plinths for vintage turntables. The whole
site is one file: **`index.html`** (HTML + CSS + JS, no build step).

- **Live site (GitHub Pages):** https://duartegarciacnt-crypto.github.io/repo/
- **Repo:** `github.com/duartegarciacnt-crypto/repo` (branch `main`)
- **Passwords (client-side, case-sensitive):** `xauquintas`, `darkside`, `Ok`
- **Latest commit at handoff:** `35332fd`

## Site structure
- Top tabs: **Marcas** (brands) and **Materiais** (materials guide).
- Under Marcas, 9 brand sub-tabs, each with 3 inner tabs — **Compatibilidade**,
  **Análise de Mercado** (price table), **Competição**:
  1. Dual  2. Technics (SL series + an SP-10/SP-15 motor-unit section)
  3. Lenco  4. Garrard  5. Thorens  6. Denon  7. JVC / Victor  8. Sony  9. Marantz
- JS: `switchTab()` (top) and `switchSubTab(name, button)` (uses `:scope > .sub-tab-content`,
  so **every brand div must be a direct child of `#brands`** — keep the structure flat).

## Business thesis (drives model selection)
Best plinth candidates are **bare "motor unit" decks** where a plinth is structurally
required (not optional): Technics SP-10/SP-15, Denon DP-80/6000/3000, JVC TT-101/81/71,
Sony TTS-8000/3000, plus the idler icons (Garrard 301/401, Thorens TD-124). Integrated-plinth
decks are weaker (discretionary upgrade). Marantz is a deliberately secondary niche
(only the Model 6300 and TT-1000 Esotec have real pull).

## Work completed (all live)
1. Built/fixed the 9-brand hierarchical tab structure (earlier sessions fixed broken div
   nesting that hid Lenco/Garrard/Thorens — keep all brand divs as direct children of `#brands`).
2. Added 4 brands (Denon, JVC, Sony, Marantz) + the Technics SP-10 section.
3. **Replaced all directional prices with researched secondary-market data + source notes**
   for all 9 brands (HiFiShark, eBay/Reverb solds, Yahoo Auctions JP, Kleinanzeigen,
   Lenco Heaven, vintage-turntable.com, US/UK Audio Mart). Each price table cites sources and
   flags asking-vs-sold and US/EU↔Japan premiums.
4. Added an **"Ano"** (approximate production year) column to all 10 price tables.
5. **Mobile-friendly CSS** (two `@media` blocks): wrapping tab bars, horizontally scrollable
   tables, reduced padding/fonts on phones.
6. Added the `Ok` password.

## Known issues / caveats
- **"Ano" years are approximate production years** from domain knowledge, NOT individually
  source-verified like the prices. Optional future task: verify/refine them (some models
  spanned several years).
- Price figures are mostly **asking prices**; real solds run ~10–20% lower. Thin-data models
  are flagged "estimativa" in the tables.

## IMPORTANT — environment quirks for whoever resumes
1. **Desktop folder access (macOS TCC):** During this session the local working copy at
   `~/Desktop/claudestuff/personal/turntable` lost filesystem read/write access
   ("Operation not permitted" on the folder/file, even for `git`/`cp`/`head`). This is a
   macOS privacy protection on the Desktop folder that got revoked.
   **Fix:** System Settings → Privacy & Security → Full Disk Access → enable your terminal /
   IDE app, then fully quit & reopen it. (Or move the project out of `~/Desktop`.)
   This last commit was made from a `/tmp` clone and pushed, because the Desktop copy was blocked.
   **After restart + restoring access, run:** `git pull` in the project folder to sync this commit
   (including this HANDOFF.md and `tools/verify_structure.py`).
2. **Git auth:** HTTPS / `gh` on this machine resolve to GitHub account `duartegarcia-ui`, which
   does **NOT** have push rights to `duartegarciacnt-crypto/repo` (got 403). **Push via SSH** —
   the SSH key correctly maps to `duartegarciacnt-crypto`. If a clone uses an HTTPS origin, switch it:
   `git remote set-url origin git@github.com:duartegarciacnt-crypto/repo.git`

## How to verify after changes
`tools/verify_structure.py` parses `index.html` and checks: every brand div is a direct child
of `#brands`, tab visibility on load + simulated clicks, every section is non-empty, and price
tables have consistent column counts. Run: `python3 tools/verify_structure.py`
Also sanity-check div balance is equal: count `<div` vs `</div>` in the body.

## Possible next steps (none in progress)
- Verify/refine the "Ano" production years against references.
- Consider a Tier-2 expansion (EMT, Rek-O-Kut, Empire) if desired — discussed but not built.
- Tighten thin-data prices (DP-100, DP-72L, TT-1000 MkII, SP-20, Lenco L84/B55) with more comps.
