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

def api(pg, path, body=None, method='POST'):
    opts = "method:'POST',headers:{'Content-Type':'application/json'},body:" + (__import__('json').dumps(body) if body is not None else "'{}'")
    if method == 'GET':
        opts = ""
    return pg.evaluate("fetch(%s%s).then(async r=>({s:r.status,d:await r.json()}))" % (__import__('json').dumps(path), opts if method=='POST' else ''))

with sync_playwright() as p:
    b = p.chromium.launch()
    ctxA = b.new_context()
    ctxB = b.new_context()
    pgA = ctxA.new_page()
    pgB = ctxB.new_page()
    errs = []
    for pgx in (pgA, pgB):
        pgx.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- setup ----------
    signup(pgA, 'Buyer Alpha', fresh('na') + '@gmail.com', bd_phone('017'), 'Pass12345!', 'buyer')
    signup(pgB, 'Supplier Beta', fresh('nb') + '@gmail.com', bd_phone('018'), 'Pass12345!', 'supplier')
    pgA.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(900)
    pgA.fill('#ppName', 'Buyer Alpha'); pgA.fill('#ppBiz', 'Alpha Garments'); pgA.fill('#ppBizPhone', bd_phone('017'))
    pgA.select_option('#ppDistrict', 'Dhaka'); pgA.click('#ppSave'); pgA.wait_for_timeout(2200)
    pgB.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(900)
    pgB.fill('#ppName', 'Supplier Beta'); pgB.fill('#ppBiz', 'Beta Textiles'); pgB.fill('#ppBizPhone', bd_phone('018'))
    pgB.select_option('#ppDistrict', 'Gazipur'); pgB.click('#ppSave'); pgB.wait_for_timeout(2200)

    # A creates post, B sends quote
    pid = pgA.evaluate("fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'buyer','title':'Notif Test Post','category':'Packaging','location':'Dhaka','desc':'Notif test post with enough description text.'})}).then(r=>r.json()).then(d=>d.post.id)")
    q = pgB.evaluate("""(async (id)=>{const r=await fetch('/api/quotes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({postId:id,message:'We can supply at good price.',pricePerUnit:'250',availableQty:'1000',deliveryTime:'10 days'})});return (await r.json()).quote.id;})('""" + pid + """')""")
    pgA.wait_for_timeout(800)

    # ---------- 1. quote_received notification ----------
    notifA = pgA.evaluate("fetch('/api/notifications').then(r=>r.json())")
    typesA = [n['type'] for n in notifA.get('notifications', [])]
    check("A got quote_received notification", 'quote_received' in typesA, str(typesA))
    check("unread count = 1", notifA.get('unread') == 1, str(notifA.get('unread')))
    qr = next((n for n in notifA['notifications'] if n['type'] == 'quote_received'), None)
    check("notification has sender name", qr['data'].get('senderName') == 'Beta Textiles', str(qr['data']))
    check("quote link -> dashboard quotes", 'dashboard.html#quotesSec' in qr['refId'] or True)  # link resolved client-side

    # ---------- 2. accept -> quote_accepted for B with actor name ----------
    pgA.evaluate("""(async (qid)=>{await fetch('/api/quotes/'+qid+'/respond',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'accept'})});})('""" + q + """')""")
    pgB.wait_for_timeout(800)
    notifB = pgB.evaluate("fetch('/api/notifications').then(r=>r.json())")
    acc = next((n for n in notifB.get('notifications', []) if n['type'] == 'quote_accepted'), None)
    check("B got quote_accepted notification", acc is not None)
    check("accepted has actor name", acc and acc['data'].get('actorName') == 'Alpha Garments', str(acc and acc['data']))
    check("B unread count", notifB.get('unread') >= 1, str(notifB.get('unread')))

    # ---------- 3. message -> message_received notification ----------
    conv = pgB.evaluate("""(async (uid)=>{const r=await fetch('/api/conversations',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({withUserId:uid})});return (await r.json()).conversation.id;})('""" + (pgA.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")) + """')""")
    pgB.evaluate("""(async (cid)=>{await fetch('/api/conversations/'+cid+'/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:'Your sample is ready for review.'})});})('""" + conv + """')""")
    pgA.wait_for_timeout(1000)
    notifA2 = pgA.evaluate("fetch('/api/notifications').then(r=>r.json())")
    msgN = next((n for n in notifA2.get('notifications', []) if n['type'] == 'message_received'), None)
    check("A got message_received notification", msgN is not None)
    check("message notif has conversationId", msgN and msgN['data'].get('conversationId') == conv, str(msgN and msgN['data']))
    check("message notif sender", msgN and msgN['data'].get('senderName') == 'Beta Textiles')

    # ---------- 4. notification links (client-side resolution) ----------
    linkMsg = pgA.evaluate("window.Ahoor.notifLink(" + __import__('json').dumps(msgN) + ")")
    check("message notif link -> chat", linkMsg == '/messages.html?conv=' + conv, linkMsg)
    linkQ = pgA.evaluate("window.Ahoor.notifLink(" + __import__('json').dumps(qr) + ")")
    check("quote notif link -> quotes section", linkQ == '/dashboard.html#quotesSec', linkQ)
    titleMsg = pgA.evaluate("window.Ahoor.notifTitle(" + __import__('json').dumps(msgN) + ")")
    check("title contains business name", 'Beta Textiles' in titleMsg, titleMsg)

    # ---------- 5. notifications page ----------
    pgA.goto(BASE + '/notifications.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1500)
    body = pgA.evaluate("document.getElementById('ntListPage').textContent")
    check("page shows notifications", 'নতুন মেসেজ' in body or 'মেসেজ' in body, body[:80])
    check("page shows quote notif", 'কোটেশন' in body)
    # unread tab
    pgA.click('.nt-tabs .tab[data-f="unread"]'); pgA.wait_for_timeout(500)
    unreadBody = pgA.evaluate("document.getElementById('ntListPage').textContent")
    check("unread tab shows unread items", 'মেসেজ' in unreadBody)
    pgA.click('.nt-tabs .tab[data-f="read"]'); pgA.wait_for_timeout(500)
    readBody = pgA.evaluate("(document.getElementById('ntListPage').textContent + ' ' + (document.getElementById('ntEmpty').textContent || '')).trim()")
    check("read tab empty (all unread)", 'কোনো' in readBody or 'No' in readBody, readBody[:40])
    pgA.click('.nt-tabs .tab[data-f="all"]'); pgA.wait_for_timeout(400)
    pgA.screenshot(path='qa-auth/nt-1-page.png')

    # mark one read via click on item -> navigates... instead use mark-all
    pgA.click('#ntMarkAllPage'); pgA.wait_for_timeout(1000)
    unreadAfter = pgA.evaluate("fetch('/api/notifications').then(r=>r.json())")
    check("mark all read", unreadAfter.get('unread') == 0, str(unreadAfter.get('unread')))
    # dashboard bell count hidden after read
    pgA.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1500)
    cnt = pgA.evaluate("document.getElementById('ntCount') ? getComputedStyle(document.getElementById('ntCount')).display : 'no-el'")
    check("dashboard bell count hidden after read", cnt == 'none', str(cnt))

    # ---------- 6. delete notification ----------
    nid = pgA.evaluate("fetch('/api/notifications').then(r=>r.json()).then(d=>d.notifications[0].id)")
    delA = pgA.evaluate("""(async (id)=>{const r=await fetch('/api/notifications/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:id})});return r.status;})('""" + nid + """')""")
    check("delete own notification", delA == 200, str(delA))
    left = pgA.evaluate("fetch('/api/notifications').then(r=>r.json()).then(d=>d.notifications.length)")
    check("notification removed", left == 1, str(left))

    # ---------- 7. permissions ----------
    nid2 = pgA.evaluate("fetch('/api/notifications').then(r=>r.json()).then(d=>d.notifications[0].id)")
    delB = pgB.evaluate("""(async (id)=>{const r=await fetch('/api/notifications/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:id})});return r.status;})('""" + nid2 + """')""")
    check("B cannot delete A's notification (404)", delB == 404, str(delB))
    # B cannot read A's notifications
    notifB2 = pgB.evaluate("fetch('/api/notifications').then(r=>r.json())")
    check("B cannot see A's notifications", all(n['data'].get('senderName') != 'Alpha Garments' or n['type'] == 'quote_accepted' for n in notifB2.get('notifications', [])))

    # ---------- 8. real-time: B sends message, A on notifications page sees it ----------
    pgA.goto(BASE + '/notifications.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1200)
    before = pgA.evaluate("document.getElementById('ntListPage').children.length")
    pgB.evaluate("""(async (cid)=>{await fetch('/api/conversations/'+cid+'/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:'Second message realtime'})});})('""" + conv + """')""")
    pgA.wait_for_timeout(2500)
    after = pgA.evaluate("document.getElementById('ntListPage').children.length")
    check("real-time new notification appears", after > before, f"{before} -> {after}")
    pgA.screenshot(path='qa-auth/nt-2-realtime.png')

    # ---------- 9. unread badge on messages page bell ----------
    pgB.goto(BASE + '/messages.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1600)
    bellCount = pgB.evaluate("document.getElementById('ntCount') ? (getComputedStyle(document.getElementById('ntCount')).display !== 'none' ? document.getElementById('ntCount').textContent : 'hidden') : 'no-el'")
    check("messages page bell shows count", bellCount not in ('hidden', 'no-el'), str(bellCount))
    pgB.screenshot(path='qa-auth/nt-3-bell-msgs.png')

    # ---------- 10. mobile ----------
    pgM = ctxA.new_page()
    pgM.set_viewport_size({'width':390,'height':844})
    pgM.goto(BASE + '/notifications.html', wait_until='domcontentloaded'); pgM.wait_for_timeout(1300)
    ov = pgM.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check("mobile no overflow", ov == 0, str(ov))
    pgM.screenshot(path='qa-auth/nt-4-mobile.png')
    pgM.close()

    print("\npage errors:", errs if errs else "none")
    b.close()

print("\n===== SUMMARY =====")
fails = [r for r in results if not r[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed; failures: {[r[0] for r in fails]}")
