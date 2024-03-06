from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import requests
import time
import json


def fetch_and_send_crypto_data(fetch_non_changing_data=False):
    # Define Kafka configuration
    conf = {"bootstrap.servers": "localhost:9092"}

    # Create AdminClient instance
    a = AdminClient(conf)

    # Create a new topic
    new_topic = NewTopic("top_crypto_topic", num_partitions=1, replication_factor=1)
    a.create_topics([new_topic])

    # Create Producer instance
    p = Producer(**conf)

    def delivery_report(err, msg):
        if err is not None:
            print("Message delivery failed: {}".format(err))
        else:
            print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False,
    }
    response = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets", params=params
    )
    coins = response.json()

    for coin in coins:
        all_data = {**coin}

        if fetch_non_changing_data:
            coin_response = requests.get(
                f'https://api.coingecko.com/api/v3/coins/{coin["id"]}'
            )
            coin_data = coin_response.json()
            tickers_response = requests.get(
                f'https://api.coingecko.com/api/v3/coins/{coin["id"]}/tickers'
            )
            tickers_data = tickers_response.json()

            historical_params = {"vs_currency": "usd", "days": "max"}
            historical_response = requests.get(
                f'https://api.coingecko.com/api/v3/coins/{coin["id"]}/market_chart',
                params=historical_params,
            )
            historical_data = historical_response.json()

            all_data.update(
                {
                    **coin_data,
                    "tickers": tickers_data,
                    "historical_data": historical_data,
                }
            )

        p.produce("top_crypto_topic", json.dumps(all_data), callback=delivery_report)

        time.sleep(2)

    p.flush()
