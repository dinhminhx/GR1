from kafka import KafkaProducer
import csv
import time

# Kafka Configuration
bootstrap_servers = 'localhost:9092'
topic_name = 'stocks_data'

# Read CSV and send data to Kafka
def read_csv_and_produce(csv_file):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            message = ','.join(row.values()).encode('utf-8')
            producer.send(topic_name, value=message)

if __name__ == '__main__':
    csv_file_path = './stockdata.csv'
    read_csv_and_produce(csv_file_path)