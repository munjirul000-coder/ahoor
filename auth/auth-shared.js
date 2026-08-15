/* ============================================================
   Ahoor — Auth pages shared JS: i18n (bn/en) + API + UI helpers
   ============================================================ */
(function(){
'use strict';

/* ---------------- dictionary ---------------- */
var D = {
 "back.home":["← Back to Home","← হোমে ফিরে যান"],
 "lang.aria":["Language","ভাষা"],
 "meta.login":["Ahoor — Sign In","Ahoor — সাইন ইন"],
 "meta.signup":["Ahoor — Create Account","Ahoor — অ্যাকাউন্ট তৈরি করুন"],
 "meta.forgot":["Ahoor — Forgot Password","Ahoor — পাসওয়ার্ড ভুলে গেছেন"],
 "meta.dash":["Ahoor — My Account","Ahoor — আমার অ্যাকাউন্ট"],
 "meta.profile":["Ahoor — Account Ready","Ahoor — অ্যাকাউন্ট প্রস্তুত"],
 "foot.made":["Made in Bangladesh","বাংলাদেশে তৈরি"],
 "foot.cr":["© 2026 Ahoor. All rights reserved.","© ২০২৬ Ahoor. সর্বস্বত্ব সংরক্ষিত।"],

 "login.title":["Welcome Back","আবার স্বাগতম"],
 "login.sub":["Sign in to continue to Ahoor.","Ahoor ব্যবহার চালিয়ে যেতে সাইন ইন করুন।"],
 "login.id":["Email address or phone number","ইমেইল বা মোবাইল নম্বর"],
 "login.idPh":["you@company.com or 01XXXXXXXXX","you@company.com বা 01XXXXXXXXX"],
 "login.pw":["Password","পাসওয়ার্ড"],
 "login.pwPh":["Enter your password","আপনার পাসওয়ার্ড লিখুন"],
 "login.show":["Show","দেখুন"],
 "login.hide":["Hide","লুকান"],
 "login.remember":["Remember me","মনে রাখুন"],
 "login.forgot":["Forgot password?","পাসওয়ার্ড ভুলে গেছেন?"],
 "login.btn":["Sign In","সাইন ইন"],
 "login.loading":["Signing in…","সাইন ইন হচ্ছে…"],
 "login.noAccount":["Don't have an account?","অ্যাকাউন্ট নেই?"],
 "login.create":["Create Account","অ্যাকাউন্ট তৈরি করুন"],
 "login.verifyNote":["Your account is not verified yet.","আপনার অ্যাকাউন্ট এখনো যাচাই করা হয়নি।"],
 "login.verifyBtn":["Verify now","এখনই যাচাই করুন"],
 "login.verifiedOk":["Account verified. You can sign in now.","অ্যাকাউন্ট যাচাই হয়েছে। এখন সাইন ইন করতে পারেন।"],

 "su.title":["Create Account","অ্যাকাউন্ট তৈরি করুন"],
 "su.sub":["Start your Ahoor journey in minutes.","মিনিটেই শুরু করুন আপনার Ahoor যাত্রা।"],
 "su.s1l":["Step 1 of 3 — Account","ধাপ ১/৩ — অ্যাকাউন্ট"],
 "su.name":["Full Name","সম্পূর্ণ নাম"],
 "su.namePh":["e.g. Rahim Uddin","যেমন: রহিম উদ্দিন"],
 "su.email":["Email Address","ইমেইল ঠিকানা"],
 "su.emailPh":["you@company.com","you@company.com"],
 "su.phone":["Mobile Number","মোবাইল নম্বর"],
 "su.phonePh":["01XXXXXXXXX","01XXXXXXXXX"],
 "su.pw":["Password","পাসওয়ার্ড"],
 "su.pwPh":["Create a strong password","শক্তিশালী পাসওয়ার্ড দিন"],
 "su.pw2":["Confirm Password","পাসওয়ার্ড নিশ্চিত করুন"],
 "su.pw2Ph":["Re-enter your password","পাসওয়ার্ড আবার লিখুন"],
 "su.reqTitle":["Password must include","পাসওয়ার্ডে অবশ্যই থাকতে হবে"],
 "su.req1":["At least 8 characters","কমপক্ষে ৮ অক্ষর"],
 "su.req2":["A letter and a number","একটি অক্ষর ও একটি সংখ্যা"],
 "su.strength":["Password strength","পাসওয়ার্ডের শক্তি"],
 "su.st0":["Too short","খুব ছোট"],
 "su.st1":["Weak","দুর্বল"],
 "su.st2":["Fair","মোটামুটি"],
 "su.st3":["Good","ভালো"],
 "su.st4":["Strong","শক্তিশালী"],
 "su.continue":["Continue","চালিয়ে যান"],
 "su.continueLoad":["Creating account…","অ্যাকাউন্ট তৈরি হচ্ছে…"],
 "su.back":["Back","পেছনে"],
 "su.s2l":["Step 2 of 3 — Account Type","ধাপ ২/৩ — অ্যাকাউন্টের ধরন"],
 "su.typeTitle":["How will you use Ahoor?","আপনি Ahoor কীভাবে ব্যবহার করবেন?"],
 "su.typeSub":["Choose one — you can change this later.","একটি বেছে নিন — পরে পরিবর্তন করা যাবে।"],
 "su.typeBuyer":["Buyer","ক্রেতা"],
 "su.typeBuyerD":["I want to find products, suppliers, manufacturers, or business services.","আমি পণ্য, সরবরাহকারী, প্রস্তুতকারক বা ব্যবসায়িক সেবা খুঁজতে চাই।"],
 "su.typeSupplier":["Supplier / Manufacturer","সরবরাহকারী / প্রস্তুতকারক"],
 "su.typeSupplierD":["I want to offer products, services, or manufacturing capabilities.","আমি পণ্য, সেবা বা উৎপাদন সুবিধা দিতে চাই।"],
 "su.typeBoth":["Both","দুটোই"],
 "su.typeBothD":["I want to both buy and sell through Ahoor.","আমি Ahoor-এর মাধ্যমে কিনতে এবং বিক্রি—দুটোই করতে চাই।"],
 "su.typeErr":["Please select an account type.","অনুগ্রহ করে অ্যাকাউন্টের ধরন নির্বাচন করুন।"],
 "su.s3l":["Step 3 of 3 — Verify","ধাপ ৩/৩ — যাচাই করুন"],
 "su.verifyTitle":["Verify Your Account","আপনার অ্যাকাউন্ট যাচাই করুন"],
 "su.verifySub":["We sent a 6-digit verification code to your email.","আপনার ইমেইলে ৬ সংখ্যার যাচাই কোড পাঠানো হয়েছে।"],
 "su.code":["Verification code","যাচাই কোড"],
 "su.resend":["Resend code","কোড আবার পাঠান"],
 "su.resendIn":["Resend in {s}s","{s} সেকেন্ড পর আবার পাঠান"],
 "su.verifyBtn":["Verify & Create Account","যাচাই করে অ্যাকাউন্ট তৈরি করুন"],
 "su.verifyLoad":["Verifying…","যাচাই করা হচ্ছে…"],
 "su.done":["Account Created Successfully","অ্যাকাউন্ট সফলভাবে তৈরি হয়েছে"],
 "su.doneSub":["Setting up your account…","আপনার অ্যাকাউন্ট তৈরি হচ্ছে…"],

 "fp.title":["Forgot Password","পাসওয়ার্ড ভুলে গেছেন"],
 "fp.sub":["Enter your email or mobile number — we'll send you a verification code.","আপনার ইমেইল বা মোবাইল নম্বর দিন — আমরা একটি যাচাই কোড পাঠাব।"],
 "fp.s1l":["Step 1 of 3 — Identify","ধাপ ১/৩ — শনাক্তকরণ"],
 "fp.id":["Email address or phone number","ইমেইল বা মোবাইল নম্বর"],
 "fp.idPh":["you@company.com or 01XXXXXXXXX","you@company.com বা 01XXXXXXXXX"],
 "fp.send":["Send Code","কোড পাঠান"],
 "fp.sendLoad":["Sending…","পাঠানো হচ্ছে…"],
 "fp.s2l":["Step 2 of 3 — Verify","ধাপ ২/৩ — যাচাই করুন"],
 "fp.verifyTitle":["Enter the verification code","যাচাই কোডটি লিখুন"],
 "fp.verifySub":["We sent a 6-digit code to your email.","আপনার ইমেইলে ৬ সংখ্যার কোড পাঠানো হয়েছে।"],
 "fp.verifyBtn":["Verify Code","কোড যাচাই করুন"],
 "fp.s3l":["Step 3 of 3 — New Password","ধাপ ৩/৩ — নতুন পাসওয়ার্ড"],
 "fp.newTitle":["Set a new password","নতুন পাসওয়ার্ড দিন"],
 "fp.newPw":["New Password","নতুন পাসওয়ার্ড"],
 "fp.newPwPh":["Enter a new password","নতুন পাসওয়ার্ড লিখুন"],
 "fp.newPw2":["Confirm New Password","নতুন পাসওয়ার্ড নিশ্চিত করুন"],
 "fp.reset":["Reset Password","পাসওয়ার্ড রিসেট করুন"],
 "fp.resetLoad":["Resetting…","রিসেট করা হচ্ছে…"],
 "fp.done":["Password changed successfully.","পাসওয়ার্ড সফলভাবে পরিবর্তিত হয়েছে।"],
 "fp.doneSub":["You can now sign in with your new password.","এখন নতুন পাসওয়ার্ড দিয়ে সাইন ইন করতে পারবেন।"],
 "fp.signin":["Sign In","সাইন ইন"],

 "db.title":["My Account","আমার অ্যাকাউন্ট"],
 "db.welcome":["Welcome to Ahoor, {name}","Ahoor-এ স্বাগতম, {name}"],
 "db.sub":["Here's a quick look at your account.","আপনার অ্যাকাউন্টের এক নজরে সারসংক্ষেপ।"],
 "db.type.buyer":["Buyer","ক্রেতা"],
 "db.type.supplier":["Supplier / Manufacturer","সরবরাহকারী / প্রস্তুতকারক"],
 "db.type.both":["Buyer & Supplier","ক্রেতা ও সরবরাহকারী"],
 "db.member":["Member since {d}","{d} থেকে সদস্য"],
 "db.profile":["My Profile","আমার প্রোফাইল"],
 "db.profileD":["Your business information","আপনার ব্যবসার তথ্য"],
 "db.opps":["My Opportunities","আমার সুযোগ"],
 "db.oppsD":["Requirements & offers you posted","আপনার পোস্ট করা প্রয়োজন ও অফার"],
 "db.msgs":["Messages","মেসেজ"],
 "db.msgsD":["Business conversations","ব্যবসায়িক কথোপকথন"],
 "db.settings":["Account Settings","অ্যাকাউন্ট সেটিংস"],
 "db.settingsD":["Security & preferences","নিরাপত্তা ও পছন্দ"],
 "db.soon":["Coming soon","শীঘ্রই আসছে"],
 "db.home":["Back to Home","হোমে ফিরে যান"],
 "db.signout":["Sign Out","সাইন আউট"],
 "db.signingout":["Signing out…","সাইন আউট হচ্ছে…"],

 "ps.title":["Your Ahoor account is ready.","আপনার Ahoor অ্যাকাউন্ট প্রস্তুত।"],
 "ps.sub":["Next, complete your business profile to start finding opportunities and connecting with businesses.","এরপর ব্যবসার প্রোফাইল সম্পূর্ণ করুন — সুযোগ খুঁজতে এবং ব্যবসার সাথে কানেক্ট হতে।"],
 "ps.btn":["Complete Profile","প্রোফাইল সম্পূর্ণ করুন"],
 "ps.btnSoon":["The business profile builder is coming soon.","ব্যবসার প্রোফাইল তৈরির ফিচার শীঘ্রই আসছে।"],
 "ps.dash":["Go to Dashboard","ড্যাশবোর্ডে যান"],
 "ps.thanks":["Thanks for joining Ahoor!","Ahoor-এ যোগ দেওয়ার জন্য ধন্যবাদ!"],

 "err.email":["Please enter a valid email address.","সঠিক ইমেইল ঠিকানা দিন।"],
 "err.phone":["Please enter a valid Bangladeshi mobile number.","সঠিক বাংলাদেশি মোবাইল নম্বর দিন।"],
 "err.name":["Please enter your full name (at least 2 characters).","আপনার সম্পূর্ণ নাম দিন (কমপক্ষে ২ অক্ষর)।"],
 "err.weak":["Password must be at least 8 characters with a letter and a number.","পাসওয়ার্ড কমপক্ষে ৮ অক্ষরের হতে হবে, একটি অক্ষর ও একটি সংখ্যাসহ।"],
 "err.mismatch":["Passwords do not match.","পাসওয়ার্ড দুটি মিলছে না।"],
 "err.required":["Please fill in all fields.","সব ঘর পূরণ করুন।"],
 "err.email_exists":["An account already exists with this email address.","এই ইমেইল দিয়ে ইতোমধ্যে একটি অ্যাকাউন্ট রয়েছে।"],
 "err.phone_exists":["An account already exists with this phone number.","এই মোবাইল নম্বর দিয়ে ইতোমধ্যে একটি অ্যাকাউন্ট রয়েছে।"],
 "err.invalid":["Incorrect email/phone or password.","ইমেইল/ফোন বা পাসওয়ার্ড সঠিক নয়।"],
 "err.not_found":["No account found with this email or phone.","এই ইমেইল বা ফোনে কোনো অ্যাকাউন্ট পাওয়া যায়নি।"],
 "err.invalid_code":["Invalid verification code.","যাচাই কোডটি সঠিক নয়।"],
 "err.expired":["This code has expired. Request a new one.","কোডটির মেয়াদ শেষ। নতুন কোড নিন।"],
 "err.too_many":["Too many attempts. Please try again later.","অনেকবার চেষ্টা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।"],
 "err.cooldown":["Please wait {s}s before resending.","আবার পাঠাতে {s} সেকেন্ড অপেক্ষা করুন।"],
 "err.locked":["Too many attempts. Try again in {m} min.","অনেকবার চেষ্টা হয়েছে। {m} মিনিট পর আবার চেষ্টা করুন।"],
 "err.unverified":["Your account is not verified yet.","আপনার অ্যাকাউন্ট এখনো যাচাই করা হয়নি।"],
 "err.network":["Network error. Please check your connection and try again.","নেটওয়ার্ক সমস্যা। ইন্টারনেট সংযোগ পরীক্ষা করে আবার চেষ্টা করুন।"],
 "err.offline":["Server not reachable — please open this page from the live Ahoor preview (run node server.js).","সার্ভারের সাথে সংযোগ হচ্ছে না — লাইভ Ahoor প্রিভিউ লিংক থেকে পেজটি খুলুন (node server.js চালু থাকতে হবে)।"],
 "err.bad_response":["The server returned an unexpected response. Please try again.","সার্ভার থেকে অপ্রত্যাশিত সাড়া এসেছে। আবার চেষ্টা করুন।"],
 "err.missing":["Please fill in all fields.","সব ঘর পূরণ করুন।"],
 "err.no_session":["Your session has expired. Please sign in again.","আপনার সেশন শেষ হয়ে গেছে। আবার সাইন ইন করুন।"],
 "err.route":["This action is not available right now. Please try again.","এই কাজটি এখন করা যাচ্ছে না। আবার চেষ্টা করুন।"],
 "err.method":["This action is not available right now. Please try again.","এই কাজটি এখন করা যাচ্ছে না। আবার চেষ্টা করুন।"],
 "err.purpose":["This action is not available right now. Please try again.","এই কাজটি এখন করা যাচ্ছে না। আবার চেষ্টা করুন।"],
 "err.forbidden":["This action is not allowed.","এই কাজটি করার অনুমতি নেই।"],
 "err.locked":["Too many attempts. Try again in {m} min.","অনেকবার চেষ্টা হয়েছে। {m} মিনিট পর আবার চেষ্টা করুন।"],
 "err.generic":["Something went wrong. Please try again.","কিছু একটা সমস্যা হয়েছে। আবার চেষ্টা করুন।"],
 "err.code":["Enter the 6-digit code.","৬ সংখ্যার কোডটি লিখুন।"],
 "err.type":["Please select an account type.","অনুগ্রহ করে অ্যাকাউন্টের ধরন নির্বাচন করুন।"],
 "ok.sent":["Code sent!","কোড পাঠানো হয়েছে!"],
 "ok.verified":["Verified!","যাচাই হয়েছে!"],
 "dev.note":["Demo mode — your code: {c} (in production it is sent by SMS/email)","ডেমো মোড — আপনার কোড: {c} (প্রকৃত পরিবেশে এটি এসএমএস/ইমেইলে যাবে)"],
 "ui.loading":["Loading…","লোড হচ্ছে…"]
};

var LANG = (function(){
  try{ var s = localStorage.getItem('ahoor-lang'); if(s==='en'||s==='bn') return s; }catch(e){}
  return 'bn';
})();

function t(key, params){
  var v = D[key];
  if(!v) return key;
  var s = v[LANG==='bn'?1:0];
  if(params){ for(var k in params){ s = s.replace('{'+k+'}', params[k]); } }
  return s;
}
function applyLang(){
  document.documentElement.lang = LANG;
  document.querySelectorAll('[data-i18n]').forEach(function(el){
    var v = D[el.getAttribute('data-i18n')];
    if(v) el.textContent = v[LANG==='bn'?1:0];
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(function(el){
    var v = D[el.getAttribute('data-i18n-ph')];
    if(v) el.setAttribute('placeholder', v[LANG==='bn'?1:0]);
  });
  document.querySelectorAll('.lang-btn').forEach(function(b){
    var on = b.getAttribute('data-lang')===LANG;
    b.classList.toggle('on',on);
    b.setAttribute('aria-pressed', on?'true':'false');
  });
  var metaKey = document.body.getAttribute('data-meta');
  if(metaKey && D[metaKey]) document.title = D[metaKey][LANG==='bn'?1:0];
  document.dispatchEvent(new CustomEvent('langchange'));
}
function setLang(l){
  LANG = l;
  try{ localStorage.setItem('ahoor-lang', l); }catch(e){}
  applyLang();
}
document.querySelectorAll('.lang-btn').forEach(function(b){
  b.addEventListener('click', function(){ setLang(b.getAttribute('data-lang')); });
});
window.__t = t;

/* ---------------- helpers ---------------- */
function $(s, c){ return (c||document).querySelector(s); }
function $all(s, c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); }
function esc(s){ var d=document.createElement('div'); d.textContent=s; return d.innerHTML; }

function api(path, body){
  var opts = { method:'POST', headers:{'Content-Type':'application/json'}, credentials:'same-origin' };
  if(body) opts.body = JSON.stringify(body);
  return fetch(path, opts).then(function(r){
    var ct = r.headers.get('content-type') || '';
    if(ct.indexOf('application/json') === -1){
      return { status:r.status, data:{ error:'bad_response' } };
    }
    return r.json().then(function(j){ return { status:r.status, data:j }; })
      .catch(function(){ return { status:r.status, data:{ error:'bad_response' } }; });
  }).catch(function(){ return { status:0, data:{ error:'offline' } }; });
}
var ERR_CODES = ['email_exists','phone_exists','invalid','not_found','weak','unverified','invalid_code','expired','too_many','network','offline','bad_response','missing','no_session','route','method','purpose','forbidden','email','phone','name','mismatch','required','type','code','locked','generic'];
function errMsg(e){
  e = e || 'generic';
  if(ERR_CODES.indexOf(e) >= 0) return t('err.'+e);
  return t('err.generic');
}

/* message boxes */
function showMsg(el, type, text){
  if(!el) return;
  el.className = 'msg show msg-' + type;
  var ic = type==='error' ? '<svg class="msg-ic" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v4.5M12 16h.01"/></svg>'
       : type==='success' ? '<svg class="msg-ic" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="m8.5 12.2 2.4 2.4 4.6-4.8"/></svg>'
       : '<svg class="msg-ic" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.5h.01"/></svg>';
  el.innerHTML = ic + '<span>' + esc(text) + '</span>';
}
function hideMsg(el){ if(el) el.classList.remove('show'); }

/* toast */
var toastTimer=null;
function toast(text, type){
  var el = $('#toast');
  if(!el){
    el = document.createElement('div');
    el.id='toast'; el.className='toast';
    document.body.appendChild(el);
  }
  el.className = 'toast show ' + (type||'ok');
  el.innerHTML = '<span class="tic"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg></span><span>'+esc(text)+'</span>';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(function(){ el.classList.remove('show'); }, 3600);
}

/* loading state on buttons */
function setLoading(btn, on, loadKey){
  if(!btn) return;
  if(on){
    btn.classList.add('loading');
    btn.setAttribute('disabled','disabled');
    if(loadKey){ var label=$('.btn-label', btn); if(label) label.textContent = t(loadKey); }
  } else {
    btn.classList.remove('loading');
    btn.removeAttribute('disabled');
  }
}

/* validators */
function validEmail(v){ return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(v||'').trim()); }
function validPhone(v){
  var d = String(v||'').replace(/[^\d+]/g,'');
  return /^(?:\+?880|0)1[3-9]\d{8}$/.test(d);
}
function pwScore(pw){
  var s=0;
  if(pw.length>=8) s++;
  if(pw.length>=12) s++;
  if(/[A-Za-z]/.test(pw) && /\d/.test(pw)) s++;
  if(/[^A-Za-z0-9]/.test(pw)) s++;
  return s;
}

/* password strength meter + requirements */
function initStrength(input, barsEl, labelEl){
  function update(){
    var v = input.value;
    var s = pwScore(v);
    if(!v){ barsEl.querySelectorAll('i').forEach(function(i){ i.className=''; }); labelEl.querySelector('em').textContent=''; return; }
    var active = v.length>=8 ? Math.max(1, s) : 0;
    var colors = ['f','f','g','g','v'];
    barsEl.querySelectorAll('i').forEach(function(i, idx){
      i.className = idx < active ? colors[active-1] : '';
    });
    labelEl.querySelector('em').textContent = t('su.st'+active);
    labelEl.querySelector('em').style.color = active>=4 ? '#0E9F7E' : active>=2 ? '#F0A000' : '#E5484D';
    /* requirements */
    var reqs = input.getAttribute('data-reqs');
    if(reqs){
      var r1 = $('[data-req="len"]'), r2 = $('[data-req="mix"]');
      if(r1) r1.classList.toggle('ok', v.length>=8);
      if(r2) r2.classList.toggle('ok', /[A-Za-z]/.test(v) && /\d/.test(v));
    }
  }
  input.addEventListener('input', update);
  return update;
}

/* password show/hide toggles */
function initPwToggles(root){
  $all('.pw-toggle', root).forEach(function(btn){
    btn.addEventListener('click', function(){
      var input = document.getElementById(btn.getAttribute('data-target'));
      if(!input) return;
      var show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      btn.innerHTML = show
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><path d="m1 1 22 22"/><path d="M14.12 14.12a3 3 0 1 1-4.24-4.24"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>';
    });
  });
}

/* OTP inputs */
function initOtp(inputs, onComplete){
  inputs.forEach(function(inp, i){
    inp.setAttribute('inputmode','numeric');
    inp.setAttribute('maxlength','1');
    inp.addEventListener('input', function(){
      var v = inp.value.replace(/[^0-9]/g,'').slice(0,1);
      inp.value = v;
      if(v){ inp.classList.add('filled'); if(i < inputs.length-1) inputs[i+1].focus(); }
      var full = inputs.every(function(x){ return x.value; });
      if(full && onComplete) onComplete(inputs.map(function(x){ return x.value; }).join(''));
    });
    inp.addEventListener('keydown', function(e){
      if(e.key==='Backspace' && !inp.value && i>0){ inputs[i-1].focus(); inputs[i-1].value=''; inputs[i-1].classList.remove('filled'); }
    });
    inp.addEventListener('paste', function(e){
      e.preventDefault();
      var txt = (e.clipboardData||window.clipboardData).getData('text').replace(/[^0-9]/g,'').slice(0, inputs.length);
      inputs.forEach(function(x, j){ x.value = txt[j]||''; x.classList.toggle('filled', !!txt[j]); });
      var full = inputs.every(function(x){ return x.value; });
      if(full && onComplete) onComplete(txt);
      else inputs[Math.min(txt.length, inputs.length-1)].focus();
    });
  });
}

/* countdown resend button */
function startCountdown(btn, seconds, labelKey){
  var left = seconds;
  btn.disabled = true;
  var iv = setInterval(function(){
    left--;
    if(left<=0){
      clearInterval(iv);
      btn.disabled = false;
      btn.textContent = t('su.resend');
    } else {
      btn.textContent = t('su.resendIn', {s:left});
    }
  }, 1000);
}

/* field error */
function fieldErr(input, key){
  var wrap = input.closest('.field');
  var el = wrap ? $('.field-err', wrap) : null;
  if(el){ el.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v4.5M12 16h.01"/></svg><span>' + esc(t(key)) + '</span>'; el.classList.add('show'); }
  input.classList.add('err');
  input.addEventListener('input', function h(){ input.classList.remove('err'); if(el) el.classList.remove('show'); input.removeEventListener('input', h); }, {once:true});
}
function clearFieldErr(input){
  var wrap = input.closest('.field');
  var el = wrap ? $('.field-err', wrap) : null;
  if(el) el.classList.remove('show');
  input.classList.remove('err');
}

/* server reachability probe (shows a clear banner when the page is opened
   outside the running server, e.g. the file preview or server is down) */
function probeServer(){
  fetch('/api/session', { method:'POST', credentials:'same-origin' })
    .catch(function(){
      var b = document.createElement('div');
      b.id = 'offlineBanner';
      b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999;background:#E5484D;color:#fff;padding:11px 16px;text-align:center;font-size:.84rem;font-weight:600;line-height:1.5;box-shadow:0 8px 24px rgba(0,0,0,.18)';
      b.textContent = t('err.offline');
      document.body.prepend(b);
    });
}
if(document.readyState === 'complete'){ probeServer(); }
else { window.addEventListener('load', probeServer); }

window.Ahoor = {
  t:t, applyLang:applyLang, api:api, errMsg:errMsg, showMsg:showMsg, hideMsg:hideMsg,
  toast:toast, setLoading:setLoading, validEmail:validEmail, validPhone:validPhone,
  initStrength:initStrength, initPwToggles:initPwToggles, initOtp:initOtp,
  startCountdown:startCountdown, fieldErr:fieldErr, clearFieldErr:clearFieldErr, esc:esc
};
applyLang();
})();
