#!/usr/bin/env python3
"""
Locksmith WhatsApp Outreach — Number Finder & Verifier
Run on YOUR laptop. Finds UAE locksmith WhatsApp numbers and generates outreach tool.
Usage: pip install requests && python3 find_locksmiths.py
"""
import requests, re, csv, time, urllib.parse

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# === STEP 1: Search Google for locksmith WhatsApp numbers ===
print("Step 1: Searching Google for locksmith WhatsApp numbers...")
queries = [
    "locksmith whatsapp number dubai 05",
    "locksmith whatsapp number abu dhabi 05",
    "key maker whatsapp number sharjah 05",
    "car key locksmith whatsapp dubai 05",
    "locksmith whatsapp 971",
    "key cutting whatsapp uae 05",
    "lock repair whatsapp dubai 05",
    "locksmith near me whatsapp uae 05",
    "locksmith mobile number uae 056",
    "locksmith mobile number uae 050",
    "locksmith mobile number uae 052",
    "locksmith mobile number uae 054",
    "locksmith mobile number uae 055",
    "locksmith mobile number uae 058",
]

all_phones = set()
for q in queries:
    try:
        r = requests.get(f"https://www.google.com/search?q={urllib.parse.quote(q)}&num=30", headers=headers, timeout=15)
        mobiles = re.findall(r'(?:\+?971[\s\-]?)?05\d[\s\-]?\d{3}[\s\-]?\d{4}', r.text)
        for m in mobiles:
            digits = re.sub(r'\D', '', m)
            if len(digits) >= 9 and digits[0] == '5':
                all_phones.add('971' + digits[-9:])
        print(f"  {q[:45]}: {len(mobiles)} found")
        time.sleep(2)
    except Exception as e:
        print(f"  {q[:45]}: failed")

print(f"\nFound {len(all_phones)} unique numbers")

# === STEP 2: Verify on WhatsApp ===
print("\nStep 2: Verifying numbers on WhatsApp...")
verified = []
for i, phone in enumerate(sorted(all_phones), 1):
    try:
        r = requests.get(f"https://wa.me/{phone}", headers=headers, timeout=10)
        t = r.text
        if 'whatsapp' in t.lower() and 'invalid' not in t.lower() and "doesn't" not in t.lower():
            verified.append(phone)
            print(f"  [{i}/{len(all_phones)}] YES {phone}")
        else:
            print(f"  [{i}/{len(all_phones)}] NO  {phone}")
    except:
        print(f"  [{i}/{len(all_phones)}] ERR {phone}")
    time.sleep(1)

print(f"\nWhatsApp verified: {len(verified)} out of {len(all_phones)}")

# === STEP 3: Generate outreach HTML ===
if verified:
    DUAL_MSG = """السلام عليكم،

لاحظنا إن نشاطكم التجاري مب ظاهر على خرائط قوقل (Google Maps). احنا نساعد محلات تصليح ونسخ المفاتيح في الإمارات — حتى لو تم تعليق الحساب من قبل.

مهتمين؟ ردوا بـ نعم ونرسل لكم التفاصيل.

gxlocate.com

---

Hi, we noticed your business may not be visible on Google Maps. We help UAE locksmith & key cutting businesses get verified — even if suspended before.

Interested? Reply YES and we'll share details.

gxlocate.com"""

    html = '<html><head><meta charset="utf-8"><title>Locksmith Outreach</title>'
    html += '<meta name="viewport" content="width=device-width,initial-scale=1">'
    html += '<style>body{font-family:Arial;max-width:600px;margin:10px auto;padding:10px;background:#e5ddd5}'
    html += '.bar{position:sticky;top:0;background:#075e54;color:white;padding:12px 16px;border-radius:12px;margin-bottom:10px;z-index:99;text-align:center}'
    html += '.bar h2{margin:0;font-size:17px}.bar p{margin:4px 0 0;font-size:13px;opacity:.85}'
    html += '.card{background:white;border-radius:10px;padding:12px 14px;margin:6px 0;display:flex;align-items:center;gap:10px}'
    html += '.num{font-weight:600;font-size:14px;color:#075e54;flex:1}'
    html += '.btn{padding:10px 18px;border-radius:22px;text-decoration:none;font-weight:600;font-size:13px;background:#25D366;color:white;white-space:nowrap}'
    html += '.btn:hover{background:#1da851}.done{opacity:.25;pointer-events:none}'
    html += '.idx{color:#999;font-size:11px;width:28px;text-align:right}</style></head><body>'
    html += f'<div class="bar"><h2>Locksmith Outreach UAE</h2><p id="ctr">0 / {len(verified)} sent</p></div>'
    
    for i, phone in enumerate(verified, 1):
        display = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:]}"
        wa_url = f"https://wa.me/{phone}?text={urllib.parse.quote(DUAL_MSG)}"
        html += f'<div class="card" id="c{i}"><span class="idx">#{i}</span><span class="num">{display}</span><a class="btn" href="{wa_url}" target="_blank" onclick="s({i})">Send</a></div>\n'
    
    html += f'<script>let c=0;function s(i){{document.getElementById("c"+i).classList.add("done");c++;document.getElementById("ctr").textContent=c+" / {len(verified)} sent"}}</script></body></html>'
    
    with open("locksmith_whatsapp_outreach.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nDone! Open locksmith_whatsapp_outreach.html")
else:
    print("\nNo verified numbers found. Try again or add more search queries.")

# Also save CSV
with open("locksmith_verified_numbers.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Phone", "Formatted"])
    for p in verified:
        w.writerow([p, f"+{p[:3]} {p[3:5]} {p[5:8]} {p[8:]}"])
print("CSV saved: locksmith_verified_numbers.csv")