# Implementation

Um den _Producer_ beziehungsweise die Börse zu simulieren, wird zunächst eine neue Python-Datei angelegt:

`touch aktionaer.py`{{execute}}

Die Datei `aktionaer.py`{{open}} lässt sich nun im Editor öffnen. Zunächst werden die erforderlichen Bibliotheken importiert:

<pre class="file" data-filename="aktionaer.py" data-target="replace">
import sys
import json
from kafka import KafkaConsumer, TopicPartition

TOPIC = 'Aktienkurse'
SERVER = 'localhost:9092'

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