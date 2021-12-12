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

### Beschreibung der Tags in diesem Dictionary:

- `tags` (notwendig): Gibt die Tags an, die einem Way hinzugefügt werden, wenn diese(s) Verkehrsschild(er) ausgewählt wird/werden.
- `remove` (optional): Gibt die Tags bzw. die spezifischen Tag-Value-Paare an, die entfernt werden, falls sie vorhanden sind
- `img` (notwendig): Gibt einen direkten Link zu einer .png-Datei an, die dieses Zeichen/diese Zeichenkombination zeigt, damit sie in der App angezeigt werden kann.
- `ipfs` (optional): Gibt den einen IPFS-Hash zu einer .png-Datei an, die dieses Zeichen/diese Zeichenkombination zeigt, damit sie in der App angezeigt werden kann.
- `wrong` (optional): Gibt an, ob eine Verkehrszeichenkombination "falsch"/"sinnlos" ist. Sollte weggelassen werden, wenn `false`
- `cat` (notwendig): Gibt die Kategorie des Zeichens an

### Genauere Erklärung und Verwendung der Tags innerhalb der App:

#### `remove`

Eigentlich sollte die App nur Daten zu Wegen hinzufügen, allerdings kann es sein, dass das einfache hinzufügen von Daten zu widersprüchlichen Daten führen kann. Wenn die App zum Beispiel einen Fußweg, der fälschlicherweise als gemeinsamer Fuß- und Radweg getaggt ist (`foot=designated;bicycle=designated`) einfach die Tags laut `tags` hinzufügt bzw. updated, würde im beschriebenen Szenario `bicycle=designated` bestehen bleiben. Das wäre widersprüchlich. Deswegen entfernt die App gewisse Kombinationen, die eventuell bereits vorhanden sind.
Wichtig hierbei zu erwähnen ist auch, dass die App absichtlich meistens nicht ganze Tags löscht, sondern nur bestimmte Kombinationen. Dadurch soll redundantes, aber prinzipiell korrektes Tagging bestehen bleiben. Einen Fußweg mit `bicycle=no` zu kennzeichnen ist technisch gesehen nicht notwendig, da das andere Tagging bereits impliziert, dass Fahrräder hier verboten sind. Aber da es faktisch korrekt ist, und wir bei OSM keine faktisch korrekten Daten löschen wollen, lasse ich diesen Tag so.

#### `ipfs`

Ich möchte, dass die App die Bilder möglichst aus dem IPFS abruft, sodass sie nicht vom funktionieren eines bestimmten Servers abhängig ist.

#### `wrong`

Manche Verkehrszeichenkombinationen sind "rechtlich gesehen nicht zulässig", "redundant", "falsch", "sinnlos", wie man es auch immer nennen möchte. 
Ein gutes Beispiel ist die Kombination der Zeichen "Fußweg" und "Radfahrer absteigen".  Auf einem Fußweg müssen Radfahrer sowieso absteigen, die Anweisung durch das Zusatzschild ist also redundant.
Allerdings orientiert sich diese App an der "on-the-ground-Regel" von OpenStreetMap. Heißt: Wenn es explizit ein Schild gibt, das etwas anweist, auch wenn die Anweisung eigentlich nicht notwendig ist, wird es mit getaggt.
So wird also "Fußweg" mit `foot=designated` getaggt, aber "Fußweg;Radfahrer absteigen" mit `foot=designated;bicycle=dismount`. Genau so wird "Fußweg;Fahrradfahren verboten" mit `foot=designated;biycle=no` getaggt, obwohl auch auf einem normalen Fußweg implizit `bicycle=no` gilt.
Ist der Schlüssel `wrong` auf `true` gesetzt (er sollte nicht vorhanden sein, wenn es nicht so ist) so wird diese Kombination in einem seperaten Abschnitt angezeigt. 

#### `cat`
Damit die Verkehrszeichen in der App geordnet werden können, haben sie alle eine Kategorie. Es gibt folgende Kategorien:

^ Nummer ^ Name ^
| 1 | Gebotszeichen |
| 2 | Verbotszeichen |
| 3 | Warnzeichen |
| 4 | Sonstige |

## Namenskonventionen der png-Dateien und Schlüsselwerte

Die Schlüssel der Dictionarys und die Namen der .png-Dateien folgen folgender Konvention:

- Es werden die offiziellen Nummern der Verkehrszeichen in Deutschland verwendet, auch, wenn diese von der Konvention in OpenStreetMap abweichen
- Die Nummern werden in der Reihenfolge aufgeschrieben, in der sie von oben nach unten am Mast hängen
- Bindestriche werden übernommen, `;` und `,` werden durch `_` ersetzt

