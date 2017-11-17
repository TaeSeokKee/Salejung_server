# -*- coding: utf-8 -*-

import logging
import os
from decouple import config

from .models import Photo
from .serializers import PhotoGetSerializer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .form import PhotoForm

# FCM request
import requests
import json

# Import the Firebase service
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

# firebase authentication
cred = credentials.Certificate(config('FIREBASE_ADMIN_KEY'))
default_app = firebase_admin.initialize_app(cred)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
firebaseAddminKeyPath = os.path.join(BASE_DIR, config('FIREBASE_ADMIN_KEY'))

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('photo logger')

# Search range from present LOCATION(lat, lng). It's equal to search space(square)'s half length.
# If SEARCH_RANGE is 1, then search space is 2*2 square.
SEARCH_RANGE = 60
POST_SUCCESS = 1
POST_FAIL = 0

url_server = 'https://fcm.googleapis.com/fcm/send'

def sendFCMByTopic(topic):

    url_server = 'https://fcm.googleapis.com/fcm/send'

    post_data = {
      "to": "/topics/" + topic,
      "data": {
        "message": "This is a Firebase Cloud Messaging Topic Message!",
       }
    }

    post_headers = { 
        "Authorization" : "key=" + config('FCM_KEY'),
        "content-type" : "application/json" 
    }

    response = requests.post(url_server, headers = post_headers, data = json.dumps(post_data))
    print(response.text)
    print(response.headers)


def index(request):
    template_name = 'photos/index.html'
    return render(request, template_name)


def get_query(lat, lng):
    return Photo.objects.filter(lng__gt=Decimal(lng)-Decimal(SEARCH_RANGE))\
    .filter(lng__lt=Decimal(lng)+Decimal(SEARCH_RANGE))\
    .filter(lat__gt=Decimal(lat)-Decimal(SEARCH_RANGE))\
    .filter(lat__lt=Decimal(lat)+Decimal(SEARCH_RANGE))[:50]


def authentication_check(userId, userIdToken):
    # id_token comes from the client app (shown above)
    # Retrieve services via the auth package...
    decoded_token = auth.verify_id_token(userIdToken)
    uid = decoded_token['uid']
    print(uid)
    print(userId)
    if uid == userId:
        return True
    else:
        logger.warning("uid or userIdToken is invalid")
        return False


@api_view(['POST'])
@csrf_exempt
def postLatLng(request):
    if request.method == 'POST':
        
        print(request.POST)

        userId = request.POST['userId']
        userIdToken = request.POST['userIdToken']
        lat = request.POST['lat']
        lng = request.POST['lng']

        if userId == "":
            logger.warning("userId is None")

        if userIdToken == "":
            logger.warning("userIdToken is None")

        if lat == "":
            logger.warning("lat is None")

        if lng == "":
            logger.warning("lng is None")


        if authentication_check(userId, userIdToken) == True:
            serializer = PhotoGetSerializer(get_query(lat, lng), many=True)
            return Response(serializer.data)
        else:
            # TODO : fix return 
            return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def postPhoto(request):
    if request.method == 'POST':

        print(request.POST)

        userId = request.POST['userId']
        userIdToken = request.POST['userIdToken']

        if userId == "":
            logger.warning("userId is None")

        if userIdToken == "":
            logger.warning("userIdToken is None")

        if authentication_check(userId, userIdToken) == True:
            logger.debug("authentication_check success")
            form = PhotoForm(request.POST)
            if form.is_valid():
                logger.debug("form is valid")
                form.save()
                sendFCMByTopic(request.POST['topic']);
                return Response(POST_SUCCESS, status=status.HTTP_201_CREATED)
            else:
                return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)
