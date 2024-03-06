from confluent_kafka import Consumer, KafkaException
import pandas as pd
from sqlalchemy import create_engine
import json


def consume_and_store_data():
    # Define Kafka configuration
    conf = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "group1",
        "auto.offset.reset": "earliest",
    }

    # Create Consumer instance
    c = Consumer(conf)

    # Subscribe to topic
    c.subscribe(["top_crypto_topic"])

    # Create a connection to the PostgreSQL database
    engine = create_engine("postgresql://user:password@localhost:5432/crypto")

    try:
        # Consume message from Kafka
        msg = c.poll(1.0)
        if msg is None:
            return
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Deserialize message from JSON
            data = json.loads(msg.value())

            # Transform data into DataFrames
            coins_df = pd.DataFrame([data])
            coins_df.to_sql("coins", engine, if_exists="append", index=False)

            if "historical_data" in data:
                historical_data_df = pd.DataFrame(data["historical_data"])
                historical_data_df.to_sql(
                    "historical_data", engine, if_exists="append", index=False
                )

            if "tickers" in data:
                tickers_df = pd.DataFrame(data["tickers"])
                tickers_df.to_sql("tickers", engine, if_exists="append", index=False)

            if "roi" in data:
                roi_df = pd.DataFrame(data["roi"])
                roi_df.to_sql("roi", engine, if_exists="append", index=False)

            if "community_data" in data:
                community_data_df = pd.DataFrame([data["community_data"]])
                community_data_df.to_sql(
                    "community_data", engine, if_exists="append", index=False
                )

            if "developer_data" in data:
                developer_data_df = pd.DataFrame([data["developer_data"]])
                developer_data_df.to_sql(
                    "developer_data", engine, if_exists="append", index=False
                )

    except KeyboardInterrupt:
        pass

    # Close down consumer to commit final offsets.
    c.close()
