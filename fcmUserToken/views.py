# -*- coding: utf-8 -*-

import logging
import os
from decouple import config

from .models import FcmUserToken
from .serializers import FcmTokenSerializer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .form import FcmUserTokenForm

# Import the Firebase service
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials


POST_SUCCESS = 1
POST_FAIL = 0


# firebase authentication
cred = credentials.Certificate(config('FIREBASE_ADMIN_KEY'))
default_app = firebase_admin.initialize_app(cred)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
firebaseAddminKeyPath = os.path.join(BASE_DIR, config('FIREBASE_ADMIN_KEY'))


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Item logger')


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




def query_get_fcmUserToken_ByUserId(userid):
	return FcmUserToken.objects.get(userId=userid)


@api_view(['POST'])
@csrf_exempt
def getFcmUserToken(request):
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
            serializer = FcmTokenSerializer(query_get_fcmUserToken_ByUserId(userId), many=False)
            return Response(serializer.data)
        else:
            return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@csrf_exempt
def setFcmUserToken(request):
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
            form = FcmUserTokenForm(request.POST)
            if form.is_valid():
                logger.debug("form is valid")
                form.save()
                return Response(POST_SUCCESS, status=status.HTTP_201_CREATED)
            else:
                return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)
