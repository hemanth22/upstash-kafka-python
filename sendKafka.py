from kafka import KafkaProducer
import json
import os

bootstrap_servers_sv1 = os.environ.get('SERVER_NAME')
sasl_mechanism_sv1 = os.environ.get('SASL_MECH')
security_protocol_sv1 = os.environ.get('SSL_SEC')
sasl_plain_username_sv1 = os.environ.get('SASL_USERNAME')
sasl_plain_password_sv1 = os.environ.get('SASL_PASSD')

producer = KafkaProducer(
  bootstrap_servers=bootstrap_servers_sv1,
  sasl_mechanism=sasl_mechanism_sv1,
  security_protocol=security_protocol_sv1,
  sasl_plain_username=sasl_plain_username_sv1,
  sasl_plain_password=sasl_plain_password_sv1,
  value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
# ...

topic_name = 'news'
data = [
    {"name": "John", "age": 30, "city": "New York"},
    {"name": "Alice", "age": 25, "city": "San Francisco"},
    {"name": "Bob", "age": 35, "city": "Chicago"},
    {"content": "<html><body><p>Hello World</p></body></html>"}
]

# Function to serialize data to JSON string
def serialize_data(data):
    return json.dumps(data)

# Produce JSON messages to the Kafka topic
for message in data:
    serialized_message = serialize_data(message)
    producer.send(topic_name, value=serialized_message)
    print(f"Produced: {serialized_message}")

producer.close()
