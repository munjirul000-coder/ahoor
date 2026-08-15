#!/usr/bin/env python3
# Build script v2: injects Bangla font, i18n CSS, bilingual body, i18n JS + main JS
import base64, json, re

INDEX = 'index.html'
BODY = 'body_fragment.html'

T = {
 "skip": ("Skip to content", "কনটেন্টে যান"),
 "nav.burger": ("Toggle menu", "মেনু"),
 "lang.aria": ("Language", "ভাষা"),
 "lang.label": ("Language", "ভাষা"),
 "nav.home": ("Home", "হোম"),
 "nav.how": ("How It Works", "কীভাবে কাজ করে"),
 "nav.opps": ("Opportunities", "ব্যবসার সুযোগ"),
 "nav.suppliers": ("Suppliers", "সরবরাহকারী"),
 "nav.cats": ("Categories", "ক্যাটাগরি"),
 "nav.market": ("Marketplace", "মার্কেটপ্লেস"),
 "foot.l1d": ("Marketplace", "মার্কেটপ্লেস"),
 "nav.signin": ("Sign In", "সাইন ইন"),
 "nav.join": ("Join Ahoor", "Ahoor-এ যোগ দিন"),

 "hero.pill": ("Post → Match → Quote → Connect → Deal", "পোস্ট → ম্যাচ → কোটেশন → কানেক্ট → ডিল"),
 "hero.h1a": ("Find Buyers. Find Suppliers.", "ক্রেতা খুঁজুন। সরবরাহকারী খুঁজুন।"),
 "hero.h1b": ("Grow Your Business.", "আপনার ব্যবসা বাড়ান।"),
 "hero.sub": ("Post what your business needs or what your business offers. Ahoor helps connect you with relevant buyers, suppliers, manufacturers, and business opportunities across Bangladesh.", "আপনার ব্যবসার যা প্রয়োজন বা যা অফার করতে চান, তা পোস্ট করুন। সারা বাংলাদেশের উপযুক্ত ক্রেতা, সরবরাহকারী, প্রস্তুতকারক ও ব্যবসার সুযোগের সাথে Ahoor আপনাকে যুক্ত করবে।"),
 "hero.buyTag": ("I WANT TO BUY", "আমি কিনতে চাই"),
 "hero.buyTitle": ("Post What You Need", "যা প্রয়োজন, পোস্ট করুন"),
 "hero.buyDesc": ("Tell businesses exactly what you are looking for and receive relevant quotations and responses.", "আপনি ঠিক কী খুঁজছেন, তা ব্যবসাগুলোকে জানান এবং উপযুক্ত কোটেশন ও সাড়া পান।"),
 "hero.buyCta": ("Post a Requirement", "প্রয়োজন পোস্ট করুন"),
 "hero.sellTag": ("I WANT TO SELL", "আমি বিক্রি করতে চাই"),
 "hero.sellTitle": ("Show What You Offer", "যা অফার করেন, দেখান"),
 "hero.sellDesc": ("Showcase your products, services, manufacturing capabilities, or available production capacity.", "আপনার পণ্য, সেবা, উৎপাদন সক্ষমতা বা খালি উৎপাদন ক্ষমতা তুলে ধরুন।"),
 "hero.sellCta": ("Create a Business Offer", "ব্যবসায়িক অফার তৈরি করুন"),
 "hero.note": ("No storefronts. No listings clutter. Just businesses finding the right businesses.", "কোনো দোকানের ঝামেলা নেই, তালিকার বিশৃঙ্খলা নেই — শুধুই সঠিক ব্যবসার সাথে ব্যবসার মিলন।"),

 "trust.1t": ("Built for Bangladeshi Businesses", "বাংলাদেশি ব্যবসার জন্য তৈরি"),
 "trust.1d": ("Made for the local market, by people who know it.", "দেশীয় বাজারের জন্য তৈরি — যারা বাজার চেনেন, তাদের হাতে।"),
 "trust.2t": ("Manufacturers & Suppliers", "প্রস্তুতকারক ও সরবরাহকারী"),
 "trust.2d": ("Garments, textiles, packaging, and beyond.", "গার্মেন্টস, টেক্সটাইল, প্যাকেজিংসহ আরও অনেক খাত।"),
 "trust.3t": ("Bulk Buyers", "পাইকারি ক্রেতা"),
 "trust.3d": ("For wholesale, sourcing, and production orders.", "পাইকারি, সোর্সিং ও উৎপাদন অর্ডারের জন্য।"),
 "trust.4t": ("Business Opportunities", "ব্যবসার সুযোগ"),
 "trust.4d": ("Buy requests, offers, and available capacity.", "ক্রয়ের অনুরোধ, অফার ও খালি উৎপাদন ক্ষমতা।"),

 "hiw.eyebrow": ("How Ahoor Works", "Ahoor যেভাবে কাজ করে"),
 "hiw.p1": ("Post", "পোস্ট"), "hiw.p2": ("Match", "ম্যাচ"), "hiw.p3": ("Quote", "কোটেশন"),
 "hiw.p4": ("Connect", "কানেক্ট"), "hiw.p5": ("Deal", "ডিল"),
 "hiw.lead": ("A business requirement turns into a deal — watch the whole flow, step by step.", "একটি ব্যবসার প্রয়োজন কীভাবে ডিলে পরিণত হয় — পুরো প্রক্রিয়াটি ধাপে ধাপে দেখুন।"),
 "hiw.t1": ("Post", "পোস্ট"), "hiw.t1s": ("Buyer posts a requirement", "ক্রেতা একটি প্রয়োজন পোস্ট করেন"),
 "hiw.t2": ("Match", "ম্যাচ"), "hiw.t2s": ("Ahoor finds relevant businesses", "Ahoor উপযুক্ত ব্যবসাগুলো খুঁজে বের করে"),
 "hiw.t3": ("Quote", "কোটেশন"), "hiw.t3s": ("Suppliers send quotations", "সরবরাহকারীরা কোটেশন পাঠান"),
 "hiw.t4": ("Deal", "ডিল"), "hiw.t4s": ("Compare, connect, close", "তুলনা করুন, কানেক্ট হোন, ডিল করুন"),
 "hiw.foot": ("Auto-playing demo · hover to pause · click a step to jump", "স্বয়ংক্রিয় ডেমো · পজ করতে হোভার করুন · যেকোনো ধাপে যেতে ক্লিক করুন"),

 "s1.tag": ("Buyer Requirement", "ক্রেতার প্রয়োজন"),
 "s1.title": ("Need 1,000 Custom T-Shirts", "১,০০০ কাস্টম টি-শার্ট প্রয়োজন"),
 "s1.desc": ("Cotton t-shirts with custom print — sizes S–XL, for a new retail line.", "কাস্টম প্রিন্টের কটন টি-শার্ট — সাইজ S–XL, নতুন খুচরা লাইনের জন্য।"),
 "s1.qty": ("1,000 pcs", "১,০০০ পিস"), "s1.loc": ("Dhaka", "ঢাকা"), "s1.deadline": ("20 days", "২০ দিন"),
 "s1.btn": ("Post Requirement", "প্রয়োজন পোস্ট করুন"),
 "s1.side": ("What happens next", "এরপর যা ঘটে"),
 "s1.a": ("Your requirement is published to relevant businesses", "আপনার প্রয়োজন উপযুক্ত ব্যবসাগুলোর কাছে প্রকাশিত হয়"),
 "s1.b": ("Ahoor matches on category, product, location, and quantity", "Ahoor ক্যাটাগরি, পণ্য, অবস্থান ও পরিমাণের ভিত্তিতে ম্যাচ করে"),
 "s1.c": ("Suppliers send you quotations — no endless searching", "সরবরাহকারীরা কোটেশন পাঠান — আর অন্তহীন খোঁজাখুঁজির দরকার নেই"),
 "s2.core": ("Need 1,000 Custom T-Shirts", "১,০০০ কাস্টম টি-শার্ট প্রয়োজন"),
 "s2.coresub": ("Buyer requirement · Dhaka", "ক্রেতার প্রয়োজন · ঢাকা"),
 "s2.badge": ("12 Relevant Suppliers Matched", "১২টি উপযুক্ত সরবরাহকারী ম্যাচ হয়েছে"),
 "s2.cap": ("Surfaced by category, product type, location, quantity, and business profile.", "ক্যাটাগরি, পণ্যের ধরন, অবস্থান, পরিমাণ ও ব্যবসার প্রোফাইলের ভিত্তিতে দেখানো হয়েছে।"),
 "s3.per": (" / pcs", " / পিস"),
 "s3.pA": ("250", "২৫০"), "s3.pB": ("230", "২৩০"), "s3.pC": ("270", "২৭০"),
 "s3.roleD": ("Manufacturer · Dhaka", "প্রস্তুতকারক · ঢাকা"),
 "s3.roleG": ("Manufacturer · Gazipur", "প্রস্তুতকারক · গাজীপুর"),
 "s3.delivery": ("Delivery", "ডেলিভারি"), "s3.moq": ("MOQ", "MOQ"),
 "s3.d10": ("10 days", "১০ দিন"), "s3.d15": ("15 days", "১৫ দিন"), "s3.d7": ("7 days", "৭ দিন"),
 "s3.m500": ("500 pcs", "৫০০ পিস"), "s3.m300": ("300 pcs", "৩০০ পিস"), "s3.m200": ("200 pcs", "২০০ পিস"),
 "s3.best": ("Best price", "সেরা দাম"), "s3.fast": ("Fastest", "দ্রুততম"),
 "s3.cap": ("Three quotations received for your requirement — compare price, delivery, and MOQ.", "আপনার প্রয়োজন অনুযায়ী তিনটি কোটেশন এসেছে — দাম, ডেলিভারি ও MOQ তুলনা করুন।"),
 "s4.col1": ("Supplier", "সরবরাহকারী"), "s4.col2": ("Price / pcs", "দাম / পিস"),
 "s4.col3": ("Delivery", "ডেলিভারি"), "s4.col4": ("MOQ", "MOQ"),
 "s4.tagBest": ("Best price", "সেরা দাম"), "s4.tagFast": ("Fastest", "দ্রুততম"),
 "s4.btn1": ("Compare Offers", "অফার তুলনা করুন"),
 "s4.btn2": ("Start Conversation", "কথোপকথন শুরু করুন"),
 "s4.btn3": ("Make a Deal", "ডিল সম্পন্ন করুন"),
 "s4.cap": ("Choose what fits your business — then take the conversation forward.", "আপনার ব্যবসার জন্য যা মানানসই, তা বেছে নিন — তারপর কথোপকথন এগিয়ে নিয়ে যান।"),

 "lbl.loc": ("Location", "অবস্থান"), "lbl.qty": ("Quantity", "পরিমাণ"),
 "lbl.deadline": ("Deadline", "সময়সীমা"), "lbl.moq": ("MOQ", "MOQ"),
 "lbl.prod": ("Production time", "উৎপাদন সময়"), "lbl.sup": ("Supplier", "সরবরাহকারী"),
 "lbl.cap": ("Available production", "উৎপাদন ক্ষমতা"), "lbl.ready": ("Ready to quote", "কোটেশন প্রস্তুত"),

 "opps.eyebrow": ("Business Opportunities", "ব্যবসার সুযোগ"),
 "opps.title": ("Explore Business Opportunities", "ব্যবসার সুযোগ খুঁজে দেখুন"),
 "opps.lead": ("Buy requests, manufacturing offers, and available capacity — posted by businesses like yours.", "ক্রয়ের অনুরোধ, উৎপাদন অফার ও খালি ক্ষমতা — আপনার মতো ব্যবসাগুলোরই পোস্ট।"),
 "opp1.tag": ("Buy Request", "ক্রয়ের অনুরোধ"),
 "opp1.title": ("Need 5,000 Custom T-Shirts", "৫,০০০ কাস্টম টি-শার্ট প্রয়োজন"),
 "opp1.desc": ("Regular-fit cotton T-shirts with custom printing, for a new product line.", "কাস্টম প্রিন্টসহ রেগুলার-ফিট কটন টি-শার্ট, নতুন প্রোডাক্ট লাইনের জন্য।"),
 "opp1.loc": ("Dhaka, Bangladesh", "ঢাকা, বাংলাদেশ"),
 "opp1.qty": ("5,000 pcs", "৫,০০০ পিস"), "opp1.dead": ("30 days", "৩০ দিন"),
 "opp1.cta": ("Send Quote", "কোটেশন পাঠান"),
 "opp2.tag": ("Manufacturing Offer", "উৎপাদন অফার"),
 "opp2.title": ("Custom Hoodie Manufacturing", "কাস্টম হুডি উৎপাদন"),
 "opp2.desc": ("Fleece hoodies with custom branding — suitable for small and medium orders.", "কাস্টম ব্র্যান্ডিংসহ ফ্লিস হুডি — ছোট ও মাঝারি অর্ডারের জন্য উপযুক্ত।"),
 "opp2.moq": ("100 pcs", "১০০ পিস"), "opp2.prod": ("7–14 days", "৭–১৪ দিন"),
 "opp2.sup": ("Verified factory", "যাচাইকৃত কারখানা"),
 "opp2.cta": ("View Supplier", "সরবরাহকারী দেখুন"),
 "opp3.tag": ("Available Capacity", "খালি উৎপাদন ক্ষমতা"),
 "opp3.title": ("T-Shirt Factory Has Available Capacity", "টি-শার্ট কারখানায় খালি উৎপাদন ক্ষমতা রয়েছে"),
 "opp3.desc": ("Facility in Gazipur with spare monthly capacity for export-quality orders.", "গাজীপুরের কারখানা — এক্সপোর্ট-কোয়ালিটি অর্ডারের জন্য মাসিক খালি ক্ষমতা রয়েছে।"),
 "opp3.cap": ("20,000 pcs / month", "২০,০০০ পিস / মাস"),
 "opp3.loc": ("Gazipur, Dhaka", "গাজীপুর, ঢাকা"),
 "opp3.ready": ("Within 24 hours", "২৪ ঘণ্টার মধ্যে"),
 "opp3.cta": ("Contact Factory", "কারখানার সাথে যোগাযোগ করুন"),
 "opps.note": ("Sample opportunities shown for illustration.", "উদাহরণ হিসেবে নমুনা সুযোগ দেখানো হয়েছে।"),
 "opps.more": ("Explore All Opportunities", "সব সুযোগ দেখুন"),

 "feat.eyebrow": ("Features", "বৈশিষ্ট্য"),
 "feat.title": ("Everything You Need to Find the Right Business", "সঠিক ব্যবসা খুঁজে পেতে যা যা প্রয়োজন"),
 "feat.lead": ("Built for real B2B workflows — sourcing, quoting, and partnership building.", "বাস্তব B2B কাজের জন্য তৈরি — সোর্সিং, কোটেশন ও অংশীদারিত্ব গঠন।"),
 "f1.t": ("Smart Business Matching", "স্মার্ট বিজনেস ম্যাচিং"),
 "f1.d": ("Ahoor helps relevant buyers and suppliers find each other — so the right people discover your opportunity.", "Ahoor উপযুক্ত ক্রেতা ও সরবরাহকারীকে একে অপরের সাথে মিলিয়ে দেয় — যাতে সঠিক মানুষ আপনার সুযোগটি খুঁজে পায়।"),
 "f2.t": ("Post Requirements", "প্রয়োজন পোস্ট করুন"),
 "f2.d": ("Post exactly what you need — product, quantity, location, deadline — and receive offers from businesses that can deliver.", "ঠিক যা প্রয়োজন তা পোস্ট করুন — পণ্য, পরিমাণ, অবস্থান, সময়সীমা — এবং ডেলিভারি দিতে পারে এমন ব্যবসাগুলোর কাছ থেকে অফার পান।"),
 "f3.t": ("Direct Business Communication", "সরাসরি ব্যবসায়িক যোগাযোগ"),
 "f3.d": ("Connect and discuss opportunities directly — clarify specs, negotiate terms, and build trust on your own terms.", "সরাসরি কানেক্ট হয়ে সুযোগ নিয়ে আলোচনা করুন — স্পেসিফিকেশন পরিষ্কার করুন, শর্ত নিয়ে আলোচনা করুন, নিজের মতো করে আস্থা গড়ুন।"),
 "f4.t": ("Supplier & Factory Profiles", "সরবরাহকারী ও কারখানার প্রোফাইল"),
 "f4.d": ("Explore what businesses manufacture, supply, and offer — from product ranges to production capacity.", "ব্যবসাগুলো কী তৈরি করে, কী সরবরাহ করে ও কী অফার করে তা জানুন — প্রোডাক্ট রেঞ্জ থেকে উৎপাদন ক্ষমতা পর্যন্ত।"),
 "f5.t": ("Compare Offers", "অফার তুলনা করুন"),
 "f5.d": ("Compare quotations, MOQ, production time, and other details side by side — then choose what fits your business.", "কোটেশন, MOQ, উৎপাদন সময়সহ অন্যান্য বিবরণ পাশাপাশি তুলনা করুন — তারপর বেছে নিন আপনার ব্যবসার জন্য যা মানানসই।"),
 "f6.t": ("Business Verification", "ব্যবসা যাচাইকরণ"),
 "f6.d": ("Clear verification levels help you understand how much business information is available before you engage.", "পরিষ্কার যাচাইকরণ স্তর আপনাকে বুঝতে সাহায্য করে যে কাজ শুরু করার আগে কতটা ব্যবসায়িক তথ্য পাওয়া যায়।"),
 "f7.t": ("Smart Opportunity Matching", "স্মার্ট সুযোগ ম্যাচিং"),
 "f7.d": ("When a business posts a requirement or offer, Ahoor intelligently surfaces it to the most relevant businesses — based on category, product type, location, quantity, and business profile.", "যখন কোনো ব্যবসা প্রয়োজন বা অফার পোস্ট করে, Ahoor সেটি সবচেয়ে উপযুক্ত ব্যবসাগুলোর কাছে পৌঁছে দেয় — ক্যাটাগরি, পণ্যের ধরন, অবস্থান, পরিমাণ ও ব্যবসার প্রোফাইলের ভিত্তিতে।"),
 "f7.c1": ("Category", "ক্যাটাগরি"), "f7.c2": ("Product", "পণ্য"), "f7.c3": ("Location", "অবস্থান"),
 "f7.c4": ("Quantity", "পরিমাণ"), "f7.c5": ("Profile", "প্রোফাইল"),

 "buy.eyebrow": ("For Buyers", "ক্রেতাদের জন্য"),
 "buy.title": ("Stop Searching Everywhere.", "আর এদিক-সেদিক খোঁজার দরকার নেই।"),
 "buy.lead": ("Post your business requirement once and let relevant suppliers and manufacturers find you.", "আপনার ব্যবসার প্রয়োজন একবার পোস্ট করুন — উপযুক্ত সরবরাহকারী ও প্রস্তুতকারকেরা আপনাকে খুঁজে নেবেন।"),
 "buy.c1": ("Post once — reach every supplier who can actually deliver", "একবার পোস্ট করুন — যারা সত্যিই ডেলিভারি দিতে পারে, সব সরবরাহকারীর কাছে পৌঁছান"),
 "buy.c2": ("Receive quotations with MOQ, pricing, and timelines", "MOQ, দাম ও সময়সূচিসহ কোটেশন পান"),
 "buy.c3": ("Compare offers and negotiate directly — no middlemen", "অফার তুলনা করুন ও সরাসরি দরদাম করুন — কোনো মধ্যস্বত্বভোগী ছাড়াই"),
 "buy.cta1": ("Post a Requirement", "প্রয়োজন পোস্ট করুন"),
 "buy.cta2": ("See How It Works", "কীভাবে কাজ করে দেখুন"),
 "buy.mockHead": ("Post a Requirement", "প্রয়োজন পোস্ট করুন"),
 "buy.mockSub": ("Buyer view", "ক্রেতার ভিউ"),
 "buy.l1": ("What do you need?", "আপনার কী প্রয়োজন?"),
 "buy.mockNeed": ("Custom T-Shirts", "কাস্টম টি-শার্ট"),
 "buy.l2": ("Quantity", "পরিমাণ"), "buy.mockQty": ("1,000 pcs", "১,০০০ পিস"),
 "buy.l3": ("Location", "অবস্থান"), "buy.mockLoc": ("Dhaka", "ঢাকা"),
 "buy.mockBtn": ("Submit Requirement", "প্রয়োজন জমা দিন"),
 "buy.mockFoot": ("Your requirement stays visible to relevant businesses", "আপনার প্রয়োজন উপযুক্ত ব্যবসাগুলোর কাছে দৃশ্যমান থাকে"),
 "buy.chip1": ("3 new quotes received", "৩টি নতুন কোটেশন এসেছে"),
 "buy.chip1s": ("Suppliers responded to your post", "সরবরাহকারীরা আপনার পোস্টে সাড়া দিয়েছেন"),
 "buy.chip2": ("Matched with 12 relevant suppliers", "১২টি উপযুক্ত সরবরাহকারীর সাথে ম্যাচ হয়েছে"),
 "buy.chip2s": ("Based on your requirement", "আপনার প্রয়োজন অনুযায়ী"),

 "sup.eyebrow": ("For Suppliers & Manufacturers", "সরবরাহকারী ও প্রস্তুতকারকদের জন্য"),
 "sup.title": ("More Opportunities. Better Connections.", "আরও সুযোগ। আরও ভালো কানেকশন।"),
 "sup.lead": ("Showcase what you manufacture or supply and discover businesses actively looking for your products.", "আপনি যা তৈরি করেন বা সরবরাহ করেন তা প্রদর্শন করুন এবং যেসব ব্যবসা আপনার পণ্য খুঁজছে, তাদের খুঁজে বের করুন।"),
 "sup.c1": ("Present your products, services, and production capacity", "আপনার পণ্য, সেবা ও উৎপাদন ক্ষমতা তুলে ধরুন"),
 "sup.c2": ("Discover businesses actively looking for what you make", "আপনার তৈরি পণ্যের সন্ধানে থাকা ব্যবসাগুলো খুঁজে বের করুন"),
 "sup.c3": ("Respond to buyer requests and send quotations in minutes", "ক্রেতার অনুরোধে সাড়া দিন ও মিনিটেই কোটেশন পাঠান"),
 "sup.cta1": ("Join as a Supplier", "সরবরাহকারী হিসেবে যোগ দিন"),
 "sup.cta2": ("How Matching Works", "ম্যাচিং যেভাবে কাজ করে"),
 "dash.title": ("Ahoor · Supplier Dashboard", "Ahoor · সরবরাহকারী ড্যাশবোর্ড"),
 "dash.pill": ("Active", "সচল"),
 "dash.s1": ("New Buyer Requests", "নতুন ক্রেতার অনুরোধ"),
 "dash.s2": ("Quotes Sent", "পাঠানো কোটেশন"),
 "dash.s3": ("Available Opportunities", "সুযোগ পাওয়া যাচ্ছে"),
 "dash.s4": ("Profile Views", "প্রোফাইল দেখা"),
 "dash.req": ("Buyer needs 5,000 custom polo shirts", "ক্রেতার প্রয়োজন ৫,০০০ কাস্টম পোলো শার্ট"),
 "dash.reqsub": ("Gazipur, Dhaka · Quote by 20 Aug", "গাজীপুর, ঢাকা · ২০ আগস্টের মধ্যে কোটেশন"),
 "dash.tag": ("Matches your capacity", "আপনার ক্ষমতার সাথে মানানসই"),
 "dash.btn": ("Send Quote", "কোটেশন পাঠান"),
 "dash.more": ("View all opportunities", "সব সুযোগ দেখুন"),
 "sup.chip": ("New buyer request", "নতুন ক্রেতার অনুরোধ"),
 "sup.chips": ("5,000 pcs · polo shirts", "৫,০০০ পিস · পোলো শার্ট"),

 "cats.eyebrow": ("Categories", "ক্যাটাগরি"),
 "cats.title": ("Explore Business Categories", "ব্যবসার ক্যাটাগরি খুঁজে দেখুন"),
 "cats.lead": ("From garments to packaging — discover businesses across Bangladesh's key industries.", "গার্মেন্টস থেকে প্যাকেজিং — বাংলাদেশের প্রধান শিল্পগুলোর ব্যবসা আবিষ্কার করুন।"),
 "cat1": ("Garments & Apparel", "গার্মেন্টস ও পোশাক"),
 "cat2": ("Textile & Fabric", "টেক্সটাইল ও ফেব্রিক"),
 "cat3": ("Packaging", "প্যাকেজিং"),
 "cat4": ("Leather Products", "চামড়াজাত পণ্য"),
 "cat5": ("Jute Products", "পাটজাত পণ্য"),
 "cat6": ("Food & Agriculture", "খাদ্য ও কৃষি"),
 "cat7": ("Machinery", "মেশিনারি"),
 "cat8": ("Electronics", "ইলেকট্রনিক্স"),
 "cat9": ("Construction Materials", "নির্মাণ সামগ্রী"),
 "cat10": ("Chemicals & Raw Materials", "রাসায়নিক ও কাঁচামাল"),

 "why.eyebrow": ("Why Ahoor", "কেন Ahoor"),
 "why.title": ("Business Is Better When the Right People Find Each Other.", "সঠিক মানুষ যখন একে অপরকে খুঁজে পায়, ব্যবসা তখনই ভালো হয়।"),
 "why.lead": ("Ahoor is building a simpler way for Bangladeshi businesses to discover opportunities, find reliable business partners, and grow together.", "বাংলাদেশি ব্যবসাগুলোর জন্য Ahoor একটি সহজ উপায় গড়ে তুলছে — সুযোগ খুঁজে বের করা, নির্ভরযোগ্য ব্যবসায়িক অংশীদার খুঁজে পাওয়া এবং একসাথে এগিয়ে যাওয়া।"),
 "viz.buyers": ("Buyers", "ক্রেতা"),
 "viz.suppliers": ("Suppliers", "সরবরাহকারী"),
 "viz.mfrs": ("Manufacturers", "প্রস্তুতকারক"),
 "viz.factories": ("Factories", "কারখানা"),
 "viz.exporters": ("Exporters", "রপ্তানিকারক"),
 "viz.traders": ("Traders", "ব্যবসায়ী"),
 "viz.yours": ("Your Business", "আপনার ব্যবসা"),

 "cta.eyebrow": ("Join the network", "নেটওয়ার্কে যোগ দিন"),
 "cta.t1": ("Your Next Business Opportunity Could Be", "আপনার পরবর্তী ব্যবসার সুযোগটি হতে পারে"),
 "cta.t2": ("One Connection Away.", "মাত্র একটি কানেকশন দূরে।"),
 "cta.desc": ("Join Ahoor and start discovering new buyers, suppliers, manufacturers, and opportunities.", "Ahoor-এ যোগ দিন এবং নতুন ক্রেতা, সরবরাহকারী, প্রস্তুতকারক ও সুযোগ খুঁজে নেওয়া শুরু করুন।"),
 "cta.b1": ("Join Ahoor", "Ahoor-এ যোগ দিন"),
 "cta.b2": ("Explore Opportunities", "সুযোগ খুঁজে দেখুন"),
 "cta.mini": ("Post what you need or show what you offer — it takes minutes.", "যা প্রয়োজন পোস্ট করুন বা যা অফার করেন দেখান — লাগবে মাত্র কয়েক মিনিট।"),

 "foot.desc": ("Connecting businesses. Creating opportunities. A B2B marketplace and opportunity network built for Bangladesh.", "ব্যবসার সাথে ব্যবসা যুক্ত করা। সুযোগ তৈরি করা। বাংলাদেশের জন্য তৈরি একটি B2B মার্কেটপ্লেস ও সুযোগের নেটওয়ার্ক।"),
 "foot.made": ("Made in Bangladesh", "বাংলাদেশে তৈরি"),
 "foot.h1": ("Platform", "প্ল্যাটফর্ম"),
 "foot.h2": ("Business", "ব্যবসা"),
 "foot.h3": ("Company", "কোম্পানি"),
 "foot.l1a": ("How It Works", "কীভাবে কাজ করে"),
 "foot.l1b": ("Opportunities", "ব্যবসার সুযোগ"),
 "foot.l1c": ("Categories", "ক্যাটাগরি"),
 "foot.l2a": ("Find Suppliers", "সরবরাহকারী খুঁজুন"),
 "foot.l2b": ("Post Requirement", "প্রয়োজন পোস্ট করুন"),
 "foot.l2c": ("Join as Supplier", "সরবরাহকারী হিসেবে যোগ দিন"),
 "foot.l3a": ("About Ahoor", "Ahoor সম্পর্কে"),
 "foot.l3b": ("Contact", "যোগাযোগ"),
 "foot.l3c": ("Privacy", "গোপনীয়তা"),
 "foot.l3d": ("Terms", "শর্তাবলি"),
 "foot.cr": ("© 2026 Ahoor. All rights reserved.", "© ২০২৬ Ahoor. সর্বস্বত্ব সংরক্ষিত।"),
 "fl.1": ("POST", "পোস্ট"), "fl.2": ("MATCH", "ম্যাচ"), "fl.3": ("QUOTE", "কোটেশন"),
 "fl.4": ("CONNECT", "কানেক্ট"), "fl.5": ("DEAL", "ডিল"),

 "meta.title": ("Ahoor — Find the Right Business. Create the Next Opportunity.", "Ahoor — সঠিক ব্যবসা খুঁজুন, নতুন সুযোগ তৈরি করুন।"),
 "meta.desc": ("Ahoor is the B2B opportunity network for Bangladesh — post what you need, discover suppliers and manufacturers, compare offers, and find your next business opportunity.", "Ahoor হলো বাংলাদেশের B2B ব্যবসার সুযোগের নেটওয়ার্ক — যা প্রয়োজন পোস্ট করুন, সরবরাহকারী ও প্রস্তুতকারক খুঁজুন, কোটেশন তুলনা করুন এবং পরবর্তী ব্যবসার সুযোগটি খুঁজে নিন।"),
}

I18N = {k: {"en": v[0], "bn": v[1]} for k, v in T.items()}
I18N_JSON = json.dumps(I18N, ensure_ascii=False)

def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()

INTER_B64 = b64('assets/inter-latin.woff2')
NSB_B64 = b64('assets/noto-bengali-full.woff2')

FONT_CSS = """/* ============ Fonts: Bangla ============ */
@font-face{
  font-family:'Noto Sans Bengali';
  font-style:normal;
  font-weight:100 900;
  font-display:swap;
  src:url(data:font/woff2;base64,__NSB__) format('woff2');
}

/* ============ Bangla mode ============ */
html[lang="bn"]{--font:'Noto Sans Bengali','Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif}
html[lang="bn"] body{line-height:1.72}
html[lang="bn"] h1,html[lang="bn"] h2{line-height:1.3;letter-spacing:-.01em}
html[lang="bn"] .hero h1{font-size:clamp(2.1rem,5vw,3.55rem)}
html[lang="bn"] h2.h2{font-size:clamp(1.7rem,3.4vw,2.45rem)}
html[lang="bn"] .eyebrow{letter-spacing:.08em}
html[lang="bn"] .btn{white-space:normal}
html[lang="bn"] .hero-pill{font-size:.78rem}
html[lang="bn"] .hcard p,html[lang="bn"] .feat-card p,html[lang="bn"] .opp-desc,html[lang="bn"] .md-side li,html[lang="bn"] .hero .sub,html[lang="bn"] .cta-inner p,html[lang="bn"] .footer-desc{line-height:1.75}

/* ============ Language switcher ============ */
.lang-switch{display:inline-flex;align-items:center;gap:2px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:3px}
.lang-switch .lang-btn{font-family:inherit;font-size:.8rem;font-weight:650;line-height:1;color:#C7D2EC;padding:6px 12px;border-radius:999px;border:none;background:transparent;transition:background .25s ease,color .25s ease}
.lang-switch .lang-btn:hover{color:#fff}
.lang-switch .lang-btn.on{background:linear-gradient(135deg,#4C84FF,#2F6BFF);color:#fff;box-shadow:0 4px 10px -4px rgba(47,107,255,.6)}
.lang-switch .lsep{color:#5B6B93;font-size:.72rem;padding:0 2px;user-select:none}
.mlang{display:flex;align-items:center;gap:12px;margin-top:20px}
.mlang-label{font-size:.75rem;font-weight:650;letter-spacing:.1em;text-transform:uppercase;color:#8FA3CE}
@media (max-width:420px){.nav-actions .lang-switch{order:-1}.brand-name{display:none}}
""".replace('__NSB__', NSB_B64)

I18N_JS = """<script>
(function(){
  'use strict';
  var I18N = __JSON__;
  var STORE = 'ahoor-lang';

  function apply(lang, persist){
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-i18n]').forEach(function(el){
      var k = el.getAttribute('data-i18n');
      var v = I18N[k];
      if(v && v[lang]) el.textContent = v[lang];
    });
    document.querySelectorAll('[data-i18n-aria]').forEach(function(el){
      var k = el.getAttribute('data-i18n-aria');
      var v = I18N[k];
      if(v && v[lang]) el.setAttribute('aria-label', v[lang]);
    });
    document.querySelectorAll('.lang-btn').forEach(function(b){
      var on = b.getAttribute('data-lang') === lang;
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    if(I18N['meta.title'] && I18N['meta.title'][lang]) document.title = I18N['meta.title'][lang];
    var md = document.querySelector('meta[name="description"]');
    if(md && I18N['meta.desc'] && I18N['meta.desc'][lang]) md.setAttribute('content', I18N['meta.desc'][lang]);
    if(persist){
      try{ localStorage.setItem(STORE, lang); }catch(e){}
    }
  }

  var saved = null;
  try{ saved = localStorage.getItem(STORE); }catch(e){}
  var initial = (saved === 'en' || saved === 'bn') ? saved : 'bn';
  apply(initial, false);

  document.querySelectorAll('.lang-btn').forEach(function(b){
    b.addEventListener('click', function(){ apply(b.getAttribute('data-lang'), true); });
  });
})();
</script>
""".replace('__JSON__', I18N_JSON)

MAIN_JS = """<script>
(function(){
  'use strict';

  /* ---------- Navbar: glass on scroll ---------- */
  var nav = document.getElementById('nav');
  function onScroll(){
    nav.classList.toggle('scrolled', window.scrollY > 12);
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  /* ---------- Mobile menu ---------- */
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('mobileMenu');
  function setMenu(open){
    document.body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  burger.addEventListener('click', function(){
    setMenu(!document.body.classList.contains('menu-open'));
  });
  menu.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click', function(){ setMenu(false); });
  });
  document.querySelectorAll('.lang-btn').forEach(function(b){
    b.addEventListener('click', function(){ setMenu(false); });
  });

  /* ---------- Scroll reveal ---------- */
  var revealEls = document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, {threshold:.12, rootMargin:'0px 0px -36px 0px'});
    revealEls.forEach(function(el){ io.observe(el); });
  } else {
    revealEls.forEach(function(el){ el.classList.add('in'); });
  }

  /* ---------- Active nav link ---------- */
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.nav-links a');
  if('IntersectionObserver' in window){
    var navIO = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){
          navLinks.forEach(function(a){
            a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id);
          });
        }
      });
    }, {rootMargin:'-42% 0px -52% 0px'});
    sections.forEach(function(s){ navIO.observe(s); });
  }

  /* ---------- Matching flow demo ---------- */
  var demo = document.getElementById('mdemo');
  if(demo){
    var dtabs = demo.querySelectorAll('.md-tab');
    var dsteps = demo.querySelectorAll('.md-step');
    var dprog = document.getElementById('mdProg');
    var dmatch = document.getElementById('mdMatch');
    var reducedM = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var PAUSE = 5200, cur = 1, timer = null;
    var playing = !reducedM;

    function activate(n){
      cur = n;
      dtabs.forEach(function(t){
        var on = +t.dataset.step === n;
        t.classList.toggle('active', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      dsteps.forEach(function(s){ s.classList.toggle('active', +s.dataset.step === n); });
      if(dmatch){
        dmatch.classList.remove('playing');
        if(n === 2){ void dmatch.offsetWidth; dmatch.classList.add('playing'); }
      }
      if(playing){
        clearTimeout(timer);
        timer = setTimeout(function(){ activate(cur === 4 ? 1 : cur + 1); }, PAUSE);
        if(dprog){
          dprog.classList.remove('run');
          void dprog.offsetWidth;
          dprog.classList.add('run');
        }
      }
    }

    dtabs.forEach(function(t){
      t.addEventListener('click', function(){ activate(+t.dataset.step); });
    });
    var postBtn = demo.querySelector('.md-post-btn');
    if(postBtn){
      postBtn.addEventListener('click', function(){ activate(2); });
    }
    demo.addEventListener('mouseenter', function(){
      if(playing){ clearTimeout(timer); if(dprog) dprog.style.animationPlayState = 'paused'; }
    });
    demo.addEventListener('mouseleave', function(){
      if(playing){
        if(dprog) dprog.style.animationPlayState = 'running';
        activate(cur);
      }
    });
    if(playing) activate(1);
  }

  /* ---------- Hero network canvas ---------- */
  var canvas = document.getElementById('net');
  if(canvas){
    var ctx = canvas.getContext('2d');
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var W = 0, H = 0, nodes = [], raf = null, visible = false;
    var mouse = {x:-9999, y:-9999};
    var DPR = Math.min(window.devicePixelRatio || 1, 2);
    var LINK = 150;

    function resize(){
      var parent = canvas.parentElement;
      W = Math.max(320, parent.clientWidth);
      H = Math.max(520, parent.clientHeight);
      canvas.width = Math.round(W * DPR);
      canvas.height = Math.round(H * DPR);
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      var count = Math.max(34, Math.min(80, Math.round(W * H / 24000)));
      nodes = [];
      for(var i = 0; i < count; i++){
        nodes.push({
          x: Math.random() * W,
          y: Math.random() * H,
          vx: (Math.random() - .5) * .22,
          vy: (Math.random() - .5) * .22,
          r: Math.random() * 1.5 + .7
        });
      }
    }

    function draw(t){
      ctx.clearRect(0, 0, W, H);
      var n = nodes.length, i, j, a, b, dx, dy, d2, d, o;

      for(i = 0; i < n; i++){
        a = nodes[i];
        a.x += a.vx; a.y += a.vy;
        if(a.x < -24) a.x = W + 24; else if(a.x > W + 24) a.x = -24;
        if(a.y < -24) a.y = H + 24; else if(a.y > H + 24) a.y = -24;
        dx = a.x - mouse.x; dy = a.y - mouse.y; d2 = dx * dx + dy * dy;
        if(d2 < 16900 && d2 > .01){
          d = Math.sqrt(d2);
          var f = (130 - d) / 130 * .055;
          a.x += dx / d * f; a.y += dy / d * f;
        }
      }

      for(i = 0; i < n; i++){
        a = nodes[i];
        for(j = i + 1; j < n; j++){
          b = nodes[j];
          dx = a.x - b.x; dy = a.y - b.y; d2 = dx * dx + dy * dy;
          if(d2 < LINK * LINK){
            d = Math.sqrt(d2);
            o = (1 - d / LINK) * .16;
            ctx.strokeStyle = 'rgba(112,145,255,' + o.toFixed(3) + ')';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }

      for(i = 0; i < n; i++){
        a = nodes[i];
        var pulse = .7 + .3 * Math.sin(t / 900 + a.r * 7);
        ctx.fillStyle = 'rgba(168,189,255,' + (pulse * .5).toFixed(3) + ')';
        ctx.beginPath();
        ctx.arc(a.x, a.y, a.r, 0, 6.2832);
        ctx.fill();
      }
      raf = requestAnimationFrame(draw);
    }

    function start(){
      if(visible) return;
      visible = true;
      resize();
      if(reduced){ draw(0); return; }
      raf = requestAnimationFrame(draw);
    }
    function stop(){
      visible = false;
      if(raf) cancelAnimationFrame(raf);
      raf = null;
    }

    window.addEventListener('resize', function(){
      if(visible) resize();
    }, {passive:true});
    window.addEventListener('mousemove', function(e){
      mouse.x = e.clientX; mouse.y = e.clientY;
    }, {passive:true});
    window.addEventListener('mouseout', function(){
      mouse.x = -9999; mouse.y = -9999;
    });

    if('IntersectionObserver' in window){
      var cio = new IntersectionObserver(function(es){
        es.forEach(function(e){
          if(e.isIntersecting) start(); else stop();
        });
      }, {threshold:.02});
      cio.observe(canvas);
    } else {
      start();
    }
  }
})();
</script>
"""

# ---------------- build ----------------
src = open(INDEX, encoding='utf-8').read()

# 1. html lang + title + meta (Bangla default)
src = src.replace('<html lang="en">', '<html lang="bn">')
src = re.sub(r'<title>.*?</title>',
             '<title>Ahoor — সঠিক ব্যবসা খুঁজুন, নতুন সুযোগ তৈরি করুন।</title>', src, count=1, flags=re.S)
src = re.sub(r'<meta name="description" content="[^"]*">',
             '<meta name="description" content="Ahoor হলো বাংলাদেশের B2B ব্যবসার সুযোগের নেটওয়ার্ক — যা প্রয়োজন পোস্ট করুন, সরবরাহকারী ও প্রস্তুতকারক খুঁজুন, কোটেশন তুলনা করুন এবং পরবর্তী ব্যবসার সুযোগটি খুঁজে নিন।">', src, count=1)
src = re.sub(r'<meta property="og:title" content="[^"]*">',
             '<meta property="og:title" content="Ahoor — সঠিক ব্যবসা খুঁজুন, নতুন সুযোগ তৈরি করুন।">', src, count=1)
src = re.sub(r'<meta property="og:description" content="[^"]*">',
             '<meta property="og:description" content="Ahoor হলো বাংলাদেশের B2B ব্যবসার সুযোগের নেটওয়ার্ক — পোস্ট করুন, ম্যাচ হোক, কোটেশন পান, ডিল করুন।">', src, count=1)

# 2. fonts + i18n CSS
src = src.replace('FONT_BASE64', INTER_B64)
src = re.sub(r'/\* ============ Fonts: Bangla ============ \*/.*?(?=/\* ============ Tokens ============ \*/)', '', src, flags=re.S)
src = src.replace('/* ============ Tokens ============ */', FONT_CSS + '\n/* ============ Tokens ============ */', 1)

# 3. body + scripts
body = open(BODY, encoding='utf-8').read()
body = body.replace('</body>', I18N_JS + '\n' + MAIN_JS + '\n</body>', 1)
src = re.sub(r'<body>.*?</body>', body, src, count=1, flags=re.S)

open(INDEX, 'w', encoding='utf-8').write(src)
print("BUILD OK —", len(src), "bytes")
