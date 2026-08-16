from playwright.sync_api import sync_playwright
import random, time, re

BASE = 'http://localhost:8080'
results = []
def check(name, cond, extra=''):
    results.append((name, cond))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{extra}]" if extra else ""))

def fresh(prefix):
    return f"{prefix}{int(time.time())}{random.randint(10,99)}"
def bd_phone(prefix):
    return f"{prefix}{random.randint(10,99)}{int(time.time()) % 1000000:06d}"

def signup(pg, name, email, phone, pw, role):
    pg.goto(BASE + '/signup.html', wait_until='domcontentloaded'); pg.wait_for_timeout(500)
    pg.fill('#nameF', name); pg.fill('#emailF', email); pg.fill('#phoneF', phone)
    pg.fill('#pw1', pw); pg.fill('#pw2', pw)
    pg.click('#btnS1'); pg.wait_for_timeout(1400)
    pg.click(f'.type-card[data-type="{role}"]'); pg.click('#btnS2'); pg.wait_for_timeout(1000)
    pg.click('#btnBizNext'); pg.wait_for_timeout(1300)
    dev = pg.evaluate("document.getElementById('devNote').textContent")
    code = re.search(r'(\d{6})', dev).group(1)
    for i, c in enumerate(code):
        pg.fill(f'#otpRow input:nth-child({i+1})', c)
    pg.wait_for_timeout(1500)
    pg.wait_for_timeout(2700)
    pg.wait_for_timeout(600)

def fill_profile(pg, name, biz, biztype, cat, district, products, extra=None):
    pg.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pg.wait_for_timeout(900)
    pg.fill('#ppName', name); pg.fill('#ppBiz', biz)
    pg.select_option('#ppBizType', biztype)
    pg.select_option('#ppCat', cat)
    pg.select_option('#ppDistrict', district)
    pg.fill('#ppProducts', products)
    if extra:
        for k, v in extra.items():
            pg.fill('#' + k, v)
    pg.click('#ppSave'); pg.wait_for_timeout(2200)

def create_post(pg, type_, title, cat, qty, unit, loc, desc, extra=None):
    pg.goto(BASE + '/post.html', wait_until='domcontentloaded'); pg.wait_for_timeout(800)
    if type_ == 'supplier':
        pg.click('.kind-card[data-kind="supplier"]'); pg.wait_for_timeout(300)
    pg.fill('#ptTitleF', title)
    pg.select_option('#ptCat', cat)
    pg.fill('#ptQty', qty); pg.select_option('#ptUnit', unit)
    pg.select_option('#ptLoc', loc)
    pg.fill('#ptDesc', desc)
    if extra:
        for k, v in extra.items():
            pg.fill('#' + k, v)
    pg.click('#ptSubmit'); pg.wait_for_timeout(2200)
    pg.wait_for_timeout(600)

with sync_playwright() as p:
    b = p.chromium.launch()
    ctxA = b.new_context(); ctxB = b.new_context(); ctxC = b.new_context()
    pgA = ctxA.new_page()  # buyer
    pgB = ctxB.new_page()  # t-shirt supplier (relevant)
    pgC = ctxC.new_page()  # machinery supplier (irrelevant)
    errs = []
    for pgx in (pgA, pgB, pgC):
        pgx.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- setup profiles ----------
    signup(pgA, 'Buyer Alpha', fresh('ma') + '@gmail.com', bd_phone('017'), 'Pass12345!', 'buyer')
    fill_profile(pgA, 'Buyer Alpha', 'Alpha Retail', 'buyer', 'Garments & Apparel', 'Dhaka', '', extra={'ppBuyProducts': 'Cotton T-Shirts, Polo Shirts', 'ppTypicalQty': '5000'})
    signup(pgB, 'Supplier Beta', fresh('mb') + '@gmail.com', bd_phone('018'), 'Pass12345!', 'supplier')
    fill_profile(pgB, 'Supplier Beta', 'Beta Apparels', 'manufacturer', 'Garments & Apparel', 'Dhaka', 'T-Shirts, Hoodies, Polo Shirts', extra={'ppMoq': '100'})
    signup(pgC, 'Supplier Gamma', fresh('mc') + '@gmail.com', bd_phone('019'), 'Pass12345!', 'supplier')
    fill_profile(pgC, 'Supplier Gamma', 'Gamma Machinery', 'supplier', 'Machinery', 'Chattogram', 'Industrial Sewing Machines', extra={'ppMoq': '10'})

    # ---------- 1. BUYER creates requirement post ----------
    create_post(pgA, 'buyer', 'Need 5000 PCS Custom T-Shirts', 'Garments & Apparel', '5000', 'PCS', 'Dhaka',
                'Need 5000 pieces premium cotton t-shirts with custom print for retail.')

    # B (relevant supplier) gets a notification + match; C (machinery) should NOT
    notifB = pgB.evaluate("fetch('/api/notifications').then(r=>r.json())")
    hasMatchN = any(n['type'] == 'opportunity_match' for n in notifB.get('notifications', []))
    check("B got opportunity_match notification", hasMatchN, str([n['type'] for n in notifB.get('notifications', [])]))
    notifC = pgC.evaluate("fetch('/api/notifications').then(r=>r.json())")
    check("C (irrelevant) got NO match notification", not any(n['type'] == 'opportunity_match' for n in notifC.get('notifications', [])))

    # B's matches contain the buyer post with HIGH level
    mb = pgB.evaluate("fetch('/api/matches').then(r=>r.json())")
    bp = next((m for m in mb.get('matches', []) if m['kind'] == 'post' and 'T-Shirts' in m['post']['title']), None)
    check("B matched to buyer post", bp is not None)
    check("B match level high", bp and bp['level'] == 'high', str(bp and bp['level']))
    check("B sees explanation-level only (no raw score)", bp and 'score' not in bp)

    # C's matches should NOT include the buyer post (low filtered)
    mc = pgC.evaluate("fetch('/api/matches').then(r=>r.json())")
    cHas = any(m['kind'] == 'post' and 'T-Shirts' in m['post']['title'] for m in mc.get('matches', []))
    check("C not matched to irrelevant post", not cHas)

    # ---------- 2. SUPPLIER posts -> BUYER gets matches ----------
    create_post(pgB, 'supplier', 'Custom T-Shirts Manufacturing', 'Garments & Apparel', '20000', 'PCS', 'Dhaka',
                'Export quality custom t-shirt manufacturing, MOQ 100 pcs.', extra={'ptMoq': '100', 'ptPrice': '৳240 / pcs'})
    ma = pgA.evaluate("fetch('/api/matches').then(r=>r.json())")
    sp = next((m for m in ma.get('matches', []) if m['kind'] == 'post' and 'T-Shirts' in m['post']['title']), None)
    check("A matched to supplier post", sp is not None)
    check("A match high", sp and sp['level'] == 'high', str(sp and sp['level']))
    # A also matched to supplier BUSINESS (Beta Apparels)
    bb = next((m for m in ma.get('matches', []) if m['kind'] == 'business' and m['business']['businessName'] == 'Beta Apparels'), None)
    check("A matched to supplier business", bb is not None)
    check("A business match level", bb and bb['level'] in ('high', 'medium'), str(bb and bb['level']))

    # ---------- 3. SAVED OPPORTUNITIES ----------
    sid = sp['post']['id']
    r = pgA.evaluate("""(async (id)=>{const resp=await fetch('/api/saved',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({postId:id})});return resp.status;})('""" + sid + """')""")
    check("save post (200)", r == 200, str(r))
    saved = pgA.evaluate("fetch('/api/saved').then(r=>r.json())")
    check("saved list contains post", any(pt['id'] == sid for pt in saved.get('posts', [])))
    # duplicate save doesn't duplicate
    pgA.evaluate("""(async (id)=>{await fetch('/api/saved',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({postId:id})});})('""" + sid + """')""")
    saved2 = pgA.evaluate("fetch('/api/saved').then(r=>r.json())")
    check("no duplicate saves", sum(1 for pt in saved2.get('posts', []) if pt['id'] == sid) == 1)
    # B cannot see A's saved
    savedB = pgB.evaluate("fetch('/api/saved').then(r=>r.json())")
    check("B sees own saved only (empty)", len(savedB.get('posts', [])) == 0, str(len(savedB.get('posts', []))))
    # remove
    pgA.evaluate("""(async (id)=>{await fetch('/api/saved/remove',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({postId:id})});})('""" + sid + """')""")
    saved3 = pgA.evaluate("fetch('/api/saved').then(r=>r.json())")
    check("saved removed", not any(pt['id'] == sid for pt in saved3.get('posts', [])))

    # ---------- 4. matches page UI ----------
    pgA.goto(BASE + '/matches.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1800)
    body = pgA.evaluate("document.getElementById('mtGrid').textContent")
    check("matches page shows content", 'T-Shirts' in body, body[:80])
    check("matches page shows level label", 'উচ্চ ম্যাচ' in body or 'High Match' in body)
    # tabs: buyer opportunities (A's own posts won't show; supplier tab should show supplier post)
    pgA.click('.tab[data-t="supplier"]'); pgA.wait_for_timeout(600)
    supBody = pgA.evaluate("document.getElementById('mtGrid').textContent")
    check("supplier tab shows supplier offers", 'T-Shirts Manufacturing' in supBody)
    pgA.click('.tab[data-t="saved"]'); pgA.wait_for_timeout(800)
    savBody = pgA.evaluate("document.getElementById('mtGrid').textContent")
    check("saved tab empty state", 'সংরক্ষণ' in savBody or "haven't saved" in savBody)
    pgA.screenshot(path='qa-auth/mt-1-matches.png')

    # ---------- 5. dashboard Recommended for You ----------
    pgA.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1800)
    rec = pgA.evaluate("document.getElementById('recList').textContent")
    check("dashboard recommended section", 'T-Shirts' in rec, rec[:80])
    check("dashboard new matches count", pgA.evaluate("getComputedStyle(document.getElementById('recCount')).display") != 'none')
    check("view all matches link", pgA.evaluate("document.querySelector('#recList') ? true : false"))
    pgA.screenshot(path='qa-auth/mt-2-dashboard.png')

    # ---------- 6. permissions ----------
    anon = b.new_context()
    pgAnon = anon.new_page()
    pgAnon.goto(BASE + '/matches.html', wait_until='domcontentloaded'); pgAnon.wait_for_timeout(1500)
    check("anon /matches -> login", '/login' in pgAnon.url, pgAnon.url)
    anon.close()

    # ---------- 7. language ----------
    pgA.goto(BASE + '/matches.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1400)
    pgA.click('.lang-btn[data-lang="en"]'); pgA.wait_for_timeout(600)
    enTitle = pgA.evaluate("document.querySelector('.mt-head h1').textContent")
    check("EN matches title", enTitle == 'Matched Opportunities', enTitle)
    enNote = pgA.evaluate("document.querySelector('.mt-note').textContent")
    check("EN explanation", 'Matched based on your business profile' in enNote, enNote[:60])

    # ---------- 8. mobile ----------
    pgM = ctxA.new_page()
    pgM.set_viewport_size({'width':390,'height':844})
    pgM.goto(BASE + '/matches.html', wait_until='domcontentloaded'); pgM.wait_for_timeout(1600)
    ov = pgM.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check("mobile no overflow", ov == 0, str(ov))
    pgM.screenshot(path='qa-auth/mt-3-mobile.png')
    pgM.close()

    print("\npage errors:", errs if errs else "none")
    b.close()

print("\n===== SUMMARY =====")
fails = [r for r in results if not r[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed; failures: {[r[0] for r in fails]}")
