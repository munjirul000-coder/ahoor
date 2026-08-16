#!/usr/bin/env python3
"""Regenerate about/contact/privacy/terms templates with correct markup."""
import os

NAV = """<header class="auth-nav">
  <div class="container">
    <a class="brand" href="/index.html" aria-label="Ahoor — home">
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true">
        <rect width="32" height="32" rx="9" fill="url(#lg1)"/>
        <path d="M16 8.5 9.6 23.5h12.8z" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/>
        <circle cx="16" cy="8.5" r="2.7" fill="#fff"/><circle cx="9.6" cy="23.5" r="2.7" fill="#fff"/><circle cx="22.4" cy="23.5" r="2.7" fill="#FF8A4C"/>
        <defs><linearGradient id="lg1" x1="0" y1="0" x2="32" y2="32"><stop stop-color="#3B77FF"/><stop offset="1" stop-color="#1E4FD8"/></linearGradient></defs>
      </svg>
      <span class="brand-name">Ahoor<em>.</em></span>
    </a>
    <div class="auth-nav-right">
      <a class="back-home" href="/index.html">
        <svg class="arr" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>
        <span data-i18n="back.home">← Back to Home</span>
      </a>
      <div class="lang-switch" role="group" aria-label="Language">
        <button type="button" class="lang-btn on" data-lang="bn" aria-pressed="true">বাংলা</button>
        <span class="lsep" aria-hidden="true">|</span>
        <button type="button" class="lang-btn" data-lang="en" aria-pressed="false">EN</button>
      </div>
    </div>
  </div>
</header>"""

FOOT = """<footer class="auth-foot">
  <div class="container">
    <p data-i18n="foot.made">Made in Bangladesh</p>
    <p style="margin-top:6px" data-i18n="foot.cr">© 2026 Ahoor. All rights reserved.</p>
    <div class="flinks">
      <a href="/about.html" data-i18n="foot.about">About</a>
      <a href="/contact.html" data-i18n="foot.contact">Contact</a>
      <a href="/privacy.html" data-i18n="foot.privacy">Privacy</a>
      <a href="/terms.html" data-i18n="foot.terms">Terms</a>
    </div>
  </div>
</footer>"""

def page(name, title_en, meta, sections):
    """sections: list of (h2_key, h2_fb, p_key, p_fb)"""
    body = ['    <h1 data-i18n="%s.title">%s</h1>' % (name, title_en),
            '    <p class="lead" data-i18n="%s.lead"></p>' % name,
            '    <p class="updated" data-i18n="%s.updated"></p>' % name]
    for h2k, h2fb, pk, pfb in sections:
        body.append('    <h2 data-i18n="%s">%s</h2>' % (h2k, h2fb))
        body.append('    <p data-i18n="%s">%s</p>' % (pk, pfb))
    html = """<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ahoor — %s</title>
<meta name="theme-color" content="#0A1122">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%%3E%%3Crect width='32' height='32' rx='8' fill='%%230B1430'/'%%3E%%3Cpath d='M16 8.5 9.6 23.5h12.8z' fill='none' stroke='%%23fff' stroke-width='2.4' stroke-linejoin='round'/'%%3E%%3Ccircle cx='16' cy='8.5' r='2.6' fill='%%23fff'/'%%3E%%3Ccircle cx='9.6' cy='23.5' r='2.6' fill='%%23fff'/'%%3E%%3Ccircle cx='22.4' cy='23.5' r='2.6' fill='%%23FF8A4C'/'%%3E%%3C/svg%%3E">
<style>
@font-face{font-family:'Inter';font-style:normal;font-weight:100 900;font-display:swap;src:url(data:font/woff2;base64,__INTER__) format('woff2')}
@font-face{font-family:'Noto Sans Bengali';font-style:normal;font-weight:100 900;font-display:swap;src:url(data:font/woff2;base64,__NSB__) format('woff2')}
:root{--ink:#0A1122;--bg:#F4F6FA;--text:#101828;--font:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif}
html[lang="bn"]{--font:'Noto Sans Bengali','Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif}
html[lang="bn"] body{line-height:1.72}
__CSS__
</style>
</head>
<body data-meta="meta.%s">

%s

<main class="auth-main">
  <div class="auth-card info-card">
%s
  </div>
</main>

%s

<script>
__JS__
</script>
</body>
</html>
""" % (title_en, name, NAV, "\n".join(body), FOOT)
    return html

SECTIONS = {
 "about": [
   ("about.h1","Who we are","about.p1","Ahoor helps Bangladeshi businesses find each other. Buyers post what they need; suppliers and manufacturers post what they offer. Our smart matching surfaces the right opportunities to the right businesses — without endless searching."),
   ("about.h2","What we do","about.p2","Businesses on Ahoor can post requirements and offers, receive and compare quotations, chat directly with potential partners, get matched with relevant opportunities, and track their performance through business analytics."),
   ("about.h3","Who it's for","about.p3","Ahoor is for manufacturers, suppliers, wholesalers, exporters, importers, and bulk buyers across Bangladesh — from textiles and garments to agro products, jute, leather, packaging, and more."),
   ("about.h4","Contact us","about.p4","Questions or feedback? Reach us through the contact page — or sign in and use in-app messaging to talk to any business on the platform."),
 ],
 "contact": [
   ("contact.h1","Email","contact.p1","For general questions and support, email us at munjirul000@gmail.com."),
   ("contact.h2","Report a problem","contact.p2","See something wrong on the platform — a suspicious post, an unfair quotation, or a bug? Sign in and use the Report option on any post or business profile."),
   ("contact.h3","Response time","contact.p3","We typically respond within 1–2 business days."),
 ],
 "privacy": [
   ("privacy.h1","Information we collect","privacy.p1","When you create an account we collect your name, email, phone number, and the business information you choose to add (business name, category, location, products, and similar details). We also store the posts, quotations, messages, and reports you create, plus basic usage events such as profile and post views."),
   ("privacy.h2","How we use it","privacy.p2","Your information is used to run the platform: connecting you with relevant businesses, showing your posts and profile to other members, sending notifications and quotations, matching opportunities, and showing you your own analytics. We never invent or publish fake business data."),
   ("privacy.h3","What we don't share","privacy.p3","We do not sell your personal data. Your phone number and email are only visible to other members according to your own visibility settings. We never expose passwords, session tokens, or private analytics of other businesses."),
   ("privacy.h4","Security","privacy.p4","Passwords are stored as salted hashes, sessions use secure random tokens, and all account pages require login. As with any online service, please use a strong, unique password."),
   ("privacy.h5","Your choices","privacy.p5","You can edit or remove your business information from your profile anytime. To close your account or ask questions about your data, contact us from the contact page."),
 ],
 "terms": [
   ("terms.h1","Using the platform","terms.p1","Ahoor connects buyers and suppliers in Bangladesh. We provide the venue; the actual business dealings, negotiations, and payments happen between the parties themselves. Always verify the credibility of your business partners before entering into any agreement."),
   ("terms.h2","Accounts","terms.p2","You must provide accurate information when creating an account. You are responsible for keeping your login credentials safe and for everything done from your account."),
   ("terms.h3","Acceptable use","terms.p3","Do not post false or misleading business information, send spam, harass other members, or use the platform for anything unlawful. Posts, quotations, and messages should represent genuine business intent."),
   ("terms.h4","Reporting","terms.p4","If you see a violation, report it through the Report option on the platform. We review reports and may suspend accounts that violate these terms."),
   ("terms.h5","Liability","terms.p5","Ahoor is provided as-is. To the extent permitted by law, we are not liable for losses arising from transactions, communications, or decisions made between businesses on the platform."),
   ("terms.h6","Changes","terms.p6","We may update these terms as the platform grows. The latest version will always be available on this page."),
 ],
}

for name, secs in SECTIONS.items():
    t = page(name, {"about":"About","contact":"Contact","privacy":"Privacy Policy","terms":"Terms of Service"}[name], name, secs)
    open("auth/templates/%s.html" % name, "w", encoding="utf-8").write(t)
    print("regenerated", name + ".html")
print("INFO PAGES OK")
