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
    pg.goto(BASE + '/signup.html', wait_until='domcontentloaded'); pg.wait_for_timeout(600)
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
    pg.wait_for_timeout(700)

def fill_business_profile(pg, opts):
    pg.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pg.wait_for_timeout(1000)
    pg.fill('#ppName', opts['name'])
    pg.fill('#ppBiz', opts['biz'])
    if opts.get('biztype'):
        pg.select_option('#ppBizType', opts['biztype'])
    if opts.get('category'):
        pg.select_option('#ppCat', opts['category'])
    pg.fill('#ppDesc', opts.get('desc', 'Business description with enough details.'))
    if opts.get('division'):
        pg.select_option('#ppDivision', opts['division'])
    if opts.get('district'):
        pg.select_option('#ppDistrict', opts['district'])
    if opts.get('city'):
        pg.fill('#ppCity', opts['city'])
    if opts.get('address'):
        pg.fill('#ppAddr', opts['address'])
    if opts.get('products'):
        pg.fill('#ppProducts', opts['products'])
    if opts.get('moq'):
        pg.fill('#ppMoq', opts['moq'])
    if opts.get('capacity'):
        pg.fill('#ppCapacity', opts['capacity'])
    if opts.get('employees'):
        pg.fill('#ppEmployees', opts['employees'])
    if opts.get('years'):
        pg.fill('#ppYears', opts['years'])
    if opts.get('bizphone'):
        pg.fill('#ppBizPhone', opts['bizphone'])
    if opts.get('bizemail'):
        pg.fill('#ppBizEmail', opts['bizemail'])
    if opts.get('website'):
        pg.fill('#ppWebsite', opts['website'])
    if opts.get('fb'):
        pg.fill('#ppFb', opts['fb'])
    if opts.get('phonevis'):
        pg.select_option('#ppPhoneVis', opts['phonevis'])
    if opts.get('emailvis'):
        pg.select_option('#ppEmailVis', opts['emailvis'])
    pg.click('#ppSave'); pg.wait_for_timeout(2200)

with sync_playwright() as p:
    b = p.chromium.launch()
    ctxA = b.new_context()
    ctxB = b.new_context()
    ctxAnon = b.new_context()
    pgA = ctxA.new_page()
    pgB = ctxB.new_page()
    pgAnon = ctxAnon.new_page()
    errs = []
    for pgx in (pgA, pgB, pgAnon):
        pgx.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- A: buyer with FULL business profile ----------
    A_phone = bd_phone('017')
    A_email = fresh('ba') + '@gmail.com'
    signup(pgA, 'Rahim Uddin', A_email, A_phone, 'Pass12345!', 'buyer')
    fill_business_profile(pgA, {
        'name':'Rahim Uddin', 'biz':'Rahim Garments', 'biztype':'wholesaler', 'category':'Garments & Apparel',
        'desc':'Wholesale supplier of quality garments in Dhaka.',
        'division':'dhaka', 'district':'Dhaka', 'city':'Mirpur', 'address':'House 12, Road 5, Mirpur-10, Dhaka',
        'products':'T-Shirts, Hoodies, Polo Shirts', 'moq':'100 pcs', 'capacity':'50,000 pcs per month',
        'employees':'25', 'years':'6', 'bizphone':'01712345678', 'bizemail':'biz@rahimgarments.com',
        'website':'https://rahimgarments.com', 'fb':'facebook.com/rahimgarments'
    })
    check("save -> dashboard", pgA.url.endswith('/dashboard.html'), pgA.url)
    pgA.wait_for_timeout(800)
    comp = pgA.evaluate("document.getElementById('dashCompPct').textContent")
    check("dashboard completion (no logo) 90%", comp in ('90%','100%'), comp)
    check("view public link has id", 'business.html?id=' in pgA.evaluate("document.getElementById('viewBiz').href"))

    # create a buyer post
    pgA.goto(BASE + '/post.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(800)
    pgA.fill('#ptTitleF', 'Need 1000 PCS Premium Cotton T-Shirts')
    pgA.select_option('#ptCat', 'Garments & Apparel')
    pgA.fill('#ptQty', '1000'); pgA.select_option('#ptUnit', 'PCS')
    pgA.select_option('#ptLoc', 'Dhaka')
    pgA.fill('#ptDesc', 'Need 1000 pieces premium cotton t-shirts with custom print for retail.')
    pgA.click('#ptSubmit'); pgA.wait_for_timeout(2200)

    A_id = pgA.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")

    # ---------- public profile: anonymous (default visibility = members) ----------
    pgAnon.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgAnon.wait_for_timeout(1400)
    body = pgAnon.evaluate("document.body.textContent")
    check("public page shows business name", 'Rahim Garments' in body)
    check("public page shows business type", 'পাইকারি ব্যবসায়ী' in body or 'Wholesaler' in body)
    check("public page shows location", 'Mirpur' in body)
    check("public page shows products", 'T-Shirts, Hoodies' in body)
    check("public page shows capacity", '50,000 pcs' in body)
    check("public page shows active post", 'Premium Cotton T-Shirts' in body)
    check("anon: phone hidden (members)", '01712345678' not in body)
    check("anon: email hidden (members)", 'biz@rahimgarments.com' not in body)
    check("website public", 'rahimgarments.com' in body)
    check("edit btn hidden for others", pgAnon.evaluate("document.getElementById('bpEditBtn').style.display") == 'none')
    pgAnon.screenshot(path='qa-auth/bp-1-public-anon.png')

    # ---------- B (logged in) sees members-only contact ----------
    signup(pgB, 'Karim Ahmed', fresh('sb') + '@gmail.com', bd_phone('018'), 'Pass12345!', 'supplier')
    pgB.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgB.wait_for_timeout(1400)
    bodyB = pgB.evaluate("document.body.textContent")
    check("member sees phone", '01712345678' in bodyB)
    check("member sees email", 'biz@rahimgarments.com' in bodyB)

    # ---------- A switches phone to public, email to hidden ----------
    fill_business_profile(pgA, {'name':'Rahim Uddin','biz':'Rahim Garments','phonevis':'public','emailvis':'hidden'})
    pgAnon.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgAnon.wait_for_timeout(1400)
    bodyA2 = pgAnon.evaluate("document.body.textContent")
    check("anon sees phone when public", '01712345678' in bodyA2)
    check("anon blocked from hidden email", 'biz@rahimgarments.com' not in bodyA2)
    pgB.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgB.wait_for_timeout(1400)
    bodyB2 = pgB.evaluate("document.body.textContent")
    check("member also blocked from hidden email", 'biz@rahimgarments.com' not in bodyB2)

    # ---------- edit: description change reflected ----------
    fill_business_profile(pgA, {'name':'Rahim Uddin','biz':'Rahim Garments','desc':'Updated: now exporting to Europe as well.'})
    pgAnon.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgAnon.wait_for_timeout(1200)
    check("edited description live", 'now exporting' in pgAnon.evaluate("document.body.textContent"))

    # ---------- own view shows edit button ----------
    pgA.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgA.wait_for_timeout(1200)
    check("own view shows edit btn", pgA.evaluate("getComputedStyle(document.getElementById('bpEditBtn')).display") != 'none')

    # ---------- marketplace: business name clickable ----------
    pgB.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1400)
    link = pgB.evaluate("""()=>{
      const a = document.querySelector('#mpGrid .po-info a');
      return a ? a.getAttribute('href') : '';
    }""")
    check("marketplace owner link to business page", 'business.html?id=' in link, link)
    check("marketplace shows business type", 'পাইকারি' in pgB.evaluate("document.getElementById('mpGrid').textContent"))
    pgB.click('#mpGrid .po-info a'); pgB.wait_for_timeout(1600)
    check("click opens business page", 'business.html' in pgB.url, pgB.url)
    check("business page loaded", 'Rahim Garments' in pgB.evaluate("document.body.textContent"))

    # ---------- not found ----------
    pgAnon.goto(BASE + '/business.html?id=00000000-0000-0000-0000-000000000000', wait_until='domcontentloaded'); pgAnon.wait_for_timeout(1200)
    check("bad id -> not found page", 'পাওয়া যায়নি' in pgAnon.evaluate("document.body.textContent"))

    # ---------- supplier & both account types ----------
    pgB.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1000)
    pgB.select_option('#ppBizType', 'manufacturer')
    pgB.fill('#ppCapacity', '20,000 pcs per month')
    pgB.fill('#ppProducts', 'Hoodies, Sweatshirts')
    pgB.click('#ppSave'); pgB.wait_for_timeout(2200)
    B_id = pgB.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")
    pgB.goto(BASE + '/business.html?id=' + B_id, wait_until='domcontentloaded'); pgB.wait_for_timeout(1300)
    bodyBp = pgB.evaluate("document.body.textContent")
    check("supplier biz type manufacturer", 'প্রস্তুতকারক' in bodyBp)
    check("supplier capacity shown", '20,000 pcs' in bodyBp)

    # ---------- language switch EN ----------
    pgB.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgB.wait_for_timeout(1000)
    pgB.click('.lang-btn[data-lang="en"]'); pgB.wait_for_timeout(600)
    bodyEn = pgB.evaluate("document.body.textContent")
    check("EN: Business Type label", 'Business Type' in bodyEn)
    check("EN: Wholesaler type", 'Wholesaler' in bodyEn)
    check("EN: Active Opportunities", 'Active Opportunities' in bodyEn)
    pgB.screenshot(path='qa-auth/bp-2-public-en.png')

    print("\npage errors:", errs if errs else "none")
    b.close()

print("\n===== SUMMARY =====")
fails = [r for r in results if not r[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed; failures: {[r[0] for r in fails]}")
