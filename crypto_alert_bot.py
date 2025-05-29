import requests
import time

# === Configurare Telegram ===
TELEGRAM_TOKEN = 'AICI_PUI_TOKENUL_TAU'
CHAT_ID = '5308384382'

# === Lista monede și limite în USDT ===
monede = {
    'ETHUSDT': {'symbol': 'ETH', 'achizitie': 2245.17, 'limita_sus': 2800},
    'FETUSDT': {'symbol': 'FET', 'achizitie': 0.65, 'limita_sus': 1.2},
    'SOLUSDT': {'symbol': 'SOL', 'achizitie': 148.65, 'limita_sus': 180},
    'RNDRUSDT': {'symbol': 'RNDR', 'achizitie': 4.07, 'limita_sus': 5.5},
    'DOTUSDT': {'symbol': 'DOT', 'achizitie': 4.07, 'limita_sus': 5.5},
    'ARBUSDT': {'symbol': 'ARB', 'achizitie': 0.34, 'limita_sus': 0.6},
    'BTCUSDT': {'symbol': 'BTC', 'achizitie': 93072.29, 'limita_sus': 100000},
    'TAOUSDT': {'symbol': 'TAO', 'achizitie': 369.32, 'limita_sus': 500},
    'FILUSDT': {'symbol': 'FIL', 'achizitie': 2.47, 'limita_sus': 3.5},
}

def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    try:
        response = requests.get(url)
        data = response.json()
        return float(data['price'])
    except Exception as e:
        print(f"⚠️ Eroare la {symbol}: {e}")
        return None

def send_alert(mesaj):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': mesaj}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❗ Eroare la trimiterea mesajului Telegram: {e}")

# === Buclă de monitorizare ===
while True:
    print("\n🔄 Verificare prețuri în USDT...")
    for symbol_binance, info in monede.items():
        pret = get_price(symbol_binance)
        if pret is None:
            print(f"⚠️ Nu s-a putut obține prețul pentru {info['symbol']}")
            continue

        simbol = info['symbol']
        limita_jos = round(info['achizitie'] * 0.85, 4)
        limita_sus = info['limita_sus']

        print(f"{simbol}: {pret} USDT (Limite: {limita_jos} - {limita_sus})")

        if pret <= limita_jos:
            send_alert(f"📉 ALERTĂ: {simbol} a scăzut sub -15% ({pret} USDT)")
        elif pret >= limita_sus:
            send_alert(f"📈 ALERTĂ: {simbol} a depășit limita superioară ({pret} USDT)")

    time.sleep(5400)  # verifică la fiecare 90 de minute
