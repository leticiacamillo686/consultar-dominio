from flask import Flask, request
import requests
import socket

app = Flask(__name__)

@app.route("/consulta")
def consulta():
    dominio = request.args.get("dominio", "")
    if not dominio:
        return "sem domínio,-,-"

    dominio = dominio.replace("http://", "").replace("https://", "").strip("/")
    rdap_url = f"https://rdap.org/domain/{dominio}"

    headers = {
        "User-Agent": "HTTPie/3.2.2",
        "Accept": "application/rdap+json",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }

    try:
        r = requests.get(rdap_url, headers=headers)
        if r.status_code == 404:
            ip = get_ip(dominio)
            return f"disponivel,-,{ip}"
        elif r.status_code != 200:
            ip = get_ip(dominio)
            return f"erro ({r.status_code}),-,{ip}"

        data = r.json()
        status = ",".join(data.get("status", [])).lower() or "sem status"

        exp = "-"
        for event in data.get("events", []):
            if event.get("eventAction") == "expiration":
                exp = event.get("eventDate", "").split("T")[0]
                break

        ip = get_ip(dominio)
        return f"{status},{exp},{ip}"

    except Exception:
        return "erro,-,-"

def get_ip(dominio):
    try:
        return socket.gethostbyname(dominio)
    except:
        return "-"
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
