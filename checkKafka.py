from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'stock_analytics', 
    bootstrap_servers='localhost:9092'
)

for message in consumer:
    print(message.value.decode('utf-8'))

consumer.close()
