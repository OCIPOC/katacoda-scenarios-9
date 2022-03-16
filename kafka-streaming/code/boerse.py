from time import sleep
from random import uniform
import json
from datetime import datetime
from kafka import KafkaProducer

TOPIC = 'Aktienkurse'
SERVER = 'localhost:9092'
NUMBER_OF_STOCKS = 2

producer = KafkaProducer(bootstrap_servers=SERVER)

current_price = [50] * NUMBER_OF_STOCKS

def gen_data(stock: int) -> str:
    new_price = current_price[stock] * uniform(.9, 1.1)
    current_price[stock] = new_price
    data = {
        'timestamp': datetime.now().isoformat(),
        'value': new_price,
    }
    return json.dumps(data).encode('utf-8')

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

if __name__ == '__main__':
    main()
