# coding=utf-8
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from rest_framework import views, response

# Create your views here.

# =============================================================================
class IndexView(views.APIView):
    # -------------------------------------------------------------------------
    def get(self, request):
        return response.Response({'resources': [
        ]})

