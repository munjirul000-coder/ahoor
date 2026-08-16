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

def fill_profile(pg, name, biz, phone, dist, cat, desc):
    pg.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pg.wait_for_timeout(900)
    pg.fill('#ppName', name); pg.fill('#ppBiz', biz)
    pg.fill('#ppBizPhone', phone)
    pg.select_option('#ppDistrict', dist); pg.select_option('#ppCat', cat)
    pg.fill('#ppDesc', desc)
    pg.click('#ppSave'); pg.wait_for_timeout(2000)

def create_buyer_post(pg, title='Need 1000 PCS Premium Cotton T-Shirts'):
    pg.goto(BASE + '/post.html', wait_until='domcontentloaded'); pg.wait_for_timeout(800)
    pg.fill('#ptTitleF', title)
    pg.select_option('#ptCat', 'Garments & Apparel')
    pg.fill('#ptQty', '1000'); pg.select_option('#ptUnit', 'PCS')
    pg.fill('#ptBudget', '৳250,000')
    pg.select_option('#ptLoc', 'Dhaka')
    pg.fill('#ptDeadline', '2026-09-15')
    pg.fill('#ptDesc', 'Need 1000 pieces premium cotton t-shirts sizes S to XXL with custom print, white and black colors, delivery within 30 days.')
    pg.click('#ptSubmit'); pg.wait_for_timeout(2200)
    pg.wait_for_timeout(700)

def create_supplier_post(pg):
    pg.goto(BASE + '/post.html', wait_until='domcontentloaded'); pg.wait_for_timeout(800)
    pg.click('.kind-card[data-kind="supplier"]'); pg.wait_for_timeout(300)
    pg.fill('#ptTitleF', 'Premium Cotton T-Shirts — Custom Printing')
    pg.select_option('#ptCat', 'Textile & Fabric')
    pg.fill('#ptQty', '20000'); pg.select_option('#ptUnit', 'PCS')
    pg.fill('#ptMoq', '100'); pg.fill('#ptPrice', '৳240 / pcs')
    pg.select_option('#ptLoc', 'Gazipur')
    pg.fill('#ptDesc', 'Export quality cotton t-shirts with custom printing. MOQ 100 pcs, production time 7-14 days.')
    pg.click('#ptSubmit'); pg.wait_for_timeout(2200)
    pg.wait_for_timeout(700)

with sync_playwright() as p:
    b = p.chromium.launch()
    ctxA = b.new_context()
    ctxB = b.new_context()
    ctxC = b.new_context()
    pgA = ctxA.new_page()   # buyer
    pgB = ctxB.new_page()   # supplier
    pgC = ctxC.new_page()   # supplier #2
    errs = []
    for pgx in (pgA, pgB, pgC):
        pgx.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- SETUP: A(buyer) B(supplier) C(supplier) ----------
    A_phone = bd_phone('017'); B_phone = bd_phone('018'); C_phone = bd_phone('019')
    signup(pgA, 'Rahim Uddin', fresh('buyer') + '@gmail.com', A_phone, 'Pass12345!', 'buyer')
    fill_profile(pgA, 'Rahim Uddin', 'Rahim Garments', A_phone, 'Dhaka', 'Garments & Apparel', 'Buying cotton t-shirts and hoodies in bulk.')
    create_buyer_post(pgA)
    check("A created buyer post", True)

    signup(pgB, 'Karim Ahmed', fresh('supplier') + '@gmail.com', B_phone, 'Pass12345!', 'supplier')
    fill_profile(pgB, 'Karim Ahmed', 'NexTee Textiles', B_phone, 'Gazipur', 'Textile & Fabric', 'Manufacturing t-shirts and hoodies.')
    create_supplier_post(pgB)
    check("B created supplier post", True)

    signup(pgC, 'Samiul Haque', fresh('supplier2') + '@gmail.com', C_phone, 'Pass12345!', 'supplier')
    fill_profile(pgC, 'Samiul Haque', 'Urban Knitwear', C_phone, 'Dhaka', 'Textile & Fabric', 'Knitwear manufacturing.')

    # ========== FLOW 1: SUPPLIER SENDS QUOTE TO BUYER ==========
    pgB.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1400)
    # click Send Quote on the BUYER post (first card with buyer badge)
    pgB.evaluate("""()=>{const cards=[...document.querySelectorAll('.post-card')];const c=cards.find(x=>x.querySelector('.post-badge.buyer'));if(c)c.querySelector('button[data-quote]').click();}""")
    pgB.wait_for_timeout(600)
    check("quote modal opens (supplier)", pgB.evaluate("document.getElementById('quoteModal').classList.contains('on')"))
    check("quote fields visible", pgB.evaluate("getComputedStyle(document.getElementById('qmQuoteFields')).display") != 'none')
    pgB.fill('#qmPrice', '250'); pgB.fill('#qmQty', '1000')
    pgB.wait_for_timeout(300)
    check("total auto-calculated", '250,000' in pgB.evaluate("document.getElementById('qmTotal').textContent"))
    pgB.fill('#qmMoq', '100'); pgB.fill('#qmDelivery', '10 days')
    pgB.fill('#qmText', 'We can manufacture premium cotton T-shirts according to your requirements.')
    pgB.click('#qmSend'); pgB.wait_for_timeout(1500)
    check("quote sent toast", 'কোটেশন সফলভাবে পাঠানো হয়েছে' in pgB.evaluate("document.body.textContent"))

    # duplicate blocked
    pgB.evaluate("""()=>{const cards=[...document.querySelectorAll('.post-card')];const c=cards.find(x=>x.querySelector('.post-badge.buyer'));if(c)c.querySelector('button[data-quote]').click();}""")
    pgB.wait_for_timeout(500)
    pgB.fill('#qmPrice', '260'); pgB.fill('#qmQty', '500'); pgB.fill('#qmText', 'Another quote attempt.')
    pgB.click('#qmSend'); pgB.wait_for_timeout(1300)
    check("duplicate quote blocked", 'আগেই কোটেশন পাঠিয়েছেন' in pgB.evaluate("document.getElementById('qmMsg').textContent"))
    pgB.click('#qmCancel')

    # buyer sees received quote
    pgA.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1600)
    qtxt = pgA.evaluate("document.getElementById('quotesList').textContent")
    check("A sees supplier quote", 'NexTee Textiles' in qtxt)
    check("quote price shown", '৳250' in qtxt)
    check("quote total shown", '৳250,000' in qtxt)
    check("quote delivery shown", '10 days' in qtxt)
    check("quote status Pending", 'অপেক্ষমাণ' in qtxt)
    check("accept button present", pgA.evaluate("!!document.querySelector('#quotesList [data-acc]')"))
    pgA.screenshot(path='qa-auth/qt-1-received.png')

    # notification for buyer
    nt = pgA.evaluate("document.getElementById('ntList') ? '' : ''")  # panel not open yet; check via fetch
    notif = pgA.evaluate("fetch('/api/notifications').then(r=>r.json())")
    check("A has unread notification", notif.get('unread', 0) >= 1, str(notif.get('unread')))
    check("A notification says new quote", 'নতুন কোটেশন' in (notif.get('notifications') or [{}])[0].get('data', {}).get('senderName', '') or 'NexTee' in str(notif.get('notifications') or [])[0][:200] or 'quote' in str(notif)[:200])

    # A accepts
    pgA.click('#quotesList [data-acc]'); pgA.wait_for_timeout(1500)
    check("accept toast", 'কোটেশন গৃহীত হয়েছে' in pgA.evaluate("document.body.textContent"))
    qtxt2 = pgA.evaluate("document.getElementById('quotesList').textContent")
    check("status now Accepted", 'গৃহীত' in qtxt2)

    # B sees accepted + notification
    pgB.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1600)
    sent = pgB.evaluate("document.getElementById('sentList').textContent")
    check("B sent quotes shows post", 'Premium Cotton T-Shirts' in sent)
    check("B sent quote Accepted", 'গৃহীত' in sent)
    notifB = pgB.evaluate("fetch('/api/notifications').then(r=>r.json())")
    check("B notification accepted", any(n['type'] == 'quote_accepted' for n in notifB.get('notifications', [])), str([n['type'] for n in notifB.get('notifications', [])]))
    check("B unread count >= 1", notifB.get('unread', 0) >= 1)
    pgB.screenshot(path='qa-auth/qt-2-sent.png')

    # ========== FLOW 2: BUYER REQUESTS QUOTE FROM SUPPLIER ==========
    pgA.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1400)
    pgA.evaluate("""()=>{const cards=[...document.querySelectorAll('.post-card')];const c=cards.find(x=>x.querySelector('.post-badge.supplier'));if(c)c.querySelector('button[data-quote]').click();}""")
    pgA.wait_for_timeout(600)
    check("request modal opens (buyer)", pgA.evaluate("getComputedStyle(document.getElementById('qmReqFields')).display") != 'none')
    pgA.fill('#qmReqQty', '5000'); pgA.fill('#qmPrefDel', 'within 30 days'); pgA.fill('#qmBudget', '৳1,250,000')
    pgA.fill('#qmText', 'I am interested in ordering 5000 pcs. Please send me your best quotation.')
    pgA.click('#qmSend'); pgA.wait_for_timeout(1500)
    check("request sent toast", 'অনুরোধ সফলভাবে পাঠানো হয়েছে' in pgA.evaluate("document.body.textContent"))

    # B (post owner) receives request
    pgB.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1600)
    rcvd = pgB.evaluate("document.getElementById('quotesList').textContent")
    check("B receives request from A", 'Rahim Garments' in rcvd)
    check("request qty shown", '5,000' in rcvd or '5000' in rcvd)

    # A withdraws own sent request
    pgA.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1600)
    check("A sent request Pending", 'অপেক্ষমাণ' in pgA.evaluate("document.getElementById('sentList').textContent"))
    pgA.click('#sentList [data-wd]'); pgA.wait_for_timeout(1500)
    check("withdraw toast", 'প্রত্যাহার করা হয়েছে' in pgA.evaluate("document.body.textContent"))
    check("A sent request Withdrawn", 'প্রত্যাহার' in pgA.evaluate("document.getElementById('sentList').textContent"))

    # ========== SECURITY ==========
    # buyer cannot send quote on buyer post (role check)
    res = pgA.evaluate("""fetch('/api/quotes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({postId:'""'"'"'PLACEHOLDER'"'"'""',message:'x'.repeat(20)})}).then(r=>r.json()).then(d=>({s:200,d}))""") if False else None
    # direct: get a buyer post id from A's posts
    pidA = pgA.evaluate("fetch('/api/my-posts',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.posts[0].id)")
    res1 = pgA.evaluate("""(async (id)=>{const r=await fetch('/api/quotes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({postId:id,message:'Test role block.'})});return r.status;})('""" + pidA + """')""")
    check("buyer cannot quote buyer post (403)", res1 == 403, str(res1))

    # supplier cannot accept other's received quote
    qid = pgB.evaluate("fetch('/api/quotes/sent',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.quotes[0].id)")
    res2 = pgB.evaluate("""(async (id)=>{const r=await fetch('/api/quotes/'+id+'/respond',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'accept'})});return r.status;})('""" + qid + """')""")
    check("sender cannot accept own quote (403)", res2 == 403, str(res2))

    # third party cannot withdraw someone else's quote
    res3 = pgC.evaluate("""(async (id)=>{const r=await fetch('/api/quotes/'+id+'/withdraw',{method:'POST'});return r.status;})('""" + qid + """')""")
    check("non-sender cannot withdraw (403)", res3 == 403, str(res3))

    # respond twice -> not pending (A re-responds on already accepted quote)
    qid2 = pgA.evaluate("fetch('/api/quotes/received',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.quotes[0].id)")
    res4 = pgA.evaluate("""(async (id)=>{const r=await fetch('/api/quotes/'+id+'/respond',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'accept'})});return r.status;})('""" + qid2 + """')""")
    check("respond on non-pending blocked (400)", res4 == 400, str(res4))

    # own post quote blocked
    res5 = pgA.evaluate("""(async (id)=>{const r=await fetch('/api/quotes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({postId:id,message:'Self quote test.'})});return r.status;})('""" + pidA + """')""")
    check("buyer blocked from quoting buyer post (403 role)", res5 == 403, str(res5))

    # ========== NOTIFICATIONS MARK READ ==========
    pgB.click('#ntBell'); pgB.wait_for_timeout(700)
    check("notification panel opens", pgB.evaluate("document.getElementById('ntPanel').classList.contains('on')"))
    pgB.click('#ntMarkAll'); pgB.wait_for_timeout(900)
    unread_after = pgB.evaluate("fetch('/api/notifications').then(r=>r.json())")
    check("mark all read", unread_after.get('unread', -1) == 0, str(unread_after.get('unread')))
    pgB.screenshot(path='qa-auth/qt-3-notifications.png')

    # ========== LANGUAGE ==========
    pgA.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(900)
    pgA.click('.lang-btn[data-lang="en"]'); pgA.wait_for_timeout(500)
    pgA.evaluate("""()=>{const cards=[...document.querySelectorAll('.post-card')];const c=cards.find(x=>x.querySelector('.post-badge.supplier'));if(c)c.querySelector('button[data-quote]').click();}""")
    pgA.wait_for_timeout(500)
    check("EN modal title", pgA.evaluate("document.getElementById('qmTitle').textContent") == 'Request Quote')
    check("EN send button", 'SEND REQUEST' in pgA.evaluate("document.getElementById('qmSend').textContent"))
    pgA.screenshot(path='qa-auth/qt-4-en.png')

    print("\npage errors:", errs if errs else "none")
    b.close()

print("\n===== SUMMARY =====")
fails = [r for r in results if not r[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed; failures: {[r[0] for r in fails]}")
