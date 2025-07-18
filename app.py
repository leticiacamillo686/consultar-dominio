from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/consulta")
def consulta():
    dominio = request.args.get("dominio", "")
    if not dominio:
        return "Sem domínio"

    dominio = dominio.replace("http://", "").replace("https://", "").strip("/")
    rdap_url = f"https://rdap.registro.br/domain/{dominio}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/rdap+json"
    }

    try:
        r = requests.get(rdap_url, headers=headers, timeout=10)
        if r.status_code == 404:
            return "disponivel,-"
        elif r.status_code != 200:
            return f"erro ({r.status_code}),-"

        data = r.json()
        status = ",".join(data.get("status", [])).lower() or "sem status"

        exp = "-"
        for event in data.get("events", []):
            if event.get("eventAction") == "expiration":
                exp = event.get("eventDate", "").split("T")[0]
                break

        return f"{status},{exp}"

    except Exception:
        return "erro,-"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
