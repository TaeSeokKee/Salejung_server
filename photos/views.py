# -*- coding: utf-8 -*-

from .models import Photo
from .serializers import PhotoGetSerializer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .form import PhotoForm
from django.core.files.uploadedfile import SimpleUploadedFile


# Search range from present LOCATION(lat, lng). It's equal to search space(square)'s half length.
# If SEARCH_RANGE is 1, then search space is 2*2 square.
SEARCH_RANGE = 1
POST_SUCCESS = 1
POST_FAIL = 0

def index(request):
    template_name = 'photos/index.html'
    return render(request, template_name)


def get_query(lat, lng):
    return Photo.objects.filter(lat__gt=Decimal(lat)-Decimal(SEARCH_RANGE))\
    .filter(lat__lt=Decimal(lat)+Decimal(SEARCH_RANGE))\
    .filter(lng__gt=Decimal(lng)-Decimal(SEARCH_RANGE))\
    .filter(lng__lt=Decimal(lng)+Decimal(SEARCH_RANGE))



@api_view(['GET', 'POST'])
@csrf_exempt
def getPostPhoto(request):
    if request.method == 'GET':
        lat = request.data['lat']
        lng = request.data['lng']
        serializer = PhotoGetSerializer(get_query(lat, lng), many=True)
        return Response(GET_SUCCESS)

    elif request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        #print(request.POST)
        #print(request.FILES)
        #print(request)
        if form.is_valid():
            form.save()
            return Response(POST_SUCCESS, status=status.HTTP_201_CREATED)
        return Response(POST_FAIL, status=status.HTTP_400_BAD_REQUEST)
