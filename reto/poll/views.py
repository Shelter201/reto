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
                response_json = {'messages': u'OK', 'poll_id': opt.id}

        except IntegrityError:
            response_json = {'messages': u'We find a trouble with your request', 'poll_id': 0}
            http_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            response_json = {'messages': e, 'poll_id': 0}
            http_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        return response.Response(response_json, status=http_status)


# =============================================================================

