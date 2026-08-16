#!/usr/bin/env python3
# Builds the 5 self-contained auth pages from templates + shared css/js + fonts
import base64, re, os

TPL = 'auth/templates'
OUT = '.'  # ahoor/

def b64(p):
    return base64.b64encode(open(p, 'rb').read()).decode()

INTER = b64('assets/inter-latin.woff2')
NSB = b64('assets/noto-bengali-full.woff2')
CSS = open('auth/auth-shared.css', encoding='utf-8').read()
JS = open('auth/auth-shared.js', encoding='utf-8').read()

PAGES = ['login', 'signup', 'forgot', 'dashboard', 'profile-setup', 'marketplace', 'post', 'business', 'messages', 'notifications', 'admin', 'matches', 'verify', 'analytics',
         'about', 'contact', 'privacy', 'terms']
for name in PAGES:
    t = open(os.path.join(TPL, name + '.html'), encoding='utf-8').read()
    t = t.replace('__INTER__', INTER).replace('__NSB__', NSB)
    t = t.replace('__CSS__', CSS)
    t = t.replace('__JS__', JS)
    assert '__CSS__' not in t and '__JS__' not in t and '__INTER__' not in t, name + ' placeholders left'
    open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8').write(t)
    print('built', name + '.html', len(t), 'bytes')

# suppliers.html + opportunities.html share one listing template (parametrized by __PAGE__)
LISTING = {
  'suppliers': {
    'meta': 'meta.suppliers', 'title': 'sp.title', 'title_fb': 'Suppliers & Manufacturers',
    'sub': 'sp.sub', 'sub_fb': 'Browse supplier offers posted on Ahoor.',
    'empty': 'sp.empty', 'empty_fb': 'No supplier offers yet — be the first to post one.',
    'market': 'sp.market', 'sup_w': '700', 'sup_c': '#2F6BFF', 'sup_bg': '#EBF1FF',
    'opp_w': '600', 'opp_c': '#57627A', 'opp_bg': 'transparent'
  },
  'opportunities': {
    'meta': 'meta.opps', 'title': 'op.title', 'title_fb': 'All Business Opportunities',
    'sub': 'op.sub', 'sub_fb': 'Buyer requirements and supplier offers posted on Ahoor.',
    'empty': 'op.empty', 'empty_fb': 'No opportunities yet — be the first to post one.',
    'market': 'op.market', 'sup_w': '600', 'sup_c': '#57627A', 'sup_bg': 'transparent',
    'opp_w': '700', 'opp_c': '#2F6BFF', 'opp_bg': '#EBF1FF'
  },
}
for name, cfg in LISTING.items():
    t = open(os.path.join(TPL, 'listing.html'), encoding='utf-8').read()
    t = t.replace('__INTER__', INTER).replace('__NSB__', NSB)
    t = t.replace('__CSS__', CSS).replace('__JS__', JS)
    t = t.replace('__PAGE__', name).replace('__META__', cfg['meta'])
    t = t.replace('__TITLE_KEY__', cfg['title']).replace('__TITLE_FB__', cfg['title_fb'])
    t = t.replace('__SUB_KEY__', cfg['sub']).replace('__SUB_FB__', cfg['sub_fb'])
    t = t.replace('__EMPTY_KEY__', cfg['empty']).replace('__EMPTY_FB__', cfg['empty_fb'])
    t = t.replace('__MARKET_KEY__', cfg['market'])
    t = t.replace('__SUP_W__', cfg['sup_w']).replace('__SUP_C__', cfg['sup_c']).replace('__SUP_BG__', cfg['sup_bg'])
    t = t.replace('__OPP_W__', cfg['opp_w']).replace('__OPP_C__', cfg['opp_c']).replace('__OPP_BG__', cfg['opp_bg'])
    assert '__PAGE__' not in t and '__CSS__' not in t and '__JS__' not in t, name + ' placeholders left'
    open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8').write(t)
    print('built', name + '.html', len(t), 'bytes')
print('AUTH BUILD OK')
