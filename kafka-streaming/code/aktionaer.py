import sys
import json
from kafka import KafkaConsumer

TOPIC = 'Aktienkurse'
SERVER = 'localhost:9092'

if __name__ == '__main__':

    stocks = [int(i) for i in sys.argv[1:]]
    print(f'Ausgewählte Aktien: {stocks}')

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=SERVER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        consumer_timeout_ms=1e4,
    )
    consumer.assign(stocks)
