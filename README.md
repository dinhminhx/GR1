sudo systemctl start zookeeper
sudo systemctl start kafka 

Check : 

sudo systemctl status zookeeper 
sudo systemctl status kafka 

bin/kafka-topics.sh --list --bootstrap-server localhost:9092 

bin/kafka-topics.sh --create --topic stocksdata --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic name