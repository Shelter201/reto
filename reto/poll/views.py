# coding=utf-8
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework import views, response
from django.db import IntegrityError
from poll.models import *

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
    def put(self, request):
        """ Create a new Poll
        """
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
                        if len(vote_already) > 0:
                            response_json = {'messages': u'You already vote for this poll', 'ip':ip}
                            http_status = status.HTTP_406_NOT_ACCEPTABLE
                        else:
                            vote = PollVote(option=poll_option[0],ip=ip)
                            vote.save()
                            response_json = {'messages': u'OK', 'ip':ip}
                            http_status = status.HTTP_200_OK

        except IntegrityError:
            response_json = {'messages': u'We find a trouble with your vote'}
            http_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            response_json = {'messages': u'Error'}
            http_status = status.HTTP_500_INTERNAL_SERVER_ERROR


        return response.Response(response_json, status=http_status)