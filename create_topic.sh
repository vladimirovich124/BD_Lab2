#!/bin/bash

docker exec -it laba2-kafka-1 \
  kafka-topics.sh --create --topic bitcoin_transactions --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1