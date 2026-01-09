import os, time, requests

URL = "https://ojas.gujarat.gov.in/Preference.aspx?opt=LUbWdmhKlwjaHr%2fCUNi26A%3d%3d"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("BOT_TOKEN or CHAT_ID missing")
    exit()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"
}

DETECT_PATTERNS = [
    "f_popup(",
    "printcallletter.aspx",
    "window.open("
]

IGNORE_PATTERNS = [
    "incorrect captcha",
    "application not found",
    "invalid application"
]

found = False
last_ping = 0

print("🚀 OJAS Call Letter Watcher Running...")

while True:
    try:
        r = requests.get(URL, headers=HEADERS, timeout=20)
        html = r.text.lower()

        # Heartbeat every 10 minutes
        if time.time() - last_ping > 600:
            print("⏱ Still watching OJAS...")
            last_ping = time.time()

        if any(x in html for x in IGNORE_PATTERNS):
            time.sleep(60)
            continue

        if any(p in html for p in DETECT_PATTERNS) and not found:
            found = True
            msg = "🚨 OJAS CALL LETTER LIVE!\nOpen OJAS site now & fill captcha immediately."
            requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                params={"chat_id": CHAT_ID, "text": msg}
            )
            print("✅ Call Letter detected & Telegram alert sent.")

        time.sleep(60)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(60)
