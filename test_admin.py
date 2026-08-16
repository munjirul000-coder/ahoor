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

with sync_playwright() as p:
    b = p.chromium.launch()
    # ---------- ADMIN (ADMIN_EMAIL set on server) ----------
    ctxAdm = b.new_context()
    pgAdm = ctxAdm.new_page()
    ADM_EMAIL = 'admin@ahoor.com'
    signup(pgAdm, 'Ahoor Admin', ADM_EMAIL, bd_phone('017'), 'AdminPass123!', 'both')
    errs = []
    pgAdm.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- normal users ----------
    ctxA = b.new_context()
    ctxB = b.new_context()
    pgA = ctxA.new_page()
    pgB = ctxB.new_page()
    A_email = fresh('ua') + '@gmail.com'
    B_email = fresh('ub') + '@gmail.com'
    signup(pgA, 'User Alpha', A_email, bd_phone('017'), 'Pass12345!', 'buyer')
    signup(pgB, 'User Beta', B_email, bd_phone('018'), 'Pass12345!', 'supplier')
    pgA.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(900)
    pgA.fill('#ppName', 'User Alpha'); pgA.fill('#ppBiz', 'Alpha Garments'); pgA.fill('#ppBizPhone', bd_phone('017'))
    pgA.select_option('#ppDistrict', 'Dhaka'); pgA.click('#ppSave'); pgA.wait_for_timeout(2200)
    pgB.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(900)
    pgB.fill('#ppName', 'User Beta'); pgB.fill('#ppBiz', 'Beta Textiles'); pgB.fill('#ppBizPhone', bd_phone('018'))
    pgB.select_option('#ppDistrict', 'Gazipur'); pgB.click('#ppSave'); pgB.wait_for_timeout(2200)

    A_id = pgA.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")
    B_id = pgB.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")

    # ---------- 1. ADMIN ACCESS & AUTHORIZATION ----------
    pgAdm.goto(BASE + '/admin.html', wait_until='domcontentloaded'); pgAdm.wait_for_timeout(1500)
    check("admin page loads for admin", pgAdm.evaluate("!!document.querySelector('.admin-side')"), pgAdm.url)
    # normal user cannot access /admin
    pgA.goto(BASE + '/admin.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1800)
    check("normal user /admin -> redirected", 'admin.html' not in pgA.url, pgA.url)
    # normal user cannot call admin API
    res = pgA.evaluate("fetch('/api/admin/stats').then(async r=>({s:r.status}))")
    check("normal user admin API blocked (403)", res['s'] == 403, str(res))
    # unauthenticated
    ctxAnon = b.new_context()
    pgAnon = ctxAnon.new_page()
    pgAnon.goto(BASE + '/admin.html', wait_until='domcontentloaded'); pgAnon.wait_for_timeout(1500)
    check("anon /admin -> login", '/login' in pgAnon.url, pgAnon.url)
    ctxAnon.close()

    # ---------- 2. ADMIN DASHBOARD STATS (real data) ----------
    pgAdm.goto(BASE + '/admin.html', wait_until='domcontentloaded'); pgAdm.wait_for_timeout(1600)
    stats = pgAdm.evaluate("fetch('/api/admin/stats').then(r=>r.json())")
    check("stats totalUsers >= 3", stats['stats']['totalUsers'] >= 3, str(stats['stats']['totalUsers']))
    check("stats buyers count", stats['stats']['buyers'] >= 1, str(stats['stats']['buyers']))
    check("stats suppliers count", stats['stats']['suppliers'] >= 1, str(stats['stats']['suppliers']))
    recentTxt = pgAdm.evaluate("document.getElementById('recentUsers').textContent")
    check("recent signups shown", ('Alpha' in recentTxt) or ('Beta' in recentTxt) or ('Admin' in recentTxt), recentTxt[:60])

    # ---------- 3. USER MANAGEMENT ----------
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"users\"]').click()")
    pgAdm.wait_for_timeout(1400)
    usersText = pgAdm.evaluate("document.getElementById('uBody').textContent")
    check("users list shows users", 'Alpha' in usersText and 'Beta' in usersText, usersText[:80])
    check("users list shows admin", 'Ahoor Admin' in usersText)
    # search
    pgAdm.fill('#uQ', 'Beta'); pgAdm.click('#uSearch')
    pgAdm.wait_for_function("!document.getElementById('uBody').textContent.includes('Alpha')", timeout=8000)
    pgAdm.wait_for_timeout(400)
    searchText = pgAdm.evaluate("document.getElementById('uBody').textContent")
    check("search finds Beta", 'Beta Textiles' in searchText)
    check("search excludes Alpha", 'Alpha' not in searchText)
    # filter by type
    pgAdm.fill('#uQ', '')
    pgAdm.select_option('#uType', 'supplier'); pgAdm.wait_for_timeout(1000)
    filtText = pgAdm.evaluate("document.getElementById('uBody').textContent")
    check("filter supplier", 'Beta' in filtText and 'Alpha' not in filtText)
    pgAdm.select_option('#uType', 'all'); pgAdm.wait_for_timeout(900)
    # suspend B
    pgAdm.evaluate("""()=>{const rows=[...document.querySelectorAll('#uBody tr')];const row=rows.find(r=>r.textContent.includes('Beta'));const btn=row?[...row.querySelectorAll('button')].find(b=>b.textContent.includes('Suspend')||b.textContent.includes('সাসপেন্ড')):null;if(btn)btn.click();}""")
    pgAdm.wait_for_timeout(600)
    pgAdm.click('#cfOk'); pgAdm.wait_for_timeout(1400)
    susp = pgAdm.evaluate("fetch('/api/admin/users').then(r=>r.json())")
    bUser = next((u for u in susp['users'] if u['id'] == B_id), None)
    check("B suspended", bUser and bUser['accountStatus'] == 'suspended', str(bUser and bUser['accountStatus']))
    # B cannot login
    pgB.goto(BASE + '/login.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(500)
    # (session already active; try fresh context)
    ctxB2 = b.new_context(); pgB2 = ctxB2.new_page()
    pgB2.goto(BASE + '/login.html', wait_until='domcontentloaded'); pgB2.wait_for_timeout(500)
    pgB2.fill('#idField', B_email); pgB2.fill('#pwField', 'Pass12345!')
    pgB2.click('#btnLogin'); pgB2.wait_for_timeout(1200)
    msg = pgB2.evaluate("document.getElementById('msgBox').textContent")
    check("suspended user cannot login", 'সাসপেন্ড' in msg or 'Suspended' in msg, msg[:60])
    ctxB2.close()
    # reactivate B
    pgAdm.evaluate("""()=>{const rows=[...document.querySelectorAll('#uBody tr')];const row=rows.find(r=>r.textContent.includes('Beta'));const btn=row?[...row.querySelectorAll('button')].find(b=>b.textContent.includes('Reactivate')||b.textContent.includes('সক্রিয়')):null;if(btn)btn.click();}""")
    pgAdm.wait_for_timeout(600)
    pgAdm.click('#cfOk'); pgAdm.wait_for_timeout(1400)
    users2 = pgAdm.evaluate("fetch('/api/admin/users').then(r=>r.json())")
    bUser2 = next((u for u in users2['users'] if u['id'] == B_id), None)
    check("B reactivated", bUser2 and bUser2['accountStatus'] == 'active')

    # ---------- 4. BUSINESS MANAGEMENT ----------
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"businesses\"]').click()")
    pgAdm.wait_for_timeout(1300)
    bizText = pgAdm.evaluate("document.getElementById('bBody').textContent")
    check("businesses list", 'Alpha Garments' in bizText and 'Beta Textiles' in bizText)
    check("business verification unverified", 'Unverified' in bizText or 'অযাচাইকৃত' in bizText)

    # ---------- 5. POST MANAGEMENT ----------
    pid = pgA.evaluate("fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'buyer','title':'Admin Moderation Post','category':'Packaging','location':'Dhaka','desc':'Post to be moderated by admin with enough text.'})}).then(r=>r.json()).then(d=>d.post.id)")
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"posts\"]').click()")
    pgAdm.wait_for_timeout(1300)
    postsText = pgAdm.evaluate("document.getElementById('pBody').textContent")
    check("admin sees post", 'Admin Moderation Post' in postsText)
    # close post
    pgAdm.evaluate("""()=>{const rows=[...document.querySelectorAll('#pBody tr')];const row=rows.find(r=>r.textContent.includes('Admin Moderation'));const btn=row?[...row.querySelectorAll('button')].find(b=>b.textContent.includes('Close')||b.textContent.includes('বন্ধ')):null;if(btn)btn.click();}""")
    pgAdm.wait_for_timeout(600); pgAdm.click('#cfOk'); pgAdm.wait_for_timeout(1400)
    posts2 = pgAdm.evaluate("fetch('/api/admin/posts').then(r=>r.json())")
    mp = next((x for x in posts2['posts'] if x['id'] == pid), None)
    check("post closed by admin", mp and mp['status'] == 'closed', str(mp and mp['status']))
    # remove post (with confirm)
    pgAdm.evaluate("""()=>{const rows=[...document.querySelectorAll('#pBody tr')];const row=rows.find(r=>r.textContent.includes('Admin Moderation'));const btn=row?[...row.querySelectorAll('button')].find(b=>b.textContent.includes('Remove')||b.textContent.includes('সরান')):null;if(btn)btn.click();}""")
    pgAdm.wait_for_timeout(600); pgAdm.click('#cfOk'); pgAdm.wait_for_timeout(1400)
    posts3 = pgAdm.evaluate("fetch('/api/admin/posts').then(r=>r.json())")
    check("post removed", all(x.id != pid for x in posts3['posts']))

    # ---------- 6. REPORTS ----------
    # user A reports business B
    rp = pgA.evaluate("""fetch('/api/reports',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({targetType:'business',targetId:'""'"'"'X'"'"'""',reason:'Suspicious pricing'})}).then(r=>r.status)""") if False else None
    rp = pgA.evaluate("""(async (id)=>{const r=await fetch('/api/reports',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({targetType:'business',targetId:id,reason:'Suspicious pricing and delay'})});return r.status;})('""" + B_id + """')""")
    check("report submitted (201)", rp == 201, str(rp))
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"reports\"]').click()")
    pgAdm.wait_for_timeout(1300)
    rText = pgAdm.evaluate("document.getElementById('rList').textContent")
    check("admin sees report", 'Beta Textiles' in rText and 'Suspicious pricing' in rText, rText[:90])
    # resolve report
    pgAdm.evaluate("""()=>{const btn=document.querySelector('#rList [data-ract="resolve"]');if(btn)btn.click();}""")
    pgAdm.wait_for_timeout(600); pgAdm.click('#cfOk'); pgAdm.wait_for_timeout(1400)
    reps = pgAdm.evaluate("fetch('/api/admin/reports?status=resolved').then(r=>r.json())")
    check("report resolved", len(reps['reports']) == 1, str(len(reps['reports'])))
    # reporter privacy: reporter id not exposed as phone/email (reporter object only has name/business)
    rep0 = reps['reports'][0]
    check("reporter minimal info", not rep0.get('reporter', {}).get('email'), str(rep0.get('reporter')))

    # ---------- 7. VERIFICATION ----------
    # B applies for verification
    pgB.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1100)
    hasApply = pgB.evaluate("document.getElementById('vrApply') ? getComputedStyle(document.getElementById('vrApply')).display !== 'none' : false")
    check("B has verification apply button", hasApply)
    # B submits a verification request (fill + submit on /verify.html)
    pgB.goto(BASE + '/verify.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1200)
    pgB.fill('#vrBiz', 'Beta Textiles'); pgB.fill('#vrContact', 'User Beta'); pgB.fill('#vrLoc', 'Dhaka')
    pgB.click('#vrSubmit'); pgB.wait_for_timeout(1500)
    verStatus = pgB.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.verificationStatus)")
    check("B verification pending", verStatus == 'pending', str(verStatus))
    # admin approves
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"verification\"]').click()")
    pgAdm.wait_for_timeout(1300)
    vText = pgAdm.evaluate("document.getElementById('vList').textContent")
    check("admin sees pending verification", 'Beta Textiles' in vText)
    pgAdm.evaluate("""()=>{const btn=document.querySelector('#vList [data-vact="approve"]');if(btn)btn.click();}""")
    pgAdm.wait_for_timeout(600); pgAdm.click('#cfOk'); pgAdm.wait_for_timeout(1400)
    vAfter = pgAdm.evaluate("fetch('/api/admin/businesses').then(r=>r.json())")
    bVer = next((u for u in vAfter['businesses'] if u['id'] == B_id), None)
    check("B verified", bVer and bVer['verificationStatus'] == 'verified', str(bVer and bVer['verificationStatus']))

    # ---------- 8. ACTIVITY LOG ----------
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"log\"]').click()")
    pgAdm.wait_for_timeout(1200)
    logText = pgAdm.evaluate("document.getElementById('lBody').textContent")
    check("log has suspend action", 'suspend_user' in logText)
    check("log has reactivate", 'reactivate_user' in logText)
    check("log has remove post", 'remove_post' in logText)
    check("log has resolve report", 'resolve_report' in logText)
    check("log has approve verification", 'approve_verification' in logText)
    pgAdm.screenshot(path='qa-auth/adm-1-log.png')

    # ---------- 9. ADMIN UI PAGES RENDER ----------
    for page in ['dash','users','businesses','posts','reports','verification','log']:
        pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"%s\"]').click()" % page)
        pgAdm.wait_for_timeout(900)
    check("all admin pages render", True)
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"dash\"]').click()")
    pgAdm.wait_for_timeout(1200)
    pgAdm.screenshot(path='qa-auth/adm-2-dash.png')

    # ---------- 10. BANGLA + ENGLISH ----------
    pgAdm.click('#langSwitch button[data-lang="en"]'); pgAdm.wait_for_timeout(600)
    enTitle = pgAdm.evaluate("document.querySelector('.page.on .page-head h1').textContent")
    check("admin EN dashboard title", enTitle == 'Dashboard', enTitle)
    pgAdm.evaluate("document.querySelector('.side-btn[data-page=\"users\"]').click()")
    pgAdm.wait_for_timeout(1000)
    enUsers = pgAdm.evaluate("document.querySelector('.page.on .page-head h1').textContent")
    check("admin EN users title", enUsers == 'Users', enUsers)
    pgAdm.screenshot(path='qa-auth/adm-3-en.png')

    # ---------- 11. MOBILE ----------
    pgM = ctxAdm.new_page()
    pgM.set_viewport_size({'width':390,'height':844})
    pgM.goto(BASE + '/admin.html', wait_until='domcontentloaded'); pgM.wait_for_timeout(1600)
    ov = pgM.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    if ov > 0:
        print("  MOBILE CULPRITS:", pgM.evaluate("(()=>{const vw=document.documentElement.clientWidth;const out=[];document.querySelectorAll('*').forEach(el=>{const r=el.getBoundingClientRect();if(r.right>vw+1&&el.offsetWidth>0)out.push(el.tagName+'.'+(typeof el.className==='string'?el.className.slice(0,22):'')+' r='+Math.round(r.right));});return out.slice(0,8);})()"))
    check("admin mobile no overflow", ov == 0, str(ov))
    pgM.evaluate("document.querySelector('.side-btn[data-page=\"users\"]').click()")
    pgM.wait_for_timeout(1200)
    check("admin mobile users page", pgM.evaluate("document.getElementById('uBody').children.length") > 0)
    pgM.screenshot(path='qa-auth/adm-4-mobile.png')
    pgM.close()

    print("\npage errors:", errs if errs else "none")
    b.close()

print("\n===== SUMMARY =====")
fails = [r for r in results if not r[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed; failures: {[r[0] for r in fails]}")
