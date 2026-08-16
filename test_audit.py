#!/usr/bin/env python3
"""Ahoor full audit suite — security/access control, chat images, i18n, responsive,
console errors, session, input validation. Local server :8080."""
from playwright.sync_api import sync_playwright
import random, time, re, json

BASE = 'http://localhost:8080'
results = []
def check(name, cond, extra=''):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{extra}]" if extra else ""), flush=True)

def fresh(p): return f"{p}{int(time.time())}{random.randint(10,99)}"
def bd_phone(p): return f"{p}{random.randint(10,99)}{int(time.time()) % 1000000:06d}"

def api(pg, path, data=None):
    url = BASE + path
    if data is None:
        return pg.evaluate("async (u) => { const r = await fetch(u, {method:'POST', headers:{'Content-Type':'application/json'}}); return {status:r.status, data: await r.json().catch(()=>({}))}; }", url)
    return pg.evaluate("async (a) => { const r = await fetch(a[0], {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(a[1])}); return {status:r.status, data: await r.json().catch(()=>({}))}; }", [url, data])

def prime(pg):
    try:
        pg.goto(BASE + '/login.html', wait_until='domcontentloaded'); pg.wait_for_timeout(300)
    except Exception: pass

def reg_full(pg, name, email, phone, pw, role, profile=None):
    prime(pg)
    r = api(pg, '/api/register', {"name": name, "email": email, "phone": phone, "password": pw})
    assert r['status'] == 201, "register: %s" % r
    api(pg, '/api/type', {"type": role})
    c = api(pg, '/api/send-code', {"purpose": "signup"})
    code = c['data'].get('devCode')
    assert code, c
    v = api(pg, '/api/verify-code', {"purpose": "signup", "code": code})
    assert v['status'] == 200, v
    if profile:
        p = api(pg, '/api/profile', profile)
        assert p['status'] == 200, p
    s = api(pg, '/api/session')
    return s['data']['user']

def uid(pg):
    s = api(pg, '/api/session')
    return s['data']['user']['id']

def vis(pg, sel):
    return pg.eval_on_selector(sel, "el => getComputedStyle(el).display !== 'none'")

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctxA = b.new_context(); pgA = ctxA.new_page(); pgA.set_default_timeout(12000)
    ctxB = b.new_context(); pgB = ctxB.new_page(); pgB.set_default_timeout(12000)
    ctxC = b.new_context(); pgC = ctxC.new_page(); pgC.set_default_timeout(12000)

    ts = str(int(time.time()))
    PW = 'Audit@2026'

    # ---------- setup: buyer A, supplier B, outsider C ----------
    print("\n-- setup --", flush=True)
    A = reg_full(pgA, "Audit Buyer", fresh('auda@') + '.com', bd_phone('017'), PW, 'buyer',
                 dict(businessName="Audit Buyer Co", district="Dhaka", category="Yarn & Fabric"))
    B = reg_full(pgB, "Audit Supplier", fresh('audb@') + '.com', bd_phone('018'), PW, 'supplier',
                 dict(businessName="Audit Supplier Co", district="Gazipur", category="Yarn & Fabric"))
    reg_full(pgC, "Audit Outsider", fresh('audc@') + '.com', bd_phone('019'), PW, 'buyer',
             dict(businessName="Audit Outsider Co", district="Chattogram", category="Agro & Food"))
    check("setup: 3 accounts created", bool(A['id'] and B['id']))

    # posts: A buyer requirement, B supplier offer
    pr = api(pgA, '/api/posts', {"type":"buyer","title":"Audit requirement custom t-shirts 5000 pcs","category":"Garments & Apparel","qty":"5000","unit":"pcs","budget":"300","location":"Dhaka","desc":"Audit test requirement for t-shirt production with enough detail."})
    po = api(pgB, '/api/posts', {"type":"supplier","title":"Audit supplier offer custom t-shirts","category":"Garments & Apparel","qty":"20000","unit":"pcs","price":"280","location":"Gazipur","desc":"Audit test supplier offer for t-shirt manufacturing with capacity."})
    check("setup: posts created", pr['status'] == 201 and po['status'] == 201)
    REQ_ID = pr['data']['post']['id']; OFF_ID = po['data']['post']['id']

    # quote from supplier B -> buyer A requirement
    q = api(pgB, '/api/quotes', {"postId": REQ_ID, "pricePerUnit":"275","availableQty":"5000","moq":"1000","deliveryTime":"10 days","validUntil":"2026-10-01","message":"Audit quote: we can supply 5000 pcs at 275 BDT."})
    check("setup: quote sent", q['status'] == 201, str(q['status']))
    QID = q['data']['quote']['id']

    # conversation A-B
    cv = api(pgA, '/api/conversations', {"withUserId": B['id']})
    check("setup: conversation", cv['status'] == 200)
    CONV = cv['data']['conversation']['id']
    api(pgA, '/api/conversations/' + CONV + '/messages', {"text": "Hello supplier, we received your quote."})

    # ---------- 1. access control ----------
    print("\n-- access control --", flush=True)
    # C cannot touch A-B conversation
    rc = api(pgC, '/api/conversations/' + CONV + '/messages', {"text": "sneak peek"})
    check("outsider cannot POST to others' conversation", rc['status'] == 403, str(rc['status']))
    rcg = pgC.evaluate("async (u) => { const r = await fetch(u); return {status:r.status}; }", BASE + '/api/conversations/' + CONV + '/messages')
    check("outsider cannot GET others' conversation", rcg['status'] == 403, str(rcg['status']))
    # C cannot respond to B's quote on A's post
    rr = api(pgC, '/api/quotes/' + QID + '/respond', {"action": "accept"})
    check("outsider cannot respond to quote", rr['status'] in (403, 404), str(rr['status']))
    rw = api(pgC, '/api/quotes/' + QID + '/withdraw')
    check("outsider cannot withdraw quote", rw['status'] in (403, 404), str(rw['status']))
    # C's received quotes = only own posts' quotes (should be 0)
    rcq = api(pgC, '/api/quotes/received')
    check("received quotes scoped to own posts", len(rcq['data'].get('quotes', [])) == 0)
    # C cannot see A's post insights
    ri = pgC.evaluate("async (u) => { const r = await fetch(u); return {status:r.status}; }", BASE + '/api/posts/insights?postId=' + REQ_ID)
    check("outsider cannot view post insights", ri['status'] == 403, str(ri['status']))
    # C cannot edit B's profile via profile API (session-scoped; must not change B)
    api(pgC, '/api/profile', {"businessName": "HACKED NAME"})
    sb = api(pgB, '/api/session')
    check("profile edit is session-scoped (B unchanged)", sb['data']['user']['businessName'] == 'Audit Supplier Co')

    # admin APIs blocked for normal user
    for path in ['/api/admin/stats', '/api/admin/users', '/api/admin/businesses', '/api/admin/posts',
                 '/api/admin/reports', '/api/admin/verification-requests', '/api/admin/log']:
        r = api(pgA, path)
        check("normal user blocked: " + path, r['status'] == 403, str(r['status']))
    # anon blocked
    ctxN = b.new_context(); pgN = ctxN.new_page(); pgN.set_default_timeout(12000)
    prime(pgN)
    rn = api(pgN, '/api/admin/stats')
    check("anon blocked: admin/stats", rn['status'] in (401, 403), str(rn['status']))
    # SSE requires session
    rss = pgN.evaluate("async (u) => { const r = await fetch(u); return {status:r.status}; }", BASE + '/api/stream')
    check("SSE requires session", rss['status'] == 401, str(rss['status']))
    # protected pages redirect anon
    for page in ['dashboard.html','post.html','messages.html','matches.html','verify.html','analytics.html','admin.html']:
        r = pgN.request.get(BASE + '/' + page, max_redirects=0)
        check("anon redirected: " + page, r.status == 302 and 'login' in r.headers.get('location',''), "%s -> %s" % (r.status, r.headers.get('location','')[:50]))

    # ---------- 2. input validation ----------
    print("\n-- input validation --", flush=True)
    r1 = api(pgN, '/api/register', {"name":"X","email":"not-an-email","phone":"123","password":"weak"})
    check("register: invalid email/phone/password rejected", r1['status'] == 400, str(r1['status']))
    r2 = api(pgN, '/api/login', {"identifier":"audit","password":"x"})
    check("login: invalid creds 401", r2['status'] == 401, str(r2['status']))
    r3 = api(pgA, '/api/posts', {"type":"buyer","title":"ab","category":"Yarn","location":"Dhaka","desc":"short"})
    check("post: short title rejected", r3['status'] == 400, str(r3['status']))
    r4 = api(pgA, '/api/posts', {"type":"buyer","title":"Valid long enough title","category":"Yarn","location":"Dhaka","desc":"x"})
    check("post: short desc rejected", r4['status'] == 400, str(r4['status']))
    r5 = api(pgA, '/api/posts', {"type":"buyer","title":"Valid title here","category":"Yarn","location":"Dhaka","desc":"a valid description text","image":"x" * 500000})
    check("post: oversized image rejected", r5['status'] == 400, str(r5['status']))
    r6 = api(pgA, '/api/conversations/' + CONV + '/messages', {"text": ""})
    check("chat: empty message rejected", r6['status'] == 400, str(r6['status']))
    r7 = api(pgA, '/api/conversations/' + CONV + '/messages', {"text": "z" * 2500})
    check("chat: >2000 chars rejected", r7['status'] == 400, str(r7['status']))
    r8 = api(pgA, '/api/conversations/' + CONV + '/messages', {"image": "data:image/gif;base64,AAAA"})
    check("chat: non-jpg/png/webp image rejected", r8['status'] == 400, str(r8['status']))
    r9 = api(pgA, '/api/conversations/' + CONV + '/messages', {"image": "data:image/png;base64," + "A" * 1700000})
    check("chat: oversized image rejected", r9['status'] == 400, str(r9['status']))
    r10 = pgC.evaluate("async (u) => { const r = await fetch(u); return {status:r.status, data: await r.json().catch(()=>({}))}; }", BASE + '/api/verification-request')
    check("verification GET own scoped (200)", r10['status'] == 200 and len(r10['data'].get('requests', [])) == 0, str(r10['status']))

    # ---------- 3. chat image upload UI ----------
    print("\n-- chat image upload UI --", flush=True)
    pgB.goto(BASE + '/messages.html?with=' + A['id'], wait_until='domcontentloaded'); pgB.wait_for_timeout(1500)
    # JPG via canvas
    pgB.evaluate("""() => {
      const c = document.createElement('canvas'); c.width=40; c.height=30;
      const x = c.getContext('2d'); x.fillStyle='#2F6BFF'; x.fillRect(0,0,40,30);
      return c.toDataURL('image/jpeg');
    }""")
    def attach_file(pg, name, mime, make_blob_js):
        return pg.evaluate("""(a) => new Promise((res, rej) => {
          const c = document.createElement('canvas'); c.width=40; c.height=30;
          const x = c.getContext('2d'); x.fillStyle='#FF8A4C'; x.fillRect(0,0,40,30);
          fetch(c.toDataURL(a.mime)).then(r => r.blob()).then(blob => {
            const f = new File([blob], a.name, {type: a.mime});
            const dt = new DataTransfer(); dt.items.add(f);
            const inp = document.getElementById('chatFile');
            inp.files = dt.files;
            inp.dispatchEvent(new Event('change'));
            res(true);
          }).catch(rej);
        })""", {"name": name, "mime": mime})
    def attach_raw(pg, name, mime, bytes_js):
        return pg.evaluate("""(a) => {
          const arr = new Uint8Array(a.n);
          const f = new File([arr], a.name, {type: a.mime});
          const dt = new DataTransfer(); dt.items.add(f);
          const inp = document.getElementById('chatFile');
          inp.files = dt.files;
          inp.dispatchEvent(new Event('change'));
          return true;
        }""", {"name": name, "mime": mime, "n": bytes_js})
    # valid JPG -> preview shows
    attach_file(pgB, 'shot.jpg', 'image/jpeg', None)
    pgB.wait_for_timeout(600)
    check("chat: JPG preview shown", vis(pgB, '#chatPreview') and 'cpImg' in pgB.evaluate("document.getElementById('chatPreview').innerHTML"))
    # remove before send
    pgB.click('#cpRemove'); pgB.wait_for_timeout(300)
    check("chat: remove before send works", not vis(pgB, '#chatPreview'))
    # valid PNG -> send
    attach_file(pgB, 'shot.png', 'image/png', None)
    pgB.wait_for_timeout(500)
    pgB.click('#chatSend'); pgB.wait_for_timeout(1200)
    # A receives image
    pgA.goto(BASE + '/messages.html?with=' + B['id'], wait_until='domcontentloaded'); pgA.wait_for_timeout(1500)
    img_msgs = pgA.eval_on_selector_all('.bimg', "els => els.length")
    check("chat: PNG image received by other party", img_msgs >= 1, "imgs=%d" % img_msgs)
    # lightbox
    pgA.click('.bimg'); pgA.wait_for_timeout(400)
    check("chat: lightbox opens on image click", pgA.eval_on_selector('#lightbox', "el => el.classList.contains('on')"))
    pgA.keyboard.press('Escape'); pgA.wait_for_timeout(300)
    check("chat: lightbox closes", not pgA.eval_on_selector('#lightbox', "el => el.classList.contains('on')"))
    # WEBP valid
    pgB.goto(BASE + '/messages.html?with=' + A['id'], wait_until='domcontentloaded'); pgB.wait_for_timeout(1200)
    attach_file(pgB, 'shot.webp', 'image/webp', None)
    pgB.wait_for_timeout(500)
    pgB.click('#chatSend'); pgB.wait_for_timeout(1200)
    pgA.goto(BASE + '/messages.html?with=' + B['id'], wait_until='domcontentloaded'); pgA.wait_for_timeout(1500)
    img_msgs2 = pgA.eval_on_selector_all('.bimg', "els => els.length")
    check("chat: WEBP image received", img_msgs2 >= 2, "imgs=%d" % img_msgs2)
    # invalid type -> toast error, nothing sent
    pgB.goto(BASE + '/messages.html?with=' + A['id'], wait_until='domcontentloaded'); pgB.wait_for_timeout(1200)
    attach_raw(pgB, 'evil.txt', 'text/plain', 100)
    pgB.wait_for_timeout(400)
    check("chat: invalid file type rejected (no preview)", not vis(pgB, '#chatPreview'))
    # oversized -> rejected
    attach_raw(pgB, 'big.png', 'image/png', 1600000)
    pgB.wait_for_timeout(400)
    check("chat: oversized image rejected (no preview)", not vis(pgB, '#chatPreview'))

    # ---------- 4. i18n audit ----------
    print("\n-- i18n audit --", flush=True)
    pages = ['dashboard.html','marketplace.html','post.html','messages.html','notifications.html',
             'matches.html','verify.html','analytics.html','profile-setup.html','business.html?id=' + B['id']]
    for p in pages:
        try:
            pgA.goto(BASE + '/' + p, wait_until='domcontentloaded'); pgA.wait_for_timeout(1400)
            pgA.click('.lang-btn[data-lang="en"]'); pgA.wait_for_timeout(600)
            bad = pgA.evaluate("""() => {
              const els = document.querySelectorAll('body *');
              for (const el of els) {
                if (el.children.length) continue;
                const t = (el.textContent || '').trim();
                if (!t) continue;
                if (t === 'undefined' || /(^|\\s)(mp|su|qt|nav|err|ms|vr|an|adm)\\.[a-zA-Z0-9.]+$/.test(t)) return t.slice(0,60);
              }
              return null;
            }""")
            check("i18n clean: " + p, bad is None, str(bad))
        except Exception as e:
            check("i18n page load: " + p, False, str(e)[:60])
    # language persistence
    pgA.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1200)
    pgA.click('.lang-btn[data-lang="bn"]'); pgA.wait_for_timeout(400)
    pgA.reload(wait_until='domcontentloaded'); pgA.wait_for_timeout(800)
    check("i18n: language persists after reload", pgA.evaluate("document.documentElement.lang") == 'bn')

    # ---------- 5. responsive ----------
    print("\n-- responsive --", flush=True)
    sizes = [(390, 844), (768, 1024), (1440, 900)]
    pages2 = ['/', '/marketplace.html', '/login.html', '/signup.html', '/dashboard.html', '/messages.html',
              '/analytics.html', '/admin.html', '/verify.html', '/about.html', '/suppliers.html', '/post.html']
    for w, h in sizes:
        ctxV = b.new_context(viewport={'width': w, 'height': h})
        pgV = ctxV.new_page(); pgV.set_default_timeout(12000)
        prime(pgV)
        # login as A to access protected pages
        api(pgV, '/api/login', {"identifier": A['email'], "password": PW})
        for p in pages2:
            try:
                pgV.goto(BASE + p, wait_until='domcontentloaded'); pgV.wait_for_timeout(1100)
                ov = pgV.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                check("no h-overflow %dx%d %s" % (w, h, p), ov <= 1, "ov=%d" % ov)
            except Exception as e:
                check("responsive %dx%d %s" % (w, h, p), False, str(e)[:50])
        ctxV.close()

    # ---------- 6. console errors on key pages ----------
    print("\n-- console errors --", flush=True)
    errs = []
    pgA.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    pgA.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    for p in ['/dashboard.html','/marketplace.html','/messages.html','/analytics.html','/matches.html','/verify.html','/post.html']:
        pgA.goto(BASE + p, wait_until='domcontentloaded'); pgA.wait_for_timeout(1400)
    real = [e for e in errs if 'Failed to load resource' not in e]
    check("no console/page errors on key pages", len(real) == 0, str(real[:3]))

    # ---------- 7. session persistence & logout ----------
    print("\n-- session / logout --", flush=True)
    pgA.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1200)
    pgA.reload(wait_until='domcontentloaded'); pgA.wait_for_timeout(900)
    s = api(pgA, '/api/session')
    check("session persists across reload", s['status'] == 200 and s['data']['user']['email'] == A['email'])
    pgA.goto(BASE + '/api/logout', wait_until='domcontentloaded'); pgA.wait_for_timeout(800)
    s2 = api(pgA, '/api/session')
    check("logout clears session", s2['data']['user'] is None, str(s2['data'])[:60])
    # session cookie cleared too
    cookies = pgA.context.cookies()
    check("logout clears cookie", all(c['name'] != 'ahoor_sid' for c in cookies), str([c['name'] for c in cookies]))
    r = pgA.request.get(BASE + '/dashboard.html', max_redirects=0)
    check("protected page redirects after logout", r.status == 302)

    b.close()

print("\n===== AUDIT SUMMARY: %d/%d passed =====" % (sum(1 for _, c in results if c), len(results)))
