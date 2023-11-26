import json
import asyncio
from websockets import connect
from confluent_kafka import Producer

class Connection:
    def __init__(self, url, kafka_bootstrap_servers, kafka_topic):
        self.url = url
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka_topic = kafka_topic
        self.read_signal = asyncio.Event()
        self.bitstamp_conn = None
        self.kafka_conn = None

    async def start_read_messages(self):
        try:
            async for message in self.bitstamp_conn:
                print(f"recv: {message}")

                await self.send_data_to_kafka(message)

        except websockets.ConnectionClosed:
            pass
        finally:
            self.read_signal.set()

    async def stop_read_messages(self):
        self.read_signal.set()

    async def close_connection(self):
        if self.bitstamp_conn:
            await self.bitstamp_conn.close()

    async def send_data_to_kafka(self, data):
        self.kafka_conn.produce(self.kafka_topic, value=data)
        self.kafka_conn.flush()

    @classmethod
    async def create_connection(cls, url, kafka_bootstrap_servers, kafka_topic):
        self = cls(url, kafka_bootstrap_servers, kafka_topic)
        self.bitstamp_conn = await connect(url)
        self.kafka_conn = Producer({'bootstrap.servers': kafka_bootstrap_servers})
        return self

async def main():
    url = "wss://ws.bitstamp.net"
    kafka_bootstrap_servers = "localhost:9093"
    kafka_topic = "bitstamp-data"

    connection = await Connection.create_connection(url, kafka_bootstrap_servers, kafka_topic)

    # subscribe
    data = {
        "event": "bts:subscribe",
        "data": {
            "channel": "live_trades_btcusd",
        }
    }

    await connection.bitstamp_conn.send(json.dumps(data))

    response = await connection.bitstamp_conn.recv()
    print(f"recv: {response}")

    asyncio.create_task(connection.start_read_messages())

    await asyncio.Event().wait()  # Wait forever or until interrupted

if __name__ == "__main__":
    asyncio.run(main())
