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

/* optional SMTP mailer (nodemailer) — enables real email delivery of codes */
let nodemailer = null;
try { nodemailer = require('nodemailer'); } catch (e) { /* not installed yet */ }
let _transporter = null;
function getTransporter() {
  if (!nodemailer) return null;
  if (_transporter) return _transporter;
  if (!process.env.SMTP_HOST || !process.env.SMTP_USER || !process.env.SMTP_PASS) return null;
  _transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT || '465', 10),
    secure: String(process.env.SMTP_PORT || '465') === '465',
    auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
    connectionTimeout: 12000,
    socketTimeout: 15000,
    greetingTimeout: 12000
  });
  return _transporter;
}
async function sendCodeEmail(toEmail, code) {
  const tr = getTransporter();
  if (!tr || !toEmail) return false;
  const from = process.env.MAIL_FROM || process.env.SMTP_USER;
  try {
    await tr.sendMail({
      from: 'Ahoor <' + from + '>',
      to: toEmail,
      subject: 'Your Ahoor verification code / আপনার Ahoor যাচাই কোড',
      html: '<div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;border:1px solid #E4E9F2;border-radius:16px;padding:28px;background:#ffffff">'
        + '<div style="display:flex;align-items:center;gap:8px;margin-bottom:18px"><div style="width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#3B77FF,#1E4FD8)"></div>'
        + '<b style="font-size:18px">Ahoor<span style="color:#8FA3CE">.</span></b></div>'
        + '<h2 style="margin:0 0 6px;font-size:20px;color:#101828">Your verification code</h2>'
        + '<p style="margin:0 0 16px;font-size:14px;color:#57627A;line-height:1.6">Use this code to verify your Ahoor account. It expires in 10 minutes.</p>'
        + '<div style="background:#F4F8FF;border:1px dashed #9DBDFF;border-radius:12px;padding:14px;text-align:center;font-size:26px;font-weight:bold;letter-spacing:8px;color:#1E4FD8">' + code + '</div>'
        + '<p style="margin:16px 0 0;font-size:12px;color:#8A95AC;line-height:1.6">If you did not request this, you can safely ignore this email.<br>© 2026 Ahoor — Connecting businesses. Creating opportunities.</p></div>'
    });
    console.log('[Ahoor] code email sent to', toEmail);
    return true;
  } catch (e) {
    console.error('[Ahoor] email send failed:', e.message);
    return false;
  }
}

const ROOT = __dirname;
const DATA_DIR = path.join(ROOT, 'data');
const DB_FILE = path.join(DATA_DIR, 'db.json');
const DEV = process.env.NODE_ENV !== 'production';

/* optional Postgres persistence (Render free Postgres). When DATABASE_URL is
   set, the whole db document is mirrored to a single jsonb row, so data
   survives deploys (Render's free disk is ephemeral). Falls back to the JSON
   file when no DATABASE_URL is configured. */
let pgPool = null;
let pgReady = false;
let pgInitPromise = null;
if (process.env.DATABASE_URL) {
  try {
    const { Pool } = require('pg');
    pgPool = new Pool({ connectionString: process.env.DATABASE_URL, ssl: process.env.DATABASE_URL.includes('sslmode=require') ? { rejectUnauthorized: false } : undefined });
  } catch (e) { console.error('[Ahoor] pg unavailable:', e.message); }
}
function pgInit() {
  if (pgReady) return Promise.resolve();
  if (pgInitPromise) return pgInitPromise;
  pgInitPromise = (async () => {
    try {
      await pgPool.query('CREATE TABLE IF NOT EXISTS ahoor_state (id INT PRIMARY KEY, data JSONB NOT NULL)');
      pgReady = true;
    } catch (e) { console.error('[Ahoor] pg init failed:', e.message); }
  })();
  return pgInitPromise;
}
function pgSaveSync() {
  if (!pgPool || !pgReady) return;
  pgPool.query('INSERT INTO ahoor_state (id, data) VALUES (1, $1) ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data', [JSON.stringify(db)])
    .catch(e => console.error('[Ahoor] pg save failed:', e.message));
}
async function pgLoad() {
  if (!pgPool) return null;
  try {
    await pgInit();
    const r = await pgPool.query('SELECT data FROM ahoor_state WHERE id = 1');
    if (r.rows.length) return r.rows[0].data;
  } catch (e) { console.error('[Ahoor] pg load failed:', e.message); }
  return null;
}
// No SMS/email gateway is connected yet, so verification codes are shown
// on-screen in a labelled "demo mode" box. Set SHOW_CODES=0 once a real
// gateway is connected (Render sets NODE_ENV=production automatically).
const SHOW_CODES = process.env.SHOW_CODES !== '0';
const PORT = process.env.PORT || 8080;

/* ---------------- store (JSON file, atomic writes) ---------------- */
let db = null;
function load() {
  if (db) return db;
  try {
    db = JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
  } catch (e) {
    db = { users: [], sessions: {}, codes: {}, fails: {}, posts: [], quotes: [], notifications: [] };
  }
  if (pgPool) {
    pgLoad().then(pgData => {
      if (pgData && (pgData.users || []).length > (db.users || []).length) {
        db = pgData;
        console.log('[Ahoor] loaded state from Postgres (' + db.users.length + ' users)');
      }
    });
  }
  return db;
}
function save() {
  fs.mkdirSync(DATA_DIR, { recursive: true });
  const tmp = DB_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(db));
  fs.renameSync(tmp, DB_FILE);
  pgSaveSync();
}
load();

function publicQuote(q) {
  const post = db.posts.find(x => x.id === q.postId);
  const sender = db.users.find(u => u.id === q.senderId);
  const recipient = post ? db.users.find(u => u.id === post.ownerId) : null;
  return {
    id: q.id, postId: q.postId, kind: q.kind, status: q.status,
    pricePerUnit: q.pricePerUnit || '', totalPrice: q.totalPrice || '',
    availableQty: q.availableQty || '', moq: q.moq || '', deliveryTime: q.deliveryTime || '',
    validUntil: q.validUntil || '', reqQty: q.reqQty || '', preferredDelivery: q.preferredDelivery || '',
    budget: q.budget || '', message: q.message || '',
    createdAt: q.createdAt, respondedAt: q.respondedAt || null,
    post: post ? publicPost(post) : null,
    sender: sender ? { id: sender.id, name: sender.name, businessName: sender.businessName || '', district: sender.district || '', image: sender.image || '', phone: sender.phone } : null,
    recipient: recipient ? { id: recipient.id, name: recipient.name, businessName: recipient.businessName || '' } : null
  };
}
function addNotification(userId, type, refId, data) {
  db.notifications.push({
    id: uid(), userId, type, refId: refId || null,
    data: data || {}, read: false, createdAt: new Date().toISOString()
  });
}
function publicNotification(n) {
  return { id: n.id, type: n.type, refId: n.refId, data: n.data || {}, read: !!n.read, createdAt: n.createdAt };
}
function canQuote(user, post) {
  if (post.type === 'buyer') return user.type === 'supplier' || user.type === 'both';
  return user.type === 'buyer' || user.type === 'both';
}
function numOrEmpty(v) {
  const n = parseFloat(v);
  return !isNaN(n) && n >= 0 ? String(n) : '';
}

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
async function sendCode(target, channel, toEmail) {
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
  let emailed = false;
  try {
    emailed = await Promise.race([
      sendCodeEmail(toEmail, code),
      new Promise(res => setTimeout(() => res(false), 18000))
    ]);
  } catch (e) { emailed = false; }
  console.log(`[Ahoor] ${channel} code for ${target}: ${code} (email: ${emailed ? 'sent' : 'skipped/fallback'})`);
  return { ok: true, code: emailed ? null : (SHOW_CODES ? code : null), expiresIn: 600 };
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
      if (data.length > 2000000) { reject(new Error('too large')); req.destroy(); }
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
    const target = p === '/dashboard' ? '/dashboard.html' : p === '/profile-setup' ? '/profile-setup.html' : p === '/post' ? '/post.html' : p;
    if ((target === '/dashboard.html' || target === '/profile-setup.html' || target === '/post.html') && !getSession(req)) {
      res.writeHead(302, { Location: '/login?next=' + encodeURIComponent(target) });
      return res.end();
    }
  }

  /* --- API --- */
  if (p.startsWith('/api/')) {
    if (req.method !== 'POST' && !((p === '/api/posts' || p === '/api/notifications') && req.method === 'GET')) {
      return json(res, 405, { error: 'method' });
    }
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
        const r = await sendCode('signup:' + user.id, 'email', user.email);
        if (!r.ok) return json(res, 429, { error: 'cooldown', retryIn: r.retryIn });
        return json(res, 200, { devCode: r.code, expiresIn: r.expiresIn });
      }
      if (purpose === 'reset') {
        const user = findUser(identifier || '');
        if (!user) return json(res, 404, { error: 'not_found' });
        const rl = checkLimit(rlKey('send:' + user.id), 'send', 5, 15 * 60000);
        if (!rl.ok) return json(res, 429, { error: 'locked', retryIn: rl.retryIn });
        const r = await sendCode('reset:' + user.id, 'email', user.email);
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

    /* ---- profile ---- */
    if (p === '/api/profile') {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const user = db.users.find(u => u.id === sess.userId);
      if (!user) return json(res, 401, { error: 'no_session' });
      if (req.method !== 'POST') return json(res, 405, { error: 'method' });
      const { name, businessName, phone, district, category, description, image } = body;
      if (name !== undefined) {
        if (String(name || '').trim().length < 2) return json(res, 400, { error: 'name' });
        user.name = String(name).trim();
      }
      if (phone !== undefined) {
        if (validatePhone(phone)) return json(res, 400, { error: 'phone' });
        user.phone = String(phone).trim();
      }
      if (businessName !== undefined) user.businessName = String(businessName || '').trim().slice(0, 120);
      if (district !== undefined) user.district = String(district || '').trim().slice(0, 60);
      if (category !== undefined) user.category = String(category || '').trim().slice(0, 80);
      if (description !== undefined) user.description = String(description || '').trim().slice(0, 600);
      if (image !== undefined) {
        if (String(image).length > 400000) return json(res, 400, { error: 'image' });
        user.image = String(image || '');
      }
      save();
      return json(res, 200, { user: publicUser(user) });
    }

    /* ---- posts ---- */
    if (p === '/api/posts' && req.method === 'POST') {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const user = db.users.find(u => u.id === sess.userId);
      if (!user) return json(res, 401, { error: 'no_session' });
      const { type, title, category, qty, unit, budget, location, deadline, desc, image, moq, price } = body;
      if (type !== 'buyer' && type !== 'supplier') return json(res, 400, { error: 'type' });
      if (String(title || '').trim().length < 4) return json(res, 400, { error: 'title' });
      if (String(category || '').trim().length < 2) return json(res, 400, { error: 'category' });
      if (String(location || '').trim().length < 2) return json(res, 400, { error: 'location' });
      if (String(desc || '').trim().length < 10) return json(res, 400, { error: 'desc' });
      if (image !== undefined && String(image).length > 400000) return json(res, 400, { error: 'image' });
      const post = {
        id: uid(), ownerId: user.id, type,
        title: String(title).trim().slice(0, 160),
        category: String(category).trim(),
        qty: String(qty || '').trim(), unit: String(unit || '').trim(),
        budget: String(budget || '').trim(), location: String(location).trim(),
        deadline: String(deadline || '').trim(), desc: String(desc).trim().slice(0, 2000),
        image: String(image || ''), moq: String(moq || '').trim(), price: String(price || '').trim(),
        status: 'open', createdAt: new Date().toISOString()
      };
      db.posts.push(post);
      save();
      return json(res, 201, { post: publicPost(post) });
    }

    if (p === '/api/posts' && req.method === 'GET') {
      const url2 = new URL(req.url, 'http://x');
      const typeF = url2.searchParams.get('type') || '';
      const q = (url2.searchParams.get('q') || '').toLowerCase().trim();
      const cat = url2.searchParams.get('category') || '';
      const loc = url2.searchParams.get('location') || '';
      let list = db.posts.filter(pst => {
        if (typeF && typeF !== 'all' && pst.type !== typeF) return false;
        if (cat && pst.category !== cat) return false;
        if (loc && pst.location !== loc) return false;
        if (q) {
          const hay = (pst.title + ' ' + pst.desc + ' ' + pst.category + ' ' + pst.location).toLowerCase();
          if (!hay.includes(q)) return false;
        }
        return true;
      });
      list.sort((a, b) => (b.createdAt || '').localeCompare(a.createdAt || ''));
      list = list.slice(0, 60);
      return json(res, 200, { posts: list.map(publicPost) });
    }

    if (p === '/api/my-posts') {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const list = db.posts.filter(pt => pt.ownerId === sess.userId)
        .sort((a, b) => (b.createdAt || '').localeCompare(a.createdAt || ''));
      return json(res, 200, { posts: list.map(publicPost) });
    }

    const postMatch = p.match(/^\/api\/posts\/([0-9a-f-]{36})\/(edit|delete|toggle)$/);
    if (postMatch && (req.method === 'POST' || req.method === 'PUT' || req.method === 'DELETE')) {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const post = db.posts.find(pt => pt.id === postMatch[1]);
      if (!post) return json(res, 404, { error: 'post_not_found' });
      if (post.ownerId !== sess.userId) return json(res, 403, { error: 'forbidden' });
      const action = postMatch[2];
      if (action === 'delete') {
        db.posts = db.posts.filter(pt => pt.id !== post.id);
        db.quotes = db.quotes.filter(qq => qq.postId !== post.id);
        save();
        return json(res, 200, { ok: true });
      }
      if (action === 'toggle') {
        post.status = post.status === 'open' ? 'closed' : 'open';
        post.updatedAt = new Date().toISOString();
        save();
        return json(res, 200, { post: publicPost(post) });
      }
      if (action === 'edit') {
        const { title, category, qty, unit, budget, location, deadline, desc, image, moq, price } = body;
        if (title !== undefined) { if (String(title).trim().length < 4) return json(res, 400, { error: 'title' }); post.title = String(title).trim(); }
        if (category !== undefined) post.category = String(category).trim();
        if (qty !== undefined) post.qty = String(qty).trim();
        if (unit !== undefined) post.unit = String(unit).trim();
        if (budget !== undefined) post.budget = String(budget).trim();
        if (location !== undefined) post.location = String(location).trim();
        if (deadline !== undefined) post.deadline = String(deadline).trim();
        if (desc !== undefined) post.desc = String(desc).trim();
        if (moq !== undefined) post.moq = String(moq).trim();
        if (price !== undefined) post.price = String(price).trim();
        if (image !== undefined) post.image = String(image).slice(0, 400000);
        post.updatedAt = new Date().toISOString();
        save();
        return json(res, 200, { post: publicPost(post) });
      }
    }

    /* ---- quotes: send quote / request quote ---- */
    if (p === '/api/quotes' && req.method === 'POST') {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const user = db.users.find(u => u.id === sess.userId);
      if (!user) return json(res, 401, { error: 'no_session' });
      const { postId, message, pricePerUnit, availableQty, moq, deliveryTime, validUntil, reqQty, preferredDelivery, budget } = body;
      const post = db.posts.find(pt => pt.id === postId);
      if (!post) return json(res, 404, { error: 'post_not_found' });
      if (post.status === 'closed') return json(res, 400, { error: 'post_closed' });
      if (!canQuote(user, post)) return json(res, 403, { error: 'role_not_allowed' });
      if (post.ownerId === sess.userId) return json(res, 400, { error: 'self_quote' });
      if (String(message || '').trim().length < 5) return json(res, 400, { error: 'message' });
      // no duplicate pending quote from the same sender on the same post
      if (db.quotes.some(qq => qq.senderId === sess.userId && qq.postId === postId && qq.status === 'pending')) {
        return json(res, 409, { error: 'duplicate' });
      }
      const kind = post.type === 'buyer' ? 'quote' : 'request';
      const quote = {
        id: uid(), postId, senderId: sess.userId, kind,
        pricePerUnit: kind === 'quote' ? numOrEmpty(pricePerUnit) : '',
        totalPrice: '',
        availableQty: kind === 'quote' ? numOrEmpty(availableQty) : '',
        moq: kind === 'quote' ? numOrEmpty(moq) : '',
        deliveryTime: kind === 'quote' ? String(deliveryTime || '').trim().slice(0, 60) : '',
        validUntil: kind === 'quote' ? String(validUntil || '').trim().slice(0, 20) : '',
        reqQty: kind === 'request' ? numOrEmpty(reqQty) : '',
        preferredDelivery: kind === 'request' ? String(preferredDelivery || '').trim().slice(0, 60) : '',
        budget: kind === 'request' ? String(budget || '').trim().slice(0, 60) : '',
        message: String(message).trim().slice(0, 1000),
        status: 'pending', createdAt: new Date().toISOString(), respondedAt: null
      };
      if (kind === 'quote' && quote.pricePerUnit !== '' && quote.availableQty !== '') {
        const ppu = parseFloat(quote.pricePerUnit), aq = parseFloat(quote.availableQty);
        if (!isNaN(ppu) && !isNaN(aq)) quote.totalPrice = String(Math.round(ppu * aq));
      }
      db.quotes.push(quote);
      // notify the post owner
      addNotification(post.ownerId, kind === 'quote' ? 'quote_received' : 'request_received', quote.id,
        { senderName: user.businessName || user.name, postTitle: post.title });
      save();
      return json(res, 201, { quote: publicQuote(quote) });
    }

    /* ---- received quotes (as post owner) ---- */
    if (p === '/api/quotes/received') {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const myPostIds = new Set(db.posts.filter(pt => pt.ownerId === sess.userId).map(pt => pt.id));
      const list = db.quotes.filter(qq => myPostIds.has(qq.postId))
        .sort((a, b) => (b.createdAt || '').localeCompare(a.createdAt || ''));
      return json(res, 200, { quotes: list.map(publicQuote) });
    }

    /* ---- sent quotes (as sender) ---- */
    if (p === '/api/quotes/sent') {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const list = db.quotes.filter(qq => qq.senderId === sess.userId)
        .sort((a, b) => (b.createdAt || '').localeCompare(a.createdAt || ''));
      return json(res, 200, { quotes: list.map(publicQuote) });
    }

    /* ---- respond: accept / reject (post owner only) ---- */
    const qResp = p.match(/^\/api\/quotes\/([0-9a-f-]{36})\/respond$/);
    if (qResp) {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const quote = db.quotes.find(qq => qq.id === qResp[1]);
      if (!quote) return json(res, 404, { error: 'quote_not_found' });
      const post = db.posts.find(pt => pt.id === quote.postId);
      if (!post) return json(res, 404, { error: 'post_not_found' });
      if (post.ownerId !== sess.userId) return json(res, 403, { error: 'forbidden' });
      if (quote.senderId === sess.userId) return json(res, 403, { error: 'own_quote' });
      if (quote.status !== 'pending') return json(res, 400, { error: 'not_pending' });
      const action = body.action;
      if (action !== 'accept' && action !== 'reject') return json(res, 400, { error: 'action' });
      quote.status = action === 'accept' ? 'accepted' : 'rejected';
      quote.respondedAt = new Date().toISOString();
      const sender = db.users.find(u => u.id === quote.senderId);
      addNotification(quote.senderId, action === 'accept' ? 'quote_accepted' : 'quote_rejected', quote.id,
        { postTitle: post.title, recipientName: (sender ? '' : '') });
      save();
      return json(res, 200, { quote: publicQuote(quote) });
    }

    /* ---- withdraw (sender only, pending only) ---- */
    const qWith = p.match(/^\/api\/quotes\/([0-9a-f-]{36})\/withdraw$/);
    if (qWith) {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const quote = db.quotes.find(qq => qq.id === qWith[1]);
      if (!quote) return json(res, 404, { error: 'quote_not_found' });
      if (quote.senderId !== sess.userId) return json(res, 403, { error: 'forbidden' });
      if (quote.status !== 'pending') return json(res, 400, { error: 'not_pending' });
      quote.status = 'withdrawn';
      save();
      return json(res, 200, { quote: publicQuote(quote) });
    }

    /* ---- notifications ---- */
    if (p === '/api/notifications' && req.method === 'GET') {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const list = db.notifications.filter(n => n.userId === sess.userId)
        .sort((a, b) => (b.createdAt || '').localeCompare(a.createdAt || '')).slice(0, 50);
      const unread = db.notifications.filter(n => n.userId === sess.userId && !n.read).length;
      return json(res, 200, { notifications: list.map(publicNotification), unread });
    }

    if (p === '/api/notifications/read' && req.method === 'POST') {
      const sess = getSession(req);
      if (!sess) return json(res, 401, { error: 'no_session' });
      const { id } = body;
      if (id) {
        const n = db.notifications.find(x => x.id === id);
        if (n && n.userId === sess.userId) n.read = true;
      } else {
        db.notifications.forEach(n => { if (n.userId === sess.userId) n.read = true; });
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
  return {
    id: u.id, name: u.name, email: u.email, phone: u.phone, type: u.type, createdAt: u.createdAt,
    businessName: u.businessName || '', district: u.district || '', category: u.category || '',
    description: u.description || '', image: u.image || '', profileComplete: !!(u.businessName && u.district)
  };
}
function publicPost(p) {
  const owner = db.users.find(u => u.id === p.ownerId);
  return {
    id: p.id, type: p.type, title: p.title, category: p.category, qty: p.qty || '', unit: p.unit || '',
    budget: p.budget || '', location: p.location || '', deadline: p.deadline || '',
    desc: p.desc || '', image: p.image || '', moq: p.moq || '', price: p.price || '',
    status: p.status || 'open', createdAt: p.createdAt, updatedAt: p.updatedAt || p.createdAt,
    owner: owner ? {
      id: owner.id, name: owner.name, businessName: owner.businessName || '',
      district: owner.district || '', image: owner.image || ''
    } : null
  };
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

pgInit();

const server = http.createServer(handle);
server.listen(PORT, '0.0.0.0', () => {
  console.log(`Ahoor server running on http://0.0.0.0:${PORT}`);
  console.log(`Dev mode: ${DEV ? 'ON (verification codes returned to client for testing)' : 'OFF'}`);
});
