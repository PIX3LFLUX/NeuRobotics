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
  ```sh
  pip install numpy
  ```
  * os
  * sys
  * time
  * math
  * random
  
Sollte die Visualisierung von NEAT-Python verwendet werden, wird noch 
* graphviz
  ```sh
  pip install graphviz
  ```
  benötigt. Das File zur Visualisierung der knN visualize.py kann in [NEAT-python](https://github.com/CodeReclaimers/neat-python/tree/master/examples/xor) gefunden werden.
  
  
## Setup
  1. Repositiory klonen
  2. Mit CreatePositions.ipynb Zielpositionen für die gewünschte Anzahl an Achsen bestimmen.
  3. Einstellungen in der zweiten Zelle von NEAT-Robot.ipynb für den gewünschten Ansatz anpassen. Sollte der Pixelflux Server verwendet werden GUI UNBEDINGT auf FALSE setzen. Sonst bricht dieser sofort nach Start ab.
  4. In der dritten Zelle von NEAT-Robot.ipynb die gewünschten Inputs, welche das knN erhalten soll, in dem markierten Bereich anpassen. Dafür sind bereits in den Kommentaren Vorschläge enthalten. Wichtig dabei ist: nur einzelne Variablen als Inputs geben, keine Arrays/Listen.
  5. Conifg Datei Anpassen. Hierbei sollte vor allem die Anzahl der Inputs und Outputs an die in 3. und 4. vorgenommenen Einstellungen angepasst werden. Fitness anpassen, je nachdem ob die Orientierung des Endeffektors mit beachtet werden soll (Hier hat die Fitnessfunktion einen Wertebereich von [0,200]) oder nicht (Wertebereich von [0,100]). Für die restliche Einstellungen können verschiedene Werte überprüft werden. Die hier verwendeten entsprechen den Werten, welche in der Conifg Datei von [NEAT-python](https://github.com/CodeReclaimers/neat-python/tree/master) vorgeschlagen werden. Je nach verwendetem Prozessor bietet es sich an die Anzahl der knN pro Generation (pop_size) höher oder niedriger zu setzen. Ein höherer Wert bedeutet, es werden mehrere Roboter gleichzeitg simuliert. Dies benötigt eine größere Rechenleistung. Nach jeder Änderung das speichern, sonst werden diese nicht übernommen.
  6. In NEAT-Roboter.ipynb die einzelnen Zellen nacheinander ausführen. Die vierte Zelle startet den NEAT-Algorithmus. Es speichert das beste knN als winner-ctrnn ab. Dieses sollte nach jedem Versuch umbennant werden, um ein überschreiben zu verhindern.

## Setup Testumgebung
1. Das neuronale Netz, welches getestet werden soll, und die Zielpositionen in der zweiten Zelle von NEAT-Roboter-Test.ipynb. Anzahl der Achsen und getesteten Punkte festlegen.
2. In der vierten Zelle die Inputs anpassen. Diese müssen den Inputs entsprechen, welche in NEAT-Roboter.ipynb verwendet wurden. Auch die Reihenfolge ist hierbei einzuhalten. Sollte die Visualisierung verwendet werden, die entsprechenden Zeilen auskommentieren und die Namen der Inputs und Outputs anpassen. Bei node_names entspricht -1 dem 1. input, -2 dem zweiten usw. und 0 dem ersten Output, 1 dem zweiten usw.
3. Alle Zellen nacheinander ausführen.

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
