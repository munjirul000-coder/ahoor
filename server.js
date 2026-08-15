#!/usr/bin/env node
/* ============================================================
   Ahoor — Authentication Server (zero-dependency Node.js)
   Static hosting + real auth API:
   - scrypt password hashing (never plain text)
   - httpOnly, SameSite=Lax session cookies (hashed server-side)
   - 6-digit verification codes (hashed, expiring, attempt-limited)
   - rate limiting on login / code sending / code attempts
   - server-side protection of /dashboard and /profile-setup
   Data persisted to data/db.json (atomic writes).
   ============================================================ */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = __dirname;
const DATA_DIR = path.join(ROOT, 'data');
const DB_FILE = path.join(DATA_DIR, 'db.json');
// Dev codes are shown until a real SMS/email gateway is configured.
// Set AHOOR_DEV_CODES=false (or add SMTP/SMS creds) to hide them.
const DEV = String(process.env.AHOOR_DEV_CODES || 'true').toLowerCase() !== 'false';
const PORT = process.env.PORT || 8080;

/* ---------------- store (JSON file, atomic writes) ---------------- */
let db = null;
function load() {
  if (db) return db;
  try {
    db = JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
  } catch (e) {
    db = { users: [], sessions: {}, codes: {}, fails: {} };
  }
  return db;
}
function save() {
  fs.mkdirSync(DATA_DIR, { recursive: true });
  const tmp = DB_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(db));
  fs.renameSync(tmp, DB_FILE);
}
load();

/* ---------------- helpers ---------------- */
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PHONE_RE = /^(?:\+?880|0)1[3-9]\d{8}$/;
const json = (res, status, data) => {
  const body = JSON.stringify(data);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Referrer-Policy': 'same-origin'
  });
  res.end(body);
};
const uid = () => crypto.randomUUID();
function hashPassword(pw) {
  const salt = crypto.randomBytes(16);
  const hash = crypto.scryptSync(pw, salt, 64);
  return salt.toString('hex') + ':' + hash.toString('hex');
}
function verifyPassword(pw, stored) {
  try {
    const [saltHex, hashHex] = stored.split(':');
    const hash = crypto.scryptSync(pw, Buffer.from(saltHex, 'hex'), 64);
    return crypto.timingSafeEqual(hash, Buffer.from(hashHex, 'hex'));
  } catch (e) { return false; }
}
const sha256 = s => crypto.createHash('sha256').update(s).digest('hex');
const token = () => crypto.randomBytes(32).toString('hex');
const normId = s => String(s || '').trim().toLowerCase();
const findUser = id => {
  id = normId(id);
  return db.users.find(u => u.email === id || u.phone.replace(/\D/g, '').slice(-10) === id.replace(/\D/g, '').slice(-10));
};

/* ---------------- rate limiting ---------------- */
function checkLimit(key, kind, max, windowMs) {
  const now = Date.now();
  const e = db.fails[key];
  if (e && e.lockedUntil && e.lockedUntil > now) {
    return { ok: false, retryIn: Math.ceil((e.lockedUntil - now) / 60000) };
  }
  if (!e || now - e.firstAt > windowMs) {
    db.fails[key] = { count: 1, firstAt: now, lockedUntil: 0 };
    return { ok: true };
  }
  e.count++;
  if (e.count >= max) {
    e.lockedUntil = now + windowMs;
    save();
    return { ok: false, retryIn: Math.ceil(windowMs / 60000) };
  }
  return { ok: true };
}
function lockCheck(key) {
  const e = db.fails[key];
  const now = Date.now();
  if (e && e.lockedUntil > now) return { ok: false, retryIn: Math.ceil((e.lockedUntil - now) / 60000) };
  return { ok: true };
}
function recordFail(key) {
  const now = Date.now();
  const e = db.fails[key];
  if (!e || now - e.firstAt > 15 * 60000) db.fails[key] = { count: 1, firstAt: now, lockedUntil: 0 };
  else e.count++;
  if (db.fails[key].count >= 5) db.fails[key].lockedUntil = now + 15 * 60000;
  save();
}

/* ---------------- sessions ---------------- */
function createSession(userId, remember) {
  const t = token();
  const expires = Date.now() + (remember ? 30 : 7) * 24 * 3600 * 1000;
  db.sessions[sha256(t)] = { userId, expires, createdAt: Date.now() };
  save();
  return { t, expires };
}
function getSession(req) {
  const raw = (req.headers.cookie || '').split(';').map(s => s.trim());
  const c = raw.find(s => s.startsWith('ahoor_sid='));
  if (!c) return null;
  const s = db.sessions[sha256(c.slice(10))];
  if (!s || s.expires < Date.now()) return null;
  return s;
}
function destroySession(req) {
  const raw = (req.headers.cookie || '').split(';').map(s => s.trim());
  const c = raw.find(s => s.startsWith('ahoor_sid='));
  if (c) delete db.sessions[sha256(c.slice(10))];
  save();
}

/* ---------------- verification codes ---------------- */
function sendCode(target /* 'signup:email' | 'reset:...' */, channel) {
  const now = Date.now();
  const key = 'code:' + target;
  const old = db.codes[key];
  if (old && old.resendAt > now) {
    return { ok: false, retryIn: Math.ceil((old.resendAt - now) / 1000), code: null };
  }
  const code = String(crypto.randomInt(0, 1000000)).padStart(6, '0');
  db.codes[key] = {
    hash: sha256(code),
    expires: now + 10 * 60000,        // valid 10 minutes
    resendAt: now + 60 * 1000,        // resend cooldown 60s
    attempts: 0,
    channel
  };
  save();
  console.log(`[Ahoor dev] ${channel} code for ${target}: ${code}`);
  return { ok: true, code: DEV ? code : null, expiresIn: 600 };
}
function checkCode(target, code) {
  const e = db.codes['code:' + target];
  if (!e) return { status: 400, err: 'no_code' };
  if (e.attempts >= 5) { delete db.codes['code:' + target]; save(); return { status: 429, err: 'too_many' }; }
  if (e.expires < Date.now()) { delete db.codes['code:' + target]; save(); return { status: 410, err: 'expired' }; }
  const ok = crypto.timingSafeEqual(Buffer.from(e.hash, 'hex'), Buffer.from(sha256(String(code).trim()), 'hex'));
  if (!ok) {
    e.attempts++;
    save();
    return { status: 400, err: 'invalid' };
  }
  delete db.codes['code:' + target];
  save();
  return { status: 200, err: null };
}

/* ---------------- body parsing ---------------- */
function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', c => {
      data += c;
      if (data.length > 100000) { reject(new Error('too large')); req.destroy(); }
    });
    req.on('end', () => {
      try {
        const ct = req.headers['content-type'] || '';
        resolve(ct.includes('json') ? JSON.parse(data || '{}') : new URLSearchParams(data));
      } catch (e) { reject(new Error('bad json')); }
    });
    req.on('error', reject);
  });
}

/* ---------------- validation ---------------- */
function validatePassword(pw) {
  if (typeof pw !== 'string' || pw.length < 8) return 'weak';
  if (!/[A-Za-z]/.test(pw) || !/\d/.test(pw)) return 'weak';
  return null;
}
function validateName(n) {
  n = String(n || '').trim();
  return n.length >= 2 && n.length <= 80 ? null : 'name';
}
function validateEmail(e) {
  return EMAIL_RE.test(String(e || '').trim()) ? null : 'email';
}
function validatePhone(p) {
  const digits = String(p || '').replace(/[^\d+]/g, '');
  return PHONE_RE.test(digits) ? null : 'phone';
}

/* ---------------- routes ---------------- */
const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.json': 'application/json',
  '.woff2': 'font/woff2', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
};

async function handle(req, res) {
  const url = new URL(req.url, 'http://x');
  let p = decodeURIComponent(url.pathname);
  if (req.method === 'GET' && p === '/') p = '/index.html';

  /* --- protected pages (server-side guard) --- */
  if (req.method === 'GET') {
    const target = p === '/dashboard' ? '/dashboard.html' : p === '/profile-setup' ? '/profile-setup.html' : p;
    if ((target === '/dashboard.html' || target === '/profile-setup.html') && !getSession(req)) {
      res.writeHead(302, { Location: '/login?next=' + encodeURIComponent(target) });
      return res.end();
    }
  }

  /* --- API --- */
  if (p.startsWith('/api/')) {
    if (req.method !== 'POST') return json(res, 405, { error: 'method' });
    let body;
    try { body = await readBody(req); }
    catch (e) { return json(res, 400, { error: 'bad_request' }); }
    const ip = req.socket.remoteAddress || 'x';
    const rlKey = k => k + '|' + ip;

    /* register (step 1 of signup) */
    if (p === '/api/register') {
      const { name, email, phone, password } = body;
      const rl = checkLimit(rlKey('register'), 'register', 20, 60 * 60000);
      if (!rl.ok) return json(res, 429, { error: 'locked', retryIn: rl.retryIn });
      const eName = validateName(name), eMail = validateEmail(email), ePh = validatePhone(phone), ePw = validatePassword(password);
      if (eName) return json(res, 400, { error: eName });
      if (eMail) return json(res, 400, { error: 'email' });
      if (ePh) return json(res, 400, { error: 'phone' });
      if (ePw) return json(res, 400, { error: 'weak' });
      const em = normId(email);
      if (db.users.some(u => u.email === em)) return json(res, 409, { error: 'email_exists' });
      if (db.users.some(u => u.phone === String(phone).trim())) return json(res, 409, { error: 'phone_exists' });
      const user = {
        id: uid(), name: String(name).trim(), email: em, phone: String(phone).trim(),
        passHash: hashPassword(password), type: null, status: 'pending',
        createdAt: new Date().toISOString()
      };
      db.users.push(user);
      save();
      const s = createSession(user.id, true);
      setCookie(res, s);
      return json(res, 201, { userId: user.id });
    }

    /* login */
    if (p === '/api/login') {
      const { identifier, password } = body;
      if (!identifier || !password) return json(res, 400, { error: 'missing' });
      const rl = lockCheck(rlKey('login:' + normId(identifier)));
      if (!rl.ok) return json(res, 429, { error: 'locked', retryIn: rl.retryIn });
      const user = findUser(identifier);
      if (!user || !verifyPassword(password, user.passHash)) {
        recordFail(rlKey('login:' + normId(identifier)));
        return json(res, 401, { error: 'invalid' });
      }
      if (user.status === 'pending') return json(res, 403, { error: 'unverified' });
      const s = createSession(user.id, body.remember !== false);
      setCookie(res, s);
      return json(res, 200, { user: publicUser(user) });
    }

    /* logout */
    if (p === '/api/logout') {
      destroySession(req);
      res.writeHead(302, { Location: '/login.html' });
      return res.end();
    }

    /* current session */
    if (p === '/api/session') {
      const s = getSession(req);
      const user = s && db.users.find(u => u.id === s.userId);
      return json(res, 200, { user: user ? publicUser(user) : null });
    }

    /* account type (step 2) */
    if (p === '/api/type') {
      const s = getSession(req);
      if (!s) return json(res, 401, { error: 'no_session' });
      const { type } = body;
      if (!['buyer', 'supplier', 'both'].includes(type)) return json(res, 400, { error: 'type' });
      const user = db.users.find(u => u.id === s.userId);
      user.type = type;
      save();
      return json(res, 200, { user: publicUser(user) });
    }

    /* send verification code */
    if (p === '/api/send-code') {
      const { purpose, identifier } = body;
      const now = Date.now();
      if (purpose === 'signup') {
        const s = getSession(req);
        let user = s && db.users.find(u => u.id === s.userId);
        const byId = identifier ? findUser(identifier) : null;
        if (!user && byId && byId.status === 'pending') user = byId; // re-send from login screen
        if (!user) return json(res, 401, { error: 'no_session' });
        const rl = checkLimit(rlKey('send:' + user.id), 'send', 5, 15 * 60000);
        if (!rl.ok) return json(res, 429, { error: 'locked', retryIn: rl.retryIn });
        const r = sendCode('signup:' + user.id, 'email');
        if (!r.ok) return json(res, 429, { error: 'cooldown', retryIn: r.retryIn });
        return json(res, 200, { devCode: r.code, expiresIn: r.expiresIn });
      }
      if (purpose === 'reset') {
        const user = findUser(identifier || '');
        if (!user) return json(res, 404, { error: 'not_found' });
        const rl = checkLimit(rlKey('send:' + user.id), 'send', 5, 15 * 60000);
        if (!rl.ok) return json(res, 429, { error: 'locked', retryIn: rl.retryIn });
        const r = sendCode('reset:' + user.id, 'email');
        if (!r.ok) return json(res, 429, { error: 'cooldown', retryIn: r.retryIn });
        return json(res, 200, { devCode: r.code, expiresIn: r.expiresIn });
      }
      return json(res, 400, { error: 'purpose' });
    }

    /* verify code (signup activation or reset step) */
    if (p === '/api/verify-code') {
      const { purpose, code, identifier } = body;
      if (purpose === 'signup') {
        const s = getSession(req);
        let user = s && db.users.find(u => u.id === s.userId);
        const byId = identifier ? findUser(identifier) : null;
        if (!user && byId && byId.status === 'pending') user = byId;
        if (!user) return json(res, 401, { error: 'no_session' });
        const r = checkCode('signup:' + user.id, code);
        if (r.status !== 200) return json(res, r.status, { error: r.err });
        user.status = 'active';
        save();
        return json(res, 200, { user: publicUser(user) });
      }
      if (purpose === 'reset') {
        const user = findUser(identifier || '');
        if (!user) return json(res, 404, { error: 'not_found' });
        const r = checkCode('reset:' + user.id, code);
        if (r.status !== 200) return json(res, r.status, { error: r.err });
        // mark reset as verified for the next step (code itself is now consumed)
        db.codes['resetok:' + user.id] = { expires: Date.now() + 10 * 60000 };
        save();
        return json(res, 200, { ok: true });
      }
      return json(res, 400, { error: 'purpose' });
    }

    /* reset password */
    if (p === '/api/reset-password') {
      const { identifier, password } = body;
      const user = findUser(identifier || '');
      if (!user) return json(res, 404, { error: 'not_found' });
      const okFlag = db.codes['resetok:' + user.id];
      if (!okFlag || okFlag.expires < Date.now()) return json(res, 410, { error: 'expired' });
      delete db.codes['resetok:' + user.id];
      const ePw = validatePassword(password);
      if (ePw) return json(res, 400, { error: 'weak' });
      user.passHash = hashPassword(password);
      // invalidate all existing sessions
      for (const k of Object.keys(db.sessions)) {
        if (db.sessions[k].userId === user.id) delete db.sessions[k];
      }
      save();
      return json(res, 200, { ok: true });
    }

    return json(res, 404, { error: 'route' });
  }

  /* --- static files --- */
  const file = path.join(ROOT, p);
  if (!file.startsWith(ROOT)) return json(res, 403, { error: 'forbidden' });
  fs.readFile(file, (err, data) => {
    if (err) {
      if (req.method === 'GET' && !path.extname(p)) {
        return fs.readFile(path.join(ROOT, p + '.html'), (e2, d2) => {
          if (e2) return send404(res);
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          res.end(d2);
        });
      }
      return send404(res);
    }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream' });
    res.end(data);
  });
}

function setCookie(res, s) {
  const maxAge = Math.round((s.expires - Date.now()) / 1000);
  res.setHeader('Set-Cookie', `ahoor_sid=${s.t}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${maxAge}`);
}
function publicUser(u) {
  return { id: u.id, name: u.name, email: u.email, phone: u.phone, type: u.type, createdAt: u.createdAt };
}

/* periodic session/code cleanup */
setInterval(() => {
  const now = Date.now();
  for (const k of Object.keys(db.sessions)) if (db.sessions[k].expires < now) delete db.sessions[k];
  for (const k of Object.keys(db.codes)) if (db.codes[k].expires < now) delete db.codes[k];
  save();
}, 10 * 60000).unref();

function send404(res) {
  fs.readFile(path.join(ROOT, '404.html'), (err, d) => {
    if (err) { res.writeHead(404, { 'Content-Type': 'text/plain' }); return res.end('Not found'); }
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(d);
  });
}

const server = http.createServer(handle);
server.listen(PORT, '0.0.0.0', () => {
  console.log(`Ahoor server running on http://0.0.0.0:${PORT}`);
  console.log(`Dev mode: ${DEV ? 'ON (verification codes returned to client for testing)' : 'OFF'}`);
});
