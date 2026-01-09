import os
import requests, time, webbrowser
from bs4 import BeautifulSoup
from plyer import notification
from telegram import Bot

URL = "https://ojas.gujarat.gov.in/Preference.aspx?opt=LUbWdmhKlwjaHr%2fCUNi26A%3d%3d"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("❌ BOT_TOKEN or CHAT_ID missing in environment variables")
    exit()

bot = Bot(BOT_TOKEN)
found = False

KEYWORDS = [
    "Call Letter", "Download", "Hall Ticket", "Print",
    "Admit Card", "Print Call Letter", "Download Call Letter",
    "View Call Letter", "Generate Call Letter",
    "btnPrint", "btnDownload",
    "ctl00$ContentPlaceHolder1$BtnPrint",
    "ctl00$ContentPlaceHolder1$BtnDownload"
]

IGNORE_WORDS = [
    "Application not found",
    "Invalid Application",
    "No Record Found",
    "Details not found",
    "Try Again",
    "Enter Captcha",
    "Please enter"
]

print("🔍 OJAS Call Letter watcher started...")

while True:
    try:
        r = requests.get(URL, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text().lower()

        if any(w.lower() in text for w in IGNORE_WORDS):
            time.sleep(120)
            continue

        if any(k.lower() in text for k in KEYWORDS) and not found:
            found = True

            notification.notify(
                title="🚨 OJAS CALL LETTER AVAILABLE",
                message="Call Letter is LIVE! Fill captcha & download now.",
                timeout=10
            )

            bot.send_message(
                chat_id=CHAT_ID,
                text="🚨 *OJAS CALL LETTER LIVE!*\n\nOpen site NOW and fill captcha.",
                parse_mode="Markdown"
            )

            webbrowser.open(URL)

        time.sleep(120)

    except Exception as e:
        print("Error:", e)
        time.sleep(120)
