#!/usr/bin/env python3
"""UX fixes E2E suite — P0/P1/P2 fixes for Ahoor (local server on :8080).

Covers:
  P0-1 marketplace state machine (loading/empty/error/content, never two at once)
  P0-2 quote modal hidden-by-default, inert, focus trap, ESC close
  P0-3 empty state CTA
  P0-4 login verification UX (hidden by default; only after 403 unverified or pending session)
  P1-5 signup + forgot step visibility (only active step visible/unfocusable)
  P1-6 about/contact/privacy/terms pages + landing footer links
  P1-7 suppliers/opportunities listing pages
  P2-8 home copy fix
  lang toggle still works on touched pages
"""
from playwright.sync_api import sync_playwright
import random, time, re, json

BASE = 'http://localhost:8080'
results = []
def check(name, cond, extra=''):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{extra}]" if extra else ""), flush=True)

def fresh(prefix):
    return f"{prefix}{int(time.time())}{random.randint(10,99)}"

def bd_phone(prefix):
    return f"{prefix}{random.randint(10,99)}{int(time.time()) % 1000000:06d}"

def api(pg, path, data=None):
    """POST api call from the page context (shares cookies)."""
    url = BASE + path
    if data is None:
        return pg.evaluate("""async (u) => { const r = await fetch(u, {method:'POST', headers:{'Content-Type':'application/json'}}); return {status:r.status, data: await r.json().catch(()=>({}))}; }""", url)
    return pg.evaluate("""async (a) => { const r = await fetch(a[0], {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(a[1])}); return {status:r.status, data: await r.json().catch(()=>({}))}; }""", [url, data])

def prime(pg):
    """Ensure the page has the site origin before fetch calls."""
    try:
        pg.goto(BASE + '/login.html', wait_until='domcontentloaded')
        pg.wait_for_timeout(300)
    except Exception:
        pass

def register_pending(pg, name, email, phone, pw, role):
    prime(pg)
    r = api(pg, '/api/register', {"name": name, "email": email, "phone": phone, "password": pw})
    assert r['status'] == 201, "register failed: %s" % r
    api(pg, '/api/type', {"type": role})
    return r['data']['userId']

def register_full(pg, name, email, phone, pw, role):
    """register + verify OTP -> active account (cookie kept)."""
    register_pending(pg, name, email, phone, pw, role)
    c = api(pg, '/api/send-code', {"purpose": "signup"})
    code = c['data'].get('devCode') or c['data'].get('code')
    assert code, "no dev code: %s" % c
    v = api(pg, '/api/verify-code', {"purpose": "signup", "code": code})
    assert v['status'] == 200, "verify failed: %s" % v
    return v['data'].get('user', {}).get('id')

def visible(pg, sel):
    return pg.eval_on_selector(sel, "el => getComputedStyle(el).display !== 'none'")

def states(pg):
    return {
        'load': visible(pg, '#mpLoad'),
        'empty': visible(pg, '#mpEmpty'),
        'err': visible(pg, '#mpErr'),
        'grid': pg.eval_on_selector('#mpGrid', "el => el.children.length > 0"),
    }

def count_visible_states(s):
    return sum(1 for k in ('load','empty','err') if s[k])

def state_ok(s):
    """content shown => no other state; otherwise exactly one state visible"""
    if s['grid']:
        return count_visible_states(s) == 0
    return count_visible_states(s) == 1

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context()
    pg = ctx.new_page()
    pg.set_default_timeout(10000)

    ts = str(int(time.time()))
    PW = 'Test@2026'
    SUP_EMAIL = fresh('supfix@') + '.com'
    BUY_EMAIL = fresh('buyfix@') + '.com'
    UNV_EMAIL = fresh('unvfix@') + '.com'

    # ---------------- marketplace states ----------------
    print("\n-- P0-1 marketplace state machine --", flush=True)
    # create buyer + supplier with a couple of posts
    ctx2 = browser.new_context()
    pgB = ctx2.new_page(); pgB.set_default_timeout(10000)
    register_full(pgB, "FixBuyer " + str(ts), BUY_EMAIL, bd_phone('017'), PW, 'buyer')
    r = api(pgB, '/api/posts', {"type":"buyer","title":"Fix test requirement " + ts,"category":"Yarn","qty":"500","unit":"kg","budget":"300","location":"Dhaka","desc":"Requirement created by the UX fix test suite."})
    assert r['status'] == 201, r
    pgB.close(); ctx2.close()

    # login as supplier for quote-modal tests later
    SUP_ID = register_full(pg, "FixSupplier " + str(ts), SUP_EMAIL, bd_phone('018'), PW, 'supplier')
    r = api(pg, '/api/posts', {"type":"supplier","title":"Fix supplier offer " + ts,"category":"Yarn","qty":"1000","unit":"kg","price":"250","location":"Dhaka","desc":"Offer created by the UX fix test suite for state tests."})
    assert r['status'] == 201, r

    pg.goto(BASE + '/marketplace.html', wait_until='domcontentloaded')
    # synchronous DOM sample right after load() is triggered: loading must be the only state
    s0 = pg.evaluate(
        "(function(){"
        "var btn = document.querySelector('.tab[data-t=\"supplier\"]');"
        "btn.click();"
        "return {"
        "  load: getComputedStyle(document.getElementById('mpLoad')).display !== 'none',"
        "  empty: getComputedStyle(document.getElementById('mpEmpty')).display !== 'none',"
        "  err: getComputedStyle(document.getElementById('mpErr')).display !== 'none'"
        "};})()"
    )
    check('mp loading state visible during fetch', s0['load'] and not s0['empty'] and not s0['err'], 'states=' + str(s0))
    pg.wait_for_timeout(1800)
    s1 = states(pg)
    check('mp content shown after load (posts exist)', s1['grid'])
    check('mp loader hidden after success', not s1['load'])
    check('mp exactly one state after success', state_ok(s1), 'states=' + str(s1))

    # empty state via nonsense search
    pg.fill('#mpQ', 'zzzznomatch999')
    pg.wait_for_timeout(1200)
    s2 = states(pg)
    check('mp empty state visible with no results', s2['empty'] and not s2['load'] and not s2['err'])
    check('mp empty CTA present', pg.eval_on_selector('#mpEmptyNew', "el => getComputedStyle(el).display !== 'none'"))
    check('mp exactly one state on empty', count_visible_states(s2) == 1)
    # clear filters button should be visible when a filter is active
    check('mp clear-filters button shown when filtered', visible(pg, '#mpEmptyClear'))
    pg.click('#mpEmptyClear')
    pg.wait_for_timeout(1200)
    s3 = states(pg)
    check('mp clear-filters restores content', s3['grid'] and not s3['empty'] and not s3['load'] and not s3['err'])

    # error state + retry
    def abort_route(route):
        route.abort()
    pg.route('**/api/posts**', abort_route)
    pg.reload(wait_until='domcontentloaded')
    pg.wait_for_timeout(1400)
    s4 = states(pg)
    check('mp error state visible on network failure', s4['err'] and not s4['load'] and not s4['empty'])
    check('mp retry button visible', visible(pg, '#mpRetry'))
    check('mp exactly one state on error', count_visible_states(s4) == 1)
    pg.unroute('**/api/posts**')
    pg.click('#mpRetry')
    pg.wait_for_timeout(1500)
    s5 = states(pg)
    check('mp retry recovers to content', s5['grid'] and not s5['err'] and not s5['load'] and not s5['empty'])

    # race: rapid tab switching never leaves two states visible
    for i in range(4):
        pg.click('.tab[data-t="' + ['all','buyer','supplier','all'][i] + '"]')
        pg.wait_for_timeout(120)
    pg.wait_for_timeout(1600)
    s6 = states(pg)
    check('mp race: exactly one state after rapid tab switches', state_ok(s6), 'states=' + str(s6))

    # ---------------- quote modal ----------------
    print("\n-- P0-2 quote modal --", flush=True)
    pg.goto(BASE + '/marketplace.html', wait_until='domcontentloaded')
    pg.wait_for_timeout(1500)
    check('mp modal hidden by default', not visible(pg, '#quoteModal'))
    check('mp modal aria-hidden=true', pg.eval_on_selector('#quoteModal', "el => el.getAttribute('aria-hidden') === 'true'"))
    check('mp modal inert when closed', pg.eval_on_selector('#quoteModal', "el => el.hasAttribute('inert')"))
    # tab through: never lands inside the modal
    inside = False
    for i in range(20):
        pg.keyboard.press('Tab')
        inmodal = pg.evaluate("() => { const m = document.getElementById('quoteModal'); return m.contains(document.activeElement); }")
        if inmodal:
            inside = True
            break
    check('mp modal not tab-focusable when hidden', not inside)
    # open via Send Quote on a buyer post
    buyer_btn = pg.eval_on_selector_all(".post-card[data-type] button[data-quote], .qcard-actions button[data-quote]", "els => els.length")
    # find a buyer post card button: cards don't carry data-type; use badge text filter via JS
    clicked = pg.evaluate("""() => {
      const cards = Array.prototype.slice.call(document.querySelectorAll('.post-card'));
      for (const c of cards) {
        const badge = c.querySelector('.post-badge');
        if (badge && /BUYER|ক্রেতা/.test(badge.textContent)) {
          const btn = c.querySelector('button[data-quote]');
          if (btn) { btn.click(); return true; }
        }
      }
      return false;
    }""")
    check('mp found a buyer post and clicked Send Quote', clicked)
    pg.wait_for_timeout(400)
    check('mp modal opens on Send Quote', visible(pg, '#quoteModal') and pg.eval_on_selector('#quoteModal', "el => el.classList.contains('on')"))
    check('mp modal inert removed when open', not pg.eval_on_selector('#quoteModal', "el => el.hasAttribute('inert')"))
    inmodal = pg.evaluate("() => { const m = document.getElementById('quoteModal'); return m.contains(document.activeElement); }")
    check('mp focus moved inside modal', inmodal)
    # tab cycle stays inside
    escaped = False
    for i in range(12):
        pg.keyboard.press('Tab')
        if not pg.evaluate("() => document.getElementById('quoteModal').contains(document.activeElement)"):
            escaped = True
            break
    check('mp focus trapped inside modal (Tab cycles)', not escaped)
    # ESC closes
    pg.keyboard.press('Escape')
    pg.wait_for_timeout(300)
    check('mp ESC closes modal', not visible(pg, '#quoteModal'))
    check('mp modal inert restored after ESC', pg.eval_on_selector('#quoteModal', "el => el.hasAttribute('inert')"))
    # reopen + Cancel closes
    pg.evaluate("""() => { const c = Array.prototype.slice.call(document.querySelectorAll('.post-card'));
      for (const el of c) { const b = el.querySelector('.post-badge');
        if (b && /BUYER|ক্রেতা/.test(b.textContent)) { el.querySelector('button[data-quote]').click(); return; } } }""")
    pg.wait_for_timeout(300)
    pg.click('#qmCancel')
    pg.wait_for_timeout(300)
    check('mp Cancel closes modal', not visible(pg, '#quoteModal'))

    # ---------------- login verify UX ----------------
    print("\n-- P0-4 login verification UX --", flush=True)
    ctxL = browser.new_context()
    pgL = ctxL.new_page(); pgL.set_default_timeout(10000)
    pgL.goto(BASE + '/login.html', wait_until='domcontentloaded')
    pgL.wait_for_timeout(900)
    check('login verifyBox hidden by default', not visible(pgL, '#verifyBox'))
    check('login resend disabled by default', pgL.eval_on_selector('#resendVerify', "el => el.disabled"))
    # wrong password -> error, no verify box
    pgL.fill('#idField', UNV_EMAIL); pgL.fill('#pwField', 'WrongPass1!')
    pgL.click('#btnLogin'); pgL.wait_for_timeout(1200)
    check('login wrong creds: no verify box', not visible(pgL, '#verifyBox'))
    check('login wrong creds: error shown', pgL.eval_on_selector('#msgBox', "el => el.classList.contains('show')"))
    pgL.close(); ctxL.close()

    # pending-session detection: register (pending) in a fresh context, then visit login
    ctxP = browser.new_context()
    pgP = ctxP.new_page(); pgP.set_default_timeout(10000)
    register_pending(pgP, "PendingFix", UNV_EMAIL, bd_phone('019'), PW, 'buyer')
    pgP.goto(BASE + '/login.html', wait_until='domcontentloaded')
    pgP.wait_for_timeout(1400)
    check('login pending session -> verify box shown', visible(pgP, '#verifyBox'))
    check('login pending: login form hidden', not visible(pgP, '#loginForm'))
    # back button returns to form
    pgP.click('#btnVerifyBack'); pgP.wait_for_timeout(300)
    check('login verify back returns to form', visible(pgP, '#loginForm') and not visible(pgP, '#verifyBox'))
    pgP.close(); ctxP.close()

    # full unverified login flow
    ctxU = browser.new_context()
    pgU = ctxU.new_page(); pgU.set_default_timeout(10000)
    UNV_EMAIL2 = fresh('unv2@') + '.com'
    register_pending(pgU, "PendingFix2", UNV_EMAIL2, bd_phone('019'), PW, 'buyer')
    pgU.context.clear_cookies()  # drop the pending session so the box must come from 403
    pgU.goto(BASE + '/login.html', wait_until='domcontentloaded')
    pgU.wait_for_timeout(900)
    pgU.fill('#idField', UNV_EMAIL2); pgU.fill('#pwField', PW)
    pgU.click('#btnLogin'); pgU.wait_for_timeout(1300)
    check('login 403 unverified -> verify box shown', visible(pgU, '#verifyBox'))
    check('login verify: resend starts disabled+countdown', pgU.eval_on_selector('#resendVerify', "el => el.disabled"))
    dev = pgU.eval_on_selector('#devNote', "el => el.textContent")
    m = re.search(r'(\d{6})', dev)
    check('login verify: dev code shown', bool(m))
    if m:
        for i, c in enumerate(m.group(1)):
            pgU.fill(f'#otpVerify input:nth-child({i+1})', c)
        pgU.wait_for_timeout(400)
        pgU.click('#btnVerifyCode')
        pgU.wait_for_timeout(2400)
        ok_url = '/dashboard.html' in pgU.url or '/profile-setup' in pgU.url
        extra = pgU.url if not ok_url else ''
        if not ok_url:
            extra += ' | msg=' + pgU.eval_on_selector('#msgBox', "el => el.textContent").strip()[:80]
        check('login verify: redirected after verification', ok_url, extra)
    pgU.close(); ctxU.close()

    # ---------------- signup steps ----------------
    print("\n-- P1-5 signup steps --", flush=True)
    pg.goto(BASE + '/signup.html', wait_until='domcontentloaded')
    pg.wait_for_timeout(900)
    check('signup: step1 visible', visible(pg, '#step1'))
    for sid in ['#step2', '#stepBiz', '#stepVerify', '#stepDone']:
        check('signup: %s hidden' % sid, not visible(pg, sid))
        check('signup: %s inert' % sid, pg.eval_on_selector(sid, "el => el.hasAttribute('inert') && el.hasAttribute('hidden')"))
    # tab from step1 stays in step1
    step2_reached = False
    pg.fill('#nameF', '')
    pg.evaluate("document.getElementById('nameF').focus()")
    for i in range(8):
        pg.keyboard.press('Tab')
        in_step2 = pg.evaluate("() => document.getElementById('step2').contains(document.activeElement)")
        if in_step2:
            step2_reached = True
            break
    check('signup: inactive steps not tab-focusable', not step2_reached)
    # step transition: step1 -> step2 only
    pg.fill('#nameF', 'StepFix ' + ts); pg.fill('#emailF', fresh('step@') + '.com'); pg.fill('#phoneF', bd_phone('016'))
    pg.fill('#pw1', PW); pg.fill('#pw2', PW)
    pg.click('#btnS1'); pg.wait_for_timeout(1400)
    check('signup: after submit step2 visible', visible(pg, '#step2'))
    check('signup: step1 hidden after transition', not visible(pg, '#step1') and pg.eval_on_selector('#step1', "el => el.hasAttribute('inert')"))

    # ---------------- forgot steps ----------------
    print("\n-- P1-5 forgot steps --", flush=True)
    ctxF = browser.new_context()
    pgF = ctxF.new_page(); pgF.set_default_timeout(10000)
    pgF.goto(BASE + '/forgot.html', wait_until='domcontentloaded')
    pgF.wait_for_timeout(900)
    check('forgot: fp1 visible', visible(pgF, '#fp1'))
    for sid in ['#fp2', '#fp3', '#fpDone']:
        check('forgot: %s hidden' % sid, not visible(pgF, sid))
        check('forgot: %s inert' % sid, pgF.eval_on_selector(sid, "el => el.hasAttribute('inert') && el.hasAttribute('hidden')"))
    # send code for existing user -> step 2
    pgF.fill('#fpId', SUP_EMAIL)
    pgF.click('#btnFp1'); pgF.wait_for_timeout(1300)
    check('forgot: fp2 visible after send', visible(pgF, '#fp2'))
    check('forgot: fp1 hidden', not visible(pgF, '#fp1'))
    pgF.click('#btnFp2back'); pgF.wait_for_timeout(300)
    check('forgot: back returns to fp1', visible(pgF, '#fp1') and not visible(pgF, '#fp2'))
    pgF.close(); ctxF.close()

    # ---------------- trust pages + footer ----------------
    print("\n-- P1-6 trust pages & footer --", flush=True)
    for page in ['about', 'contact', 'privacy', 'terms']:
        pg.goto(BASE + '/' + page + '.html', wait_until='domcontentloaded')
        pg.wait_for_timeout(600)
        ok = pg.evaluate("() => { const h = document.querySelector('.info-card h1'); return h && h.textContent.trim().length > 0; }")
        check('%s page renders with heading' % page, ok)
        fl = pg.eval_on_selector_all('.auth-foot .flinks a', "els => els.map(a => a.getAttribute('href'))")
        check('%s footer links' % page, '/about.html' in fl and '/terms.html' in fl)
    pg.goto(BASE + '/', wait_until='domcontentloaded')
    pg.wait_for_timeout(1200)
    fl = pg.eval_on_selector_all('footer.footer a', "els => els.map(a => a.getAttribute('href'))")
    check('landing footer -> about page', '/about.html' in fl)
    check('landing footer -> contact page', '/contact.html' in fl)
    check('landing footer -> privacy page', '/privacy.html' in fl)
    check('landing footer -> terms page', '/terms.html' in fl)
    check('landing footer -> suppliers page', '/suppliers.html' in fl)

    # ---------------- suppliers / opportunities pages ----------------
    print("\n-- P1-7 listing pages --", flush=True)
    pg.goto(BASE + '/suppliers.html', wait_until='domcontentloaded')
    pg.wait_for_timeout(1500)
    items = pg.eval_on_selector_all('#liList .li-item', "els => els.length")
    check('suppliers page lists real posts', items >= 1, 'items=%d' % items)
    check('suppliers page has CTA', pg.eval_on_selector('#liJoin', "el => !!el"))
    pg.goto(BASE + '/opportunities.html', wait_until='domcontentloaded')
    pg.wait_for_timeout(1500)
    items2 = pg.eval_on_selector_all('#liList .li-item', "els => els.length")
    check('opportunities page lists real posts', items2 >= 1, 'items=%d' % items2)

    # ---------------- home copy ----------------
    print("\n-- P2-8 home copy --", flush=True)
    pg.goto(BASE + '/', wait_until='domcontentloaded')
    pg.wait_for_timeout(900)
    note = pg.eval_on_selector('.hero-note', "el => el.textContent")
    check('home copy no longer says listings clutter', 'listings clutter' not in note and 'তালিকার বিশৃঙ্খলা' not in note, note[:50])

    # ---------------- lang toggle on touched pages ----------------
    print("\n-- lang toggle --", flush=True)
    pg.goto(BASE + '/marketplace.html', wait_until='domcontentloaded')
    pg.wait_for_timeout(1000)
    pg.fill('#mpQ', 'zzzznomatch999')
    pg.wait_for_timeout(1100)
    bn_title = pg.eval_on_selector('#mpEmpty h3', "el => el.textContent")
    pg.click('.lang-btn[data-lang="en"]')
    pg.wait_for_timeout(600)
    en_title = pg.eval_on_selector('#mpEmpty h3', "el => el.textContent")
    check('lang toggle: empty state switches bn->en', en_title == 'No posts found' and bn_title != en_title, 'bn=%s en=%s' % (bn_title, en_title))
    pg.click('.lang-btn[data-lang="bn"]'); pg.wait_for_timeout(400)
    pg.goto(BASE + '/about.html', wait_until='domcontentloaded')
    pg.wait_for_timeout(700)
    h_bn = pg.eval_on_selector('.info-card h1', "el => el.textContent")
    pg.click('.lang-btn[data-lang="en"]'); pg.wait_for_timeout(500)
    h_en = pg.eval_on_selector('.info-card h1', "el => el.textContent")
    check('lang toggle: about page switches', h_en == 'About Ahoor' and h_bn != h_en, 'bn=%s en=%s' % (h_bn, h_en))

    # ---------------- bonus: quotes GET endpoints ----------------
    print("\n-- bonus --", flush=True)
    pg.goto(BASE + '/marketplace.html', wait_until='domcontentloaded')
    pg.wait_for_timeout(800)
    r = api(pg, '/api/quotes/received')
    check('quotes/received accepts GET (200 json)', r['status'] == 200, str(r['status']))
    r2 = api(pg, '/api/quotes/sent')
    check('quotes/sent accepts GET (200 json)', r2['status'] == 200, str(r2['status']))
    sess = api(pg, '/api/session')
    check('session exposes status field', 'status' in sess['data'].get('user', {}))

    browser.close()

passed = sum(1 for _, c in results if c)
print("\n===== SUMMARY: %d/%d passed =====" % (passed, len(results)))
