# Implementation

Um den _Producer_ beziehungsweise die Börse zu simulieren, wird zunächst eine neue _Python-Datei_ angelegt:

`touch boerse.py`{{execute T1}}

Die Datei `boerse.py`{{open}} lässt sich nun im Editor öffnen. Zunächst werden die erforderlichen Bibliotheken importiert:

<pre class="file" data-filename="boerse.py" data-target="replace">
from time import sleep
from random import uniform
import json
from datetime import datetime
from kafka import KafkaProducer
</pre>

Außerdem werden konstante Variablen definiert, die zur Konfiguration des Skriptes dienen. `TOPIC` definiert das _Topic_, in das die Aktienkursänderungen gesendet werden. Wie bei der Erstellung des _Topics_ auf dem _Apache Kafka_ Server angegeben, ist dies `'Aktienkurse'`. `SERVER` definiert den Endpunkt des Servers. Nach der Installation wurde der Server mit der Standardkonfiguration gestartet. In diesem Fall ist dieser unter `'localhost:9092'` erreichbar. `NUMBER_OF_STOCKS` legt die Anzahl an Aktien an der Börse beziehungsweise _Partitionen_ fest. Bei der Erstellung des _Topics_ wurde sich für `2` _Partitionen_ entschieden.

<pre class="file" data-filename="boerse.py" data-target="append">
TOPIC = 'Aktienkurse'
SERVER = 'localhost:9092'
NUMBER_OF_STOCKS = 2
</pre>

Nun wird ein _Kafka-Producer_ (`producer`) initialisiert:

<pre class="file" data-filename="boerse.py" data-target="append">
producer = KafkaProducer(bootstrap_servers=SERVER)
</pre>

<center style="font-size: 75%;">Unter Einbezug von [6]</center>

Die Simulation basiert nicht auf echtem Kursverhalten der Börse, sondern auf Zufall. Um zu verhindern, dass Preise innerhalb einer Iteration "von 0 auf 100" springen, werden die aktuellen Preise in der Liste `current_price` zwischengespeichert (mehr dazu in der Funktion `gen_data`). Initial haben alle Aktien den Wert `50` (in €).

<pre class="file" data-filename="boerse.py" data-target="append">
current_price = [50] * NUMBER_OF_STOCKS
</pre>

Mit Hilfe der Funktion `gen_data` lässt sich ein neuer Datenpunkt für die Aktie `stock` generieren. `stock` ist ein Integer und zeigt auf die _Partition_, die der Aktie zugeordnet ist. Zunächst wird aus dem aktuellen Wert der Aktie ein neuer gebildet, indem zufällig ein Anteil abgezogen oder hinzugefügt wird, maximal jedoch ±10%. Dann wird der neue Preis als aktueller Vermerkt und ein JSON-String mit Wert (`value`) und Zeitstempel (`timestamp`) generiert und zurückgegeben.

<pre class="file" data-filename="boerse.py" data-target="append">
def gen_data(stock: int) -> str:
    new_price = current_price[stock] * uniform(.9, 1.1)
    current_price[stock] = new_price
    data = {
        'timestamp': datetime.now().isoformat(),
        'value': new_price,
    }
    return json.dumps(data).encode('utf-8')
</pre>

In der `main`-Funktion befindet sich eine Dauerschleife. In jedem Durchlauf wird mit dem `producer` zu jeder Aktie ein Update an die entsprechende _Partition_ im _Topic_ `TOPIC` ("Aktienkurse") gesendet. Im Sinne der Transparenz werden die gesendeten Daten außerdem in der Konsole dargestellt. Zwischen den Iterationen wird zwischen 1 und 3 Sekunden gewartet.

<pre class="file" data-filename="boerse.py" data-target="append">
def main():
    while True:
        for i in range(0, NUMBER_OF_STOCKS, 1):
            data = gen_data(i)
            producer.send(
                topic=TOPIC,
                partition=i,
                value=data,
            )
            print(f'Aktie {i}: {data}')
        producer.flush()
        sleep(uniform(1, 3))
</pre>

<center style="font-size: 75%;">Unter Einbezug von [6]</center>

Jetzt bleibt nur noch übrig, die `main`-Funktion beim Start aufzurufen:

<pre class="file" data-filename="boerse.py" data-target="append">
if __name__ == '__main__':
    main()
</pre>

# Ergebnis

Das Skript `boerse.py`{{open}} generiert zufällige Börsenkurs, die an das _Topic_ "Aktienkurse" des _Apache Kafka_ Servers gesendet werden. Kursänderungen einer Aktie werden immer in der gleichen Partition gespeichert. Das Skript kann man wie folgt starten:

`python3 boerse.py`{{execute T2}}

Im Terminal sollten jetzt Kursänderungen der Aktien `0` und `1` regelmäßig erscheinen. Wir lassen den Prozess vorerst laufen und widmen uns dem Skript für Aktionär\*innen im nächsten Kapitel ...
