from confluent_kafka import Consumer, KafkaError
import json
import os
import platform
import time
from typing import List

class Tx:
    def __init__(self, tx_data: bytes, tx_price: int):
        self.tx_data = tx_data
        self.tx_price = tx_price

class TxLimitedCollection:
    def __init__(self, max_size: int):
        self.tx_collection: List[Tx] = []
        self.max_size = max_size

    def append(self, tx: Tx) -> bool:
        if len(self.tx_collection) < self.max_size:
            self.tx_collection.append(tx)

            if len(self.tx_collection) == 10:
                self.sort_des()

            return True

        if tx.tx_price > self.tx_collection[0].tx_price:
            self.tx_collection[0] = tx
        else:
            return False

        self.sort_des()

        return True

    def print_collection(self):
        clear_terminal()
        for i, tx in enumerate(reversed(self.tx_collection)):
            print(f"TX NUMBER {i+1}:\n{tx.tx_data.decode('utf-8')}\n")

        time.sleep(10)

    def sort_des(self):
        self.tx_collection.sort(key=lambda x: x.tx_price, reverse=True)

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def main():
    consumer_conf = {
        'bootstrap.servers': 'localhost:9093',
        'group.id': 'my_consumer_group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(['bitstamp-data'])

    tx_list = TxLimitedCollection(max_size=10)

    print("Getting transactions, please wait: ")

    while True:
        msg = consumer.poll(5.0)

        if msg is None:
            time.sleep(5)
        elif msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
        else:
            try:
                price_data = json.loads(msg.value())
                tx = Tx(tx_data=msg.value(), tx_price=price_data['data']['price'])

                ok = tx_list.append(tx)

                if ok and len(tx_list.tx_collection) == tx_list.max_size:
                    tx_list.print_collection()

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

if __name__ == "__main__":
    main()
