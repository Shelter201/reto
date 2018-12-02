# coding=utf-8
import json
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework import views, response
from django.db import IntegrityError
from poll.models import *
from django.db.models import F
from poll import serializers
from poll import channel
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

# =============================================================================
class IndexView(views.APIView):
    # -------------------------------------------------------------------------
    def get(self, request):
        return response.Response({'resources': [
            request.build_absolute_uri(reverse('poll:create_poll')),
            # request.build_absolute_uri(reverse('poll:vote')),
        ]})

# =============================================================================
class PollView(views.APIView):
    """
    PUT USAGE:\n
    Register a new poll:\n
        https://hostname/poll/
        {
            "name" : "",
            "options" : ["","",""],
        }
    """
    # -------------------------------------------------------------------------
    def put(self, request, poll_id=None):
        """ Create a new Poll
        """
        if poll_id:
            response_json = {'messages': u'To create a poll, do not provide a poll_id' }
            http_status = status.HTTP_400_BAD_REQUEST
        else:
            name = request.data.get('name')
            options = request.data.get('options')
            try:
                print('Recibido: {} {}'.format(name, options))
                if not name or not options:
                    response_json = {'messages': u'You need to provide a name and a set of poll options', 'poll_id': 0}
                    http_status = status.HTTP_400_BAD_REQUEST
                else:
                    poll = Poll(name=name)
                    poll.save()
                    for option in options:
                        opt = PollOption(poll=poll, option_name=option)
                        opt.save()
                    http_status = status.HTTP_200_OK
                    response_json = {'messages': u'OK', 'poll_id': poll.id}

            except IntegrityError:
                response_json = {'messages': u'We find a trouble with your request', 'poll_id': 0}
                http_status = status.HTTP_400_BAD_REQUEST
            except Exception as e:
                response_json = {'messages': e, 'poll_id': 0}
                http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        return response.Response(response_json, status=http_status)

    # -------------------------------------------------------------------------
    def get(self, request, poll_id=None):

        if not poll_id:
            response_json = {'messages': u'To get a stat, you need to provide a poll_id'}
            http_status = status.HTTP_400_BAD_REQUEST
        else:
            try:
                poll = Poll.objects.filter(id=poll_id)
                if(len(poll) == 0):
                    response_json = {'messages': u'Incorrect poll_id'}
                    http_status = status.HTTP_404_NOT_FOUND
                else:
                    poll=poll[0]
                    poll_stat = PollStat.objects.filter(option__poll=poll)
                    if(len(poll_stat) == 0):
                        response_json = {'messages': u'No one vote already'}
                        http_status = status.HTTP_204_NO_CONTENT
                    else:
                        stat_serializer = serializers.StatSerializer(poll_stat, many=True)
                        response_json = { 'poll': poll.name, 'stats': stat_serializer.data }
                        http_status = status.HTTP_200_OK
            except IntegrityError:
                response_json = {'messages': u'We find a trouble with your vote'}
                http_status = status.HTTP_400_BAD_REQUEST
            except Exception as e:
                print(e)
                response_json = {'messages': u'Error'}
                http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        return response.Response(response_json, status=http_status)

# =============================================================================

class VoteView(views.APIView):
    """
    GET USAGE:\n
    Vote:\n
        https://hostname/poll/{id}/vote
        {
            "option" : 999,
        }
    """
    # -------------------------------------------------------------------------
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    # -------------------------------------------------------------------------
    def put(self, request, poll_id=None):
        """ Vote
        """
        #print(request)
        option = request.data.get('option')
        try:
            print('Recibido: {} {}'.format(poll_id, option))
            if not poll_id or not option:
                response_json = {'messages': u'You need to provide a poll option'}
                http_status = status.HTTP_400_BAD_REQUEST
            else:
                poll=Poll.objects.filter(id=poll_id)
                print(poll)
                if len(poll) == 0:
                    response_json = {'messages': u'Incorrect poll_id'}
                    http_status = status.HTTP_404_NOT_FOUND
                else:
                    poll_option = PollOption.objects.filter(poll=poll[0],option_name__iexact=option)
                    print(poll_option)
                    if len(poll_option) == 0:
                        response_json = {'messages': u'Incorrect poll option'}
                        http_status = status.HTTP_404_NOT_FOUND
                    else:
                        ip=self.get_client_ip(request)
                        print(ip)
                        vote_already=PollVote.objects.filter(option__poll=poll[0],ip=ip)
                        if False: #len(vote_already) > 0:
                            response_json = {'messages': u'You already vote for this poll', 'ip':ip}
                            http_status = status.HTTP_406_NOT_ACCEPTABLE
                        else:
                            vote = PollVote(option=poll_option[0],ip=ip)
                            vote.save()
                            # self.stats(vote.option.id, vote.vote_date)
                            serialized=json.dumps(
                                {'id': vote.option.id, 'date': vote.vote_date},
                                sort_keys=True,
                                indent=1,
                                cls=DjangoJSONEncoder
                            )
                            #print(serialized)
                            channel.basic_publish(exchange='',
                                                  routing_key='hello',
                                                  body=serialized)
                            response_json = {'messages': u'OK',}
                            http_status = status.HTTP_200_OK

        except IntegrityError:
            response_json = {'messages': u'We find a trouble with your vote'}
            http_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            response_json = {'messages': u'Error'}
            http_status = status.HTTP_500_INTERNAL_SERVER_ERROR


        return response.Response(response_json, status=http_status)

# =============================================================================

class HourVoteView(views.APIView):
    """

    """
    # -------------------------------------------------------------------------
    def get(self, request, poll_id):

        try:
            poll = Poll.objects.filter(id=poll_id)
            if(len(poll) == 0):
                response_json = {'messages': u'Incorrect poll_id'}
                http_status = status.HTTP_404_NOT_FOUND
            else:
                poll=poll[0]
                poll_stat = PollHourStat.objects.filter(option__poll=poll)
                if(len(poll_stat) == 0):
                    response_json = {'messages': u'No one vote already'}
                    http_status = status.HTTP_204_NO_CONTENT
                else:
                    stat_serializer = serializers.HourStatSerializer(poll)
                    response_json = stat_serializer.data
                    #stat_serializer = serializers.HourStatSerializer(poll_stat, many=True)
                    #response_json = { 'poll': poll.name, 'stats': stat_serializer.data }
                    http_status = status.HTTP_200_OK
        except IntegrityError:
            response_json = {'messages': u'We find a trouble with your vote'}
            http_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            response_json = {'messages': u'Error'}
            http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        return response.Response(response_json, status=http_status)
