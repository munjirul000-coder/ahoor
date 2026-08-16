# Ahoor — B2B Marketplace for Bangladesh

Premium bilingual (বাংলা / EN) landing page + **real authentication system**.

## Run it

```bash
cd ahoor
node server.js        # no dependencies needed
# → http://localhost:8080
```

- Landing page: `/`
- Sign in: `/login` · Sign up: `/signup` · Forgot password: `/forgot`
- Protected: `/dashboard` (existing users), `/profile-setup` (new users)

## Architecture

| File | Purpose |
|---|---|
| `server.js` | Zero-dependency Node.js server: static hosting + auth REST API |
| `index.html` | Landing page (self-contained, bilingual, embedded fonts) |
| `login.html` `signup.html` `forgot.html` `dashboard.html` `profile-setup.html` | Auth pages (self-contained; generated from `auth/templates/` by `build-auth.py`) |
| `auth/auth-shared.css` / `auth/auth-shared.js` | Shared auth styles + i18n dictionary & helpers |
| `data/db.json` | Persistent store (auto-created; atomic writes) |
| `test_auth.py` | End-to-end Playwright test suite (42 checks) |

## Security features

- **Passwords**: never stored plaintext — scrypt + per-user random salt, timing-safe comparison
- **Sessions**: random 256-bit tokens, stored only as SHA-256 hashes server-side; `HttpOnly`, `SameSite=Lax` cookies; sessions invalidated on password reset
- **Verification codes**: 6-digit, generated via `crypto.randomInt`, stored hashed, 10-minute expiry, max 5 attempts, 60-second resend cooldown, 5 sends / 15 min
- **Rate limiting**: login locks after 5 failures (15 min), register limited per IP
- **Protected routes**: `/dashboard` and `/profile-setup` redirect to login server-side
- Input validation on both client and server (email, BD mobile `01[3-9]XXXXXXXX`, password policy)
- Security headers on API responses (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`)

> **Dev mode note**: there is no SMS/email gateway in this environment, so verification codes are displayed on-screen in a clearly-labeled "Demo mode" box (and logged to the server console). Set `NODE_ENV=production` to disable this and route codes through a real SMS/email provider.

## i18n

- Default language: **বাংলা**; switcher (`বাংলা | EN`) in the navbar of every page
- Choice stored in `localStorage` (`ahoor-lang`) and shared across all pages
- Every string — forms, errors, success messages, countdowns, dashboard — exists in both languages (see `auth/auth-shared.js` dictionary and `build.py` for the landing page)

## Rebuilding pages

```bash
python3 build-auth.py    # regenerate auth pages after template/dictionary edits
python3 build.py         # regenerate index.html (landing)
```

## Known limitations (by design)

- Dashboard cards, "Complete Profile" and messages are placeholders ("Coming soon") — business profile system is the next build.
- Verification codes arrive via dev-mode display, not real SMS/email.
- Sessions live in `data/db.json`; restart the server to pick up code changes.

---

## Deploy

Push to GitHub → Deploy on Render (free tier):

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/munjirul000-coder/ahoor)

## Features (v2 — Profile + Marketplace)

- **Business profile setup** — role, business name, district (64 districts, bn/en), category, description, logo; editable anytime
- **Marketplace feed** — browse all posts with tabs (All / Buyer Requirements / Supplier Products), search, category & district filters
- **Buyer posts** — requirement with title, category, quantity+unit, budget, location, deadline, description, reference image
- **Supplier posts** — product with MOQ, price (or "Contact for Price"), capacity, images
- **Quote requests** — "Get Quotes" / "Request Quote" buttons; sellers see received quotes in dashboard
- **Dashboard** — profile summary, my posts (edit/close/delete), received quotes, create-post & marketplace shortcuts
- Owner-only editing/deletion enforced server-side (403 otherwise); all pages bilingual

## Features (v3 — Quote & Response System)

- **Supplier → Buyer**: SEND QUOTE on buyer requirement posts — price/unit, auto-calculated total, available quantity, MOQ, delivery time, valid-until, message
- **Buyer → Supplier**: REQUEST QUOTE on supplier posts — required quantity, preferred delivery, budget, message
- **Quote statuses**: pending → accepted / rejected / withdrawn; post owner accepts/rejects, sender withdraws pending quotes; no self-actions
- **Dashboard**: full Received Quotes cards (price, total, qty, delivery, message, status + Accept/Reject/Contact) and My Sent Quotes (status tracking + withdraw)
- **In-app notifications**: new quote/request received, accepted, rejected — unread bell with count, mark-all-read, 30s polling (no email yet)
- **Security**: role gating (supplier/both ↔ buyer/both), duplicate & closed-post prevention, ownership checks on every action
- All new UI fully bilingual (বাংলা/EN)

## Features (v4 — Business Profile System)

- **Full business profile editor** (`/profile-setup.html`): business type (Manufacturer/Supplier/Wholesaler/Buyer/Exporter/Importer/Service/Other), division (8) + district (64) + city + address, products/services, MOQ, production capacity, employees, years in business, business phone/email, website, Facebook
- **Privacy controls**: phone & email visibility — Public / Only logged-in users / Hidden (enforced server-side)
- **Public business profile page** (`/business.html?id=...`): logo, name, type, location, verification status, about, business details, active opportunities, contact per privacy; Edit button only for owner
- **Profile completion %**: live bar in editor + dashboard card, friendly suggestion; post page shows tip banner when <60%
- **Marketplace cards**: business name links to public profile with logo, type, location
- Business logo upload with preview (400KB limit, data-URI storage)
- Fully bilingual (বাংলা/EN); 30/30 business E2E tests + full regression pass

## Features (v4.1 — Role-based Signup Business Info)

- After choosing Account Type during signup, a **Business Info step** shows role-specific fields:
  - **Buyer**: company name, products you usually buy, product category, typical quantity, location
  - **Supplier / Manufacturer**: company name, products you make/supply, category, MOQ, location
  - **Both**: both buyer & supplier sections
- All fields optional (Skip for now) — editable anytime from the Business Profile
- Saved to profile: businessName, category, district, buyProducts, typicalQty, productsServices, moq
- Public business page shows "Products usually bought" + "Typical quantity" when filled

## Features (v5 — Real-time Business Messaging / Chat)

- **Private conversations** between businesses — start from Business Profile ("Contact Business"), Marketplace post (💬 button), Quote cards ("Contact Supplier"), or directly `/messages.html?with=USERID`
- **Messages page**: conversation list (logo, name, last message, time, unread badge) + chat pane (bubbles, timestamps, day separators); mobile shows list first with back button
- **Text + image messages**: attach JPG/PNG/WEBP (≤1.5MB, client+server validated), preview before sending, remove option, click-to-open lightbox
- **Real-time via SSE** (`/api/stream`) — new messages appear instantly; polling fallback (list 20s, chat 6s) only when tab visible
- **Unread counts**: badge on conversation items + dashboard Messages card; auto-cleared on read
- **Security**: participants-only access (403 otherwise), unauthenticated redirect, safe image validation, input limits — no secrets exposed
- Fully bilingual (বাংলা/EN); 28/28 chat E2E tests + full regression pass

## Features (v5.1 — Real-time In-App Notification System)

- **Notification events**: new quote, quote request, quote accepted/rejected (with business name), new message — created automatically on each action
- **Dedicated page** `/notifications.html`: All / Unread / Read tabs, mark-one-read (click), mark-all-read, delete individual notifications, empty states
- **Bell everywhere**: dashboard bell + messages page bell — unread count, dropdown panel, "View all" link
- **Deep links**: notification click opens the right resource — quote → dashboard quotes section, accepted/rejected → sent quotes, message → chat conversation
- **Real-time via SSE**: new notifications appear instantly (30s polling fallback)
- **Security**: users see/manage only their own notifications (404 otherwise), all links authorized
- Fully bilingual (বাংলা/EN); 26/26 notifications E2E tests + full regression pass

## Features (v6 — Admin Panel)

- **Admin role**: set `ADMIN_EMAIL` env var — that email becomes admin on signup; `/admin` protected server-side (normal users redirected, API 403)
- **Admin dashboard**: real stats (users, buyers, suppliers, businesses, posts, open buyer reqs, supplier offers, quotes, conversations, reports, pending verification) + recent signups/posts
- **User management**: search, filter by type, suspend/reactivate/disable/delete (with confirmation), view status
- **Business management**: search, filter by business type & verification status, view public profile, suspend
- **Post management**: search, filter by type/category/location/status, close/open/remove (with confirmation)
- **Reports**: users can report business/post from public pages; admin sees reporter (minimal info) + reason + target, resolve/dismiss
- **Verification**: businesses apply from profile; admin approves/rejects (with reason); status shows on profiles
- **Activity log**: every admin action recorded (suspend, reactivate, remove post, verification, report actions)
- **Privacy**: no unrestricted access to private conversations (only via valid report workflow)
- Fully bilingual (বাংলা/EN); responsive; 39/39 admin E2E tests + full regression pass

## Features (v7 — Smart Business Matching System)

- **Rule-based matching engine** (no fake AI): scores by category match (+40), product keywords via category keyword map (+30), text keyword overlap (+25), business-type relevance (+10), location match (+10), quantity/MOQ/capacity compatibility (+10/-10)
- **Match levels**: High / Medium / Low (Low filtered out); raw scores never exposed to clients
- **`/api/matches`**: buyer gets relevant supplier offers + supplier businesses; supplier gets relevant buyer requirements — with type/category/location/level filters
- **Matched Opportunities page** (`/matches.html`): tabs (Best / Buyer / Supplier / Saved), filters, match-level badges, View Business / View Offer / Message actions, explanation note ("Matched based on your business profile and products.")
- **Dashboard "Recommended for You"**: top 4 matches with 🔥 count + View All Matches link
- **Saved Opportunities**: save/remove/bookmark, owner-only access
- **Notifications**: high-match posts trigger `opportunity_match` notification (deduplicated per post, no spam)
- Fully bilingual (বাংলা/EN); 26/26 matching E2E tests + full regression pass

## Features (v8 — Business Verification System)

- **Apply flow**: Unverified → Apply (business info + documents: Trade License / Registration / Other Proof — PDF/JPG/PNG ≤1.5MB, client+server validated, private) → Pending Review → Verified / Rejected
- **Verify page** (`/verify.html`): status card, 3-step progress (Info ✓ → Docs ✓ → Under Review), document pick/preview/remove, rejection reason + reapply, withdraw
- **Admin review**: Verification page shows pending requests with contact info + document previews (images inline, PDF link); approve / reject with optional reason; owner gets in-app notification on submit/approve/reject
- **Verified badge**: shown on Business Profile, Marketplace post cards, Received Quote cards, Chat header — only when truly verified
- **Security**: documents never public — only owner (own app) and admins can view; non-admin API access blocked (403); validated uploads (no exe/svg)
- Fully bilingual (বাংলা/EN); 24/24 verification E2E tests + full regression pass

## Features (v9 — Business Analytics & Insights)

- **Real analytics only** (no fake numbers): profile views, post views, messages received/sent, quotes/requests received, quotes sent, accepted/rejected quotes, active posts, saved opportunities, new matches
- **View tracking**: unique-ish profile & post views (same viewer counted once per 30 min), stored in `events` collection
- **Time filters**: Last 7 / 30 / 90 days / All time — every stat updates
- **Analytics page** (`/analytics.html`): summary cards, post performance table (views/quotes/requests/saves per post + View Insights), quote performance bars, messaging bars, real recent-activity feed
- **Dashboard Business Insights** section: 5 summary cards + recent activity + "View Full Analytics"
- **Post insights** (`/api/posts/insights`): owner-only, per-post views/quotes/requests/saves
- **Privacy**: users see only their own analytics (403 otherwise); no visitor identity exposed
- Buyer/Supplier/Both-friendly labels; fully bilingual (বাংলা/EN); mobile responsive
- 26/26 analytics E2E tests + full regression pass
