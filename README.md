# Plinio Gold – dashboard sterline d’oro

PWA (installabile su telefono e computer) con capitale, plusvalenza e guadagno netto (imposta 26%) delle tue sterline.

## Pubblicare su GitHub

1. Crea un repository su GitHub e carica **tutti** i file di questa cartella (compresa `.github`), nel ramo `main`.
2. Vai in **Settings → Pages** e, in *Build and deployment → Source*, scegli **GitHub Actions**.
3. Vai in **Actions → Aggiorna quotazioni e pubblica → Run workflow**. Alla fine trovi l’indirizzo del sito in Settings → Pages.
4. Apri l’indirizzo dal telefono e scegli *Aggiungi a schermata Home* (iPhone) o *Installa app* (Android/Chrome).

## Come si aggiornano i dati

- Ogni giorno feriale (circa 16:30–17:30 ora italiana) GitHub esegue `scripts/aggiorna.py`, che legge la quotazione al denaro da Confinvest, la aggiunge a `data/storico.json` e ripubblica il sito.
- Il pulsante **Leggi quotazione** ricarica l’archivio. Se l’archivio è indietro, prova anche a leggere Confinvest direttamente tramite un servizio pubblico (`allorigins`), che può non funzionare. In ogni caso puoi aggiungere una quotazione a mano dal modulo in fondo alla pagina.
- Se la pagina di Confinvest cambia struttura, il workflow segnala che non trova la quotazione: bisogna adattare le espressioni regolari in `scripts/aggiorna.py` (e in `index.html`, funzione `parseConfinvest`).

## Modificare gli acquisti

Nel file `index.html`, costante `LOTS`: data, numero di monete e prezzo di ogni acquisto. Il tipo (`vc` vecchio conio, `nc` nuovo conio) decide quale quotazione usare. L’aliquota è `TAX`.

## Prova in locale

`python3 -m http.server` nella cartella, poi apri http://localhost:8000
