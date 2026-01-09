import os, time, requests
from telegram import Bot

URL = "https://ojas.gujarat.gov.in/Preference.aspx?opt=LUbWdmhKlwjaHr%2fCUNi26A%3d%3d"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("BOT_TOKEN or CHAT_ID missing")
    exit()

bot = Bot(BOT_TOKEN)
found = False

DETECT_PATTERNS = [
    "f_popup(",
    "printcallletter.aspx",
    "window.open("
]

print("OJAS Call Letter Watcher Running...")

while True:
    try:
        r = requests.get(URL, timeout=20)
        html = r.text.lower()

        if any(p in html for p in DETECT_PATTERNS) and not found:
            found = True
            bot.send_message(
                chat_id=CHAT_ID,
                text="🚨 OJAS CALL LETTER WINDOW ENABLED!\nOpen OJAS site now and fill captcha."
            )
            print("Call Letter detected!")

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
