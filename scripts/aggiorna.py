#!/usr/bin/env python3
"""Legge le quotazioni (denaro) delle sterline da Confinvest e le aggiunge a data/storico.json.

Uso:  python scripts/aggiorna.py            (scarica la pagina)
      python scripts/aggiorna.py --file p.html   (prova su una pagina salvata)
"""
import json, re, sys, html, urllib.request
from pathlib import Path

URL = "https://www.confinvest.it/quotazioni/"
STORICO = Path(__file__).resolve().parent.parent / "data" / "storico.json"


def scarica():
    req = urllib.request.Request(URL, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def leggi(pagina):
    t = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", pagina, flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"\s+", " ", t)
    d = re.search(r"Quotazioni indicative del (\d{2})-(\d{2})-(\d{4})", t, re.I)
    v = re.search(r"Sterlina Vecchio Conio\s*\|?\s*([\d.]+,\d{2})", t, re.I)
    n = re.search(r"Sterlina Nuovo Conio\s*\|?\s*([\d.]+,\d{2})", t, re.I)
    if not (d and v and n):
        return None
    num = lambda s: float(s.replace(".", "").replace(",", "."))
    return f"{d[3]}-{d[2]}-{d[1]}", num(v[1]), num(n[1])


def main():
    pagina = Path(sys.argv[2]).read_text(encoding="utf-8") if len(sys.argv) > 2 and sys.argv[1] == "--file" else scarica()
    q = leggi(pagina)
    if not q:
        print("Quotazione non trovata: la pagina potrebbe essere cambiata.")
        sys.exit(1)
    storico = json.loads(STORICO.read_text(encoding="utf-8"))
    per_data = {r[0]: r for r in storico}
    nuovo = per_data.get(q[0]) != list(q)
    per_data[q[0]] = list(q)
    if nuovo:
        STORICO.write_text(json.dumps(sorted(per_data.values()), separators=(",", ":")), encoding="utf-8")
    print(("Aggiornato: " if nuovo else "Già presente: ") + f"{q[0]}  v.c. {q[1]}  n.c. {q[2]}")


if __name__ == "__main__":
    main()
