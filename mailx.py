import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kafka import KafkaConsumer
import json
import os

bootstrap_servers_sv1 = os.environ.get('SERVER_NAME')
sasl_mechanism_sv1 = os.environ.get('SASL_MECH')
security_protocol_sv1 = os.environ.get('SSL_SEC')
sasl_plain_username_sv1 = os.environ.get('SASL_USERNAME')
sasl_plain_password_sv1 = os.environ.get('SASL_PASSD')

topic_name = 'news'

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
    print(json_data)


def send_email(receiver_email: str, subject: str, bodyhtml: str):
    API_KEY_HELPER = os.environ.get('API_KEY_HELPER')
    SMTP_URL_FINAL = os.environ.get('SMTP_URL_FINAL')
    SMTP_PORT = os.environ.get('SMTP_PORT')

    sender_email = "hemanth22hemu@gmail.com"
    #receiver_email = "hemanthbitra@live.com"
    message = MIMEMultipart("alternative")

    #message["Subject"] = "[LV] Report"
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = ",".join(receiver_email)

    text = bodyhtml
    html = bodyhtml

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP(SMTP_URL_FINAL, SMTP_PORT) as server:
        server.starttls()
        server.login(sender_email, API_KEY_HELPER)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
        server.quit()
        print("Connection Closed")
    return {"message": "Email sent successfully."}


send_email("hemanthbitra@live.com", "Mail server running in Vagrant", "<html><body><p>Hello from Vagrant</p></body></html>")