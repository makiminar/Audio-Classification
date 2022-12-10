# NI-VMM audio classification
* autoři: Martin Šír, Markéta Minářová

# Popis
Projekt slouží pro klasifikaci písniček. Použité jsou 2 metody, které jsou více popsány ve zprávě:
* `Song-wise Mfccs`
* `Centroid Mfccs`


## Spuštění
### Spuštění Backendu
* Pro backend je potřeba mít stažený Python.
* Dále je potřeba přejít do složky `server`.
* Dále aktivovat virtuální prostředí pomocí příkazu `.venv/bin/activate`.
* Dále už jen stačí spustit server pomocí příkazu `python -m flask --app app run`.
### Spuštění Frontendu
* Pro frontend je potřeba mít stažený Node.js.
* Dále je potřeba přejít do složky `nuxt-app`, která se nachází se složce `client`.
* Dále je potřeba stáhnout balíčky pomocí příkazu `npm install`.
* Dále už jen stačí spustit klienta pomocí příkazu `npm run dev`, který poté poběží na stránce `http://localhost:3000/`.
