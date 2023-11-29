# Apache Kafka

This project demonstrates the implementation of a data storing and processing pipeline using Apache Kafka. The pipeline includes a producer that connects to a WebSocket, listens for a data stream, and publishes messages to Apache Kafka. On the consumer side, the logic is implemented to consume the data, compute the top 10 bitcoin transactions by the price field, and print the results to stdout.

## Prerequisites

- [Docker](https://www.docker.com/) installed
- [docker-compose](https://docs.docker.com/compose/install/) installed

## Getting Started

1. Clone this repository:

    git clone https://github.com/vladimirovich124/BD_Lab2

2. Navigate to the project directory:

    ```bash
    cd your-repo
    ```

3. Run the following command to set up the Kafka environment:

    ```bash
    docker-compose up -d
    ```

4. Execute the setup script to create the Kafka topic:

    ```bash
    ./setup.sh
    ```

## Running the Producer

1. Navigate to the `src` directory:

    ```bash
    cd src
    ```

2. Run the producer:

    ```bash
    python producer.py
    ```

## Running the Consumer

1. Navigate to the `src` directory:

    ```bash
    cd src
    ```

2. Run the consumer:

    ```bash
    python consumer.py
    ```

## Results

The consumer will compute and print the top 10 bitcoin transactions by price to the console.

## Additional Information

- The `create_topic.sh` script is provided to create the Kafka topic manually if needed.

- Ensure that the necessary dependencies are installed.
