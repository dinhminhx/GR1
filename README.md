sudo systemctl start zookeeper
sudo systemctl start kafka 

Check : 

sudo systemctl status zookeeper 
sudo systemctl status kafka 

bin/kafka-topics.sh --list --bootstrap-server localhost:9092 