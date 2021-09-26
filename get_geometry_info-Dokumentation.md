**Projektinfo laden :**

{server}/dqart/{fingerprint}:handshake}/project\_utilities/get\_geometry\_info/{project\_id}/{level\_of\_detail}/{with\_product\_information}/{with\_roller\_conveyor\_information}/{with\_materials}

*   server {string} ist der Server auf dem das Projekt liegt. Produktivsystem ist **item.engineering**
    
*   finterprint und handshake sind hier optional, es kann stattdessen auch "0:DEde" verwendet werden
    
*   project\_id {string} - Projeknummer oder C-Artikelnummer
    
*   level\_of\_detail {0, 1, 2} - Detailgrad (0 : niedrig, 1 : mittel, 2 : hoch)
    
*   with\_product\_information {0,1} - ob zu den Geometriedaten noch length, name, g\_id und art enthalten sein soll
    
*   with\_roller\_conveyor\_information {0,1} - ob zu den Geometriedaten noch für Rollenbahnen Anfangs und Endpunkt enthalten sein soll
    
*   with\_materials {0,1} - ob neben den objekten ebenso die materialien mit übergeben werden sollen. _Achtung : Das wiedergegebene Objekt hat eine andere Struktur um die Materialien mit zu übergeben. Dies ist allerding um Konsistenz mit bestehenden Systemen zu gewährleisten nur der Fall, wenn dieser Parameter als true übergeben wird._
    

Rückgabe hat folgende Form :

with\_materials = false :

```
 {
	"p": {
        part_id: {
			"g": [
				{
					"m": model,
					"s": scale,
					"p": position, 
					"r": rotation,
				}, 
				...
			],
			"length": length,
			"name": product_name,
			"g_id": group_id,
			"art": article_number
			"roller_conveyor": roller_conveyor
		}, 
		…
	}
}
```

with\_materials = true :

```
{
	"p": {
		"objects":{
            part_id: {
				"g": [
					{
						"m": model,
						"s": scale,
						"p": position, 
						"r": rotation,
						"material": material_id 
					}, 
					...
				],
				"length": length,
				"name": product_name,
				"g_id": group_id,
				"art": article_number
				"roller_conveyor": roller_conveyor
			}, 
			…
		},
		"materials": { 
			material_id : {
				"ambient":,
				"color":,
				"specular":,
				"shinyness":,
				"type":,
				"opacity":
			}, 
			…
		}
	}
}
```

*   part\_id {string} - Eindeutige ID des Produkts im Projekt
    
*   model {string} - Geometriepfad (siehe Anfrage unten) oder Grundgeometrie (cube, cylinder, ball oder cone)
    
*   scale {vector} - Skalierung der Geometrie
    
*   positon {vector} - Absolute Position der Geometrie
    
*   rotation {vector} - Absolute Rotation der Geometrie (als XYZ Eulerwinkel)
    
*   length {number} - Länge des Produkts (für Profile und Rollenbahnen) (optional)
    
*   name {string} - Produkname (optional)
    
*   g\_id {string} - Gruppen ID des Produkts (identische Teile werden zur gleichen Gruppen ID zusammengefasst - entspricht unserer Positionsnummer) (optional)
    
*   art {number} - Artikelnummer des Produkts (optional)
    
*   roller\_conveyor {vector\[\]} - Enthält Anfangs- und Endpunkt einer Rollenbahn (optional)
    
*   material\_id {number} (optional) - eindeutige ID eines Materials
    
*   ambient {string} (optional) - color hex
    
*   color {string} (optional) - color hex
    
*   specular {string} (optional) - color hex
    
*   type {string} (optional) - Gibt den Materialtyp an (basic, phong oder lambert)
    
*   opacity {number} (optional) - ∈ \[0,1\]
    

Beispielaufruf für Projekt 40afa1e3886fecd2adc719793b1414971 :

![](https://item24.atlassian.net/wiki/download/attachments/2106490885/image-20210920-145550.png?api=v2)

[https://item.engineering/dqart/0:DEde/project\_utilities/get\_geometry\_info/40afa1e3886fecd2adc719793b1414971/1/1/1/1](https://item.engineering/dqart/0:DEde/project_utilities/get_geometry_info/40afa1e3886fecd2adc719793b1414971/1/1/1/1)

Liefert folgendes Ergebnis :

```
{
	"0": 0,
	"p": {
		"objects": {
			"1": {
				"length": 200,
				"name": "Rollenbahn St D30, grau",
				"g_id": "1",
				"art": "63753",
				"roller_conveyor": [{
					"x": 0,
					"y": -117.38,
					"z": -165.46
				}, {
					"x": 0,
					"y": 165.46,
					"z": 117.38
				}],
				"g": [{
					"m": "objects\/457\/g\/2\/3.obj",
					"s": {
						"x": 1,
						"y": 1,
						"z": 200
					},
					"p": {
						"x": 11.5,
						"y": 70.71,
						"z": 96.17
					},
					"r": {
						"x": -45,
						"y": 0,
						"z": 0
					},
					"material": 1
				}, {
					"m": "cube",
					"s": {
						"x": 11.5,
						"y": 14,
						"z": 100
					},
					"p": {
						"x": 11.5,
						"y": 86.97,
						"z": 79.9
					},
					"r": {
						"x": -45,
						"y": 0,
						"z": 0
					},
					"material": 1
				}]
			}
		},
		"materials": {
			"1": {
				"ambient": "#8f8f98",
				"color": "#bdbfc8",
				"specular": "#adb3bc",
				"shinyness": 30,
				"type": "basic",
				"opacity": 1
			}
		}
	}
}
```

**Geometrien Anfragen** :

 {server}/objectPoolData/{geometry\_path}

geometry\_path {string} - hat die Form "objects/…/g/…/….obj"

 liefert obj Zurück

Beispielaufruf : [https://item.engineering/objectPoolData/objects/8/g/4/3.obj](https://src.i24.ws/objectPoolData/objects/8/g/4/3.obj)