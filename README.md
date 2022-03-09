# Erstellen eines neuronalen Netzes zur Steuerung eines Roboterarmes durch neuronevolutionäre Algorithmen

Dieses Repository besteht aus 4 Jupyter Lab Notebooks
-NEAT Algorithmus zum entwickeln der knN,
-Umgebung zur Auswahl von möglichen Zielpunkten,
-Testumgebung für die entwickelten knN,
-Umgebung, in der man den Roboter mit Tasten steuern kann.

## Benötigte Pakete
* NEAT-Python
  ```sh
  pip install neat-python
  ```
* PyBullet
  ```sh
  pip install pybullet
  ```
  Die restlichen verwendeten Pakete werden häufiger in Python verwendet:
  * numpy
  * os
  * sys
  * time
  * math
  * random
  
Sollte die Visualisierung von NEAT-Python verwendet werden, wird noch 
* raphviz
  ```sh
  pip install graphviz
  ```
  benötigt.
## Umgebung zur Auswahl der Zielpunkte
Enthält zwei Möglichkeiten sich eine Liste von Zielpunkten erstellen zu lassen. Erstere bewegt den Roboter in zufällige Positionen, überprüft ob diese zulässig sind und fügt sie dann der Liste hinzu. Diese Methode wird für Versuche mit mehr als 3 Achsen empfohlen.
Die Zweite Variante, approximiert den Bereich der möglichen Zielpunkte als Hohlkugel um den Punkt 0,0,0.36 und nutzt diese, um Zielpunkte zu bestimmen.  Diese Zielpunkte lassen sich auch auf nur bestimmte Bereiche eingrenzen. Wird für Versuche mit 3 oder weniger Achsen empfohlen.

## NEAT Algorithmus
Eigentliche Hauptaufgabe dieser Arbeit. Vor Anwendung sollten die verwendete Config Datei und die dem knN gegeben Inputs überprüft werden. Auch muss die Anzahl der Verwendeten Achsen mit den in der Config Datei beschriebenen Anzahl an Outputs übereinstimmen
Benötigt des weitern auch eine Datei mit den gesuchten Zielpunkten. Bei Verwendung auf dem Pixelflux Server, GUI unbedingt aus False setzen. Sämtliche Einstellungen können hier zu Beginn vorgenommen werden, mit Ausnahme der Inputs des knN. Diese müssen weiter unten in einem markierten Bereich vorgenommen werden. Es werden verschiedene Beispiele für Inputs gegeben.
Dieses Notebook wurde so geschrieben, um möglichst adaptive zu sein und schnell verändert werden kann für einen neuen Versuch.

## Testumgebung
Enthält eine Umgebung, in die von NEAT entwickelte knN geladen werden und getestet werden können. Bestimmt die Distanz nach jedem Zielpunkt und gibt Kollisionen an. Kann schnell um zusätzliche Funktionen erweitert werden, wenn gewünscht.

## Roboter Umgebung
Hier kann ein Roboter einfach über Tasten gesteuert werden. Erlaubt es, maximal Punkte zu überprüfen oder einfach sich selbst mit dem Roboter vertraut zu machen.

## Src
Der src Ordner enthält die zur Simulation des Roboter verwendete Klasse mit allen Funktionen zur Steuerung des Roboter. Diese ist zwar für den Kuka Iiwa ausgelegt, kann aber mit ein paar Änderung auf ein anderes Roboter Modell angewendet werden.
