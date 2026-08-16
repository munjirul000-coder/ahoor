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
 "su.s3l":["Step 3 of 4 — Business Info","ধাপ ৩/৪ — ব্যবসার তথ্য"],
 "su.s4l":["Step 4 of 4 — Verify","ধাপ ৪/৪ — যাচাই করুন"],
 "su.bizTitle":["Tell us about your business","আপনার ব্যবসা সম্পর্কে জানান"],
 "su.bizSub":["You can edit these anytime from your business profile.","যেকোনো সময় বিজনেস প্রোফাইল থেকে এডিট করতে পারবেন।"],
 "su.bizName":["Company / Business Name","কোম্পানি / ব্যবসার নাম"],
 "su.bizNamePh":["e.g. Rahim Garments","যেমন: রহিম গার্মেন্টস"],
 "su.buyerSec":["Buying Information","ক্রয় সংক্রান্ত তথ্য"],
 "su.supplierSec":["Supplier / Manufacturing Information","সরবরাহ / উৎপাদন সংক্রান্ত তথ্য"],
 "su.buyProducts":["What products do you usually want to buy?","আপনি সাধারণত কী কী পণ্য কিনে থাকেন?"],
 "su.buyProductsPh":["e.g. Cotton T-Shirts, Yarn, Packaging","যেমন: কটন টি-শার্ট, সুতা, প্যাকেজিং"],
 "su.supplyProducts":["What products do you make or supply?","আপনি কী কী পণ্য তৈরি করেন বা সরবরাহ করেন?"],
 "su.supplyProductsPh":["e.g. T-Shirts, Hoodies, Polo Shirts","যেমন: টি-শার্ট, হুডি, পোলো শার্ট"],
 "su.typicalQty":["Typical required quantity","সাধারণ প্রয়োজনীয় পরিমাণ"],
 "su.typicalQtyPh":["e.g. 1,000 pcs","যেমন: ১,০০০ পিস"],
 "su.moq":["Minimum Order Quantity (MOQ)","ন্যূনতম অর্ডার পরিমাণ (MOQ)"],
 "su.moqPh":["e.g. 100 pcs","যেমন: ১০০ পিস"],
 "su.category":["Product Category","পণ্যের ক্যাটাগরি"],
 "su.location":["Location","অবস্থান"],
 "su.bizSkip":["Skip for now — complete later","এখনই না — পরে সম্পূর্ণ করব"],
 "bp.buyProducts":["Products usually bought","সাধারণত কেনা পণ্য"],
 "bp.typicalQty":["Typical quantity","সাধারণ পরিমাণ"],
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
 "err.suspended":["Your account has been suspended. Contact support for help.","আপনার অ্যাকাউন্ট সাসপেন্ড করা হয়েছে। সাহায্যের জন্য সাপোর্টে যোগাযোগ করুন।"],
 "err.disabled":["Your account has been disabled.","আপনার অ্যাকাউন্ট নিষ্ক্রিয় করা হয়েছে।"],
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
 "err.title":["Please enter a title (at least 4 characters).","শিরোনাম দিন (কমপক্ষে ৪ অক্ষর)।"],
 "err.category":["Please select a category.","ক্যাটাগরি নির্বাচন করুন।"],
 "err.location":["Please select a location.","অবস্থান নির্বাচন করুন।"],
 "err.desc":["Please write a description (at least 10 characters).","বর্ণনা লিখুন (কমপক্ষে ১০ অক্ষর)।"],
 "err.message":["Please write a short message.","একটি ছোট মেসেজ লিখুন।"],
 "err.image":["Image is too large. Please choose a smaller image (max 400KB).","ছবিটি অনেক বড়। ছোট ছবি বাছাই করুন (সর্বোচ্চ ৪০০KB)।"],
 "err.self_quote":["You cannot request a quote on your own post.","নিজের পোস্টে কোটেশন চাওয়া যাবে না।"],
 "err.post_not_found":["Post not found.","পোস্টটি পাওয়া যায়নি।"],
 "err.role_not_allowed":["Your account type is not allowed to do this.","আপনার অ্যাকাউন্টের ধরন দিয়ে এটি করা যাবে না।"],
 "err.duplicate":["You already sent a quote for this post.","এই পোস্টে আপনি আগেই কোটেশন পাঠিয়েছেন।"],
 "err.post_closed":["This post is closed for new quotes.","নতুন কোটেশনের জন্য এই পোস্টটি বন্ধ।"],
 "err.quote_not_found":["Quote not found.","কোটেশনটি পাওয়া যায়নি।"],
 "err.not_pending":["This quote is no longer pending.","এই কোটেশনটি আর অপেক্ষমাণ নেই।"],
 "err.own_quote":["You cannot respond to your own quote.","নিজের কোটেশনে সাড়া দেওয়া যাবে না।"],
 "err.action":["Invalid action.","ভুল নির্দেশ।"],
 "err.self_conv":["You cannot message yourself.","নিজেকে মেসেজ পাঠানো যাবে না।"],
 "err.conv_not_found":["Conversation not found.","কথোপকথনটি পাওয়া যায়নি।"],
 "ok.sent":["Code sent!","কোড পাঠানো হয়েছে!"],
 "ok.verified":["Verified!","যাচাই হয়েছে!"],
 "dev.note":["Demo mode — your code: {c} (in production it is sent by SMS/email)","ডেমো মোড — আপনার কোড: {c} (প্রকৃত পরিবেশে এটি এসএমএস/ইমেইলে যাবে)"],
 "ui.loading":["Loading…","লোড হচ্ছে…"],

 /* marketplace states */
 "mp.emptyTitle":["No posts found","কোনো পোস্ট পাওয়া যায়নি"],
 "mp.emptySub":["Try changing your filters, or be the first to post here.","ফিল্টার বদলে দেখুন, অথবা এখানে প্রথম পোস্টটি আপনিই করুন।"],
 "mp.emptyLogin":["You'll need to sign in to create a post.","পোস্ট তৈরি করতে সাইন ইন করতে হবে।"],
 "mp.clearFilters":["Clear Filters","ফিল্টার মুছুন"],
 "mp.retry":["Retry","আবার চেষ্টা করুন"],
 "foot.about":["About","আমাদের সম্পর্কে"],
 "foot.contact":["Contact","যোগাযোগ"],
 "foot.privacy":["Privacy","গোপনীয়তা"],
 "foot.terms":["Terms","শর্তাবলি"],
 "nav.suppliersLand":["Suppliers","সরবরাহকারী"],
 "nav.oppsLand":["Opportunities","সুযোগ"],

 /* static info pages */
 "meta.about":["Ahoor — About","Ahoor — আমাদের সম্পর্কে"],
 "about.updated":["Last updated: August 2026","সর্বশেষ হালনাগাদ: আগস্ট ২০২৬"],
 "about.title":["About Ahoor","Ahoor সম্পর্কে"],
 "about.lead":["A B2B marketplace and opportunity network built for Bangladesh.","বাংলাদেশের জন্য তৈরি একটি B2B মার্কেটপ্লেস ও ব্যবসার সুযোগের নেটওয়ার্ক।"],
 "about.h1":["Who we are","আমরা কারা"],
 "about.p1":["Ahoor helps Bangladeshi businesses find each other. Buyers post what they need; suppliers and manufacturers post what they offer. Our smart matching surfaces the right opportunities to the right businesses — without endless searching.","Ahoor বাংলাদেশি ব্যবসাগুলোকে একে অপরকে খুঁজে পেতে সাহায্য করে। ক্রেতারা যা প্রয়োজন তা পোস্ট করেন; সরবরাহকারী ও প্রস্তুতকারকেরা যা অফার করেন তা পোস্ট করেন। আমাদের স্মার্ট ম্যাচিং সঠিক সুযোগগুলো সঠিক ব্যবসার কাছে পৌঁছে দেয় — অন্তহীন খোঁজাখুঁজি ছাড়াই।"],
 "about.h2":["What we do","আমরা যা করি"],
 "about.p2":["Businesses on Ahoor can post requirements and offers, receive and compare quotations, chat directly with potential partners, get matched with relevant opportunities, and track their performance through business analytics.","Ahoor-এ ব্যবসাগুলো প্রয়োজন ও অফার পোস্ট করতে পারে, কোটেশন পেতে ও তুলনা করতে পারে, সম্ভাব্য অংশীদারদের সাথে সরাসরি চ্যাট করতে পারে, উপযুক্ত সুযোগের সাথে ম্যাচ হতে পারে এবং বিজনেস অ্যানালিটিক্সের মাধ্যমে নিজেদের পারফরম্যান্স দেখতে পারে।"],
 "about.h3":["Who it's for","কাদের জন্য"],
 "about.p3":["Ahoor is for manufacturers, suppliers, wholesalers, exporters, importers, and bulk buyers across Bangladesh — from textiles and garments to agro products, jute, leather, packaging, and more.","Ahoor বাংলাদেশের প্রস্তুতকারক, সরবরাহকারী, পাইকারি বিক্রেতা, রপ্তানিকারক, আমদানিকারক ও পাইকারি ক্রেতাদের জন্য — টেক্সটাইল ও গার্মেন্টস থেকে শুরু করে কৃষি পণ্য, পাট, চামড়া, প্যাকেজিংসহ আরও অনেক খাতে।"],
 "about.h4":["Contact us","যোগাযোগ করুন"],
 "about.p4":["Questions or feedback? Reach us through the contact page — or sign in and use in-app messaging to talk to any business on the platform.","প্রশ্ন বা মতামত আছে? যোগাযোগ পৃষ্ঠার মাধ্যমে আমাদের জানান — অথবা সাইন ইন করে প্ল্যাটফর্মের যেকোনো ব্যবসার সাথে ইন-অ্যাপ মেসেজিংয়ে কথা বলুন।"],

 "meta.contact":["Ahoor — Contact","Ahoor — যোগাযোগ"],
 "contact.title":["Contact Us","যোগাযোগ করুন"],
 "contact.updated":["Last updated: August 2026","সর্বশেষ হালনাগাদ: আগস্ট ২০২৬"],
 "contact.lead":["We'd love to hear from you — questions, feedback, or partnership ideas.","আমরা আপনার কাছ থেকে শুনতে চাই — প্রশ্ন, মতামত বা অংশীদারিত্বের আইডিয়া।"],
 "contact.h1":["Email","ইমেইল"],
 "contact.p1":["For general questions and support, email us at munjirul000@gmail.com.","সাধারণ প্রশ্ন ও সাপোর্টের জন্য ইমেইল করুন: munjirul000@gmail.com"],
 "contact.h2":["Report a problem","সমস্যা জানান"],
 "contact.p2":["See something wrong on the platform — a suspicious post, an unfair quotation, or a bug? Sign in and use the Report option on any post or business profile.","প্ল্যাটফর্মে কিছু ভুল দেখলে — সন্দেহজনক পোস্ট, অসাধু কোটেশন বা কোনো ত্রুটি? সাইন ইন করে যেকোনো পোস্ট বা বিজনেস প্রোফাইলে রিপোর্ট অপশন ব্যবহার করুন।"],
 "contact.h3":["Response time","উত্তরের সময়"],
 "contact.p3":["We typically respond within 1–2 business days.","সাধারণত ১–২ কার্যদিবসের মধ্যে আমরা উত্তর দিই।"],

 "meta.privacy":["Ahoor — Privacy Policy","Ahoor — গোপনীয়তা নীতি"],
 "privacy.title":["Privacy Policy","গোপনীয়তা নীতি"],
 "privacy.updated":["Last updated: August 2026","সর্বশেষ হালনাগাদ: আগস্ট ২০২৬"],
 "privacy.lead":["This policy explains what information Ahoor collects and how we use it.","এই নীতিতে বলা হয়েছে Ahoor কী তথ্য সংগ্রহ করে এবং সেগুলো কীভাবে ব্যবহার করে।"],
 "privacy.h1":["Information we collect","আমরা যা সংগ্রহ করি"],
 "privacy.p1":["When you create an account we collect your name, email, phone number, and the business information you choose to add (business name, category, location, products, and similar details). We also store the posts, quotations, messages, and reports you create, plus basic usage events such as profile and post views.","অ্যাকাউন্ট তৈরি করার সময় আমরা আপনার নাম, ইমেইল, ফোন নম্বর এবং আপনি যে ব্যবসায়িক তথ্য যোগ করেন (ব্যবসার নাম, ক্যাটাগরি, অবস্থান, পণ্য ইত্যাদি) সংগ্রহ করি। আপনার তৈরি পোস্ট, কোটেশন, মেসেজ ও রিপোর্ট এবং প্রোফাইল/পোস্ট ভিউয়ের মতো মৌলিক ব্যবহারের তথ্যও আমরা সংরক্ষণ করি।"],
 "privacy.h2":["How we use it","কীভাবে ব্যবহার করি"],
 "privacy.p2":["Your information is used to run the platform: connecting you with relevant businesses, showing your posts and profile to other members, sending notifications and quotations, matching opportunities, and showing you your own analytics. We never invent or publish fake business data.","আপনার তথ্য প্ল্যাটফর্ম চালাতে ব্যবহৃত হয়: উপযুক্ত ব্যবসার সাথে যুক্ত করা, আপনার পোস্ট ও প্রোফাইল অন্য সদস্যদের দেখানো, নোটিফিকেশন ও কোটেশন পাঠানো, সুযোগ ম্যাচ করা এবং আপনার নিজের অ্যানালিটিক্স দেখানো। আমরা কখনো ভুয়া ব্যবসার তথ্য তৈরি করি না বা প্রকাশ করি না।"],
 "privacy.h3":["What we don't share","যা আমরা শেয়ার করি না"],
 "privacy.p3":["We do not sell your personal data. Your phone number and email are only visible to other members according to your own visibility settings. We never expose passwords, session tokens, or private analytics of other businesses.","আমরা আপনার ব্যক্তিগত তথ্য বিক্রি করি না। আপনার ফোন নম্বর ও ইমেইল শুধুমাত্র আপনার ভিজিবিলিটি সেটিংস অনুযায়ী অন্য সদস্যদের কাছে দৃশ্যমান হয়। আমরা কখনো পাসওয়ার্ড, সেশন টোকেন বা অন্য ব্যবসার ব্যক্তিগত অ্যানালিটিক্স প্রকাশ করি না।"],
 "privacy.h4":["Security","নিরাপত্তা"],
 "privacy.p4":["Passwords are stored as salted hashes, sessions use secure random tokens, and all account pages require login. As with any online service, please use a strong, unique password.","পাসওয়ার্ড সল্টেড হ্যাশ হিসেবে সংরক্ষিত থাকে, সেশনে সিকিউর র্যান্ডম টোকেন ব্যবহৃত হয় এবং সব অ্যাকাউন্ট পৃষ্ঠায় লগইন আবশ্যক। যেকোনো অনলাইন সেবার মতো, দয়া করে শক্তিশালী ও আলাদা পাসওয়ার্ড ব্যবহার করুন।"],
 "privacy.h5":["Your choices","আপনার পছন্দ"],
 "privacy.p5":["You can edit or remove your business information from your profile anytime. To close your account or ask questions about your data, contact us from the contact page.","আপনার প্রোফাইল থেকে যেকোনো সময় ব্যবসায়িক তথ্য সম্পাদনা বা মুছে ফেলতে পারেন। অ্যাকাউন্ট বন্ধ করতে বা আপনার ডেটা নিয়ে প্রশ্ন থাকলে যোগাযোগ পৃষ্ঠা থেকে আমাদের জানান।"],

 "meta.terms":["Ahoor — Terms of Service","Ahoor — ব্যবহারের শর্তাবলি"],
 "terms.title":["Terms of Service","ব্যবহারের শর্তাবলি"],
 "terms.updated":["Last updated: August 2026","সর্বশেষ হালনাগাদ: আগস্ট ২০২৬"],
 "terms.lead":["By using Ahoor you agree to these terms. Please read them carefully.","Ahoor ব্যবহার করে আপনি এই শর্তগুলো মেনে নিচ্ছেন। দয়া করে মন দিয়ে পড়ুন।"],
 "terms.h1":["Using the platform","প্ল্যাটফর্ম ব্যবহার"],
 "terms.p1":["Ahoor connects buyers and suppliers in Bangladesh. We provide the venue; the actual business dealings, negotiations, and payments happen between the parties themselves. Always verify the credibility of your business partners before entering into any agreement.","Ahoor বাংলাদেশের ক্রেতা ও সরবরাহকারীদের সংযুক্ত করে। আমরা শুধু প্ল্যাটফর্মটি দিই; প্রকৃত ব্যবসায়িক লেনদেন, আলোচনা ও পেমেন্ট পক্ষদ্বয়ের মধ্যে হয়। কোনো চুক্তিতে যাওয়ার আগে সর্বদা আপনার ব্যবসায়িক অংশীদারের বিশ্বাসযোগ্যতা যাচাই করুন।"],
 "terms.h2":["Accounts","অ্যাকাউন্ট"],
 "terms.p2":["You must provide accurate information when creating an account. You are responsible for keeping your login credentials safe and for everything done from your account.","অ্যাকাউন্ট তৈরি করার সময় সঠিক তথ্য দিতে হবে। আপনার লগইন তথ্য নিরাপদ রাখা এবং আপনার অ্যাকাউন্ট থেকে যা কিছু করা হয় তার দায়িত্ব আপনার।"],
 "terms.h3":["Acceptable use","গ্রহণযোগ্য ব্যবহার"],
 "terms.p3":["Do not post false or misleading business information, send spam, harass other members, or use the platform for anything unlawful. Posts, quotations, and messages should represent genuine business intent.","ভুয়া বা বিভ্রান্তিকর ব্যবসায়িক তথ্য পোস্ট করা, স্প্যাম পাঠানো, অন্য সদস্যদের হয়রানি করা বা কোনো অবৈধ কাজে প্ল্যাটফর্ম ব্যবহার করা যাবে না। পোস্ট, কোটেশন ও মেসেজ প্রকৃত ব্যবসায়িক উদ্দেশ্য প্রকাশ করবে।"],
 "terms.h4":["Reporting","রিপোর্টিং"],
 "terms.p4":["If you see a violation, report it through the Report option on the platform. We review reports and may suspend accounts that violate these terms.","কোনো লঙ্ঘন দেখলে প্ল্যাটফর্মের রিপোর্ট অপশনের মাধ্যমে জানান। আমরা রিপোর্ট পর্যালোচনা করি এবং শর্ত লঙ্ঘনকারী অ্যাকাউন্ট স্থগিত করতে পারি।"],
 "terms.h5":["Liability","দায়বদ্ধতা"],
 "terms.p5":["Ahoor is provided as-is. To the extent permitted by law, we are not liable for losses arising from transactions, communications, or decisions made between businesses on the platform.","Ahoor যেমন আছে তেমনই প্রদান করা হয়। আইন যতটুকু অনুমতি দেয়, প্ল্যাটফর্মে ব্যবসাগুলোর মধ্যে হওয়া লেনদেন, যোগাযোগ বা সিদ্ধান্ত থেকে উদ্ভূত ক্ষতির জন্য আমরা দায়ী নই।"],
 "terms.h6":["Changes","পরিবর্তন"],
 "terms.p6":["We may update these terms as the platform grows. The latest version will always be available on this page.","প্ল্যাটফর্ম বাড়ার সাথে সাথে আমরা এই শর্তাবলি হালনাগাদ করতে পারি। সর্বশেষ সংস্করণ সবসময় এই পৃষ্ঠায় থাকবে।"],

 /* suppliers / opportunities listing pages */
 "meta.suppliers":["Ahoor — Suppliers","Ahoor — সরবরাহকারী"],
 "sp.title":["Suppliers & Manufacturers","সরবরাহকারী ও প্রস্তুতকারক"],
 "sp.sub":["Browse supplier offers posted on Ahoor.","Ahoor-এ পোস্ট করা সরবরাহকারীদের অফার দেখুন।"],
 "sp.empty":["No supplier offers yet — be the first to post one.","এখনো কোনো সরবরাহকারীর অফার নেই — প্রথম অফারটি আপনিই দিন।"],
 "sp.market":["Open Marketplace","মার্কেটপ্লেস খুলুন"],
 "sp.join":["Join Ahoor","Ahoor-এ যোগ দিন"],
 "sp.postOffer":["Post an Offer","অফার পোস্ট করুন"],
 "sp.browseBuyers":["Browse Buyer Requirements","ক্রেতার প্রয়োজন দেখুন"],
 "meta.opps":["Ahoor — Opportunities","Ahoor — ব্যবসার সুযোগ"],
 "op.title":["All Business Opportunities","সব ব্যবসার সুযোগ"],
 "op.sub":["Buyer requirements and supplier offers posted on Ahoor.","Ahoor-এ পোস্ট করা ক্রেতার প্রয়োজন ও সরবরাহকারীর অফার।"],
 "op.empty":["No opportunities yet — be the first to post one.","এখনো কোনো সুযোগ নেই — প্রথম পোস্টটি আপনিই করুন।"],
 "op.market":["Open Marketplace","মার্কেটপ্লেস খুলুন"],
 "op.postReq":["Post a Requirement","প্রয়োজন পোস্ট করুন"]
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

/* ---------------- quotes & notifications dictionary ---------------- */
var Q_EXT = {
 "qt.sendQuote":["Send Quote","কোটেশন পাঠান"],
 "qt.reqQuote":["Request Quote","কোটেশন চান"],
 "qt.sendQuoteTitle":["Send Quote","কোটেশন পাঠান"],
 "qt.reqQuoteTitle":["Request Quote","কোটেশন চান"],
 "qt.forPost":["For post:","পোস্টের জন্য:"],
 "qt.priceUnit":["Price per unit","প্রতি একক দাম"],
 "qt.priceUnitPh":["e.g. ৳250 / pcs","যেমন: ৳২৫০ / পিস"],
 "qt.totalPrice":["Total price (auto-calculated)","মোট দাম (স্বয়ংক্রিয়)"],
 "qt.availQty":["Available quantity","পাওয়া যাবে পরিমাণ"],
 "qt.availQtyPh":["e.g. 1000","যেমন: ১০০০"],
 "qt.moq":["Minimum Order Quantity (optional)","ন্যূনতম অর্ডার পরিমাণ (ঐচ্ছিক)"],
 "qt.moqPh":["e.g. 100","যেমন: ১০০"],
 "qt.delivery":["Estimated delivery / production time","আনুমানিক ডেলিভারি / উৎপাদন সময়"],
 "qt.deliveryPh":["e.g. 10 days","যেমন: ১০ দিন"],
 "qt.valid":["Valid until (optional)","বৈধ থাকবে (ঐচ্ছিক)"],
 "qt.msg":["Message / Additional details","মেসেজ / অতিরিক্ত বিবরণ"],
 "qt.msgPhQuote":["We can manufacture premium cotton T-shirts according to your requirements.","আপনার প্রয়োজন অনুযায়ী প্রিমিয়াম কটন টি-শার্ট তৈরি করতে পারি।"],
 "qt.reqQty":["Required quantity","প্রয়োজনীয় পরিমাণ"],
 "qt.reqQtyPh":["e.g. 5000","যেমন: ৫০০০"],
 "qt.prefDel":["Preferred delivery date","পছন্দের ডেলিভারি তারিখ"],
 "qt.prefDelPh":["e.g. within 30 days","যেমন: ৩০ দিনের মধ্যে"],
 "qt.budget":["Budget (optional)","বাজেট (ঐচ্ছিক)"],
 "qt.budgetPh":["e.g. ৳1,250,000","যেমন: ৳১২,৫০,০০০"],
 "qt.msgPhReq":["I am interested in ordering 5,000 pcs. Please send me your best quotation.","আমি ৫,০০০ পিস অর্ডার করতে আগ্রহী। অনুগ্রহ করে আপনার সেরা কোটেশন পাঠান।"],
 "qt.send":["SEND QUOTE","কোটেশন পাঠান"],
 "qt.sendReq":["SEND REQUEST","অনুরোধ পাঠান"],
 "qt.sending":["Sending…","পাঠানো হচ্ছে…"],
 "qt.sentOk":["Quote sent successfully.","কোটেশন সফলভাবে পাঠানো হয়েছে।"],
 "qt.reqSentOk":["Quote request sent successfully.","কোটেশন অনুরোধ সফলভাবে পাঠানো হয়েছে।"],
 "qt.statusPending":["Pending","অপেক্ষমাণ"],
 "qt.statusAccepted":["Accepted","গৃহীত"],
 "qt.statusRejected":["Rejected","প্রত্যাখ্যাত"],
 "qt.statusWithdrawn":["Withdrawn","প্রত্যাহার"],
 "qt.accept":["Accept Quote","কোটেশন গ্রহণ করুন"],
 "qt.reject":["Reject Quote","কোটেশন প্রত্যাখ্যান করুন"],
 "qt.contact":["Contact Supplier","সরবরাহকারীর সাথে যোগাযোগ"],
 "qt.viewSupplier":["View Supplier","সরবরাহকারী দেখুন"],
 "qt.withdraw":["Withdraw","প্রত্যাহার করুন"],
 "qt.acceptedOk":["Quote accepted.","কোটেশন গৃহীত হয়েছে।"],
 "qt.rejectedOk":["Quote rejected.","কোটেশন প্রত্যাখ্যান করা হয়েছে।"],
 "qt.withdrawnOk":["Quote withdrawn.","কোটেশন প্রত্যাহার করা হয়েছে।"],
 "qt.sentQuotes":["My Sent Quotes","আমার পাঠানো কোটেশন"],
 "qt.receivedQuotes":["Received Quotes","প্রাপ্ত কোটেশন"],
 "qt.noSent":["You haven't sent any quotes yet.","আপনি এখনো কোনো কোটেশন পাঠাননি।"],
 "qt.noReceived":["No quotes received yet.","এখনো কোনো কোটেশন আসেনি।"],
 "qt.pricePer":["Price / unit","দাম / একক"],
 "qt.total":["Total","মোট"],
 "qt.roleBlocked":["Only suppliers can send quotes on buyer posts.","ক্রেতার পোস্টে শুধু সরবরাহকারীরাই কোটেশন পাঠাতে পারেন।"],
 "qt.roleBlockedReq":["Only buyers can request quotes on supplier posts.","সরবরাহকারীর পোস্টে শুধু ক্রেতারাই কোটেশন চাইতে পারেন।"],
 "qt.loginFirst":["Please sign in to continue.","চালিয়ে যেতে সাইন ইন করুন।"],
 "qt.alreadySent":["You already sent a quote for this post.","এই পোস্টে আপনি আগেই কোটেশন পাঠিয়েছেন।"],
 "qt.postClosed":["This post is closed.","এই পোস্টটি বন্ধ।"],
 "nt.unread":["Notifications","নোটিফিকেশন"],
 "nt.markAll":["Mark all as read","সব পঠিত করুন"],
 "nt.empty":["No notifications yet.","এখনো কোনো নোটিফিকেশন নেই।"],
 "nt.quote_received":["You received a new quote from {name}.","{name} থেকে একটি নতুন কোটেশন পেয়েছেন।"],
 "nt.request_received":["You received a new quote request from {name}.","{name} থেকে একটি নতুন কোটেশন অনুরোধ পেয়েছেন।"],
 "nt.quote_accepted":["Your quote was accepted by {name}.","{name} আপনার কোটেশন গ্রহণ করেছেন।"],
 "nt.quote_rejected":["Your quote was not accepted by {name}.","{name} আপনার কোটেশন গ্রহণ করেননি।"],
 "nt.message_received":["You received a new message from {name}.","{name} থেকে একটি নতুন মেসেজ পেয়েছেন।"],
 "nt.title":["Notifications","নোটিফিকেশন"],
 "nt.all":["All","সব"],
 "nt.unreadTab":["Unread","অপঠিত"],
 "nt.readTab":["Read","পঠিত"],
 "nt.viewAll":["View all","সব দেখুন"],
 "nt.delete":["Delete","মুছে ফেলুন"],
 "nt.deleted":["Notification deleted.","নোটিফিকেশন মুছে ফেলা হয়েছে।"],
 "nt.noUnread":["No unread notifications.","কোনো অপঠিত নোটিফিকেশন নেই।"],
 "nt.photo":["Photo","ছবি"],
 "rp.title":["Report","রিপোর্ট"],
 "rp.reason":["Reason","কারণ"],
 "rp.reasonPh":["Describe the issue…","সমস্যাটি বর্ণনা করুন…"],
 "rp.sent":["Report submitted. Thank you for keeping Ahoor safe.","রিপোর্ট জমা হয়েছে। Ahoor নিরাপদ রাখতে সাহায্য করার জন্য ধন্যবাদ।"],
 "rp.reportBiz":["Report Business","ব্যবসাটি রিপোর্ট করুন"],
 "rp.reportPost":["Report Post","পোস্টটি রিপোর্ট করুন"],
 "rp.errShort":["Please describe the issue (at least 5 characters).","সমস্যাটি বর্ণনা করুন (কমপক্ষে ৫ অক্ষর)।"],
 "vr.title":["Verification","যাচাইকরণ"],
 "vr.apply":["Apply for Verification","যাচাইকরণের জন্য আবেদন করুন"],
 "vr.pending":["Verification pending review","যাচাইকরণ পর্যালোচনাধীন"],
 "vr.verified":["Verified Business","যাচাইকৃত ব্যবসা"],
 "vr.rejected":["Verification rejected","যাচাইকরণ প্রত্যাখ্যাত"],
 "vr.applied":["Verification request submitted!","যাচাইকরণ অনুরোধ জমা হয়েছে!"],
 "vr.noBiz":["Complete your business profile first.","আগে আপনার ব্যবসার প্রোফাইল সম্পূর্ণ করুন।"],
 "vr.already":["Request already submitted or verified.","অনুরোধ ইতিমধ্যে জমা হয়েছে বা যাচাইকৃত।"],
 "vr.status.unverified":["Unverified","অযাচাইকৃত"],
 "vr.status.pending":["Pending Review","পর্যালোচনাধীন"],
 "vr.status.verified":["Verified","যাচাইকৃত"],
 "vr.status.rejected":["Rejected","প্রত্যাখ্যাত"],
 "vr.verifiedBadge":["Verified Business","যাচাইকৃত ব্যবসা"],
 "vr.applyTitle":["Apply for Business Verification","ব্যবসা যাচাইকরণের জন্য আবেদন করুন"],
 "vr.applySub":["Submit your business information and supporting documents for review.","পর্যালোচনার জন্য আপনার ব্যবসার তথ্য ও সহায়ক নথি জমা দিন।"],
 "vr.formInfo":["Business Information","ব্যবসার তথ্য"],
 "vr.formDocs":["Supporting Documents","সহায়ক নথি"],
 "vr.step1":["Step 1: Business Information","ধাপ ১: ব্যবসার তথ্য"],
 "vr.step2":["Step 2: Supporting Documents","ধাপ ২: সহায়ক নথি"],
 "vr.step3":["Step 3: Under Review","ধাপ ৩: পর্যালোচনাধীন"],
 "vr.tradeLicense":["Trade License (optional)","ট্রেড লাইসেন্স (ঐচ্ছিক)"],
 "vr.regDoc":["Business Registration (optional)","ব্যবসা নিবন্ধন (ঐচ্ছিক)"],
 "vr.otherDoc":["Other Business Proof (optional)","অন্যান্য প্রমাণ (ঐচ্ছিক)"],
 "vr.choose":["Choose file","ফাইল বাছাই করুন"],
 "vr.fileChosen":["{name} selected","{name} নির্বাচিত হয়েছে"],
 "vr.removeFile":["Remove","সরান"],
 "vr.docHint":["PDF, JPG or PNG — max 1.5MB each","PDF, JPG বা PNG — প্রতিটি সর্বোচ্চ ১.৫MB"],
 "vr.submit":["Submit Application","আবেদন জমা দিন"],
 "vr.submitting":["Submitting…","জমা হচ্ছে…"],
 "vr.submitted":["Application submitted! Your verification request is under review.","আবেদন জমা হয়েছে! আপনার যাচাইকরণ অনুরোধ পর্যালোচনাধীন।"],
 "vr.underReview":["Your application is under review.","আপনার আবেদন পর্যালোচনাধীন।"],
 "vr.reviewNote":["Our team is reviewing your documents. You will be notified when the review is complete.","আমাদের টিম আপনার নথি পর্যালোচনা করছে। পর্যালোচনা শেষ হলে আপনাকে জানানো হবে।"],
 "vr.rejectedTitle":["Verification Rejected","যাচাইকরণ প্রত্যাখ্যাত"],
 "vr.rejectedReason":["Reason: {reason}","কারণ: {reason}"],
 "vr.reapply":["Update Information & Apply Again","তথ্য আপডেট করে আবার আবেদন করুন"],
 "vr.withdraw":["Withdraw Application","আবেদন প্রত্যাহার করুন"],
 "vr.withdrawn":["Application withdrawn.","আবেদন প্রত্যাহার করা হয়েছে।"],
 "vr.docTypeErr":["Only PDF, JPG or PNG files are allowed.","শুধু PDF, JPG বা PNG ফাইল অনুমোদিত।"],
 "vr.docSizeErr":["File too large (max 1.5MB).","ফাইল অনেক বড় (সর্বোচ্চ ১.৫MB)।"],
 "vr.needBusiness":["Complete your business profile before applying.","আবেদনের আগে আপনার ব্যবসার প্রোফাইল সম্পূর্ণ করুন।"],
 "vr.myStatus":["Verification Status","যাচাইকরণ স্ট্যাটাস"],
 "vr.docsPrivate":["Documents are private — only Ahoor admins can view them.","নথিগুলো ব্যক্তিগত — শুধু Ahoor অ্যাডমিনরা দেখতে পারেন।"],
 "vr.viewRequests":["View verification requests","যাচাইকরণ অনুরোধ দেখুন"],
 "vr.approvedToast":["Your business has been verified!","আপনার ব্যবসা যাচাইকৃত হয়েছে!"],
 "vr.rejectedToast":["Your verification request was rejected.","আপনার যাচাইকরণ অনুরোধ প্রত্যাখ্যাত হয়েছে।"],
 "nt.verification_submitted":["Your verification request is under review.","আপনার যাচাইকরণ অনুরোধ পর্যালোচনাধীন।"],
 "nt.verification_approved":["Your business has been verified.","আপনার ব্যবসা যাচাইকৃত হয়েছে।"],
 "nt.verification_rejected":["Your verification request was rejected.","আপনার যাচাইকরণ অনুরোধ প্রত্যাখ্যাত হয়েছে।"],
 "an.title":["Business Insights","ব্যবসায়িক ইনসাইটস"],
 "an.sub":["Real analytics from your Ahoor activity","আপনার Ahoor কার্যকলাপের আসল পরিসংখ্যান"],
 "an.businessInsights":["Business Insights","ব্যবসায়িক ইনসাইটস"],
 "an.viewFull":["View Full Analytics","সম্পূর্ণ অ্যানালিটিক্স দেখুন"],
 "an.period7":["Last 7 Days","শেষ ৭ দিন"],
 "an.period30":["Last 30 Days","শেষ ৩০ দিন"],
 "an.period90":["Last 90 Days","শেষ ৯০ দিন"],
 "an.periodAll":["All Time","সব সময়"],
 "an.profileViews":["Profile Views","প্রোফাইল দেখা"],
 "an.postViews":["Post Views","পোস্ট দেখা"],
 "an.messagesReceived":["Messages Received","প্রাপ্ত মেসেজ"],
 "an.messagesSent":["Messages Sent","পাঠানো মেসেজ"],
 "an.quotesReceived":["Quotes Received","প্রাপ্ত কোটেশন"],
 "an.requestsReceived":["Quote Requests","কোটেশন অনুরোধ"],
 "an.quotesSent":["Quotes Sent","পাঠানো কোটেশন"],
 "an.acceptedQuotes":["Accepted Quotes","গৃহীত কোটেশন"],
 "an.rejectedQuotes":["Rejected Quotes","প্রত্যাখ্যাত কোটেশন"],
 "an.activePosts":["Active Posts","সক্রিয় পোস্ট"],
 "an.savedOpps":["Saved Opportunities","সংরক্ষিত সুযোগ"],
 "an.newMatches":["New Matches","নতুন ম্যাচ"],
 "an.postPerformance":["Post Performance","পোস্টের পারফরম্যান্স"],
 "an.quotePerformance":["Quote Performance","কোটেশনের পারফরম্যান্স"],
 "an.messaging":["Messaging Activity","মেসেজিং কার্যকলাপ"],
 "an.matching":["Matching Activity","ম্যাচিং কার্যকলাপ"],
 "an.recentActivity":["Recent Activity","সাম্প্রতিক কার্যকলাপ"],
 "an.post":["Post","পোস্ট"],
 "an.views":["Views","দেখা"],
 "an.quotes":["Quotes","কোটেশন"],
 "an.requests":["Requests","অনুরোধ"],
 "an.saves":["Saves","সংরক্ষণ"],
 "an.insights":["Insights","ইনসাইটস"],
 "an.noData":["Not enough data yet.","এখনো পর্যাপ্ত ডেটা নেই।"],
 "an.noPosts":["You haven't posted anything in this period.","এই সময়ে আপনি কোনো পোস্ট করেননি।"],
 "an.noActivity":["No activity in this period yet.","এই সময়ে কোনো কার্যকলাপ নেই।"],
 "an.profileNote":["Your profile received {n} view(s) in this period.","এই সময়ে আপনার প্রোফাইল {n} বার দেখা হয়েছে।"],
 "an.postNote":["Your posts received {n} view(s) in this period.","এই সময়ে আপনার পোস্ট {n} বার দেখা হয়েছে।"],
 "an.sentLabel":["Sent","পাঠানো"],
 "an.receivedLabel":["Received","প্রাপ্ত"],
 "an.acceptedLabel":["Accepted","গৃহীত"],
 "an.rejectedLabel":["Rejected","প্রত্যাখ্যাত"],
 "an.act.post_created":["New post created","নতুন পোস্ট তৈরি"],
 "an.act.quote_sent":["Sent a quote","কোটেশন পাঠানো হয়েছে"],
 "an.act.quote_received":["Received a quote","কোটেশন প্রাপ্ত"],
 "an.act.msg_sent":["Sent a message","মেসেজ পাঠানো হয়েছে"],
 "an.act.msg_received":["Received a message","মেসেজ প্রাপ্ত"],
 "an.viewsInsights":["View Insights","ইনসাইটস দেখুন"],
 "an.loading":["Loading analytics…","অ্যানালিটিক্স লোড হচ্ছে…"],
 "an.error":["Could not load analytics.","অ্যানালিটিক্স লোড করা যায়নি।"],
 "ad.promote":["Make Admin","অ্যাডমিন করুন"],
 "ad.demote":["Remove Admin","অ্যাডমিন সরান"],
 "ad.confirmPromote":["Promote this user to Admin? They will get full access to the admin panel.","এই ইউজারকে অ্যাডমিন করবেন? তারা অ্যাডমিন প্যানেলে সম্পূর্ণ অ্যাক্সেস পাবে।"],
 "ad.confirmDemote":["Remove admin access from this user?","এই ইউজারের অ্যাডমিন অ্যাক্সেস সরাবেন?"],
 "ad.roleDone":["Admin role updated.","অ্যাডমিন ভূমিকা আপডেট হয়েছে।"],
 "mt.title":["Matched Opportunities","ম্যাচকৃত সুযোগ"],
 "mt.sub":["Opportunities matched to your business profile","আপনার ব্যবসার প্রোফাইলের সাথে মিলে যাওয়া সুযোগ"],
 "mt.explain":["Matched based on your business profile and products.","আপনার ব্যবসার প্রোফাইল ও পণ্যের ভিত্তিতে ম্যাচ করা হয়েছে।"],
 "mt.best":["Best Matches","সেরা ম্যাচ"],
 "mt.buyerOpps":["Buyer Opportunities","ক্রেতার সুযোগ"],
 "mt.supplierOpps":["Supplier Opportunities","সরবরাহকারীর সুযোগ"],
 "mt.saved":["Saved Opportunities","সংরক্ষিত সুযোগ"],
 "mt.recommended":["Recommended for You","আপনার জন্য সুপারিশকৃত"],
 "mt.newMatches":["{n} New Matches","{n}টি নতুন ম্যাচ"],
 "mt.viewAll":["View All Matches","সব ম্যাচ দেখুন"],
 "mt.level.high":["High Match","উচ্চ ম্যাচ"],
 "mt.level.medium":["Medium Match","মাঝারি ম্যাচ"],
 "mt.level.low":["Low Match","কম ম্যাচ"],
 "mt.levelAll":["All levels","সব স্তর"],
 "mt.catAll":["All Categories","সব ক্যাটাগরি"],
 "mt.locAll":["All Locations","সব জেলা"],
 "mt.viewBusiness":["View Business","ব্যবসা দেখুন"],
 "mt.viewOffer":["View Offer","অফার দেখুন"],
 "mt.viewRequirement":["View Requirement","প্রয়োজন দেখুন"],
 "mt.message":["Message","মেসেজ"],
 "mt.save":["Save","সংরক্ষণ"],
 "mt.savedYes":["Saved","সংরক্ষিত"],
 "mt.remove":["Remove","সরান"],
 "mt.savedOk":["Opportunity saved.","সুযোগটি সংরক্ষিত হয়েছে।"],
 "mt.removedOk":["Opportunity removed from saved.","সংরক্ষিত থেকে সুযোগটি সরানো হয়েছে।"],
 "mt.noMatches":["No matching opportunities right now. Check back soon.","এখন কোনো ম্যাচিং সুযোগ নেই। কিছুক্ষণ পর আবার দেখুন।"],
 "mt.noSaved":["You haven't saved any opportunities yet.","আপনি এখনো কোনো সুযোগ সংরক্ষণ করেননি।"],
 "mt.openMarket":["Browse Marketplace","মার্কেটপ্লেস দেখুন"],
 "nt.opportunity_match":["A new business opportunity may match what you offer.","একটি নতুন ব্যবসার সুযোগ আপনার অফারের সাথে মিলতে পারে।"],
 "nt.quote_withdrawn":["A quote was withdrawn.","একটি কোটেশন প্রত্যাহার করা হয়েছে।"],
 "nt.onPost":["on","এর জন্য"],
 "nt.justNow":["just now","এইমাত্র"],
 "nt.timeAgo":["{m} min ago","{m} মিনিট আগে"],
 "nt.hoursAgo":["{h} hr ago","{h} ঘণ্টা আগে"],
 "bp.title":["Business Profile","ব্যবসায়িক প্রোফাইল"],
 "bp.myTitle":["My Business Profile","আমার ব্যবসায়িক প্রোফাইল"],
 "bp.complete":["Profile Completion","প্রোফাইল সম্পূর্ণতা"],
 "bp.pct":["{p}% Complete","{p}% সম্পূর্ণ"],
 "bp.sectionBasic":["Basic Information","মৌলিক তথ্য"],
 "bp.bizType":["Business Type","ব্যবসার ধরন"],
 "bp.selBizType":["Select business type…","ব্যবসার ধরন নির্বাচন করুন…"],
 "bp.contactPerson":["Contact Person Name","যোগাযোগকারী ব্যক্তির নাম"],
 "bp.sectionLoc":["Location","অবস্থান"],
 "bp.division":["Division","বিভাগ"],
 "bp.selDivision":["Select division…","বিভাগ নির্বাচন করুন…"],
 "bp.city":["City / Area","শহর / এলাকা"],
 "bp.cityPh":["e.g. Mirpur, Dhaka","যেমন: মিরপুর, ঢাকা"],
 "bp.address":["Full Business Address (optional)","সম্পূর্ণ ব্যবসার ঠিকানা (ঐচ্ছিক)"],
 "bp.addressPh":["House, road, area…","বাসা, রোড, এলাকা…"],
 "bp.sectionDetails":["Business Details","ব্যবসার বিবরণ"],
 "bp.products":["Products / Services","পণ্য / সেবা"],
 "bp.productsPh":["e.g. T-Shirts, Hoodies, Polo Shirts","যেমন: টি-শার্ট, হুডি, পোলো শার্ট"],
 "bp.moq":["Minimum Order Quantity (MOQ)","ন্যূনতম অর্ডার পরিমাণ (MOQ)"],
 "bp.moqPh":["e.g. 100 pcs","যেমন: ১০০ পিস"],
 "bp.capacity":["Production Capacity","উৎপাদন ক্ষমতা"],
 "bp.capacityPh":["e.g. 50,000 pcs per month","যেমন: মাসে ৫০,০০০ পিস"],
 "bp.employees":["Number of Employees","কর্মচারীর সংখ্যা"],
 "bp.employeesPh":["e.g. 50","যেমন: ৫০"],
 "bp.years":["Years in Business","ব্যবসায়ের বছর"],
 "bp.yearsPh":["e.g. 5","যেমন: ৫"],
 "bp.sectionContact":["Contact Information","যোগাযোগের তথ্য"],
 "bp.bizPhone":["Business Phone Number","ব্যবসার ফোন নম্বর"],
 "bp.bizEmail":["Business Email","ব্যবসার ইমেইল"],
 "bp.website":["Website (optional)","ওয়েবসাইট (ঐচ্ছিক)"],
 "bp.websitePh":["https://yourbusiness.com","https://yourbusiness.com"],
 "bp.facebook":["Facebook Page (optional)","ফেসবুক পেজ (ঐচ্ছিক)"],
 "bp.facebookPh":["facebook.com/yourbusiness","facebook.com/yourbusiness"],
 "bp.sectionPrivacy":["Privacy Settings","গোপনীয়তা সেটিংস"],
 "bp.phoneVis":["Phone visibility","ফোন নম্বর দেখা যাবে"],
 "bp.emailVis":["Email visibility","ইমেইল দেখা যাবে"],
 "bp.visPublic":["Public","মুক্ত"],
 "bp.visMembers":["Only logged-in users","শুধু লগইন করা ইউজার"],
 "bp.visHidden":["Hidden","লুকানো"],
 "bp.save":["Save Business Profile","ব্যবসায়িক প্রোফাইল সেভ করুন"],
 "bp.saving":["Saving…","সেভ হচ্ছে…"],
 "bp.saved":["Business profile saved successfully!","ব্যবসায়িক প্রোফাইল সফলভাবে সেভ হয়েছে!"],
 "bp.edit":["Edit Business Profile","ব্যবসায়িক প্রোফাইল সম্পাদনা করুন"],
 "bp.viewPublic":["View Public Profile","পাবলিক প্রোফাইল দেখুন"],
 "bp.suggest":["Complete your business profile to increase trust and help relevant businesses understand what you offer.","ব্যবসায়িক প্রোফাইল সম্পূর্ণ করুন — এতে আস্থা বাড়বে এবং উপযুক্ত ব্যবসাগুলো আপনার অফার বুঝতে পারবে।"],
 "bp.publicTitle":["Business Profile","ব্যবসায়িক প্রোফাইল"],
 "bp.about":["About","সম্পর্কে"],
 "bp.details":["Business Details","ব্যবসার বিবরণ"],
 "bp.opps":["Active Opportunities","সক্রিয় সুযোগ"],
 "bp.noOpps":["No active opportunities right now.","এখন কোনো সক্রিয় সুযোগ নেই।"],
 "bp.contact":["Contact Business","ব্যবসার সাথে যোগাযোগ"],
 "bp.viewOpps":["View Opportunities","সুযোগ দেখুন"],
 "bp.contactTitle":["Contact","যোগাযোগ"],
 "bp.noContact":["This business has not shared contact information.","এই ব্যবসাটি যোগাযোগের তথ্য শেয়ার করেনি।"],
 "bp.loginToContact":["Sign in to view contact information.","যোগাযোগের তথ্য দেখতে সাইন ইন করুন।"],
 "bp.verif.basic":["Basic Profile","মৌলিক প্রোফাইল"],
 "bp.verif.verified":["Verified","যাচাইকৃত"],
 "bp.postBanner":["Tip: complete your business profile to increase trust before posting.","টিপ: পোস্ট করার আগে ব্যবসায়িক প্রোফাইল সম্পূর্ণ করুন — এতে আস্থা বাড়বে।"],
 "bp.backMarket":["Back to Marketplace","মার্কেটপ্লেসে ফিরুন"],
 "bp.notFound":["Business profile not found.","ব্যবসায়িক প্রোফাইল পাওয়া যায়নি।"],
 "bp.role.buyer":["Buyer","ক্রেতা"],
 "bp.role.supplier":["Supplier / Manufacturer","সরবরাহকারী / প্রস্তুতকারক"],
 "bp.role.both":["Buyer & Supplier","ক্রেতা ও সরবরাহকারী"],
 "ms.title":["Messages","মেসেজ"],
 "ms.sub":["Business conversations","ব্যবসায়িক কথোপকথন"],
 "ms.noConv":["No conversations yet","এখনো কোনো কথোপকথন নেই"],
 "ms.noConvD":["Message a business from their profile or a marketplace post to start.","কোনো ব্যবসার প্রোফাইল বা মার্কেটপ্লেস পোস্ট থেকে মেসেজ পাঠিয়ে শুরু করুন।"],
 "ms.startChat":["Start the conversation","কথোপকথন শুরু করুন"],
 "ms.startChatD":["Send a message to discuss requirements, pricing, or samples.","প্রয়োজন, দাম বা নমুনা নিয়ে আলোচনা করতে মেসেজ পাঠান।"],
 "ms.typeMsg":["Write a message…","মেসেজ লিখুন…"],
 "ms.send":["Send","পাঠান"],
 "ms.attach":["Attach image","ছবি যুক্ত করুন"],
 "ms.removeImg":["Remove image","ছবি সরান"],
 "ms.you":["You","আপনি"],
 "ms.back":["← Back to conversations","← কথোপকথনে ফিরুন"],
 "ms.loading":["Loading…","লোড হচ্ছে…"],
 "ms.sendError":["Could not send message. Please try again.","মেসেজ পাঠানো যায়নি। আবার চেষ্টা করুন।"],
 "ms.loadError":["Could not load messages.","মেসেজ লোড করা যায়নি।"],
 "ms.imageTooBig":["Image is too large (max 1.5MB).","ছবিটি অনেক বড় (সর্বোচ্চ ১.৫MB)।"],
 "ms.imageType":["Only JPG, PNG or WEBP images are allowed.","শুধু JPG, PNG বা WEBP ছবি অনুমোদিত।"],
 "ms.viewImage":["View full image","পুরো ছবি দেখুন"],
 "ms.close":["Close","বন্ধ করুন"],
 "ms.newChat":["Message","মেসেজ"],
 "ms.unreadBadge":["Unread","অপঠিত"],
 "ms.justNow":["just now","এইমাত্র"],
 "ms.minAgo":["{m} min","{m} মি"],
 "ms.hrAgo":["{h} hr","{h} ঘ"],
 "ms.dayAgo":["{d} d","{d} দিন"],
 "ms.photo":["Photo","ছবি"],
 "ms.connecting":["Connecting…","সংযুক্ত হচ্ছে…"]
};
for (var k in Q_EXT) { D[k] = Q_EXT[k]; }

/* ---------------- marketplace dictionary extension ---------------- */
var EXT = {
 "nav.home":["Home","হোম"],
 "nav.join":["Join Ahoor","Ahoor-এ যোগ দিন"],
 "nav.market":["Marketplace","মার্কেটপ্লেস"],
 "nav.dash":["Dashboard","ড্যাশবোর্ড"],
 "bp.sub":["Help the right businesses find you.","সঠিক ব্যবসাগুলো যেন আপনাকে খুঁজে পায়, তা নিশ্চিত করুন।"],
 "qt.status":["Status","স্ট্যাটাস"],
 "ad.search":["Search","খুঁজুন"],
 "mp.title":["Ahoor Marketplace","Ahoor মার্কেটপ্লেস"],
 "mp.sub":["Buyer requirements & supplier offers across Bangladesh","সারাদেশের ক্রেতার প্রয়োজন ও সরবরাহকারীর অফার"],
 "mp.tabAll":["All","সব"],
 "mp.tabBuyer":["Buyer Requirements","ক্রেতার প্রয়োজন"],
 "mp.tabSupplier":["Supplier Products","সরবরাহকারীর পণ্য"],
 "mp.searchPh":["Search products, requirements…","পণ্য বা প্রয়োজন খুঁজুন…"],
 "mp.catAll":["All Categories","সব ক্যাটাগরি"],
 "mp.locAll":["All Locations","সব জেলা"],
 "mp.empty":["No posts found. Try changing filters.","কোনো পোস্ট পাওয়া যায়নি। ফিল্টার বদলে দেখুন।"],
 "mp.newPost":["Create Post","নতুন পোস্ট"],
 "mp.badgeBuyer":["BUYER REQUEST","ক্রেতার অনুরোধ"],
 "mp.badgeSupplier":["SUPPLIER OFFER","সরবরাহকারীর অফার"],
 "mp.open":["Open","খোলা"],
 "mp.closed":["Closed","বন্ধ"],
 "mp.getQuotes":["Get Quotes","কোটেশন পান"],
 "mp.reqQuote":["Request Quote","কোটেশন চান"],
 "mp.postedBy":["Posted by","পোস্ট করেছেন"],
 "mp.postedOn":["Posted on","পোস্টের তারিখ"],
 "mp.loginNeeded":["Please sign in to continue.","চালিয়ে যেতে সাইন ইন করুন।"],
 "mp.quoteSent":["Your quote request was sent!","আপনার কোটেশন অনুরোধ পাঠানো হয়েছে!"],
 "mp.qty":["Quantity","পরিমাণ"],
 "mp.moq":["MOQ","MOQ"],
 "mp.price":["Price","দাম"],
 "mp.budget":["Budget","বাজেট"],
 "mp.contactPrice":["Contact for Price","দামের জন্য যোগাযোগ করুন"],
 "mp.deadline":["Deadline","সময়সীমা"],
 "mp.quoteMsg":["Your message","আপনার মেসেজ"],
 "mp.quoteMsgPh":["e.g. We can supply at ৳240/pcs, delivery 12 days","যেমন: আমরা ৳২৪০/পিসে সরবরাহ করতে পারি, ডেলিভারি ১২ দিন"],
 "mp.send":["Send","পাঠান"],
 "mp.cancel":["Cancel","বাতিল"],

 "pp.title":["Complete Your Business Profile","আপনার ব্যবসার প্রোফাইল সম্পূর্ণ করুন"],
 "pp.sub":["Help the right businesses find you.","সঠিক ব্যবসাগুলো যেন আপনাকে খুঁজে পায়।"],
 "pp.role":["Business Role","ব্যবসার ভূমিকা"],
 "pp.roleBuyer":["Buyer","ক্রেতা"],
 "pp.roleSupplier":["Supplier / Manufacturer","সরবরাহকারী / প্রস্তুতকারক"],
 "pp.roleBoth":["Both","দুটোই"],
 "pp.name":["Full Name","সম্পূর্ণ নাম"],
 "pp.biz":["Business Name","ব্যবসার নাম"],
 "pp.bizPh":["e.g. Rahim Garments","যেমন: রহিম গার্মেন্টস"],
 "pp.phone":["Phone Number","মোবাইল নম্বর"],
 "pp.district":["District / Location","জেলা / অবস্থান"],
 "pp.cat":["Business Category","ব্যবসার ক্যাটাগরি"],
 "pp.desc":["Short Business Description","সংক্ষিপ্ত ব্যবসা বর্ণনা"],
 "pp.descPh":["What do you make, supply, or buy?","আপনি কী তৈরি করেন, সরবরাহ করেন বা কিনে থাকেন?"],
 "pp.image":["Profile Image / Company Logo (optional)","প্রোফাইল ছবি / কোম্পানি লোগো (ঐচ্ছিক)"],
 "pp.upload":["Choose image","ছবি বাছাই করুন"],
 "pp.removeImg":["Remove","মুছে ফেলুন"],
 "pp.save":["Save Profile","প্রোফাইল সেভ করুন"],
 "pp.saving":["Saving…","সেভ হচ্ছে…"],
 "pp.saved":["Profile saved successfully!","প্রোফাইল সফলভাবে সেভ হয়েছে!"],
 "pp.done":["Go to Dashboard","ড্যাশবোর্ডে যান"],
 "pp.required":["Please fill in the required fields.","অনুগ্রহ করে প্রয়োজনীয় ঘরগুলো পূরণ করুন।"],
 "pp.skip":["Skip for now","এখনই না"],
 "pp.skipNote":["You can complete your profile anytime from the dashboard.","ড্যাশবোর্ড থেকে যেকোনো সময় প্রোফাইল সম্পূর্ণ করতে পারবেন।"],

 "pt.titleNew":["Create New Post","নতুন পোস্ট তৈরি করুন"],
 "pt.titleEdit":["Edit Post","পোস্ট সম্পাদনা করুন"],
 "pt.sub":["Share your requirement or offer with the marketplace","মার্কেটপ্লেসে আপনার প্রয়োজন বা অফার শেয়ার করুন"],
 "pt.kind":["Post Type","পোস্টের ধরন"],
 "pt.kindBuyer":["I want to buy","আমি কিনতে চাই"],
 "pt.kindSupplier":["I want to sell","আমি বিক্রি করতে চাই"],
 "pt.title":["Title","শিরোনাম"],
 "pt.titleBuyerPh":["e.g. Need 1000 PCS Premium Cotton T-Shirts","যেমন: ১০০০ পিস প্রিমিয়াম কটন টি-শার্ট প্রয়োজন"],
 "pt.titleSupplierPh":["e.g. Premium Cotton T-Shirts — Custom Printing","যেমন: প্রিমিয়াম কটন টি-শার্ট — কাস্টম প্রিন্টিং"],
 "pt.category":["Category","ক্যাটাগরি"],
 "pt.qty":["Quantity / Capacity","পরিমাণ / ক্ষমতা"],
 "pt.qtyPh":["e.g. 1000","যেমন: ১০০০"],
 "pt.unit":["Unit","একক"],
 "pt.budget":["Budget (optional)","বাজেট (ঐচ্ছিক)"],
 "pt.budgetPh":["e.g. ৳250,000","যেমন: ৳২,৫০,০০০"],
 "pt.moq":["Minimum Order Quantity (MOQ)","ন্যূনতম অর্ডার পরিমাণ (MOQ)"],
 "pt.moqPh":["e.g. 100","যেমন: ১০০"],
 "pt.price":["Price","দাম"],
 "pt.pricePh":["e.g. ৳240 / pcs","যেমন: ৳২৪০ / পিস"],
 "pt.contactPrice":["Contact for Price","দামের জন্য যোগাযোগ করুন"],
 "pt.location":["Location","অবস্থান"],
 "pt.deadline":["Deadline / Required Date","সময়সীমা / প্রয়োজনীয় তারিখ"],
 "pt.desc":["Detailed Requirements / Description","বিস্তারিত প্রয়োজন / বিবরণ"],
 "pt.descPh":["Mention quality, size, color, delivery terms…","মান, সাইজ, রং, ডেলিভারির শর্ত উল্লেখ করুন…"],
 "pt.image":["Product / Reference Image (optional)","পণ্য / রেফারেন্স ছবি (ঐচ্ছিক)"],
 "pt.publish":["Publish Post","পোস্ট প্রকাশ করুন"],
 "pt.saveEdit":["Save Changes","পরিবর্তন সেভ করুন"],
 "pt.publishing":["Publishing…","প্রকাশ হচ্ছে…"],
 "pt.savingE":["Saving…","সেভ হচ্ছে…"],
 "pt.published":["Post published!","পোস্ট প্রকাশিত হয়েছে!"],
 "pt.updated":["Post updated!","পোস্ট আপডেট হয়েছে!"],
 "pt.errTitle":["Please enter a title (at least 4 characters).","শিরোনাম দিন (কমপক্ষে ৪ অক্ষর)।"],
 "pt.errCat":["Please select a category.","ক্যাটাগরি নির্বাচন করুন।"],
 "pt.errLoc":["Please select a location.","অবস্থান নির্বাচন করুন।"],
 "pt.errDesc":["Please write a description (at least 10 characters).","বর্ণনা লিখুন (কমপক্ষে ১০ অক্ষর)।"],
 "pt.goMarket":["View in Marketplace","মার্কেটপ্লেসে দেখুন"],
 "pt.selCat":["Select category…","ক্যাটাগরি নির্বাচন করুন…"],
 "pt.selLoc":["Select district…","জেলা নির্বাচন করুন…"],

 "db.posts":["My Posts","আমার পোস্ট"],
 "db.postsD":["Your requirements & offers","আপনার প্রয়োজন ও অফার"],
 "db.newPost":["Create New Post","নতুন পোস্ট তৈরি করুন"],
 "db.received":["Received Quotes","প্রাপ্ত কোটেশন"],
 "db.receivedD":["Inquiries on your posts","আপনার পোস্টে আসা অনুসন্ধান"],
 "db.noPosts":["You haven't posted anything yet.","আপনি এখনো কোনো পোস্ট করেননি।"],
 "db.noQuotes":["No quotes received yet.","এখনো কোনো কোটেশন আসেনি।"],
 "db.edit":["Edit","সম্পাদনা"],
 "db.delete":["Delete","মুছে ফেলুন"],
 "db.delConfirm":["Delete this post?","এই পোস্টটি মুছে ফেলবেন?"],
 "db.deleted":["Post deleted.","পোস্ট মুছে ফেলা হয়েছে।"],
 "db.closed":["Closed","বন্ধ"],
 "db.reopen":["Reopen","আবার খুলুন"],
 "db.completeProfile":["Complete Your Profile","প্রোফাইল সম্পূর্ণ করুন"],
 "db.profileDone":["Profile complete","প্রোফাইল সম্পূর্ণ"],
 "db.viewMarket":["View Marketplace","মার্কেটপ্লেস দেখুন"],
 "db.business":["Business","ব্যবসা"],
 "db.from":["From","থেকে"],
 "db.quoteOn":["Quote on","কোটেশন"],
 "db.msgPlaceholder":["Messages system is coming soon.","মেসেজ সিস্টেম শীঘ্রই আসছে।"],
 "db.quotesPlaceholder":["When businesses ask for quotes on your posts, they will appear here.","আপনার পোস্টে ব্যবসাগুলো কোটেশন চাইলে সেগুলো এখানে দেখাবে।"]
};
for (var k in EXT) { D[k] = EXT[k]; }

/* shared data: categories, districts, units (bn/en) */
var DATA = {
 categories: [
  ["Garments & Apparel","গার্মেন্টস ও পোশাক"],["Textile & Fabric","টেক্সটাইল ও ফেব্রিক"],["Packaging","প্যাকেজিং"],
  ["Leather Products","চামড়াজাত পণ্য"],["Jute Products","পাটজাত পণ্য"],["Food & Agriculture","খাদ্য ও কৃষি"],
  ["Machinery","মেশিনারি"],["Electronics","ইলেকট্রনিক্স"],["Construction Materials","নির্মাণ সামগ্রী"],
  ["Chemicals & Raw Materials","রাসায়নিক ও কাঁচামাল"]
 ],
 districts: [
  ["Dhaka","ঢাকা"],["Gazipur","গাজীপুর"],["Narayanganj","নারায়ণগঞ্জ"],["Tangail","টাঙ্গাইল"],["Narsingdi","নরসিংদী"],
  ["Manikganj","মানিকগঞ্জ"],["Munshiganj","মুন্সিগঞ্জ"],["Faridpur","ফরিদপুর"],["Rajbari","রাজবাড়ী"],["Gopalganj","গোপালগঞ্জ"],
  ["Madaripur","মাদারীপুর"],["Shariatpur","শরীয়তপুর"],["Kishoreganj","কিশোরগঞ্জ"],["Chattogram","চট্টগ্রাম"],["Cox's Bazar","কক্সবাজার"],
  ["Cumilla","কুমিল্লা"],["Noakhali","নোয়াখালী"],["Feni","ফেনী"],["Lakshmipur","লক্ষ্মীপুর"],["Chandpur","চাঁদপুর"],
  ["Brahmanbaria","ব্রাহ্মণবাড়িয়া"],["Khagrachhari","খাগড়াছড়ি"],["Rangamati","রাঙ্গামাটি"],["Bandarban","বান্দরবান"],
  ["Sylhet","সিলেট"],["Moulvibazar","মৌলভীবাজার"],["Habiganj","হবিগঞ্জ"],["Sunamganj","সুনামগঞ্জ"],["Rajshahi","রাজশাহী"],
  ["Bogura","বগুড়া"],["Naogaon","নওগাঁ"],["Natore","নাটোর"],["Chapainawabganj","চাঁপাইনবাবগঞ্জ"],["Pabna","পাবনা"],
  ["Sirajganj","সিরাজগঞ্জ"],["Joypurhat","জয়পুরহাট"],["Khulna","খুলনা"],["Bagerhat","বাগেরহাট"],["Satkhira","সাতক্ষীরা"],
  ["Jashore","যশোর"],["Jhenaidah","ঝিনাইদহ"],["Magura","মাগুরা"],["Narail","নড়াইল"],["Kushtia","কুষ্টিয়া"],
  ["Chuadanga","চুয়াডাঙ্গা"],["Meherpur","মেহেরপুর"],["Barishal","বরিশাল"],["Bhola","ভোলা"],["Patuakhali","পটুয়াখালী"],
  ["Barguna","বরগুনা"],["Pirojpur","পিরোজপুর"],["Jhalokathi","ঝালকাঠি"],["Rangpur","রংপুর"],["Dinajpur","দিনাজপুর"],
  ["Gaibandha","গাইবান্ধা"],["Kurigram","কুড়িগ্রাম"],["Lalmonirhat","লালমনিরহাট"],["Nilphamari","নীলফামারী"],
  ["Panchagarh","পঞ্চগড়"],["Thakurgaon","ঠাকুরগাঁও"],["Mymensingh","ময়মনসিংহ"],["Jamalpur","জামালপুর"],
  ["Sherpur","শেরপুর"],["Netrokona","নেত্রকোনা"]
 ],
 units: [["PCS","পিস"],["KG","কেজি"],["Ton","টন"],["Meter","মিটার"],["Dozen","ডজন"],["Set","সেট"],["Liter","লিটার"],["Bag","ব্যাগ"],["Carton","কার্টন"]],
 divisions: [
  ["dhaka","ঢাকা"],["chattogram","চট্টগ্রাম"],["rajshahi","রাজশাহী"],["khulna","খুলনা"],
  ["barishal","বরিশাল"],["sylhet","সিলেট"],["rangpur","রংপুর"],["mymensingh","ময়মনসিংহ"]
 ],
 businessTypes: [
  ["manufacturer","প্রস্তুতকারক"],["supplier","সরবরাহকারী"],["wholesaler","পাইকারি ব্যবসায়ী"],
  ["buyer","ক্রেতা"],["exporter","রপ্তানিকারক"],["importer","আমদানিকারক"],
  ["service","সেবা প্রদানকারী"],["other","অন্যান্য"]
 ],
 visibilities: [["public","মুক্ত"],["members","শুধু লগইন করা ইউজার"],["hidden","লুকানো"]]
};
function locName(arr, val){ for(var i=0;i<arr.length;i++){ if(arr[i][0]===val||arr[i][1]===val) return LANG==='bn'?arr[i][1]:arr[i][0]; } return val; }
window.AhoorData = {
  categories: DATA.categories, districts: DATA.districts, units: DATA.units,
  divisions: DATA.divisions, businessTypes: DATA.businessTypes, visibilities: DATA.visibilities,
  locName: locName,
  businessTypeNames: {
    manufacturer:'Manufacturer', supplier:'Supplier', wholesaler:'Wholesaler', buyer:'Buyer',
    exporter:'Exporter', importer:'Importer', service:'Service Provider', other:'Other'
  }
};
function fillSelect(sel, list, selected){
  var cur = LANG==='bn'?1:0;
  sel.innerHTML = '';
  list.forEach(function(item){
    var o = document.createElement('option');
    o.value = item[0];
    o.textContent = item[cur];
    if(selected && item[0]===selected) o.selected = true;
    sel.appendChild(o);
  });
}

/* ---------------- helpers ---------------- */
function $(s, c){ return (c||document).querySelector(s); }
function $all(s, c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); }
function esc(s){ var d=document.createElement('div'); d.textContent=s; return d.innerHTML; }

function api(path, body){
  var opts = { method:'POST', headers:{'Content-Type':'application/json'}, credentials:'same-origin' };
  if(body) opts.body = JSON.stringify(body);
  var ctrl = null;
  if(typeof AbortController !== 'undefined'){
    ctrl = new AbortController();
    opts.signal = ctrl.signal;
    setTimeout(function(){ ctrl.abort(); }, 15000);
  }
  return fetch(path, opts).then(function(r){
    var ct = r.headers.get('content-type') || '';
    if(ct.indexOf('application/json') === -1){
      return { status:r.status, data:{ error:'bad_response' } };
    }
    return r.json().then(function(j){ return { status:r.status, data:j }; })
      .catch(function(){ return { status:r.status, data:{ error:'bad_response' } }; });
  }).catch(function(){ return { status:0, data:{ error:'offline' } }; });
}
var ERR_CODES = ['email_exists','phone_exists','invalid','not_found','weak','unverified','invalid_code','expired','too_many','network','offline','bad_response','missing','no_session','route','method','purpose','forbidden','email','phone','name','mismatch','required','type','code','locked','generic','title','category','location','desc','message','image','self_quote','post_not_found','role_not_allowed','duplicate','post_closed','quote_not_found','not_pending','own_quote','action','self_conv','conv_not_found','suspended','disabled'];
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

document.addEventListener('langchange', function(){
  document.querySelectorAll('[data-fill="category"]').forEach(function(s){ fillSelect(s, DATA.categories, s.value); });
  document.querySelectorAll('[data-fill="district"]').forEach(function(s){ fillSelect(s, DATA.districts, s.value); });
  document.querySelectorAll('[data-fill="unit"]').forEach(function(s){ fillSelect(s, DATA.units, s.value); });
  document.querySelectorAll('[data-fill="division"]').forEach(function(s){ fillSelect(s, DATA.divisions, s.value); });
  document.querySelectorAll('[data-fill="businesstype"]').forEach(function(s){ fillSelect(s, DATA.businessTypes, s.value); });
  document.querySelectorAll('[data-fill="visibility"]').forEach(function(s){ fillSelect(s, DATA.visibilities, s.value); });
});

/* ---------- shared notification helpers ---------- */
function nTimeAgo(iso){
  var diff = (Date.now() - new Date(iso).getTime()) / 60000;
  if (diff < 1) return t('ms.justNow');
  if (diff < 60) return t('ms.minAgo').replace('{m}', Math.floor(diff));
  if (diff < 1440) return t('ms.hrAgo').replace('{h}', Math.floor(diff / 60));
  return t('ms.dayAgo').replace('{d}', Math.floor(diff / 1440));
}
function notifTitle(n){
  if (!n || !n.type) return '';
  return t('nt.' + n.type).replace('{name}', n.data && (n.data.senderName || n.data.actorName) || '');
}
function notifDesc(n){
  if (!n || !n.data) return '';
  if (n.data.postTitle) return n.data.postTitle;
  if (n.data.preview) return n.data.preview;
  if (n.type === 'message_received' && !n.data.preview) return t('nt.photo');
  return '';
}
function notifLink(n){
  if (!n) return '/dashboard.html';
  switch (n.type) {
    case 'quote_received':
    case 'request_received': return '/dashboard.html#quotesSec';
    case 'quote_accepted':
    case 'quote_rejected': return '/dashboard.html#sentSec';
    case 'message_received': return '/messages.html?conv=' + (n.data && n.data.conversationId ? n.data.conversationId : '');
    case 'opportunity_match': return '/matches.html';
    case 'verification_submitted':
    case 'verification_approved':
    case 'verification_rejected': return '/verify.html';
    default: return '/dashboard.html';
  }
}
function notifIcon(n){
  if (!n || !n.type) return '📩';
  if (n.type === 'verification_approved') return '✅';
  if (n.type === 'verification_rejected') return '❌';
  if (n.type === 'verification_submitted') return '🛡️';
  if (n.type === 'opportunity_match') return '🔥';
  if (n.type.indexOf('accepted') >= 0) return '✅';
  if (n.type.indexOf('rejected') >= 0) return '❌';
  if (n.type === 'message_received') return '💬';
  if (n.type === 'request_received') return '📩';
  return '📩';
}
function onNotif(cb){
  if (typeof EventSource === 'undefined') return;
  try {
    var es = new EventSource('/api/stream');
    es.onmessage = function(ev){
      try { var d = JSON.parse(ev.data); if (d.type === 'notification') cb(d); } catch(e){}
    };
  } catch(e){}
}
function initNotificationBell(container){
  if (!container || container.querySelector('#ntBell')) return;
  var bell = document.createElement('div');
  bell.className = 'nt-bell';
  bell.id = 'ntBell';
  bell.title = t('nt.unread');
  bell.innerHTML = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg><span class="nt-count" id="ntCount" style="display:none">0</span>';
  var panel = document.createElement('div');
  panel.className = 'nt-panel';
  panel.id = 'ntPanel';
  panel.innerHTML = '<div class="nt-head"><b>' + t('nt.unread') + '</b><div style="display:flex;gap:10px;align-items:center"><a href="/notifications.html" style="font-size:.74rem;font-weight:650;color:#2F6BFF;white-space:nowrap">' + t('nt.viewAll') + '</a><button id="ntMarkAll" style="font-size:.74rem;font-weight:650;color:#2F6BFF;background:none;border:none;cursor:pointer;white-space:nowrap">' + t('nt.markAll') + '</button></div></div><div class="nt-list" id="ntList"></div>';
  container.prepend(bell);
  document.body.appendChild(panel);

  var open = false;
  function loadNotifs(){
    fetch('/api/notifications', { credentials:'same-origin' })
      .then(function(r){ return r.json(); })
      .then(function(d){
        var count = document.getElementById('ntCount');
        var list = document.getElementById('ntList');
        if (!d) return;
        count.style.display = d.unread > 0 ? '' : 'none';
        count.textContent = d.unread > 99 ? '99+' : d.unread;
        list.innerHTML = '';
        if (!d.notifications || !d.notifications.length) {
          list.innerHTML = '<div class="nt-empty">' + t('nt.empty') + '</div>';
          return;
        }
        d.notifications.slice(0, 15).forEach(function(n){
          var el = document.createElement('div');
          el.className = 'nt-item' + (n.read ? '' : ' unread');
          el.innerHTML = '<span class="nt-ic">' + notifIcon(n) + '</span><div><p>' + esc(notifTitle(n)) + '</p><span>' + esc(notifDesc(n)) + ' · ' + nTimeAgo(n.createdAt) + '</span></div>';
          el.addEventListener('click', function(){
            if (!n.read) fetch('/api/notifications/read', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ id: n.id }), credentials:'same-origin' });
            location.href = notifLink(n);
          });
          list.appendChild(el);
        });
      })
      .catch(function(){});
  }
  bell.addEventListener('click', function(e){
    e.stopPropagation();
    open = !open;
    panel.classList.toggle('on', open);
    if (open) loadNotifs();
  });
  document.addEventListener('click', function(e){
    if (open && !e.target.closest('#ntPanel') && !e.target.closest('#ntBell')) {
      open = false;
      panel.classList.remove('on');
    }
  });
  document.getElementById('ntMarkAll').addEventListener('click', function(){
    fetch('/api/notifications/read', { method:'POST', headers:{'Content-Type':'application/json'}, body:'{}', credentials:'same-origin' })
      .then(loadNotifs);
  });
  setInterval(loadNotifs, 30000);
  onNotif(loadNotifs);
  loadNotifs();
  return bell;
}

/* ---- accessible modal helpers: focus trap + ESC + inert while hidden ---- */
function modalFocusable(el){
  return Array.prototype.slice.call(el.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'))
    .filter(function(x){ return x.offsetParent !== null; });
}
function openModal(el, focusSel){
  if(!el || el.__ahoorOpen) return;
  el.__ahoorOpen = true;
  el.__ahoorLast = document.activeElement;
  el.removeAttribute('inert');
  el.setAttribute('aria-hidden', 'false');
  el.classList.add('on');
  var f = focusSel ? el.querySelector(focusSel) : null;
  if(!f || f.offsetParent === null){ var fb = modalFocusable(el); f = fb[0] || null; }
  if(f && f.focus) f.focus();
  function onKey(e){
    if(e.key === 'Escape'){ e.preventDefault(); closeModal(el); return; }
    if(e.key !== 'Tab') return;
    var items = modalFocusable(el);
    if(!items.length) return;
    var first = items[0], last = items[items.length - 1];
    var idx = items.indexOf(document.activeElement);
    if(e.shiftKey){ if(idx <= 0){ e.preventDefault(); last.focus(); } }
    else if(idx === -1 || idx === items.length - 1){ e.preventDefault(); first.focus(); }
  }
  el.__ahoorKey = onKey;
  document.addEventListener('keydown', onKey, true);
}
function closeModal(el){
  if(!el || !el.__ahoorOpen) return;
  el.__ahoorOpen = false;
  if(el.__ahoorKey){ document.removeEventListener('keydown', el.__ahoorKey, true); el.__ahoorKey = null; }
  el.classList.remove('on');
  el.setAttribute('aria-hidden', 'true');
  el.setAttribute('inert', '');
  var last = el.__ahoorLast; el.__ahoorLast = null;
  if(last && last.focus) try{ last.focus(); }catch(e){}
}
/* show/hide a flow step: display + hidden/inert so inactive steps stay unfocusable */
function setStep(el, on){
  if(!el) return;
  if(on){ el.style.display = ''; el.removeAttribute('hidden'); el.removeAttribute('inert'); }
  else { el.style.display = 'none'; el.setAttribute('hidden', ''); el.setAttribute('inert', ''); }
}

window.Ahoor = {
  t:t, applyLang:applyLang, api:api, errMsg:errMsg, showMsg:showMsg, hideMsg:hideMsg,
  toast:toast, setLoading:setLoading, validEmail:validEmail, validPhone:validPhone,
  initStrength:initStrength, initPwToggles:initPwToggles, initOtp:initOtp,
  startCountdown:startCountdown, fieldErr:fieldErr, clearFieldErr:clearFieldErr, esc:esc,
  fillSelect:fillSelect, locName:locName,
  openModal:openModal, closeModal:closeModal, setStep:setStep,
  timeAgo:nTimeAgo, notifTitle:notifTitle, notifDesc:notifDesc, notifLink:notifLink,
  notifIcon:notifIcon, onNotif:onNotif, initNotificationBell:initNotificationBell
};
window.Ahoor.AhoorData = window.AhoorData;
window.Ahoor.fillSelect = fillSelect;
window.Ahoor.LANG = LANG;
(function(){
  var _set = setLang;
  setLang = function(l){
    LANG = l;
    window.Ahoor.LANG = l;
    _set(l);
  };
})();
applyLang();
})();
