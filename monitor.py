import json
import os
import urllib.request

STATE_FILE = "state.json"
CONFIG_FILE = "markets.json"
DEFAULT_THRESHOLD_PCT = 1.0  # pontos percentuais de variação para disparar alerta

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_market(event_slug, market_slug):
    """Busca o evento na API publica (Gamma) e acha o mercado (candidato) pelo slug dele."""
    url = f"https://gamma-api.polymarket.com/events?slug={event_slug}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.load(r)
    if not data:
        return None
    event = data[0]
    for m in event.get("markets", []):
        if m.get("slug") == market_slug:
            prices = json.loads(m["outcomePrices"])  # ex: ["0.62", "0.38"]
            return {
                "question": m.get("question", market_slug),
                "price_yes": float(prices[0]),
            }
    return None


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg}).encode()
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req, timeout=15)


def load_json(path, default):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def main():
    markets = load_json(CONFIG_FILE, [])
    state = load_json(STATE_FILE, {})

    changed = False
    for m in markets:
        event_slug = m["event_slug"]
        market_slug = m["market_slug"]
        key = market_slug  # chave usada no state.json
        label = m.get("label", market_slug)
        threshold = float(m.get("threshold_pct", DEFAULT_THRESHOLD_PCT))

        try:
            info = fetch_market(event_slug, market_slug)
        except Exception as e:
            print(f"Erro ao buscar {label}: {e}")
            continue

        if not info:
            print(f"Mercado nao encontrado: {label}")
            continue

        current = info["price_yes"]
        last = state.get(key)

        if last is None:
            # primeira execucao para esse mercado: so guarda o preco base, sem alerta
            state[key] = current
            changed = True
            print(f"{label}: preco inicial registrado em {current*100:.1f}%")
            continue

        diff_pct = abs(current - last) * 100  # em pontos percentuais
        if diff_pct >= threshold:
            direction = "subiu" if current > last else "caiu"
            send_telegram(
                f"⚠️ {label}\n"
                f"{direction} de {last*100:.1f}% para {current*100:.1f}% "
                f"(variação de {diff_pct:.1f} pontos)"
            )
            state[key] = current
            changed = True
            print(f"{label}: ALERTA disparado ({last*100:.1f}% -> {current*100:.1f}%)")
        else:
            print(f"{label}: {current*100:.1f}% (sem variação relevante)")

    if changed:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)


if __name__ == "__main__":
    main()
