import json
import urllib.parse
from time import sleep
import requests

## Dieses Skript sortiert die Einträge in signs.json nach der Häufigkeit ihrer `traffic_sign`-Werte in der OSM-Datenbank

opq_1 = "http://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A60%5D%3B%0A%28%0A%20%20nwr%5B%22traffic_sign%22%3D%22"
opq_2 = "%22%5D%3B%0A%29%3B%0Aout%20count%3B"

def getFreq(ix):
    if isinstance(ix, dict):
        return int(ix[list(ix.keys())[0]]["frequency"])
    for vzix in range(len(alt_liste)):
        if vzix == ix:
            traffic_sign_key = list(alt_liste[vzix].keys())[0]
            return int(alt_liste[vzix][traffic_sign_key]["frequency"])
    return 99999999

### Schritt 0: Die Liste aus der Datei laden

with open("../definitions/signs.json", "r") as f:
    alt_liste = json.loads(f.read())

### Schritt 1: Für jede Verkehrszeichenkombination die Häufigkeit ermitteln

for vzix in range(len(alt_liste)):
    traffic_sign_dict = alt_liste[vzix]
    traffic_sign_key = list(alt_liste[vzix].keys())[0]
    traffic_sign_tags = traffic_sign_dict[list(alt_liste[vzix].keys())[0]]["tags"]
    for t in traffic_sign_tags:
        if "traffic_sign" in t.keys():
            traffic_sign = t["traffic_sign"]
    url = opq_1 + urllib.parse.quote_plus(traffic_sign) + opq_2
    ans = requests.get(url)
    if ans.status_code == 200:
        ansj = ans.json()
        freq = ansj["elements"][0]["tags"]["total"]
        print(traffic_sign_key + " - " + freq)
    sleep(20)
    alt_liste[vzix][traffic_sign_key]["frequency"] = int(freq)

### Schritt 2: Die Liste sortieren und abspeichern

neu_liste = sorted(alt_liste, reverse=True, key=lambda x: getFreq(x))

with open("../definitions/signs.json", "w") as f:
    f.write(json.dumps(neu_liste, indent=4))
