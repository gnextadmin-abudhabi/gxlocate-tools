#!/usr/bin/env python3
"""Locksmith WhatsApp Outreach — all numbers, no verification step."""
import requests, re, csv, time, urllib.parse

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
all_phones = set()

print("Scraping Yellow Pages UAE for locksmith WhatsApp numbers...")
for page in range(1, 11):
    url = f"https://www.yellowpages-uae.com/uae/locksmith/{page}"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        mobiles = re.findall(r'(?:\+?971[\s\-]?)?05\d[\s\-]?\d{2}[\s\-]?\d{2}[\s\-]?\d{2}', r.text)
        for m in mobiles:
            digits = re.sub(r'\D', '', m)
            if len(digits) >= 9 and digits[0] == '5':
                all_phones.add('971' + digits[-9:])
        print(f"  Page {page}: {len(mobiles)} found (total: {len(all_phones)})")
        time.sleep(1)
    except Exception as e:
        print(f"  Page {page}: error")

print(f"\nTotal: {len(all_phones)} UAE mobile numbers")

if not all_phones:
    print("No numbers found. Check your internet connection.")
    exit()

# === Generate outreach HTML ===
DUAL_MSG = """%D8%A7%D9%84%D8%B3%D9%84%D8%A7%D9%85 %D8%B9%D9%84%D9%8A%D9%83%D9%85%D8%8C

%D9%84%D8%A7%D8%AD%D8%B8%D9%86%D8%A7 %D8%A5%D9%86 %D9%86%D8%B4%D8%A7%D8%B7%D9%83%D9%85 %D8%A7%D9%84%D8%AA%D8%AC%D8%A7%D8%B1%D9%8A %D9%85%D8%A8 %D8%B8%D8%A7%D9%87%D8%B1 %D8%B9%D9%84%D9%89 %D8%AE%D8%B1%D8%A7%D8%A6%D8%B7 %D9%82%D9%88%D9%82%D9%84 (Google Maps). %D8%A7%D8%AD%D9%86%D8%A7 %D9%86%D8%B3%D8%A7%D8%B9%D8%AF %D9%85%D8%AD%D9%84%D8%A7%D8%AA %D8%AA%D8%B5%D9%84%D9%8A%D8%AD %D9%88%D9%86%D8%B3%D8%AE %D8%A7%D9%84%D9%85%D9%81%D8%A7%D8%AA%D9%8A%D8%AD %D9%81%D8%A7%D9%84%D8%A5%D9%85%D8%A7%D8%B1%D8%A7%D8%AA %E2%80%94 %D8%AD%D8%AA%D9%89 %D9%84%D9%88 %D8%AA%D9%85 %D8%AA%D8%B9%D9%84%D9%8A%D9%82 %D8%A7%D9%84%D8%AD%D8%B3%D8%A7%D8%A8 %D9%85%D9%86 %D9%82%D8%A8%D9%84.

%D9%85%D9%87%D8%AA%D9%85%D9%8A%D9%86%D8%9F %D8%B1%D8%AF%D9%88%D8%A7 %D8%A8%D9%80 %D9%86%D8%B9%D9%85 %D9%88%D9%86%D8%B1%D8%B3%D9%84 %D9%84%D9%83%D9%85 %D8%A7%D9%84%D8%AA%D9%81%D8%A7%D8%B5%D9%8A%D9%84.

gxlocate.com

---

Hi, we noticed your business may not be visible on Google Maps. We help UAE locksmith businesses get verified - even if suspended before.

Interested? Reply YES.

gxlocate.com"""

phones_list = sorted(all_phones)
total = len(phones_list)

html = '<html><head><meta charset="utf-8"><title>Locksmith Outreach</title>'
html += '<meta name="viewport" content="width=device-width,initial-scale=1">'
html += '<style>body{font-family:Arial;max-width:600px;margin:10px auto;padding:10px;background:#e5ddd5}'
html += '.bar{position:sticky;top:0;background:#075e54;color:white;padding:12px 16px;border-radius:12px;margin-bottom:10px;z-index:99;text-align:center}'
html += '.bar h2{margin:0;font-size:17px}.bar p{margin:4px 0 0;font-size:13px;opacity:.85}'
html += '.card{background:white;border-radius:10px;padding:12px 14px;margin:6px 0;display:flex;align-items:center;gap:10px}'
html += '.num{font-weight:600;font-size:14px;color:#075e54;flex:1}'
html += '.btn{padding:10px 18px;border-radius:22px;text-decoration:none;font-weight:600;font-size:13px;background:#25D366;color:white;white-space:nowrap}'
html += '.done{opacity:.25;pointer-events:none}'
html += '.idx{color:#999;font-size:11px;width:28px;text-align:right}</style></head><body>'
html += f'<div class="bar"><h2>Locksmith Outreach UAE</h2><p id="ctr">0 / {total} sent</p></div>'

for i, phone in enumerate(phones_list, 1):
    display = f"+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:]}"
    wa_url = f"https://wa.me/{phone}?text={DUAL_MSG}"
    html += f'<div class="card" id="c{i}"><span class="idx">#{i}</span><span class="num">{display}</span><a class="btn" href="{wa_url}" target="_blank" onclick="s({i})">Send</a></div>'

html += f'<script>let c=0;function s(i){{document.getElementById("c"+i).classList.add("done");c++;document.getElementById("ctr").textContent=c+" / {total} sent"}}</script></body></html>'

with open("locksmith_whatsapp_outreach.html", "w", encoding="utf-8") as f:
    f.write(html)
with open("locksmith_numbers.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Phone"])
    for p in phones_list:
        w.writerow([p])

print(f"\nDone! {total} numbers in locksmith_whatsapp_outreach.html")
print("Open the file and click Send on each card.")
