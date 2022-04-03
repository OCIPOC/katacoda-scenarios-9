Bevor die theoretischen Grundlagen erörtert werden, ist es erforderlich _Apache Kafka_ auf der virtuellen Maschine zu installieren.

# Download

Die aktuelle Version von _Apache Kafka_ lässt sich immer auf der [offiziellen Webseite](https://kafka.apache.org/downloads) finden. Zum Zeitpunkt der Erstellung dieses _Katacodas_ ist die aktuelle Version **3.1.0**, weshalb diese Version benutzt wird. Gerne können Sie sich auch für eine andere Version entscheiden, allerdings kann die Funktion des _Katacodas_ dann nicht gewährleistet werden.

Mit dem Kommando `wget` lassen sich Dateien über das HTTP-Protokoll herunterladen. Der Link zur aktuellen Version ist `https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz`. Folglich kann die Datei wie folgt heruntergeladen werden:

`wget https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz`{{execute T1}}

# Entpacken

Da es sich um einen _Tar-Ball_ handelt, muss dieser entpackt werden:

`tar -xzf kafka_2.13-3.1.0.tgz`{{execute T1}}

Der _Tar-Ball_ wird nicht weiter benötigt und kann gelöscht werden:

`rm kafka_2.13-3.1.0.tgz`{{execute T1}}

Im Verzeichnis `kafka_2.13-3.1.0` befinden sich nun verschieden Skripte zum Kontrollieren von _Apache Kafka_, beispielsweise zum Starten. Damit nicht immer der absolute Pfad angegeben werden muss, sobald man auf die Skripte zugreift, empfiehlt es sich diesen Ordner zu den PATH-Variablen hinzuzufügen:

`export PATH=~/kafka_2.13-3.1.0/bin:$PATH`{{execute T1}}

# Starten

Nun lässt sich _Kafka_ mit der Standardkonfiguration im Hintergrund starten [3]:

````
zookeeper-server-start.sh kafka_2.13-3.1.0/config/zookeeper.properties > /dev/null &
kafka-server-start.sh kafka_2.13-3.1.0/config/server.properties > /dev/null &
```{{execute T1}}
````
