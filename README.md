# userien

Server för att beräkna och summera poäng för tävlingsklasser i
Ungdomsserien i Linköping. OBS: Poängställningen är inte officiell.

## Installation

För att bygga och starta servern:
```
./dockerbuild.sh && ./dockerup.sh
```

Det kommer att starta en Docker-container som lyssnar på port 8080.
För att exponera den, använd en reverse proxy-server. Exempel för nginx:

```
location /userien/ {
    proxy_pass http://127.0.0.1:8080/;
}
```

## Användning

Ladda upp en IOF XML-fil med resultat (`ResultList`-element).
Servern har lagring där den senaste uppladdningen sparas för varje tävling
(unikt Eventor-ID). För att seriesammanställningen ska fungera, ladda upp en
slutgiltig resultat-fil efter att tävlingen är klar. `fetch-event-results.sh`
går att använda för att hämta resultat-filer på rätt format.
