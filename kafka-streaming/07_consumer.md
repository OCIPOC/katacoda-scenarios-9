# Implementation

Um den _Consumer_ für Aktionär\*innen zu implementieren, wird zunächst eine neue Python-Datei angelegt:

`touch aktionaer.py`{{execute T1}}

Die Datei `aktionaer.py`{{open}} lässt sich nun im Editor öffnen. Zunächst werden die erforderlichen Bibliotheken importiert:

<pre class="file" data-filename="aktionaer.py" data-target="replace">
import sys
import json
from kafka import KafkaConsumer, TopicPartition
</pre>

Analog zum _Producer_ werden `TOPIC` und `SERVER` definiert.

<pre class="file" data-filename="aktionaer.py" data-target="append">
TOPIC = 'Aktienkurse'
SERVER = 'localhost:9092'
</pre>

Beim Start des Skriptes sollen sich die zu beobachtenden Aktien als Kommandozeilenparameter angeben lassen, zum Beispiel `python3 aktionaer.py 0 1` um die Aktien `0` und `1` zu beobachten. Daher werden die Kommandozeilenargumente extrahiert und in die Liste `stocks` als Integer geschrieben.

Dann wir der _Kafka-Consumer_ `consumer` initialisiert, wobei eine Methode zur Deserialisierung des JSON-Strings zurück zu einem _Python-Dictionary_ angeben wird. Da die Repräsentation der ausgewählten Aktien (`stocks`) den Nummern der _Partitionen_ entspricht, lassen sich mit Hilfe der Liste `stocks` die Partitionen festlegen, auf die der Consumer lauscht.

Anschließend werden iterativ alle Nachrichten, analog zur Ausgabe im _Producer_, im Terminal ausgegeben.

<pre class="file" data-filename="aktionaer.py" data-target="append">
if __name__ == '__main__':
    stocks = [int(i) for i in sys.argv[1:]]
    print(f'Ausgewählte Aktien: {stocks}')

    consumer = KafkaConsumer(
        bootstrap_servers=SERVER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=1e4,
    )
    partitions = [TopicPartition(TOPIC, i) for i in stocks]
    consumer.assign(partitions)

    for m in consumer:
        print(f'Aktie {m.partition}: {m.value}')
</pre>

<center style="font-size: 75%;">Unter Einbezug von [7]</center>

# Ergebnis

Die von `boerse.py`{{open}} generierten Kursänderungen lassen sich nun durch das Skript `aktionaer.py`{{open}} auslesen. Welche Aktien beobachtet werden, lässt sich durch die Kommandozeilenparameter definieren. Möglichkeiten:

| Aktie 0 | Aktie 1 | Kommando                                 |
| ------- | ------- | ---------------------------------------- |
| true    | false   | `python3 aktionaer.py 0`{{execute T3}}   |
| false   | true    | `python3 aktionaer.py 1`{{execute T4}}   |
| true    | true    | `python3 aktionaer.py 0 1`{{execute T5}} |

Abhängig von der gewählten Option werden Kursänderungen zu Aktie 0, 1 oder beiden angezeigt. Es ist auch möglich mehrere _Consumer_ simultan auszuführen.
