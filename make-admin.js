#!/usr/bin/env node
/* ============================================================
   Ahoor — Make Admin
   Usage (SSH / server console, from the project folder):
     node make-admin.js youremail@example.com
   Promotes an EXISTING verified user to admin.
   (Direct DB edit, so it works even if ADMIN_EMAIL was changed.)
   ============================================================ */
'use strict';
const fs = require('fs');
const path = require('path');

const DB_FILE = path.join(__dirname, 'data', 'db.json');
const email = (process.argv[2] || '').trim().toLowerCase();

if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
  console.log('❌ Usage: node make-admin.js youremail@example.com');
  process.exit(1);
}

let db;
try {
  db = JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
} catch (e) {
  console.log('❌ data/db.json খুঁজে পাওয়া যায়নি:', e.message);
  console.log('   নিশ্চিত করুন আপনি Ahoor প্রজেক্ট ফোল্ডার থেকে চালাচ্ছেন');
  process.exit(1);
}

const user = db.users.find(u => u.email === email);
if (!user) {
  console.log(`❌ "${email}" দিয়ে কোনো অ্যাকাউন্ট পাওয়া যায়নি।`);
  console.log('   আগে সাইনআপ করুন, তারপর আবার এই স্ক্রিপ্ট চালান।');
  process.exit(1);
}
if (user.status !== 'active') {
  console.log(`⚠️ "${email}" অ্যাকাউন্টটি এখনো ভেরিফাই করা হয়নি (status=${user.status})।`);
  console.log('   আগে লগইন/ভেরিফিকেশন সম্পন্ন করুন, তারপর আবার চালান।');
  process.exit(1);
}

user.role = 'admin';
fs.writeFileSync(DB_FILE, JSON.stringify(db));
console.log(`✅ "${email}" এখন অ্যাডমিন!`);
console.log('   অ্যাডমিন প্যানেল খুলুন: /admin.html');
