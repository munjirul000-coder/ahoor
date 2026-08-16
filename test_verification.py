from playwright.sync_api import sync_playwright
import random, time, re, base64, json

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

TINY_PNG = base64.b64encode(bytes.fromhex(
    '89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489'
    '0000000d4944415478da63fcc0f0ff3f00060801ff9b15a3cf0000000049454e44ae426082'
)).decode()

with sync_playwright() as p:
    b = p.chromium.launch()
    ctxA = b.new_context(); ctxB = b.new_context(); ctxAdm = b.new_context()
    pgA = ctxA.new_page()   # business owner
    pgB = ctxB.new_page()   # other user
    pgAdm = ctxAdm.new_page()  # admin
    errs = []
    for pgx in (pgA, pgB, pgAdm):
        pgx.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- setup ----------
    signup(pgA, 'Owner One', fresh('va') + '@gmail.com', bd_phone('017'), 'Pass12345!', 'supplier')
    fill_profile(pgA, 'Owner One', 'Verified Co Ltd', 'manufacturer', 'Garments & Apparel', 'Dhaka', 'T-Shirts')
    A_id = pgA.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")

    signup(pgB, 'User Two', fresh('vb') + '@gmail.com', bd_phone('018'), 'Pass12345!', 'buyer')
    fill_profile(pgB, 'User Two', 'Beta Traders', 'buyer', 'Packaging', 'Chattogram', '')
    signup(pgAdm, 'Admin X', 'admin@ahoor.com', bd_phone('019'), 'Pass12345!', 'both')

    # ---------- 1. APPLY: docs validation (bad type) ----------
    bad = pgA.evaluate("""fetch('/api/verification-request',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({businessName:'Verified Co Ltd',contactPerson:'Owner One',location:'Dhaka',documents:[{name:'evil.exe',data:'data:application/octet-stream;base64,AAAA'}]})}).then(r=>r.json()).then(d=>d.error||'ok')""")
    check("exe document rejected", bad == 'doc_type', str(bad))

    # ---------- 2. APPLY with valid docs (pdf + png) ----------
    r = pgA.evaluate("""fetch('/api/verification-request',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({businessName:'Verified Co Ltd',contactPerson:'Owner One',businessType:'manufacturer',location:'Dhaka',phone:'01711112222',email:'biz@verified.com',documents:[{name:'license.pdf',data:'data:application/pdf;base64,JVBERi0xLjQK'},{name:'reg.png',data:'data:image/png;base64,""" + TINY_PNG + """'}]})}).then(r=>r.json())""")
    check("application submitted", r.get('request', {}).get('status') == 'pending', str(r)[:80])
    reqId = r['request']['id']
    # duplicate submit blocked
    dup = pgA.evaluate("""fetch('/api/verification-request',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({businessName:'Verified Co Ltd',contactPerson:'Owner One',location:'Dhaka'})}).then(r=>r.json()).then(d=>d.error||'ok')""")
    check("duplicate submit blocked", dup == 'already_pending', str(dup))

    # ---------- 3. OWNER sees own status + docs; OTHER cannot ----------
    mine = pgA.evaluate("fetch('/api/verification-request').then(r=>r.json())")
    check("owner sees own request", len(mine.get('requests', [])) == 1)
    check("owner sees own documents", len(mine['requests'][0].get('documents', [])) == 2)
    others = pgB.evaluate("fetch('/api/verification-request').then(r=>r.json())")
    check("other user sees no requests", len(others.get('requests', [])) == 0, str(len(others.get('requests', []))))
    # owner status pending
    st = pgA.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.verificationStatus)")
    check("owner status pending", st == 'pending', str(st))

    # ---------- 4. notification submitted ----------
    notif = pgA.evaluate("fetch('/api/notifications').then(r=>r.json())")
    check("submitted notification", any(n['type'] == 'verification_submitted' for n in notif.get('notifications', [])))

    # ---------- 5. ADMIN sees request + docs ----------
    pgAdm.goto(BASE + '/admin.html', wait_until='domcontentloaded'); pgAdm.wait_for_timeout(1500)
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"verification\"]').click()")
    pgAdm.wait_for_timeout(1400)
    vText = pgAdm.evaluate("document.getElementById('vList').textContent")
    check("admin sees pending request", 'Verified Co Ltd' in vText)
    check("admin sees contact/phone/email", 'biz@verified.com' in vText and '01711112222' in vText)
    check("admin sees document names", 'license.pdf' in vText and 'reg.png' in vText)
    pgAdm.screenshot(path='qa-auth/vr-1-admin-pending.png')

    # ---------- 6. OTHER user cannot access admin docs/review ----------
    badAdmin = pgB.evaluate("fetch('/api/admin/verification-requests?status=pending').then(r=>r.status)")
    check("other user blocked from admin docs (403)", badAdmin == 403, str(badAdmin))

    # ---------- 7. approve ----------
    pgAdm.evaluate("""()=>{const btn=document.querySelector('#vList [data-vact="approve"]');if(btn)btn.click();}""")
    pgAdm.wait_for_timeout(600); pgAdm.click('#cfOk'); pgAdm.wait_for_timeout(1400)
    st2 = pgA.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.verificationStatus)")
    check("owner verified after approval", st2 == 'verified', str(st2))
    notif2 = pgA.evaluate("fetch('/api/notifications').then(r=>r.json())")
    check("approved notification", any(n['type'] == 'verification_approved' for n in notif2.get('notifications', [])))

    # ---------- 8. VERIFIED BADGE visible ----------
    # business page
    pgB.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgB.wait_for_timeout(1300)
    bpVrf = pgB.evaluate("document.getElementById('bpVrf').textContent")
    check("business page verified badge", 'যাচাইকৃত' in bpVrf or 'Verified' in bpVrf, bpVrf)
    # marketplace post badge
    pgA.evaluate("fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'supplier','title':'Verified Co T-Shirts','category':'Garments & Apparel','location':'Dhaka','desc':'Verified supplier post with enough text.'})})")
    pgB.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1400)
    mpText = pgB.evaluate("document.getElementById('mpGrid').textContent")
    check("marketplace shows verified owner", '✅' in mpText)
    pgB.screenshot(path='qa-auth/vr-2-badge-market.png')

    # ---------- 9. REJECTION + reason + reapply ----------
    # B (buyer) also applies; admin rejects with reason
    pgB.goto(BASE + '/verify.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1200)
    check("verify page loads for B", pgB.evaluate("document.getElementById('vrFormWrap').style.display") != 'none')
    pgB.fill('#vrBiz', 'Beta Traders'); pgB.fill('#vrContact', 'User Two'); pgB.fill('#vrLoc', 'Chattogram')
    pgB.click('#vrSubmit'); pgB.wait_for_timeout(1500)
    B_req = pgB.evaluate("fetch('/api/verification-request').then(r=>r.json())")
    B_req_id = B_req['requests'][0]['id']
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"verification\"]').click()")
    pgAdm.wait_for_timeout(1300)
    pgAdm.evaluate("""()=>{const rows=[...document.querySelectorAll('#vList .panel')];const row=rows.find(r=>r.textContent.includes('Beta Traders'));const btn=row?[...row.querySelectorAll('button')].find(x=>x.textContent.includes('Reject')||x.textContent.includes('প্রত্যাখ্যান')):null;if(btn)btn.click();}""")
    pgAdm.wait_for_timeout(600)
    pgAdm.on('dialog', lambda d: d.accept('Incomplete documents'))
    pgAdm.click('#cfOk'); pgAdm.wait_for_timeout(1500)
    stB = pgB.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.verificationStatus)")
    check("B rejected", stB == 'rejected', str(stB))
    # B sees rejection reason on verify page
    pgB.goto(BASE + '/verify.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1300)
    rejText = pgB.evaluate("document.getElementById('vrRejectBox').textContent")
    check("rejection reason shown", 'Incomplete documents' in rejText, rejText[:60])
    check("reapply button shown", pgB.evaluate("document.getElementById('vrFormWrap').style.display") != 'none')
    notifB = pgB.evaluate("fetch('/api/notifications').then(r=>r.json())")
    check("rejected notification", any(n['type'] == 'verification_rejected' for n in notifB.get('notifications', [])))
    # reapply works
    pgB.fill('#vrBiz', 'Beta Traders Ltd'); pgB.fill('#vrContact', 'User Two'); pgB.fill('#vrLoc', 'Chattogram')
    pgB.click('#vrSubmit'); pgB.wait_for_timeout(1500)
    stB2 = pgB.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.verificationStatus)")
    check("B reapplied -> pending", stB2 == 'pending', str(stB2))
    pgB.screenshot(path='qa-auth/vr-3-reapply.png')

    # ---------- 10. language ----------
    pgB.goto(BASE + '/verify.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1300)
    pgB.click('.lang-btn[data-lang="en"]'); pgB.wait_for_timeout(600)
    enTitle = pgB.evaluate("document.querySelector('.auth-head h1').textContent")
    check("EN verify title", enTitle == 'Apply for Business Verification', enTitle)

    # ---------- 11. mobile ----------
    pgM = ctxA.new_page()
    pgM.set_viewport_size({'width':390,'height':844})
    pgM.goto(BASE + '/verify.html', wait_until='domcontentloaded'); pgM.wait_for_timeout(1500)
    ov = pgM.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check("mobile no overflow", ov == 0, str(ov))
    pgM.screenshot(path='qa-auth/vr-4-mobile.png')
    pgM.close()

    print("\npage errors:", errs if errs else "none")
    b.close()

print("\n===== SUMMARY =====")
fails = [r for r in results if not r[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed; failures: {[r[0] for r in fails]}")
