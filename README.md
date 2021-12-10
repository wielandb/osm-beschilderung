# osm-beschilderung

Dieses Repository enthält Definitionsdateien und Bilder für eine App, mit der schnell Beschilderungen von Wegen zur OpenStreetMap-Datenbank hinzugefügt werden können.


## Erklärung der JSON-Datei

Die JSON-Datei ist eine Liste von Dictionarys. Hier ein Beispiel für ein solches Dictionary:

```
{"237":
	{
	"tags":
		[
			{"highway":"cycleway"},
			{"bicycle":"designated"},
			{"traffic_sign":"DE:237"}
		],
	"remove": 
		[
			{"foot":"yes"},
			{"foot":"designated"}
		],
	"img": "https://example.com/img/237.png",
	"ipfs": "QmQCjuMQ4m6FKZAG7onHgXVZHLKHSdEgyT6NNXR1pEDUqN",
	"wrong": false
	}
}
```

Erklärung der Tags in diesem Dictionary:

- `tags` (notwendig): Gibt die Tags an, die einem Way hinzugefügt werden, wenn diese(s) Verkehrsschild(er) ausgewählt wird/werden.
- `remove` (optional): Gibt die Tags bzw. die spezifischen Tag-Value-Paare an, die entfernt werden, falls sie vorhanden sind
- `img` (notwendig): Gibt einen direkten Link zu einer .png-Datei an, die dieses Zeichen/diese Zeichenkombination zeigt, damit sie in der App angezeigt werden kann.
- `ipfs` (optional): Gibt den einen IPFS-Hash zu einer .png-Datei an, die dieses Zeichen/diese Zeichenkombination zeigt, damit sie in der App angezeigt werden kann.
- `wrong` (optional): Gibt an, ob eine Verkehrszeichenkombination "falsch"/"sinnlos" ist. Sollte weggelassen werden, wenn `false`

## Namenskonventionen der png-Dateien und Schlüsselwerte

Die Schlüssel der Dictionarys und die Namen der .png-Dateien folgen folgender Konvention:

- Es werden die offiziellen Nummern der Verkehrszeichen in Deutschland verwendet, auch, wenn diese von der Konvention in OpenStreetMap abweichen
- Die Nummern werden in der Reihenfolge aufgeschrieben, in der sie von oben nach unten am Mast hängen
- Bindestriche werden übernommen, `;` und `,` werden durch `_` ersetzt

