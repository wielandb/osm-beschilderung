import json
import urllib.parse
from time import sleep
import requests
import os

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


def getFreqOnline(ts):
    ans = requests.get("https://taginfo.openstreetmap.org/api/4/tag/stats?key=traffic_sign&value=" + str(ts))
    if ans.status_code == 200:
        J = ans.json()
        return J["data"][0]["count"]
    else:
        return 0


# A function that checks if the current working directory is the root of the project or the scripts folder
def check_cwd():
    if os.getcwd().split("/")[-1] == "scripts":
        os.chdir("..")        


### Schritt 0: Die Liste aus der Datei laden

check_cwd()

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
    freq = getFreqOnline(traffic_sign)
    print(traffic_sign_key + " - " + str(freq))
    alt_liste[vzix][traffic_sign_key]["frequency"] = int(freq)

### Schritt 2: Die Liste sortieren und abspeichern

neu_liste = sorted(alt_liste, reverse=True, key=lambda x: getFreq(x))

with open("definitions/signs.json", "w") as f:
    f.write(json.dumps(neu_liste, indent=4))
