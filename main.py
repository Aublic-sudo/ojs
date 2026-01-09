import os, time, threading, requests
from flask import Flask

URL = "https://ojas.gujarat.gov.in/Preference.aspx?opt=LUbWdmhKlwjaHr%2fCUNi26A%3d%3d"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

app = Flask(__name__)

@app.route("/")
def home():
    return "OJAS Watcher Running..."

DETECT_PATTERNS = [
    "f_popup(",
    "printcallletter.aspx",
    "window.open("
]

def watcher():
    found = False
    print("🚀 OJAS Call Letter Watcher Started...")
    while True:
        try:
            r = requests.get(URL, timeout=20)
            html = r.text.lower()

            if any(p in html for p in DETECT_PATTERNS) and not found:
                found = True
                requests.get(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    params={"chat_id": CHAT_ID,
                            "text": "🚨 OJAS CALL LETTER LIVE!\nOpen OJAS site now & fill captcha."}
                )
                print("✅ Alert sent to Telegram")

            time.sleep(60)
        except Exception as e:
            print("Error:", e)
            time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=watcher, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
