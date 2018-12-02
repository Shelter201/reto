from django.core.management.base import BaseCommand, CommandError
import pika


class Command(BaseCommand):
    help = 'Update Stat Database'

    # -------------------------------------------------------------------------
    def callback(self, ch, method, properties, body):
        print(' [x] Received {}'.format(body))

    # -------------------------------------------------------------------------
    def handle(self, *args, **options):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        channel.basic_consume(self.callback,
                              queue='hello',
                              no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

