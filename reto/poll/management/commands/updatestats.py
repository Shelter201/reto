from django.core.management.base import BaseCommand, CommandError
from poll.models import *
from django.db.models import F
from datetime import datetime
import pika
import json


class Command(BaseCommand):
    help = 'Update Stat Database'
    # -------------------------------------------------------------------------
    def stats(self, vote):
        option = PollOption.objects.filter(id=vote['id'])[0]
        print(option)
        poll_stat = PollStat.objects.filter(option=option)
        print(poll_stat)
        if len(poll_stat) == 0:
            PollStat(option=option, votes=1).save()
            PollHourStat(option=option,
                         vote_hour=vote['date'].replace(minute=0, second=0, microsecond=0) ,votes=1).save()
        else:
            poll_stat.update(votes=F('votes') + 1)
            poll_h_stat = PollHourStat.objects.filter(option=option,
                                                      vote_hour=vote['date'].replace(minute=0, second=0, microsecond=0))
            if len(poll_h_stat) == 0:
                PollHourStat(option=option,
                             vote_hour=vote['date'].replace(minute=0, second=0, microsecond=0), votes=1).save()
            else:
                poll_h_stat.update(votes=F('votes') + 1)
                
    # -------------------------------------------------------------------------
    def callback(self, ch, method, properties, body):
        x=json.loads(body)
        #'2018-12-01T18:35:24.035'
        x['date'] = datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f')
        print(' [x] Received {}'.format(x))
        self.stats(x)

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

