from getStockData import get_data
from time import sleep
import json
from kafka import KafkaProducer

producer = KafkaProducer(

    bootstrap_servers = 'localhost:9092',
    value_serializer= lambda x : json.dumps(x).encode('utf-8')

)

# clean up the producer
producer.flush()
data = get_data()
# producer.send('stock_analytics', data)
# sleep(1)
# producer.flush()