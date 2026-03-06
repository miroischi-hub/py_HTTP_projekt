# Dokumentation

## Virtuelle Umgebung aufsetzen

Um Selenium installieren und sauber mit Python arbeiten zu können, wurde eine **virtuelle Umgebung (.venv)** erstellt.  
Dadurch werden alle benötigten Pakete lokal im Projekt installiert und beeinflussen nicht das System.

---

## Pakete installieren

Zuerst werden die benötigten Python-Pakete installiert:

sudo apt update
sudo apt install -y python3-full python3-venv
Virtuelle Umgebung erstellen

---

## Danach wird im Projektordner eine virtuelle Umgebung erstellt:

python3 -m venv .venv

Dies erstellt den Ordner .venv, der eine eigene Python-Installation enthält.

---

## Virtuelle Umgebung aktivieren

Die Umgebung wird anschließend aktiviert:

source .venv/bin/activate

Wenn die Umgebung aktiv ist, erscheint im Terminal:

(.venv)

---

## Selenium installieren

Nun können benötigte Python-Bibliotheken installiert werden.

Zuerst wird pip aktualisiert:

pip install --upgrade pip

Danach wird Selenium installiert:

pip install selenium

Optional können auch weitere Bibliotheken installiert werden:

pip install requests webdriver-manager

---

## Arbeiten in der virtuellen Umgebung

Ab diesem Zeitpunkt wird das Projekt innerhalb der .venv Umgebung ausgeführt.
Alle Python-Befehle beziehen sich nun auf diese Umgebung.

Beispiel:

python3 /home/miro/Dokumente/Python-Projekt/test_selenium.py selenium-titel --url https://porsche.com

---

## Programm verwenden

Nachdem alle Abhängigkeiten installiert wurden, können die Funktionen des Programms verwendet werden.

Die verfügbaren Befehle sind in der Datei features.md dokumentiert.
