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

PAGES = ['login', 'signup', 'forgot', 'dashboard', 'profile-setup', 'marketplace', 'post', 'business', 'messages']
for name in PAGES:
    t = open(os.path.join(TPL, name + '.html'), encoding='utf-8').read()
    t = t.replace('__INTER__', INTER).replace('__NSB__', NSB)
    t = t.replace('__CSS__', CSS)
    t = t.replace('__JS__', JS)
    assert '__CSS__' not in t and '__JS__' not in t and '__INTER__' not in t, name + ' placeholders left'
    open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8').write(t)
    print('built', name + '.html', len(t), 'bytes')
print('AUTH BUILD OK')
