from playwright.sync_api import sync_playwright
import random, time, re, json

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
    pg.goto(BASE + '/signup.html', wait_until='domcontentloaded'); pg.wait_for_timeout(600)
    pg.fill('#nameF', name); pg.fill('#emailF', email); pg.fill('#phoneF', phone)
    pg.fill('#pw1', pw); pg.fill('#pw2', pw)
    pg.click('#btnS1'); pg.wait_for_timeout(1400)
    pg.click(f'.type-card[data-type="{role}"]'); pg.click('#btnS2'); pg.wait_for_timeout(1000)
    dev = pg.evaluate("document.getElementById('devNote').textContent")
    code = re.search(r'(\d{6})', dev).group(1)
    for i, c in enumerate(code):
        pg.fill(f'#otpRow input:nth-child({i+1})', c)
    pg.wait_for_timeout(1500)
    pg.wait_for_timeout(2700)  # redirect to profile-setup
    pg.wait_for_timeout(800)

def fill_profile(pg, name, biz, phone, dist, cat, desc):
    pg.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pg.wait_for_timeout(900)
    pg.fill('#ppName', name); pg.fill('#ppBiz', biz)
    pg.fill('#ppBizPhone', phone)
    pg.select_option('#ppDistrict', dist); pg.select_option('#ppCat', cat)
    pg.fill('#ppDesc', desc)
    pg.click('#ppSave'); pg.wait_for_timeout(2000)

def empty_visible(pg):
    el = pg.evaluate("document.getElementById('mpEmpty')")
    return el is not None and pg.evaluate("getComputedStyle(document.getElementById('mpEmpty')).display") != 'none'

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- USER A (buyer) ----------
    A_email = fresh('buyer') + '@gmail.com'
    A_phone = bd_phone('017')
    signup(pg, 'Rahim Uddin', A_email, A_phone, 'Pass12345!', 'buyer')
    check("signup -> profile-setup page", pg.url.endswith('/profile-setup.html'), pg.url)
    check("profile role buyer preselected", pg.evaluate("document.querySelector('.pp-role button[data-role=\"buyer\"]').classList.contains('on')"))

    pg.fill('#ppName', '')
    pg.click('#ppSave'); pg.wait_for_timeout(600)
    check("profile name required error", pg.evaluate("document.getElementById('ppName').classList.contains('err')"))
    pg.fill('#ppName', 'Rahim Uddin')

    fill_profile(pg, 'Rahim Uddin', 'Rahim Garments', A_phone, 'Dhaka', 'Garments & Apparel', 'Buying cotton t-shirts and hoodies in bulk for retail.')
    check("profile saved -> dashboard", pg.url.endswith('/dashboard.html'), pg.url)
    pg.wait_for_timeout(800)
    check("dashboard shows business name", 'Rahim Garments' in pg.evaluate("document.getElementById('psBiz').textContent"))
    check("no profile warn", pg.evaluate("document.getElementById('profileWarn').style.display") == 'none')

    # buyer post
    pg.goto(BASE + '/post.html', wait_until='domcontentloaded'); pg.wait_for_timeout(800)
    pg.fill('#ptTitleF', 'Need 1000 PCS Premium Cotton T-Shirts')
    pg.select_option('#ptCat', 'Garments & Apparel')
    pg.fill('#ptQty', '1000'); pg.select_option('#ptUnit', 'PCS')
    pg.fill('#ptBudget', '৳250,000')
    pg.select_option('#ptLoc', 'Dhaka')
    pg.fill('#ptDeadline', '2026-09-15')
    pg.fill('#ptDesc', 'Need 1000 pieces premium cotton t-shirts sizes S to XXL with custom print, white and black colors, delivery within 30 days.')
    pg.click('#ptSubmit'); pg.wait_for_timeout(2200)
    check("buyer post published -> dashboard", pg.url.endswith('/dashboard.html'), pg.url)
    pg.wait_for_timeout(900)
    check("my posts shows the post", 'Premium Cotton T-Shirts' in pg.evaluate("document.getElementById('myPosts').textContent"))

    # marketplace
    pg.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1200)
    check("marketplace shows buyer post", 'Premium Cotton T-Shirts' in pg.evaluate("document.getElementById('mpGrid').textContent"))
    check("buyer badge shown", 'ক্রেতার অনুরোধ' in pg.evaluate("document.getElementById('mpGrid').textContent"))
    pg.screenshot(path='qa-auth/mp-1-feed.png')

    pg.click('.tab[data-t="supplier"]')
    pg.wait_for_function("document.getElementById('mpLoad').style.display === 'none'", timeout=8000)
    pg.wait_for_timeout(400)
    check("supplier tab empty state", empty_visible(pg))
    pg.click('.tab[data-t="all"]'); pg.wait_for_timeout(600)
    pg.fill('#mpQ', 'hoodie'); pg.wait_for_timeout(1400)
    check("search 'hoodie' finds nothing", empty_visible(pg))
    pg.fill('#mpQ', 't-shirt'); pg.wait_for_timeout(1400)
    check("search 't-shirt' finds post", 'Premium Cotton T-Shirts' in pg.evaluate("document.getElementById('mpGrid').textContent"))

    # ---------- USER B (supplier) ----------
    ctx2 = b.new_context()
    pgB = ctx2.new_page()
    B_email = fresh('supplier') + '@gmail.com'
    B_phone = bd_phone('018')
    signup(pgB, 'Karim Ahmed', B_email, B_phone, 'Pass12345!', 'supplier')
    fill_profile(pgB, 'Karim Ahmed', 'NexTee Textiles', B_phone, 'Gazipur', 'Textile & Fabric', 'Manufacturing t-shirts and hoodies with custom printing.')

    pgB.goto(BASE + '/post.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(800)
    pgB.click('.kind-card[data-kind="supplier"]'); pgB.wait_for_timeout(300)
    check("supplier kind shows MOQ/price", pgB.evaluate("getComputedStyle(document.getElementById('moqWrap')).display") != 'none')
    pgB.fill('#ptTitleF', 'Premium Cotton T-Shirts — Custom Printing')
    pgB.select_option('#ptCat', 'Textile & Fabric')
    pgB.fill('#ptQty', '20000'); pgB.select_option('#ptUnit', 'PCS')
    pgB.fill('#ptMoq', '100'); pgB.fill('#ptPrice', '৳240 / pcs')
    pgB.select_option('#ptLoc', 'Gazipur')
    pgB.fill('#ptDesc', 'Export quality cotton t-shirts with custom printing. MOQ 100 pcs, production time 7-14 days.')
    pgB.click('#ptSubmit'); pgB.wait_for_timeout(2200)
    pgB.wait_for_timeout(700)

    # marketplace from B
    pgB.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1200)
    check("marketplace shows supplier post", 'Custom Printing' in pgB.evaluate("document.getElementById('mpGrid').textContent"))
    check("supplier badge shown", 'সরবরাহকারীর অফার' in pgB.evaluate("document.getElementById('mpGrid').textContent"))
    pgB.click('.tab[data-t="buyer"]'); pgB.wait_for_timeout(800)
    check("buyer tab filters", 'Custom Printing' not in pgB.evaluate("document.getElementById('mpGrid').textContent"))
    pgB.click('.tab[data-t="all"]'); pgB.wait_for_timeout(700)

    # ---------- QUOTES: A quotes B's post ----------
    pg.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1200)
    pg.click('#mpGrid .post-card button[data-quote]'); pg.wait_for_timeout(600)
    check("quote modal opens", pg.evaluate("document.getElementById('quoteModal').classList.contains('on')"))
    pg.fill('#qmReqQty', '1000')
    pg.fill('#qmPrefDel', 'within 15 days')
    pg.fill('#qmText', 'We need these urgently. Can you deliver 1000 pcs in 15 days?')
    pg.click('#qmSend'); pg.wait_for_timeout(1400)
    check("quote sent", pg.evaluate("document.body.textContent").find('পাঠানো হয়েছে') != -1)

    # B receives quote
    pgB.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1600)
    check("B received quote", 'Rahim Garments' in pgB.evaluate("document.getElementById('quotesList').textContent"))
    check("quote message shown", '1000 pcs in 15 days' in pgB.evaluate("document.getElementById('quotesList').textContent"))
    pgB.screenshot(path='qa-auth/mp-2-dashboard.png')

    # ---------- OWNERSHIP ----------
    # get A's post id
    A_post_id = pg.evaluate("fetch('/api/my-posts',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.posts[0].id)")
    res = pgB.evaluate("""(async (id)=>{
        const r = await fetch('/api/posts/'+id+'/edit', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({title:'Hacked!'})});
        return r.status;
    })('""" + A_post_id + """')""")
    check("B cannot edit A's post (403)", res == 403, str(res))
    res2 = pgB.evaluate("""(async (id)=>{
        const r = await fetch('/api/posts/'+id+'/delete', {method:'POST'});
        return r.status;
    })('""" + A_post_id + """')""")
    check("B cannot delete A's post (403)", res2 == 403, str(res2))

    # unauthenticated cannot reach post page
    ctx3 = b.new_context()
    pgC = ctx3.new_page()
    pgC.goto(BASE + '/post.html', wait_until='domcontentloaded'); pgC.wait_for_timeout(1500)
    check("unauthenticated /post.html -> login", '/login' in pgC.url, pgC.url)

    # ---------- A: toggle close ----------
    pg.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1300)
    pg.click('#myPosts .dp-link[data-act="toggle"]'); pg.wait_for_timeout(2500)
    closed = pg.evaluate("[...document.querySelectorAll('#myPosts .dp-link')].map(e=>e.textContent).join(',')")
    check("A can close own post", 'আবার খুলুন' in closed, closed)
    pg.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1000)
    check("marketplace shows closed badge", 'বন্ধ' in pg.evaluate("document.getElementById('mpGrid').textContent"))

    # ---------- edit ----------
    pg.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1000)
    pg.click('#myPosts a.dp-link[href^="/post.html?id="]'); pg.wait_for_timeout(1400)
    check("edit page loads post", pg.evaluate("document.getElementById('ptTitleF').value") == 'Need 1000 PCS Premium Cotton T-Shirts')
    pg.fill('#ptTitleF', 'Need 2000 PCS Premium Cotton T-Shirts')
    pg.click('#ptSubmit'); pg.wait_for_timeout(2200)
    pg.wait_for_timeout(800)
    check("edited title in my posts", '2000 PCS' in pg.evaluate("document.getElementById('myPosts').textContent"))

    # ---------- delete ----------
    pg.on('dialog', lambda d: d.accept())
    pg.click('#myPosts .dp-link[data-act="delete"]'); pg.wait_for_timeout(1800)
    check("post deleted", 'Premium Cotton T-Shirts' not in pg.evaluate("document.getElementById('myPosts').textContent"))
    check("empty state shown", pg.evaluate("getComputedStyle(document.getElementById('noPosts')).display") != 'none')

    # ---------- language on marketplace ----------
    pg.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pg.wait_for_timeout(800)
    pg.click('.lang-btn[data-lang="en"]'); pg.wait_for_timeout(500)
    check("marketplace EN title", pg.evaluate("document.querySelector('.mp-head h1').textContent") == 'Ahoor Marketplace')
    check("marketplace EN tab", pg.evaluate("document.querySelector('.tab[data-t=\"buyer\"]').textContent") == 'Buyer Requirements')
    pg.screenshot(path='qa-auth/mp-3-en.png')

    print("\npage errors:", errs if errs else "none")
    b.close()

print("\n===== SUMMARY =====")
fails = [r for r in results if not r[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed; failures: {[r[0] for r in fails]}")
