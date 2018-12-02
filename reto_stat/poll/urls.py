from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from poll import views

app_name = 'poll'

urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'poll/<int:poll_id>/', views.PollView.as_view(), name='stat'),
    path(r'poll/<int:poll_id>/vote/hourly/', views.HourVoteView.as_view(), name='vote_hour'),
]
