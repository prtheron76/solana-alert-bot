import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

MIN_MC = 100000
seen = set()

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def fetch_tokens():
    url = "https://api.dexscreener.com/latest/dex/pairs/solana"
    return requests.get(url).json().get("pairs", [])

while True:
    try:
        pairs = fetch_tokens()

        for p in pairs:
            mc = p.get("fdv", 0)
            addr = p.get("pairAddress")
            name = p.get("baseToken", {}).get("symbol")
            link = p.get("url")

            if not addr or addr in seen:
                continue

            if mc and mc >= MIN_MC:
                seen.add(addr)

                send(f"🚨 SOLANA ALERT\n\n{name}\nMC: ${int(mc):,}\n{link}")

        time.sleep(20)

    except Exception:
        time.sleep(5)
