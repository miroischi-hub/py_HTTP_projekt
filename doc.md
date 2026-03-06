## Dokumentation ##
### 1. Virtuelle Umgebung aufsetzen ###
Ich musste eine virtuelle Umgebung aufsetzen damit ich Selenium installieren konnte.

------------------------------------------------

Packete installieren:

sudo apt update
sudo apt install -y python3-full python3-venv

------------------------------------------------

Virtuelle Umgebung anlegen:

python3 -m venv .venv

------------------------------------------------

Aktivieren:

source .venv/bin/activate

------------------------------------------------

Selenium installieren:

pip install --upgrade pip
pip install selenium

------------------------------------------------

Ab jetzt arbeite ich in der .venv Umgebung

------------------------------------------------

Nun kann man mit hilfe der Befehle im features.md die befehle ausführen.
