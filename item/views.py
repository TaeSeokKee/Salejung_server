# -*- coding: utf-8 -*-

import logging
import os
from decouple import config

from .models import Item
from .serializers import GetItemsInfoByLngLatSerializer
from .serializers import GetItemsLocationByLngLatSerializer
from .serializers import GetItemByIdForRemoveSerializer
from .serializers import GetItemByIdSerializer

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .form import ItemForm

# FCM request
import requests
import json

# Import the Firebase service
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

from google.cloud import firestore

import google.gax


# firebase authentication
cred = credentials.Certificate(config('FIREBASE_ADMIN_KEY'))
default_app = firebase_admin.initialize_app(cred)


db = firestore.Client()


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# firebaseAddminKeyPath = os.path.join(BASE_DIR, config('FIREBASE_ADMIN_KEY'))


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Item logger')


# Search range from present LOCATION(lat, lng). It's equal to search space(square)'s half length.
# If SEARCH_RANGE is 1, then search space is 2*2 square.
SEARCH_RANGE = 0.015
POST_SUCCESS = 1
POST_FAIL = 0

FCM_TOPIC_LNG_LAT_DISTANCE = 0.005

FCM_SERVER = 'https://fcm.googleapis.com/fcm/send'

CLOUD_STORE_COLLECTION_MYWATCHLIST = u'myWatchList'
CLOUD_STORE_COLLECTION_MYITEMLIST = u'myItemList'
CLOUD_STORE_COLLECTION_ITEM_HISTORY = u'item_history'

SEARCH_LNG_LAT_STARTINDEX = 0
SEARCH_LNG_LAT_ENDINDEX = 100

PAGE_ITEM_COUNT = 30

def index(request):
    template_name = 'item/index.html'
    return render(request, template_name)



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





############ this feature not used ################
# topic format : {lng}_{lat} ex) 123.456_-123.456
# 3x3 means send FCM to 9 topics that nears from sender's location 
# which is sender's topic value's (lng, lat) near 500m distance.
# topic_5 is center(input topic value).
# 2017/11/19 at present, FCM topic is up to 5. So split request.
# def sendFCMByTopic_3x3(topic, photoFilePath, name, price, channelUrl):
#     FCM_SERVER = 'https://fcm.googleapis.com/fcm/send'

#     data = { 
#                 "photoFilePath" : photoFilePath, 
#                 "name": name,
#                 "price" : price,
#                 "channelUrl" : channelUrl,
#                 "type" : "newItem",    
#             }

#     lng_lat = topic.split("_")
    
#     lng = float(lng_lat[0])
#     lat = float(lng_lat[1])

#     topic_1 = "%.3f" % (lng - FCM_TOPIC_LNG_LAT_DISTANCE) + "_" + "%.3f" % (lat + FCM_TOPIC_LNG_LAT_DISTANCE)
#     topic_2 = "%.3f" % (lng                             ) + "_" + "%.3f" % (lat + FCM_TOPIC_LNG_LAT_DISTANCE)
#     topic_3 = "%.3f" % (lng + FCM_TOPIC_LNG_LAT_DISTANCE) + "_" + "%.3f" % (lat + FCM_TOPIC_LNG_LAT_DISTANCE)
#     topic_4 = "%.3f" % (lng - FCM_TOPIC_LNG_LAT_DISTANCE) + "_" + "%.3f" % (lat                             )
#     topic_5 = topic
#     topic_6 = "%.3f" % (lng + FCM_TOPIC_LNG_LAT_DISTANCE) + "_" + "%.3f" % (lat                             )
#     topic_7 = "%.3f" % (lng - FCM_TOPIC_LNG_LAT_DISTANCE) + "_" + "%.3f" % (lat - FCM_TOPIC_LNG_LAT_DISTANCE)
#     topic_8 = "%.3f" % (lng                             ) + "_" + "%.3f" % (lat - FCM_TOPIC_LNG_LAT_DISTANCE)
#     topic_9 = "%.3f" % (lng + FCM_TOPIC_LNG_LAT_DISTANCE) + "_" + "%.3f" % (lat - FCM_TOPIC_LNG_LAT_DISTANCE)

#     print(topic_1, topic_2, topic_3, topic_4, topic_5, topic_6, topic_7, topic_8, topic_9)

#     post_data = {
#         "condition": "'" + topic_1 + "'" +  " in topics" 
#             + " || '" + topic_2 + "' in topics"
#             + " || '" + topic_3 + "' in topics"
#             + " || '" + topic_4 + "' in topics"
#             + " || '" + topic_5 + "' in topics",
#         "data": data
#     }

#     post_headers = { 
#         "Authorization" : "key=" + config('FCM_KEY'),
#         "content-type" : "application/json" 
#     }

#     response = requests.post(FCM_SERVER, headers = post_headers, data = json.dumps(post_data))

#     print(response.text)
#     print(response.headers)


#     post_data = {
#         "condition": "'" + topic_6 + "'" +  " in topics" 
#             + " || '" + topic_7 + "' in topics"
#             + " || '" + topic_8 + "' in topics"
#             + " || '" + topic_9 + "' in topics",
#         "data": data
#     }

#     post_headers = { 
#         "Authorization" : "key=" + config('FCM_KEY'),
#         "content-type" : "application/json" 
#     }

#     response = requests.post(FCM_SERVER, headers = post_headers, data = json.dumps(post_data))

#     print(response.text)
#     print(response.headers)



def query_get_Item_By_Id(itemId):
    return Item.objects.get(id=itemId)



@api_view(['POST'])
@csrf_exempt
def getItemById(request):
    if request.method == 'POST':

        print(request.POST)

        itemId = int(request.POST['itemId'])
        userId = request.POST['userId']
        userIdToken = request.POST['userIdToken']

        if itemId == "":
            logger.warning("itemId is None")

        if userId == "":
            logger.warning("userId is None")

        if userIdToken == "":
            logger.warning("userIdToken is None")

        if authentication_check(userId, userIdToken) == True:
            logger.debug("authentication_check success")
            serializer = GetItemByIdSerializer(query_get_Item_By_Id(itemId))
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)


# it is google-cloud-python credential issue.
# when use google-cloud-python retry needs.
# because of frequent gaxerror, need to retry when error occur.
def addItemToMyItemList(itemId, request):
    try:
        collRef = db.collection(CLOUD_STORE_COLLECTION_MYITEMLIST)
        collRef.add({
            u'userId': request.POST['userId'],
            u'itemId': itemId,
            u'unReadCount': 0,
            u'updateDate': request.POST['date'],
            u'channelUrl': request.POST['channelUrl'],
            u'photoFilePath': request.POST['photoFilePath'],
            u'name': request.POST['name'],
            u'price': request.POST['price'],
            u'isClosed': False
            })
    except google.gax.errors.GaxError as e:
            logger.debug("addItemToMyItemList error")
            addItemToMyItemList(itemId, request)


# it is google-cloud-python credential issue.
# when use google-cloud-python retry needs.
# because of frequent gaxerror, need to retry when error occur.
def addItemToItemHistory(itemId, request):
    try:
        collRef = db.collection(CLOUD_STORE_COLLECTION_ITEM_HISTORY)
        collRef.add({
            u'userId': request.POST['userId'],
            u'itemId': itemId,
            u'openDate': request.POST['date'],
            u'closeDate': 0,
            u'channelUrl': request.POST['channelUrl'],
            u'photoFilePath': request.POST['photoFilePath'],
            u'name': request.POST['name'],
            u'price': request.POST['price'],
            u'isClosed': False,
            u'thumb_up': 0,
            u'thumb_down': 0
            })
    except google.gax.errors.GaxError as e:
            logger.debug("addItemToItemHistory error")
            addItemToItemHistory(request)


@api_view(['POST'])
@csrf_exempt
def addItem(request):
    if request.method == 'POST':

        print(request.POST)

        userId = request.POST['userId']
        userIdToken = request.POST['userIdToken']
        channelUrl = request.POST['channelUrl']

        if userId == "":
            logger.warning("userId is None")

        if userIdToken == "":
            logger.warning("userIdToken is None")

        if channelUrl == "":
            logger.warning("channelUrl is None")

        if authentication_check(userId, userIdToken) == True:
            logger.debug("authentication_check success")
            form = ItemForm(request.POST)
            if form.is_valid():
                logger.debug("form is valid")
                
                itemObject = form.save()
                itemId = int(itemObject.id)

                # it is google-cloud-python credential issue.
                # when use google-cloud-python retry needs.
                # because of frequent gaxerror, need to retry when error occur.
                addItemToMyItemList(itemId, request)

                # it is google-cloud-python credential issue.
                # when use google-cloud-python retry needs.
                # because of frequent gaxerror, need to retry when error occur.
                addItemToItemHistory(itemId, request)

                serializer = GetItemByIdSerializer(query_get_Item_By_Id(itemId))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.warning("Some authenticated user failed to add item because of form invalid")
                return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.warning("Some unauthenticated request tried to add item")
            return Response(POST_FAIL, status=status.HTTP_401_UNAUTHORIZED)





def query_get_ItemsInfoList_By_LngLat_Orderby_date(lng, lat, startIndex, endIndex):
    return Item.objects.filter(lng__gt=Decimal(lng)-Decimal(SEARCH_RANGE))\
    .filter(lng__lt=Decimal(lng)+Decimal(SEARCH_RANGE))\
    .filter(lat__gt=Decimal(lat)-Decimal(SEARCH_RANGE))\
    .filter(lat__lt=Decimal(lat)+Decimal(SEARCH_RANGE))\
    .filter(isClosed=False)\
    .order_by('-date')[startIndex:endIndex]



@api_view(['POST'])
@csrf_exempt
def getItemsInfoByLngLat(request):
    if request.method == 'POST':
        
        print(request.POST)

        lat = request.POST['lat']
        lng = request.POST['lng']
        offset = int(request.POST['offset'])

        startIndex = offset * PAGE_ITEM_COUNT
        endIndex = startIndex + PAGE_ITEM_COUNT

        if lat == "":
            logger.warning("lat is None")

        if lng == "":
            logger.warning("lng is None")

        serializer = GetItemsInfoByLngLatSerializer(query_get_ItemsInfoList_By_LngLat(lng, lat, startIndex, endIndex), many=True)
        print(serializer.data)
        return Response(serializer.data)



def query_get_ItemsInfoList_By_LngLat(lng, lat, startIndex, endIndex):
    return Item.objects.filter(lng__gt=Decimal(lng)-Decimal(SEARCH_RANGE))\
    .filter(lng__lt=Decimal(lng)+Decimal(SEARCH_RANGE))\
    .filter(lat__gt=Decimal(lat)-Decimal(SEARCH_RANGE))\
    .filter(lat__lt=Decimal(lat)+Decimal(SEARCH_RANGE))\
    .filter(isClosed=False)[startIndex:endIndex]


@api_view(['POST'])
@csrf_exempt
def getItemsLocationByLngLat(request):
    if request.method == 'POST':

        print(request.POST)

        lat = request.POST['lat']
        lng = request.POST['lng']


        if lat == "":
            logger.warning("lat is None")

        if lng == "":
            logger.warning("lng is None")


        serializer = GetItemsLocationByLngLatSerializer(query_get_ItemsInfoList_By_LngLat(lng, lat, SEARCH_LNG_LAT_STARTINDEX, SEARCH_LNG_LAT_ENDINDEX), many=True)
        print(serializer.data)
        return Response(serializer.data)



@api_view(['POST'])
@csrf_exempt
def sendFcmToOperator(request):
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
            
            sendFcmByOperator(
                request.POST['type'],
                request.POST['channel'],
                request.POST['message'],
                request.POST['to'],
            )

            return Response(POST_SUCCESS, status=status.HTTP_200_OK)
        else:
            logger.warning("Some unauthenticated request tried to send fcm to channel operator!")
            return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)



# it is google-cloud-python credential issue.
# when use google-cloud-python retry needs.
# because of frequent gaxerror, need to retry when error occur.
def deleteMyItemList(doc_id):
    try:
        db.collection(CLOUD_STORE_COLLECTION_MYITEMLIST).document(doc_id).delete()
    except google.gax.errors.GaxError as e:
        logger.debug("deleteMyItemList error")
        deleteMyItemList(doc_id)


# it is google-cloud-python credential issue.
# when use google-cloud-python retry needs.
# because of frequent gaxerror, need to retry when error occur.
def getDocIdFromMyItemListByItemId(itemId):
    doc_id = ""
    try:
        doc = db.collection(CLOUD_STORE_COLLECTION_MYITEMLIST)\
        .where(u'itemId', u'==', int(itemId))\
        .get()
        for mDocument in doc:
            doc_id = mDocument.id
    except google.gax.errors.GaxError as e:
        logger.debug("getDocIdFromMyItemListByItemId error")
        getDocIdFromMyItemListByItemId(itemId)
    else :
        return doc_id


# it is google-cloud-python credential issue.
# when use google-cloud-python retry needs.
# because of frequent gaxerror, need to retry when error occur.      
def deleteMyItemFromMyItemList(itemId):
    doc_id = getDocIdFromMyItemListByItemId(itemId)
    deleteMyItemList(doc_id)


@api_view(['POST'])
@csrf_exempt
def removeItem(request):
    if request.method == 'POST':

        print(request.POST)

        itemId = int(request.POST['itemId'])
        userId = request.POST['userId']
        userIdToken = request.POST['userIdToken']

        if userId == "":
            logger.warning("userId is None")

        if userIdToken == "":
            logger.warning("userIdToken is None")

        if authentication_check(userId, userIdToken) == True:
            logger.debug("authentication_check success_1")
            item = Item.objects.get(id=itemId)
            serializer = GetItemByIdForRemoveSerializer(item)
            print(serializer.data)
            if serializer.data['userId'] == userId:
                logger.debug("authentication_check success_2")

                deleteMyItemFromMyItemList(itemId)
                    
                item.isClosed = True
                item.save()

                return Response(POST_SUCCESS, status=status.HTTP_200_OK)
            else:
                logger.warning("Some user tried to remove other user's item!")
                return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.warning("Some unauthenticated request tried to remove item")
            return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)



# it is google-cloud-python credential issue.
# when use google-cloud-python retry needs.
# because of frequent gaxerror, need to retry when error occur.
def deleteHistory(doc_id):
    try:
        db.collection(CLOUD_STORE_COLLECTION_ITEM_HISTORY).document(doc_id).delete()
    except google.gax.errors.GaxError as e:
        print(e)
        deleteHistory(doc_id)


# it is google-cloud-python credential issue.
# when use google-cloud-python retry needs.
# because of frequent gaxerror, need to retry when error occur.
def getDocumentFromItemHistory(userId):
    docs = []
    try:
        docs = db.collection(CLOUD_STORE_COLLECTION_ITEM_HISTORY)\
        .where(u'userId', u'==', userId)\
        .get()
    except google.gax.errors.GaxError as e:
        print(e)
        getDocumentFromItemHistory(userId)
    else :
        return docs



def deleteHistoryFromItemHistory(userId):
    docs = getDocumentFromItemHistory(userId)
    for doc in docs:
        deleteHistory(doc.id)



@api_view(['POST'])
@csrf_exempt
def deleteAccount(request):
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
            items = Item.objects.filter(userId=userId, isClosed=False)
            print(items)
            for item in items:
                print(item.id)
                itemId = item.id
                item = Item.objects.get(id=itemId)
                item.isClosed = True
                item.save()

                deleteMyItemFromMyItemList(itemId)

                deleteHistoryFromItemHistory(userId)
            
            return Response(POST_SUCCESS, status=status.HTTP_200_OK)
            
        else:
            logger.warning("Some unauthenticated request tried to remove item")
            return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)


            

# def query_get_ItemInfoList_By_LngLat(lat, lng, startIndex, endIndex):
#     return Item.objects.filter(lng__gt=Decimal(lng)-Decimal(SEARCH_RANGE))\
#     .filter(lng__lt=Decimal(lng)+Decimal(SEARCH_RANGE))\
#     .filter(lat__gt=Decimal(lat)-Decimal(SEARCH_RANGE))\
#     .filter(lat__lt=Decimal(lat)+Decimal(SEARCH_RANGE))\
#     .filter(isClosed=False)
#     .filter(name__search='Cheese')[IndexFrom:IndexTo]