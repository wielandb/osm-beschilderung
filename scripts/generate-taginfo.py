import json
from datetime import datetime
# Dieses Skript generiert die taginfo.json für Taginfo

with open("definitions/signs.json", "r") as f:
    liste = json.loads(f.read())

TAGS = []

def get_signs_that_use(ut, uv):
    tmpsigns = []
    for item in liste:
        itval = item[list(item.keys())[0]]
        found = False
        for tvl in itval["tags"]:
            # Erstmal: Herausfinden, ob ut und uv in diesem Element sind
            for t, v in tvl.items():
                if t == ut and v == uv:
                    found = True
        if found:
            for tvl in itval["tags"]:
                # Dann: Schild zur Liste hinzufügen
                for t, v in tvl.items():
                    if t == "traffic_sign":
                        tmpsigns.append(v)
    if len(tmpsigns) > 5:
        more = str(len(tmpsigns[5:]))
        tmpsigns = tmpsigns[:5]
        tmpsigns.append("and " + more + " others")
    return tmpsigns

def get_signs_that_remove(ut, uv):
    tmpsigns = []
    for item in liste:
        itval = item[list(item.keys())[0]]
        found = False
        try:
            for tvl in itval["remove"]:
                # Erstmal: Herausfinden, ob ut und uv in diesem Element sind
                for t, v in tvl.items():
                    if t == ut and v == uv:
                        found = True
            if found:
                for tvl in itval["tags"]:
                    # Dann: Schild zur Liste hinzufügen
                    for t, v in tvl.items():
                        if t == "traffic_sign":
                            tmpsigns.append(v)
        except:
            pass
    if len(tmpsigns) > 5:
        more = str(len(tmpsigns[5:]))
        tmpsigns = tmpsigns[:5]
        tmpsigns.append("and " + more + " others")
    return tmpsigns                  

## Statische Tags

tmptag = {"key": "traffic_sign","object_types": ["way"],"description": "Main tag edited by this project"}
TAGS.append(tmptag)

## Tags, die hinzugefügt werden

for item in liste:
    itval = item[list(item.keys())[0]]
    for tvl in itval["tags"]:
        for t, v in tvl.items():
            if t == "traffic_sign":
                tmptag = {"key": t,"value": v,"object_types": ["way"],"description": "Added to represent signage"}
            else:
                tmptag = {"key": t,"value": v,"object_types": ["way"],"description": "Added/updated if implied by signage " + ", ".join(get_signs_that_use(t,v))}
            if tmptag not in TAGS:
                TAGS.append(tmptag)

## Tags, die entfernt werden

for item in liste:
    itval = item[list(item.keys())[0]]
    try:
        for tvl in itval["remove"]:
            for t, v in tvl.items():
                tmptag = {"key": t,"value": v,"object_types": ["way"],"description": "Removed as common tagging mistake for signage " + ", ".join(get_signs_that_remove(t,v))}
                if tmptag not in TAGS:
                    TAGS.append(tmptag)
    except KeyError:
        pass

TAGINFO =    {"data_format": 1, "data_url": "https://raw.githubusercontent.com/wielandb/osm-beschilderung/main/taginfo.json", "data_updated": datetime.strftime(datetime.now(), '%Y%m%dT%H%M%SZ'),"project": {"name": "osm-beschilderung","description": "An app to quickly add german traffic signs to OSM","project_url": "https://github.com/wielandb/osm-beschilderung", "doc_url": "https://github.com/wielandb/osm-beschilderung/blob/main/signs.md","icon_url": "https://raw.githubusercontent.com/wielandb/osm-beschilderung/main/images/appicon.png","contact_name": "Wieland Breitfeld", "contact_email": "mail@wielandbreitfeld.de" },"tags": TAGS}

with open("taginfo.json", "w") as f:
    f.write(json.dumps(TAGINFO, indent=4))
