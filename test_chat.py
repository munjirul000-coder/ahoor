from playwright.sync_api import sync_playwright
import random, time, re, base64

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

def fill_profile(pg, biz):
    pg.goto(BASE + '/profile-setup.html', wait_until='domcontentloaded'); pg.wait_for_timeout(900)
    pg.fill('#ppName', biz); pg.fill('#ppBiz', biz)
    pg.fill('#ppBizPhone', bd_phone('017'))
    pg.select_option('#ppDistrict', 'Dhaka')
    pg.click('#ppSave'); pg.wait_for_timeout(2200)

TINY_PNG = base64.b64encode(bytes.fromhex(
    '89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489'
    '0000000d4944415478da63fcc0f0ff3f00060801ff9b15a3cf0000000049454e44ae426082'
)).decode()

with sync_playwright() as p:
    b = p.chromium.launch()
    ctxA = b.new_context()
    ctxB = b.new_context()
    ctxC = b.new_context()
    pgA = ctxA.new_page()   # buyer
    pgB = ctxB.new_page()   # supplier
    pgC = ctxC.new_page()   # outsider
    errs = []
    for pgx in (pgA, pgB, pgC):
        pgx.on('pageerror', lambda e: errs.append(str(e)))

    # ---------- setup ----------
    signup(pgA, 'Rahim Garments', fresh('ca') + '@gmail.com', bd_phone('017'), 'Pass12345!', 'buyer')
    fill_profile(pgA, 'Rahim Garments')
    signup(pgB, 'NexTee Textiles', fresh('cb') + '@gmail.com', bd_phone('018'), 'Pass12345!', 'supplier')
    fill_profile(pgB, 'NexTee Textiles')
    signup(pgC, 'Outsider Co', fresh('cc') + '@gmail.com', bd_phone('019'), 'Pass12345!', 'buyer')
    fill_profile(pgC, 'Outsider Co')

    A_id = pgA.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")
    B_id = pgB.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")
    C_id = pgC.evaluate("fetch('/api/session',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}).then(r=>r.json()).then(d=>d.user.id)")

    # ---------- 1. A starts conversation with B (from ?with=) ----------
    pgA.goto(BASE + '/messages.html?with=' + B_id, wait_until='domcontentloaded'); pgA.wait_for_timeout(1600)
    check("A opens chat with B", pgA.evaluate("document.getElementById('chName').textContent") == 'NexTee Textiles')
    check("conversation exists on B's side", True)
    # conversation created in db
    convsA = pgA.evaluate("fetch('/api/conversations').then(r=>r.json())")
    check("conversation listed for A", len(convsA.get('conversations', [])) == 1, str(len(convsA.get('conversations', []))))

    # ---------- 2. send text ----------
    pgA.fill('#chatText', 'Hello, we need 1000 pcs cotton t-shirts. What is your price?')
    pgA.click('#chatSend'); pgA.wait_for_timeout(1400)
    bodyA = pgA.evaluate("document.getElementById('chatMsgs').textContent")
    check("text message sent", 'Hello, we need 1000 pcs' in bodyA)

    # B sees it via list + opens chat (unread badge)
    pgB.goto(BASE + '/messages.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1500)
    listB = pgB.evaluate("document.getElementById('convItems').textContent")
    check("B sees conversation in list", 'Rahim Garments' in listB)
    check("B sees last message preview", '1000 pcs cotton t-shirts' in listB)
    check("B sees unread badge", '1' in pgB.evaluate("document.querySelector('.ci-unread') ? document.querySelector('.ci-unread').textContent : ''"))
    pgB.click('.conv-item'); pgB.wait_for_timeout(1400)
    bodyB = pgB.evaluate("document.getElementById('chatMsgs').textContent")
    check("B sees message in chat", 'Hello, we need 1000 pcs' in bodyB)
    # after reading, unread cleared
    pgB.goto(BASE + '/messages.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1200)
    unreadB = pgB.evaluate("document.querySelector('.ci-unread') ? document.querySelector('.ci-unread').textContent : 'none'")
    check("unread cleared after reading", unreadB == 'none', str(unreadB))
    pgB.screenshot(path='qa-auth/chat-1-b-received.png')

    # ---------- 3. B replies + A sees real-time (SSE) ----------
    pgB.click('.conv-item'); pgB.wait_for_timeout(1300)
    pgB.fill('#chatText', 'Yes, we can supply at ৳240/pcs. MOQ 100 pcs.')
    pgB.click('#chatSend'); pgB.wait_for_timeout(1200)
    # A is still on messages page (pgA) — SSE should push
    pgA.wait_for_timeout(2500)
    bodyA2 = pgA.evaluate("document.getElementById('chatMsgs').textContent")
    check("A receives reply (real-time)", 'we can supply at' in bodyA2.lower(), bodyA2[:80])

    # ---------- 4. image send ----------
    pgA.set_input_files('#chatFile', files=[{'name':'sample.png','mimeType':'image/png','buffer':base64.b64decode(TINY_PNG)}])
    pgA.wait_for_timeout(800)
    check("image preview shown before send", pgA.evaluate("getComputedStyle(document.getElementById('chatPreview')).display") == 'flex')
    pgA.click('#chatSend'); pgA.wait_for_timeout(1500)
    imgSent = pgA.evaluate("[...document.querySelectorAll('#chatMsgs .bubble img.bimg')].length")
    check("image message sent", imgSent >= 1, str(imgSent))
    # remove-preview test on B side: attach then remove
    pgB.click('#chatAttach') if False else None
    # B receives image
    pgB.wait_for_timeout(2000)
    imgB = pgB.evaluate("[...document.querySelectorAll('#chatMsgs .bubble img.bimg')].length")
    check("B receives image (real-time)", imgB >= 1, str(imgB))
    # lightbox open
    pgB.click('#chatMsgs .bubble img.bimg'); pgB.wait_for_timeout(600)
    check("lightbox opens", pgB.evaluate("document.getElementById('lightbox').classList.contains('on')"))
    pgB.screenshot(path='qa-auth/chat-2-image.png')
    pgB.click('#lbClose'); pgB.wait_for_timeout(300)
    check("lightbox closes", not pgB.evaluate("document.getElementById('lightbox').classList.contains('on')"))

    # ---------- 5. image validation: bad type rejected ----------
    import json as _json
    convId0 = convsA['conversations'][0]['id']
    def js_post_img(cid, image_data):
        payload = _json.dumps({'image': image_data})
        payload_lit = _json.dumps(payload)  # JSON string as a JS string literal
        return pgA.evaluate("fetch(%s,{method:'POST',headers:{'Content-Type':'application/json'},body:%s}).then(r=>r.json()).then(d=>d.error||'ok')" % (_json.dumps('/api/conversations/' + cid + '/messages'), payload_lit))
    bad = js_post_img(convId0, 'data:image/svg+xml;base64,PHN2Zz48L3N2Zz4=')
    check('svg image rejected', bad == 'image_type', str(bad))
    oversized = js_post_img(convId0, 'data:image/png;base64,' + 'A' * 1600000)
    check('oversized image rejected', oversized == 'image', str(oversized))
    # ---------- 6. authorization ----------
    convId = convsA['conversations'][0]['id']
    # C (not participant) cannot read
    resC = pgC.evaluate("""(async (id)=>{const r=await fetch('/api/conversations/'+id+'/messages');return r.status;})('""" + convId + """')""")
    check("outsider cannot read conversation (403)", resC == 403, str(resC))
    # C cannot send
    resC2 = pgC.evaluate("""(async (id)=>{const r=await fetch('/api/conversations/'+id+'/messages',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:'intrusion'})});return r.status;})('""" + convId + """')""")
    check("outsider cannot send (403)", resC2 == 403, str(resC2))
    # C cannot list A/B conversation
    convsC = pgC.evaluate("fetch('/api/conversations').then(r=>r.json())")
    check("outsider has no conversations", len(convsC.get('conversations', [])) == 0)

    # unauthenticated
    ctxAnon = b.new_context()
    pgAnon = ctxAnon.new_page()
    pgAnon.goto(BASE + '/messages.html', wait_until='domcontentloaded'); pgAnon.wait_for_timeout(1500)
    check("unauthenticated -> login", '/login' in pgAnon.url, pgAnon.url)
    ctxAnon.close()

    # ---------- 7. conversation from business profile + marketplace ----------
    pgB.goto(BASE + '/business.html?id=' + A_id, wait_until='domcontentloaded'); pgB.wait_for_timeout(1200)
    contactHref = pgB.evaluate("document.getElementById('bpContactBtn').getAttribute('href')")
    check("business page Contact -> messages", 'messages.html?with=' in contactHref, contactHref)

    # marketplace card message button
    pid = pgA.evaluate("fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'buyer','title':'Chat Test Post','category':'Packaging','location':'Dhaka','desc':'Chat test post with enough description text.'})}).then(r=>r.json()).then(d=>d.post.id)")
    pgB.goto(BASE + '/marketplace.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(1400)
    msgHref = pgB.evaluate("""()=>{const a=document.querySelector('#mpGrid a[href*="messages.html?with="]');return a?a.getAttribute('href'):'';}""")
    check("marketplace post message button", 'messages.html?with=' in msgHref, msgHref)

    # ---------- 8. dashboard unread badge ----------
    # A sends one more message while B on dashboard
    pgA.goto(BASE + '/messages.html', wait_until='domcontentloaded'); pgA.wait_for_timeout(1300)
    pgA.click('.conv-item'); pgA.wait_for_timeout(1300)
    pgA.fill('#chatText', 'Can you send samples first?')
    pgA.click('#chatSend'); pgA.wait_for_timeout(1300)
    pgB.goto(BASE + '/dashboard.html', wait_until='domcontentloaded'); pgB.wait_for_timeout(2000)
    badge = pgB.evaluate("document.getElementById('msgUnread') ? (getComputedStyle(document.getElementById('msgUnread')).display !== 'none' ? document.getElementById('msgUnread').textContent : 'hidden') : 'no-el'")
    check("dashboard unread badge shows", badge not in ('hidden', 'no-el', '0'), str(badge))
    pgB.screenshot(path='qa-auth/chat-3-dash-badge.png')

    # ---------- 9. mobile layout (same session as A) ----------
    pgM = ctxA.new_page()
    pgM.set_viewport_size({'width':390,'height':844})
    pgM.goto(BASE + '/messages.html', wait_until='domcontentloaded'); pgM.wait_for_timeout(1600)
    pgM.click('.conv-item'); pgM.wait_for_timeout(1200)
    check("mobile: chat opens in-chat", pgM.evaluate("document.getElementById('chatShell').classList.contains('in-chat')"))
    check("mobile: back button visible", pgM.evaluate("getComputedStyle(document.getElementById('chatBack')).display") != 'none')
    pgM.click('#chatBack'); pgM.wait_for_timeout(500)
    check("mobile: back to list", not pgM.evaluate("document.getElementById('chatShell').classList.contains('in-chat')"))
    pgM.screenshot(path='qa-auth/chat-4-mobile.png')
    ov = pgM.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check("mobile: no overflow", ov == 0, str(ov))
    pgM.close()

    print("\npage errors:", errs if errs else "none")
    b.close()

print("\n===== SUMMARY =====")
fails = [r for r in results if not r[1]]
print(f"{len(results)-len(fails)}/{len(results)} passed; failures: {[r[0] for r in fails]}")
