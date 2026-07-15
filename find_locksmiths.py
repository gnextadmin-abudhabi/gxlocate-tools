#!/usr/bin/env python3
"""Locksmith WhatsApp Outreach — scrapes UAE business directories directly."""
import requests, re, csv, time, urllib.parse

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

all_phones = set()

# === Directly scrape Yellow Pages UAE locksmith pages ===
print("Scraping Yellow Pages UAE for locksmith numbers...")
for page in range(1, 11):
    url = f"https://www.yellowpages-uae.com/uae/locksmith/{page}"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        # Find all UAE mobile numbers (05x pattern)
        mobiles = re.findall(r'(?:\+?971[\s\-]?)?05\d[\s\-]?\d{2}[\s\-]?\d{2}[\s\-]?\d{2}', r.text)
        for m in mobiles:
            digits = re.sub(r'\D', '', m)
            if len(digits) >= 9 and digits[0] == '5':
                all_phones.add('971' + digits[-9:])
        print(f"  Page {page}: {len(mobiles)} numbers found")
        time.sleep(1.5)
    except Exception as e:
        print(f"  Page {page}: error — {e}")

print(f"\nFound {len(all_phones)} unique mobile numbers")

# === Verify on WhatsApp ===
print("\nVerifying on WhatsApp (this takes ~2 min)...")
verified = []
total = len(all_phones)
for i, phone in enumerate(sorted(all_phones), 1):
    try:
        r = requests.get(f"https://wa.me/{phone}", headers=headers, timeout=10)
        t = r.text.lower()
        # Check if WhatsApp page says "Continue to Chat" or shows the chat UI
        has_wa = ('whatsapp' in t or 'continue to chat' in t.lower()) and 'invalid' not in t
        if has_wa:
            verified.append(phone)
            print(f"  [{i}/{total}] YES {phone}")
        else:
            pass  # skip silently
    except:
        pass
    time.sleep(0.8)

print(f"\nWhatsApp verified: {len(verified)} out of {total}")

# === Generate outreach HTML ===
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
        html += f'<div class="card" id="c{i}"><span class="idx">#{i}</span><span class="num">{display}</span><a class="btn" href="{wa_url}" target="_blank" onclick="s({i})">Send</a></div>'
    html += f'<script>let c=0;function s(i){{document.getElementById("c"+i).classList.add("done");c++;document.getElementById("ctr").textContent=c+" / {len(verified)} sent"}}</script></body></html>'
    
    with open("locksmith_whatsapp_outreach.html", "w", encoding="utf-8") as f:
        f.write(html)
    with open("locksmith_verified_numbers.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Phone","Formatted"])
        for p in verified:
            w.writerow([p, f"+{p[:3]} {p[3:5]} {p[5:8]} {p[8:]}"])
    print(f"\nDone! Open locksmith_whatsapp_outreach.html")
else:
    print("\nNo verified WhatsApp numbers found.")
