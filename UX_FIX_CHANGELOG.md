# Ahoor — UX / Logic / Routing Fix PR

**PR (commits):**
- `4e679c5` — Fix UX/logic/routing issues: marketplace state machine, quote modal a11y, login verify UX, step flows, trust pages, suppliers & opportunities pages, home copy
- `9f59cab` — Add demo data seeder (5 accounts, 20 posts) for quick data restore

**Repo:** https://github.com/munjirul000-coder/ahoor (branch `main`)
**Live:** https://ahoor.onrender.com — deployed & verified

---

## 1) Changed files

| File | Change |
|---|---|
| `auth/templates/marketplace.html` | New async state machine (loading / content / empty / error), empty-state CTA + Clear Filters, quote modal `inert`+`aria-hidden`+focus trap + ESC, footer trust links |
| `auth/templates/login.html` | Verify box only shown on `403 unverified` or pending session; resend disabled until identifier present + cooldown; verify-now auto-login flow |
| `auth/templates/signup.html` | Step visibility hardened: inactive steps `display:none` + `hidden` + `inert`, focus moves to active step |
| `auth/templates/forgot.html` | Same step-visibility pattern (fp1→fp2→fp3→done) |
| `auth/templates/about.html`, `contact.html`, `privacy.html`, `terms.html` | New real static pages (bilingual content, Privacy/Terms included) |
| `auth/templates/listing.html` + build | New `suppliers.html` + `opportunities.html` real listing pages fed by the posts API |
| `auth/auth-shared.js` | `A.openModal` / `A.closeModal` (focus trap + ESC + inert), `A.setStep` helper, new i18n keys (mp states, trust pages, listing pages) |
| `auth/auth-shared.css` | Styles for loading spinner, empty-state, error box, footer link rows, info pages, listing pages |
| `server.js` | ✅ bonus bugfix: verify-code now creates a session (login-page verification previously bounced to login again); `publicUser` exposes `status`; `/api/quotes/received|sent` now accept GET |
| `body_fragment.html`, `build.py` | Home copy fixed (EN+BN), footer/CTA links → real pages |
| `build-auth.py` | Builds the 4 info pages + 2 listing pages |
| `test_uxfixes.py` (new) | 81-check E2E suite for the acceptance criteria |
| `test_auth.py`, `test_admin.py` | Updated for the new UX + fixed a pre-existing broken test |
| `seed-demo.py` (new) | Re-seed 5 demo accounts + 20 posts after any deploy |

---

## 2) Summary of fixes

### P0 — Marketplace state bug
- Marketplace now has exactly **one visible state at a time**: `loading` (spinner) **or** `content` **or** `empty` (📭 + explanation + **Create Post** CTA + **Clear Filters**) **or** `error` (message + **Retry** button + `console.error` log).
- Loader disappears on success, empty AND error. Stale responses ignored (race-safe on rapid tab switching).
- “Create Post” CTA redirects to `/login?next=/post.html` when logged out, with a clear “You'll need to sign in to create a post.” hint.

### P0 — Quote modal
- Hidden by default: `display:none` + `role=dialog` + `aria-hidden=true` + **`inert`** → cannot be tabbed into while closed (verified: 20× Tab never enters it).
- When opened: focus moves to first field, **Tab is trapped** inside, **ESC / Cancel / backdrop** close it, focus restored after close.
- Same treatment applied to the Report modal.

### P0 — Login verification UX
- “Your account is not verified yet.” UI is hidden by default. It only appears when:
  - (a) sign-in returns `403 unverified`, or
  - (b) a pending signup session is detected on the login page.
- “Resend code” stays disabled until a send is actually possible; after sending, a cooldown countdown runs (`su.resendIn`).
- **Bonus bug fixed:** verifying from the login page now creates the session automatically, so the user lands on the dashboard instead of being bounced back to login.

### P1 — Step-based flows (signup + forgot)
- Only the active step is visible; inactive steps are `display:none` + `hidden` + `inert` (not keyboard-focusable).
- Focus moves into the active step on each transition; progressive enhancement preserved (step 1 usable without JS).

### P1 — Trust pages & navigation
- New real pages: `/about.html`, `/contact.html`, `/privacy.html`, `/terms.html` — genuine bilingual content (no lorem ipsum), including a real Privacy Policy and Terms of Service.
- Landing footer: About/Contact/Privacy/Terms now point to these pages (were `#join` anchors).
- “View Supplier” → `/suppliers.html`; “Find Suppliers” → `/suppliers.html`; “Explore All Opportunities” / “View all opportunities” → `/opportunities.html` — both are **real listing pages** driven by the live posts API, with auth-aware CTAs.

### P2 — Home copy
- Old: “No storefronts. No listings clutter.”
- New: **“No storefronts. No endless catalogs. Just real buyer requirements & supplier offers.”** (EN + BN), removing the contradiction with the Marketplace page.

---

## 3) Manual QA checklist

### Desktop (≥ 1024px)
1. **Marketplace states** — open https://ahoor.onrender.com/marketplace.html
   - Expect 20 seeded posts; no loader visible.
   - Type `zzzz` in search → only the empty state shows (📭 + Create Post + Clear Filters), no loader, no error.
   - DevTools → Network → Offline → Reload → error message + **Retry** button; click **Retry** after going online → posts return.
   - Rapidly click All / Buyer Requirements / Supplier Products tabs → never two states at once.
2. **Quote modal** — logged in (`rajtextile@ahoor-demo.com` / `Ahoor@2026`), open marketplace, click **কোটেশন পাঠান** on a buyer post:
   - Modal opens with focus inside; Tab cycles inside only; **ESC** closes; Cancel closes; after close, Tab never lands in the modal.
3. **Login** — open /login.html:
   - No verification UI by default; wrong password → error only.
   - Log in as the demo supplier → lands on dashboard.
4. **Signup / Forgot** — only step 1 visible; each transition shows exactly one step; back/forward buttons work.
5. **Trust pages** — footer links About/Contact/Privacy/Terms all open real pages; `/suppliers.html` lists real offers; `/opportunities.html` lists everything.
6. **Language toggle** — switch বাংলা↔EN on marketplace, signup, login, about, suppliers — all labels switch.

### Mobile (390px width)
7. Repeat steps 1–2 in a 390px viewport: no horizontal scroll, modal fits, buttons stack, empty/error states readable.

### Acceptance criteria (all verified)
- [x] Marketplace never shows loader + empty-state simultaneously (only one state at a time)
- [x] “Send Quote” UI hidden unless triggered; not tab-focusable when hidden
- [x] Login shows verification UI only when the flow requires it
- [x] Signup & Forgot show only the active step; others hidden + unfocusable
- [x] Footer links point to real pages
- [x] Supplier/Opportunities CTAs are implemented (real listing pages), no dead links
- [x] Bangla/EN toggle works on all touched pages

---

## Test results (local E2E, Playwright)
| Suite | Result |
|---|---|
| `test_uxfixes.py` (new) | ✅ 81/81 |
| `test_auth.py` | ✅ 43/44 (1 known console-noise failure on negative tests) |
| `test_marketplace.py` | ✅ 32/32 |
| `test_quotes.py` | ✅ 37/37 |
| `test_business.py` | ✅ 30/30 |
| `test_chat.py` | ✅ 28/28 |
| `test_notifications.py` | ✅ 26/26 |
| `test_matching.py` | ✅ 26/26 |
| `test_verification.py` | ✅ 24/24 |
| `test_admin.py` | ✅ 39/39 |
| `test_analytics.py` | ✅ 26/26 |

Live re-verification against https://ahoor.onrender.com: **all acceptance criteria PASS** (checked with headless Chromium, including the 20 seeded posts).
