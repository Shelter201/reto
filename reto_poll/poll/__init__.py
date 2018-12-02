import pika
import os

connection = pika.BlockingConnection(pika.ConnectionParameters(heartbeat_interval=0,host=os.environ['RABBITMQ_HOST']))
channel = connection.channel()

channel.queue_declare(queue='polls')
channel.queue_declare(queue='votes')