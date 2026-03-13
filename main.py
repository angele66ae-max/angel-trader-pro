def get_data():

    if not API_KEY or not API_SECRET:
        return None, "Faltan credenciales"

    base = "https://api.bitso.com"
    path = "/v3/balance/"

    nonce = str(int(time.time()*1000))

    message = nonce + "GET" + path

    signature = hmac.new(
        API_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Authorization": f"Bitso {API_KEY}:{nonce}:{signature}"
    }

    try:
        r = requests.get(base + path, headers=headers)

        if r.status_code == 200:
            return r.json()["payload"]["balances"], "OK"

        return None, f"Error {r.status_code}"

    except Exception as e:
        return None, str(e)
