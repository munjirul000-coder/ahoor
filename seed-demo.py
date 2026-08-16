#!/usr/bin/env python3
"""Ahoor live demo seeder: 5 accounts + 20 posts + views/quotes/messages (public APIs only)."""
import json, urllib.request, urllib.parse, http.cookiejar, sys, time

BASE = "https://ahoor.onrender.com"
PW = "Ahoor@2026"

class Session:
    def __init__(self):
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
    def call(self, path, data=None):
        if data is not None:
            req = urllib.request.Request(BASE + path, data=json.dumps(data).encode(),
                                         headers={'Content-Type': 'application/json'}, method='POST')
        else:
            req = urllib.request.Request(BASE + path)
        try:
            with self.opener.open(req, timeout=40) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            try: return json.loads(e.read().decode() or '{}')
            except Exception: return {'error': 'http' + str(e.code)}
    def post(self, p, d): return self.call(p, d)
    def get(self, p): return self.call(p)

def signup(name, email, phone, utype, profile):
    s = Session()
    r = s.post('/api/register', {"name": name, "email": email, "phone": phone, "password": PW})
    assert 'userId' in r, "register failed: %s" % r
    s.post('/api/type', {"type": utype})
    c = s.post('/api/send-code', {"purpose": "signup"})
    code = c.get('devCode')
    assert code, "no devCode: %s" % c
    v = s.post('/api/verify-code', {"purpose": "signup", "code": code})
    assert v.get('ok') is not False, "verify failed: %s" % v
    if profile:
        pr = s.post('/api/profile', profile)
        assert 'user' in pr or pr.get('ok') is not False, "profile failed: %s" % pr
    return s

ACCOUNTS = [
    dict(name="Raj Textile Mills", email="rajtextile@ahoor-demo.com", phone="01711110101", utype="supplier",
         profile=dict(businessName="Raj Textile Mills", businessType="manufacturer", division="dhaka", district="Gazipur",
                      category="Yarn & Fabric", address="BSCIC Industrial Area, Gazipur",
                      description="Yarn and fabric manufacturer with 12 years of export experience.",
                      productsServices="Cotton yarn, polyester yarn, grey fabric, denim, dyed fabric",
                      typicalQty="5000-50000 kg", moq="1000 kg", yearsInBusiness="12", employees="150")),
    dict(name="Chattogram Agro Exports", email="agroexport@ahoor-demo.com", phone="01811110102", utype="supplier",
         profile=dict(businessName="Chattogram Agro Exports", businessType="exporter", division="chattogram", district="Chattogram",
                      category="Agro & Food", address="Agrabad C/A, Chattogram",
                      description="Exporter of fresh and processed agro products from Bangladesh.",
                      productsServices="Onion, garlic, mango, rice, potato, chili",
                      typicalQty="1-50 MT", moq="500 kg", yearsInBusiness="8", employees="40")),
    dict(name="Crafts & Jute BD", email="jutebd@ahoor-demo.com", phone="01911110103", utype="supplier",
         profile=dict(businessName="Crafts & Jute BD", businessType="manufacturer", division="dhaka", district="Dhaka",
                      category="Jute & Handicrafts", address="Mirpur 10, Dhaka",
                      description="Eco-friendly jute products and handicrafts for local and export markets.",
                      productsServices="Jute yarn, hessian fabric, jute bags, home decor",
                      typicalQty="1000-20000 pcs", moq="500 pcs", yearsInBusiness="6", employees="25")),
    dict(name="Fashion Wear Ltd", email="fashionwear@ahoor-demo.com", phone="01611110104", utype="buyer",
         profile=dict(businessName="Fashion Wear Ltd", businessType="buyer", division="dhaka", district="Savar",
                      category="RMG & Textiles", address="Jamgora, Savar, Dhaka",
                      description="Apparel manufacturer sourcing fabrics, yarn, trims and packaging.",
                      buyProducts="Fabric, yarn, buttons, zippers, labels, packaging boxes",
                      typicalQty="10000-100000 m", moq="", yearsInBusiness="10", employees="800")),
    dict(name="Leather & Shoes BD", email="leatherbd@ahoor-demo.com", phone="01511110105", utype="both",
         profile=dict(businessName="Leather & Shoes BD", businessType="manufacturer", division="dhaka", district="Savar",
                      category="Leather & Footwear", address="Hemayetpur, Savar, Dhaka",
                      description="Finished leather supplier and footwear manufacturer.",
                      productsServices="Finished cow leather, leather belts, footwear",
                      buyProducts="Leather chemicals, shoe soles, adhesives",
                      typicalQty="1000-20000 sqft", moq="500 sqft", yearsInBusiness="9", employees="120")),
]

POSTS = [
    ("rajtextile@ahoor-demo.com", dict(type="supplier", title="100% Cotton Yarn Ne 20/1 for Export", category="Yarn",
     qty="10000", unit="kg", price="310", moq="1000 kg", location="Gazipur",
     desc="Combed 100% cotton yarn, Ne 20/1, consistent quality, export packing. Delivery within 10 days.")),
    ("rajtextile@ahoor-demo.com", dict(type="supplier", title="Polyester Yarn 150D/48F Bright", category="Yarn",
     qty="5000", unit="kg", price="180", moq="500 kg", location="Gazipur",
     desc="Polyester filament yarn 150D/48F, bright, for weaving and knitting industries.")),
    ("rajtextile@ahoor-demo.com", dict(type="supplier", title="Grey Cotton Fabric 60 Inch Width", category="Fabric",
     qty="30000", unit="meter", price="95", moq="5000 meter", location="Gazipur",
     desc="Grey cotton fabric, 60 inch width, 40s x 40s construction, suitable for dyeing and printing.")),
    ("rajtextile@ahoor-demo.com", dict(type="supplier", title="Denim Fabric 10 oz for Garments", category="Fabric",
     qty="20000", unit="meter", price="215", moq="3000 meter", location="Gazipur",
     desc="10 oz indigo denim, stretch available, for jeans and jackets production.")),
    ("rajtextile@ahoor-demo.com", dict(type="supplier", title="Recycled Cotton Yarn Ne 10/1", category="Yarn",
     qty="8000", unit="kg", price="150", moq="1000 kg", location="Gazipur",
     desc="Recycled cotton yarn for towels, denim and home textile applications.")),
    ("agroexport@ahoor-demo.com", dict(type="supplier", title="Fresh Red Onion Export Quality", category="Agro",
     qty="20", unit="MT", price="45000", moq="1 MT", location="Chattogram",
     desc="Fresh red onion, hand-sorted, export quality, available year round for export.")),
    ("agroexport@ahoor-demo.com", dict(type="supplier", title="Miniket Rice Premium Grade Export", category="Agro",
     qty="50", unit="MT", price="62000", moq="2 MT", location="Chattogram",
     desc="Premium Miniket rice, machine cleaned, export packing available in 25/50 kg bags.")),
    ("agroexport@ahoor-demo.com", dict(type="supplier", title="Fresh Garlic (Deshi) Wholesale", category="Agro",
     qty="10", unit="MT", price="85000", moq="500 kg", location="Chattogram",
     desc="Deshi garlic, sun dried, cleaned, wholesale price for bulk buyers.")),
    ("agroexport@ahoor-demo.com", dict(type="supplier", title="Himsagar Mango Export Season 2026", category="Agro",
     qty="15", unit="MT", price="90000", moq="1 MT", location="Rajshahi",
     desc="Premium Himsagar mango, export grade, harvested and packed in Rajshahi.")),
    ("jutebd@ahoor-demo.com", dict(type="supplier", title="Jute Yarn 2 Ply for Hessian & Carpet", category="Jute",
     qty="12000", unit="kg", price="145", moq="500 kg", location="Dhaka",
     desc="Natural jute yarn, 2 ply, for hessian cloth, carpet backing and decorative items.")),
    ("jutebd@ahoor-demo.com", dict(type="supplier", title="Jute Shopping Bags Custom Print", category="Handicraft",
     qty="20000", unit="pcs", price="55", moq="1000 pcs", location="Dhaka",
     desc="Eco-friendly jute shopping bags with custom logo print, sizes as per buyer requirement.")),
    ("jutebd@ahoor-demo.com", dict(type="supplier", title="Hessian Jute Fabric 40 inch", category="Jute",
     qty="25000", unit="meter", price="65", moq="5000 meter", location="Dhaka",
     desc="Hessian jute fabric, 40 inch width, for packaging, agriculture and decoration.")),
    ("jutebd@ahoor-demo.com", dict(type="supplier", title="Terracotta Handicraft Home Decor Set", category="Handicraft",
     qty="5000", unit="pcs", price="120", moq="500 pcs", location="Dhaka",
     desc="Handmade terracotta home decor items: vases, planters and wall art from local artisans.")),
    ("fashionwear@ahoor-demo.com", dict(type="buyer", title="Buying: Cotton Fabric 50,000 Meter Monthly", category="Fabric",
     qty="50000", unit="meter", budget="100", location="Savar",
     desc="Looking for regular supply of 100% cotton single jersey fabric for T-shirt production. Need stable quality.")),
    ("fashionwear@ahoor-demo.com", dict(type="buyer", title="Buying: Yarn Ne 30/1 Combed", category="Yarn",
     qty="20000", unit="kg", budget="340", location="Savar",
     desc="Monthly requirement of combed cotton yarn Ne 30/1 for knitwear production.")),
    ("fashionwear@ahoor-demo.com", dict(type="buyer", title="Buying: Corrugated Carton Boxes", category="Packaging",
     qty="100000", unit="pcs", budget="22", location="Savar",
     desc="Corrugated carton boxes for garment export packing, sizes 50x40x30 cm approx.")),
    ("fashionwear@ahoor-demo.com", dict(type="buyer", title="Buying: Woven Labels & Hang Tags", category="Trims",
     qty="500000", unit="pcs", budget="1.5", location="Savar",
     desc="Woven labels and printed hang tags with logo for export garments, monthly order.")),
    ("leatherbd@ahoor-demo.com", dict(type="supplier", title="Finished Cow Leather Export Grade", category="Leather",
     qty="10000", unit="sqft", price="85", moq="1000 sqft", location="Savar",
     desc="Finished cow leather (crust and finished), export grade, consistent shade and texture.")),
    ("leatherbd@ahoor-demo.com", dict(type="supplier", title="Genuine Leather Belts Wholesale", category="Leather",
     qty="10000", unit="pcs", price="180", moq="500 pcs", location="Savar",
     desc="Genuine leather belts, men's and women's styles, multiple colors, bulk production capacity.")),
    ("leatherbd@ahoor-demo.com", dict(type="buyer", title="Buying: Leather Chemical (Syntan & Dye)", category="Chemical",
     qty="5000", unit="kg", budget="450", location="Savar",
     desc="Requirement of leather chemicals - syntan, fatliquor and dye for tannery production.")),
]

def main():
    sess, uid = {}, {}
    print("== Step 1: 5 accounts ==")
    for a in ACCOUNTS:
        s = signup(a["name"], a["email"], a["phone"], a["utype"], a["profile"])
        sess[a["email"]] = s
        print("  OK", a["email"])
    print("== Step 2: 20 posts ==")
    post_ids = {}
    for em, p in POSTS:
        r = sess[em].post('/api/posts', p)
        if 'post' not in r:
            print("  FAIL", em, p["title"], r); sys.exit(1)
        post_ids[r["post"]["id"]] = em
    print("  OK 20 posts")
    print("== Step 3: profile views ==")
    others = [e for e in uid] or [e for e in sess]
    for em in others:
        for oe in others:
            if oe != em:
                sess[em].get('/api/business?id=' + (sess[oe] and ''))
    # fetch user ids via session for view tracking
    ids = {}
    for em in sess:
        r = sess[em].get('/api/session')
        ids[em] = r.get('user', {}).get('id')
    for em in others:
        for oe in others:
            if oe != em and ids.get(oe):
                sess[em].get('/api/business?id=' + ids[oe])
    print("  OK cross-visits")
    print("== Step 4: quotes & chat ==")
    def find(part):
        for pid, em in post_ids.items():
            if part.lower() in pid:
                return pid
        # need titles; re-fetch
        for em in list(sess)[:1]:
            for post in sess[em].get('/api/posts').get('posts', []):
                if part.lower() in post['title'].lower():
                    return post['id']
        raise SystemExit("post not found: " + part)
    q1 = sess["fashionwear@ahoor-demo.com"].post('/api/quotes', {"postId": find("Cotton Yarn Ne 20"), "reqQty": "3000", "budget": "300", "preferredDelivery": "2 weeks", "message": "We need 3000 kg per month. Please confirm delivery time."})
    q2 = sess["rajtextile@ahoor-demo.com"].post('/api/quotes', {"postId": find("Cotton Fabric 50,000"), "pricePerUnit": "98", "availableQty": "50000", "moq": "5000", "deliveryTime": "15 days", "validUntil": "2026-09-15", "message": "We can supply 50,000 meter/month at BDT 98 per meter."})
    print("  quotes:", "OK" if 'quote' in q1 and 'quote' in q2 else (q1, q2))
    cv = sess["fashionwear@ahoor-demo.com"].post('/api/conversations', {"withUserId": ids.get("rajtextile@ahoor-demo.com")})
    if 'conversation' in cv:
        cid = cv["conversation"]["id"]
        sess["fashionwear@ahoor-demo.com"].post('/api/conversations/' + cid + '/messages', {"text": "Hello! Interested in your denim fabric. Please share your price list."})
        sess["rajtextile@ahoor-demo.com"].post('/api/conversations/' + cid + '/messages', {"text": "Dear Fashion Wear, thanks for reaching out. Price list coming today."})
        print("  chat OK")
    print("\nDONE")
    print("Accounts (password: %s):" % PW)
    for a in ACCOUNTS:
        print("  %-24s %s (%s)" % (a["name"], a["email"], a["utype"]))

if __name__ == '__main__':
    main()
