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

def fill_profile(pg, name, biz, biztype, cat, district, products):
    pg.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pg.wait_for_timeout(900)
    pg.fill('#ppName', name); pg.fill('#ppBiz', biz)
    pg.select_option('#ppBizType', biztype)
    pg.select_option('#ppCat', cat)
    pg.select_option('#ppDistrict', district)
    pg.fill('#ppProducts', products)
    pg.click('#ppSave'); pg.wait_for_timeout(2200)

with sync_playwright() as p:
    b = p.chromium.launch()
    ctxA = b.new_context(); ctxB = b.new_context()
    pgA = ctxA.new_page(); pgB = ctxB.new_page()
    errs = []
    for pgx in (pgA, pgB):
        pgx.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- setup: A supplier (analytics owner), B buyer (visitor) ----------
    signup(pgA, 'Analytics Owner', fresh('na') + '@gmail.com', bd_phone('017'), 'Pass12345!', 'supplier')
    fill_profile(pgA, 'Analytics Owner', 'AnCo Textiles', 'manufacturer', 'Textile & Fabric', 'Dhaka', 'T-Shirts, Fabric')
    A_id = pgA.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")
    signup(pgB, 'Visitor Buyer', fresh('nb') + '@gmail.com', bd_phone('018'), 'Pass12345!', 'buyer')

    # A creates a post
    pid = pgA.evaluate("fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'supplier','title':'Premium T-Shirts Offer','category':'Textile & Fabric','qty':'10000','unit':'PCS','moq':'100','location':'Dhaka','desc':'Premium cotton t-shirts supply offer with enough text.'})}).then(r=>r.json()).then(d=>d.post.id)")

    # ---------- 1. PROFILE VIEW TRACKING (dedupe same viewer) ----------
    pgB.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgB.wait_for_timeout(1200)
    pgB.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgB.wait_for_timeout(1000)
    # another context (C = anon) views once
    ctxC = b.new_context(); pgC = ctxC.new_page()
    pgC.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgC.wait_for_timeout(1200)
    ctxC.close()
    # B views a third time — should still count as 1 (dedupe 30min)
    pgB.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgB.wait_for_timeout(900)
    an = pgA.evaluate("fetch('/api/analytics?period=30').then(r=>r.json())")
    pv = an['analytics']['profileViews']
    check("profile views tracked (deduped)", pv == 2, str(pv))  # B=1 + anon=1

    # ---------- 2. POST VIEW TRACKING ----------
    pgB.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1400)
    pgB.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1000)
    pgC2 = b.new_context(); pgC2b = pgC2.new_page()
    pgC2b.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgC2b.wait_for_timeout(1200)
    pgC2.close()
    an2 = pgA.evaluate("fetch('/api/analytics?period=30').then(r=>r.json())")
    pv2 = an2['analytics']['postViews']
    check("post views tracked (deduped)", pv2 == 2, str(pv2))  # B=1 + anon=1
    check("postStats has my post", any(ps['id'] == pid for ps in an2['analytics']['postStats']))

    # ---------- 3. QUOTE + MESSAGE stats ----------
    q = pgB.evaluate("""(async (id)=>{const r=await fetch('/api/quotes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({postId:id,message:'We need 1000 pcs quote please.',pricePerUnit:'240',availableQty:'5000',deliveryTime:'10 days'})});return (await r.json()).quote.id;})('""" + pid + """')""")
    # A accepts
    pgA.evaluate("""(async (qid)=>{await fetch('/api/quotes/'+qid+'/respond',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'accept'})});})('""" + q + """')""")
    # message: B -> A
    conv = pgB.evaluate("""(async (id)=>{const r=await fetch('/api/conversations',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({withUserId:id})});return (await r.json()).conversation.id;})('""" + A_id + """')""")
    pgB.evaluate("""(async (cid)=>{await fetch('/api/conversations/'+cid+'/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:'Can you send samples?'})});})('""" + conv + """')""")
    pgA.evaluate("""(async (cid)=>{await fetch('/api/conversations/'+cid+'/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:'Yes, samples available'})});})('""" + conv + """')""")

    an3 = pgA.evaluate("fetch('/api/analytics?period=30').then(r=>r.json())")['analytics']
    check("requests received = 1 (supplier post)", an3['requestsReceived'] == 1, str(an3['requestsReceived']))
    check("recv accepted = 1", an3['recvAccepted'] == 1, str(an3['recvAccepted']))
    check("messages received = 1", an3['messagesReceived'] == 1, str(an3['messagesReceived']))
    check("messages sent = 1", an3['messagesSent'] == 1, str(an3['messagesSent']))
    check("active posts = 1", an3['activePosts'] == 1, str(an3['activePosts']))
    check("recent activity not empty", len(an3['activity']) > 0, str(len(an3['activity'])))

    # ---------- 4. TIME FILTERS ----------
    anAll = pgA.evaluate("fetch('/api/analytics?period=all').then(r=>r.json())")['analytics']
    an7 = pgA.evaluate("fetch('/api/analytics?period=7').then(r=>r.json())")['analytics']
    check("all-time includes same data", anAll['requestsReceived'] >= 1 and anAll['profileViews'] >= 1)
    check("7-day includes recent", an7['requestsReceived'] == 1 and an7['profileViews'] >= 1)

    # ---------- 5. POST INSIGHTS (owner only) ----------
    ins = pgA.evaluate("fetch('/api/posts/insights?postId=' + 'X' + '&period=30').then(r=>r.status)") if False else None
    ins = pgA.evaluate("""(async (id)=>{const r=await fetch('/api/posts/insights?postId='+id+'&period=30');const d=await r.json();return {s:r.status, i:d.insights};})('""" + pid + """')""")
    check("post insights owner (200)", ins['s'] == 200, str(ins['s']))
    check("post insights views", ins['i']['views'] >= 1, str(ins['i']['views']))
    check("post insights requests", ins['i']['requests'] == 1, str(ins['i']['requests']))
    # other user blocked
    insB = pgB.evaluate("""(async (id)=>{const r=await fetch('/api/posts/insights?postId='+id+'&period=30');return r.status;})('""" + pid + """')""")
    check("other user blocked from post insights (403)", insB == 403, str(insB))

    # ---------- 6. PERMISSIONS ----------
    anB = pgB.evaluate("fetch('/api/analytics?period=30').then(r=>r.json())")['analytics']
    check("B analytics own (0 quotes received)", anB['quotesReceived'] == 0, str(anB['quotesReceived']))
    check("B profile views of own (0)", anB['profileViews'] == 0, str(anB['profileViews']))

    # ---------- 7. ANALYTICS PAGE UI ----------
    pgA.goto(BASE + '/analytics.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1800)
    body = pgA.evaluate("document.getElementById('anBody').textContent")
    check("analytics page shows cards", 'প্রোফাইল দেখা' in body or 'Profile Views' in body, body[:60])
    check("analytics page shows post table", 'Premium T-Shirts Offer' in body)
    check("analytics page shows activity", 'নতুন পোস্ট' in body or 'New post' in body)
    pgA.screenshot(path='qa-auth/an-1-page.png')
    # time filter click 7d
    pgA.click('.an-period[data-p="7"]'); pgA.wait_for_timeout(1200)
    body7 = pgA.evaluate("document.getElementById('anBody').textContent")
    check("7d filter works", 'Premium T-Shirts Offer' in body7)
    pgA.screenshot(path='qa-auth/an-2-page-7d.png')

    # ---------- 8. DASHBOARD INSIGHTS SECTION ----------
    pgA.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1800)
    anSum = pgA.evaluate("document.getElementById('anSummary').textContent")
    check("dashboard insights cards", 'প্রোফাইল দেখা' in anSum or 'Profile Views' in anSum, anSum[:60])
    check("dashboard view full link", pgA.evaluate("!!document.querySelector('a[href=\"/analytics.html\"]')"))
    pgA.screenshot(path='qa-auth/an-3-dashboard.png')

    # ---------- 9. LANGUAGE ----------
    pgA.goto(BASE + '/analytics.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1300)
    pgA.click('.lang-btn[data-lang="en"]'); pgA.wait_for_timeout(800)
    enH = pgA.evaluate("document.querySelector('.an-head h1').textContent")
    check("EN analytics title", enH == 'Business Insights', enH)
    enBody = pgA.evaluate("document.getElementById('anBody').textContent")
    check("EN cards", 'Profile Views' in enBody or 'Post Views' in enBody)

    # ---------- 10. MOBILE ----------
    pgM = ctxA.new_page()
    pgM.set_viewport_size({'width':390,'height':844})
    pgM.goto(BASE + '/analytics.html', wait_until='domcontentloaded'); pgM.wait_for_timeout(1600)
    ov = pgM.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check("mobile no overflow", ov == 0, str(ov))
    pgM.screenshot(path='qa-auth/an-4-mobile.png')
    pgM.close()

    print("\npage errors:", errs if errs else "none")
    b.close()

print("\n===== SUMMARY =====")
fails = [r for r in results if not r[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed; failures: {[r[0] for r in fails]}")
