# Python HTTP Projekt

## Beschreibung

Dieses Projekt implementiert ein CLI-Tool in Python zur Demonstration
grundlegender Webtechnologien.

Das Programm kann:

-   HTTP GET Requests senden
-   HTTP POST Requests senden
-   Cookies anzeigen
-   HTML-Tags aus Webseiten auslesen (Scraping)
-   Webseiten mit Selenium und Chrome öffnen
-   Cookies und Screenshots über Selenium anzeigen

Das Tool wird über das Terminal gestartet und verwendet Python Libraries
wie `requests` und `selenium`.

------------------------------------------------------------------------

# Installation

## 1 Repository klonen

``` bash
git clone <git-url>
cd python-http-projekt
```

## 2 Python Umgebung erstellen

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3 Dependencies installieren

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

# Programm starten

Das Programm wird im Terminal gestartet mit:

``` bash
python myproject.py <command>
```

------------------------------------------------------------------------

# Commands

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Command                                                                    Beschreibung                   Beispiel
  -------------------------------------------------------------------------- ------------------------------ ------------------------------------------------------------------------------------------
  `python myproject.py "title"`                                              Zeigt Inhalt eines HTML Tags   `python myproject.py "title"`
                                                                             (z.B. `<title>`)               

  `python myproject.py scrape-tag --url <website> <tag>`                     Scraped ein bestimmtes HTML    `python myproject.py scrape-tag --url https://example.com title`
                                                                             Tag                            

  `python myproject.py get --url <website>`                                  Sendet einen HTTP GET Request  `python myproject.py get --url https://httpbin.org/get`

  `python myproject.py get --url <website> --param key=value`                GET Request mit URL Parametern `python myproject.py get --url https://httpbin.org/get --param a=1`

  `python myproject.py post --url <website> --field key=value`               Sendet einen HTTP POST Request `python myproject.py post --url https://httpbin.org/post --field name=miro`

  `python myproject.py list-cookies --url <website>`                         Zeigt Cookies einer Website    `python myproject.py list-cookies --url https://example.com`

  `python myproject.py selenium-title --url <website>`                       Öffnet Website mit Selenium    `python myproject.py selenium-title --url https://example.com`
                                                                             und zeigt Titel                

  `python myproject.py selenium-title --url <website> --show-browser`        Öffnet Chrome sichtbar         `python myproject.py selenium-title --url https://example.com --show-browser`

  `python myproject.py selenium-cookies --url <website>`                     Zeigt Cookies über Selenium    `python myproject.py selenium-cookies --url https://example.com`

  `python myproject.py selenium-screenshot --url <website> --out file.png`   Erstellt Screenshot einer      `python myproject.py selenium-screenshot --url https://example.com --out screenshot.png`
                                                                             Website                        
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Beispiel Output

GET Request:

    Status: 200 | Time: 120ms
    URL: https://httpbin.org/get?a=1

Scraping:

    Example Domain

------------------------------------------------------------------------

# Architektur

    Terminal
       │
       ▼
    CLI Parser (argparse)
       │
       ├── HTTP Funktionen
       │      ├── GET
       │      ├── POST
       │      └── Cookies
       │
       └── Selenium Funktionen
              ├── Browser öffnen
              ├── Title lesen
              ├── Cookies lesen
              └── Screenshot

------------------------------------------------------------------------

# Verwendete Technologien

-   Python 3
-   requests
-   selenium
-   webdriver-manager
-   argparse

------------------------------------------------------------------------

# Feature Dokumentation

  ------------------------------------------------------------------------
  Feature             Datei            Beschreibung
  ------------------- ---------------- -----------------------------------
  HTML Tag Scraping   myproject.py     Extrahiert HTML Tags aus Webseiten

  HTTP GET Request    myproject.py     Sendet GET Requests mit Parametern

  HTTP POST Request   myproject.py     Sendet POST Requests

  Cookie Anzeige      myproject.py     Zeigt Cookies über requests.Session

  Selenium Browser    myproject.py     Öffnet Webseiten mit Chrome

  Selenium Cookies    myproject.py     Liest Cookies aus Browser

  Screenshot          myproject.py     Speichert Screenshot einer Website
  ------------------------------------------------------------------------
