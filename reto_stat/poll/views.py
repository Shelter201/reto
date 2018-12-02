# coding=utf-8

from rest_framework import status
from rest_framework import views, response
from django.db import IntegrityError
from poll.models import *
from poll import serializers


# Create your views here.

# =============================================================================
class IndexView(views.APIView):
    # -------------------------------------------------------------------------
    def get(self, request):
        return response.Response({'resources': [
            # request.build_absolute_uri(reverse('poll:create_poll')),
            # request.build_absolute_uri(reverse('poll:vote')),
        ]})

# =============================================================================
class PollView(views.APIView):
    """
    """
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
