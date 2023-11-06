from kafka import KafkaConsumer
import subprocess

# Kafka Configuration
bootstrap_servers = 'localhost:9092'
topic_name = 'stocks_data'

# Save data to Hadoop
def save_to_hadoop():
    consumer = KafkaConsumer(topic_name, bootstrap_servers=bootstrap_servers)
    for message in consumer:
        data = message.value.decode('utf-8')
        data = data + '\n'  # Add newline to separate records in Hadoop

        # Use the 'hdfs' command to write data to HDFS
        cmd = f"echo '{data}' | hdfs dfs -appendToFile - /stocks_data/data.txt"
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while writing to HDFS: {e}")

if __name__ == '__main__':
    save_to_hadoop()
