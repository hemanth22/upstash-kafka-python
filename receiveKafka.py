from kafka import KafkaConsumer
import json
import os


bootstrap_servers_sv1 = os.environ.get('SERVER_NAME')
sasl_mechanism_sv1 = os.environ.get('SASL_MECH')
security_protocol_sv1 = os.environ.get('SSL_SEC')
sasl_plain_username_sv1 = os.environ.get('SASL_USERNAME')
sasl_plain_password_sv1 = os.environ.get('SASL_PASSD')

topic_name = 'news'

consumer = KafkaConsumer(
  topic_name,
  bootstrap_servers=bootstrap_servers_sv1,
  sasl_mechanism=sasl_mechanism_sv1,
  security_protocol=security_protocol_sv1,
  sasl_plain_username=sasl_plain_username_sv1,
  sasl_plain_password=sasl_plain_password_sv1,
  group_id='$GROUP_NAME',
  auto_offset_reset='earliest',
  consumer_timeout_ms=60000,
  value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    json_data = message.value
    print(f"Received: {json_data}")


consumer.close()
