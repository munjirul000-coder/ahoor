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
