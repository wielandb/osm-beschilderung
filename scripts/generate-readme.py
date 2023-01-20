import json

with open("definitions/signs.json", "r") as f:
    liste = json.loads(f.read())

with open("README.md", "r") as f:
    readme = f.read()

MD = "| Bild | Hinzugefügte Tags | Entfernte Tags | Kategorie | Häufigkeit in der OSM-Datenbank | " + "\n" + "|:----:|:-----------------:|:--------------:|:---------:|:-------------------------------:| " + "\n"

for item in liste:
    itval = item[list(item.keys())[0]]
    addtagstr = ""
    for t in itval["tags"]:
        addtagstr += "`" + str(list(t.keys())[0]) + "=" + str(t[list(t.keys())[0]]) +  "`<br>"
    remtagstr = ""
    if "remove" in itval.keys():
        for t in itval["remove"]:
            remtagstr += "`" + str(list(t.keys())[0]) + "=" + str(t[list(t.keys())[0]]) +  "`<br>"
    cats = ["", "Gebotszeichen", "Verbotszeichen", "Warnzeichen", "Sonstige"]
    catstr = cats[itval["cat"]]
    MD += "| ![](" + itval["img"] + ") | " + addtagstr + " | " + remtagstr + " | " + catstr + " | " + str(itval["frequency"]) + " |" + "\n" 

with open("signs.md", "w") as f:
    f.write(MD)