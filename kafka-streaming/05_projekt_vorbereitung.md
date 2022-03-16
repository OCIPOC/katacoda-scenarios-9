Bevor mit der Programmierung des _Producers_ (Börse) oder der _Consumer_ (Aktionär*innen) begonnen wird, muss zunächst das _Topic_ "Aktienkurse" erstellt werden. Dazu kann das mit _Apache Kafka_ mitgelieferte Skript `kafka-topics.sh` verwendet werden:

```bash
kafka-topics.sh \
    --create \
    --topic "Aktienkurse" \
    --replication-factor 1 \
    --partitions 2 \
    --bootstrap-server=localhost:9092
```{{execute}}

Falls das _Topic_ erfolgreich angelegt wurde, erscheint folgende Ausgabe:

```bash
Created topic Aktienkurse.
```

Mit dem folgenden Aufruf kann verifiziert werden, dass zwei Partitionen in dem _Topic_ "Aktienkurse" erstellt worden sind.

```bash
kafka-topics.sh \
    --describe \
    --topic "Aktienkurse" \
    --bootstrap-server localhost:9092
```{{execute}}

Erwartete Ausgabe:

```bash
Topic: aktienkurse      TopicId: l0HEWl4ZSNqNCYUqVguOjw PartitionCount: 2       ReplicationFactor: 1    Configs: segment.bytes=1073741824
        Topic: aktienkurse      Partition: 0    Leader: 0       Replicas: 0     Isr: 0
        Topic: aktienkurse      Partition: 1    Leader: 0       Replicas: 0     Isr: 0
```

