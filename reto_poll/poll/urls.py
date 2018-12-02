from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from poll import views

app_name = 'poll'

urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'poll/', views.PollView.as_view(), name='create_poll'),
    path(r'poll/<int:poll_id>/vote/', views.VoteView.as_view(), name='vote'),
]
