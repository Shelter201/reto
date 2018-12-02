from django.core.management.base import BaseCommand, CommandError
from poll.models import *
import os
import pika
import json


class Command(BaseCommand):
    help = 'Add Poll to Database'

    # -------------------------------------------------------------------------
    def add(self, poll_info):
        poll = Poll(name=poll_info['name'])
        poll.save()
        for option in poll_info['options']:
            opt = PollOption(poll=poll, option_name=option)
            opt.save()

    # -------------------------------------------------------------------------
    def callback(self, ch, method, properties, body):
        x=json.loads(body)
        print(' [x] Received {}'.format(x))
        self.add(x)

    # -------------------------------------------------------------------------
    def handle(self, *args, **options):
        connection = pika.BlockingConnection(pika.ConnectionParameters(heartbeat_interval=0,host=os.environ['RABBITMQ_HOST']))
        channel = connection.channel()

        channel.queue_declare(queue='polls')

        channel.basic_consume(self.callback,
                              queue='polls',
                              no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

