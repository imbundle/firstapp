# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from rest_framework import generics
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.exceptions import APIException


from models import MyDataset
from serializer import MyDatasetSerializer
import pandas as pd
import sys

#********************************************************************************
#                    ERROR
#********************************************************************************

class FilterUptimeError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = u'Cannot be greater and less at the same time'

class RefError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = u'Rank must be between 1 and 99'

#********************************************************************************
#                    API
#********************************************************************************
class MyDataViewSet(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MyDataset.objects.all()
    serializer_class = MyDatasetSerializer

    def perform_create (self, serializer):
        """Save the post data when creating a new mydataset"""
        serializer.save()


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def chart_one (request,rank=0):
    rank = int(rank)
    if rank <= 0:
        raise FilterUptimeError()
        return

    rank = float(rank)/100
    df = pd.DataFrame( _uptime())
    df_gb = df.groupby(['server_id','application_id'])['uptime'].quantile(rank)
    res = df_gb.reset_index().to_dict(orient='records')
    return Response({"data" : res})

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def ref_get (request,rank=0):
    rank = int(rank)
    if rank <= 0:
        raise FilterUptimeError()
        return

    rank = float(rank)/100
    df = pd.DataFrame( _uptime())
    df_gb = df.groupby(['server_id','application_id'])['uptime'].quantile(rank)
    res = df_gb.reset_index().to_dict(orient='records')
    return Response({"data" : res})


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def uptime (request, format=None):
    content = {"data" : _uptime()}
    return  Response(content)


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def check_uptime(request,gt=None,lt=None):
        df = pd.DataFrame( _uptime())
        if int(gt)>0:
            df['gt'] = df.apply(lambda x: _gt(x['uptime'], int(gt)), axis=1)

        if int(lt)>0:
            df['lt'] = df.apply(lambda x: _lt(x['uptime'], int(lt)), axis=1)

        content = {"data" : df.T.to_dict().values() }
        return Response(content)

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def filter_uptime(request,gt=0,lt=0):
        df = pd.DataFrame( _uptime())

        gt = int(gt)
        lt = int(lt)

        if gt > 0 and lt > 0:
            raise FilterUptimeError()
            return

        if gt > 0:
            df_filtered = df[df.uptime > gt]

        if lt > 0:
            df_filtered = df[df.uptime < lt]

        content = {"data" : df_filtered.T.to_dict().values() }
        return Response(content)

# ********************************************************************************
#                     OTHER FUNCTIONS
# ********************************************************************************
def init_dataset (request, how_many):
    import random
    import datetime, calendar

    start_datetime = datetime.datetime.now()
    newdataset = []

    MyDataset.objects.all().delete()

    for i in range (int(how_many)):
        dataset = {
            'server_id' : random.randrange (140,150),
            'application_id' : random.randrange (10,20),
            'start_timestamp' : calendar.timegm(start_datetime.timetuple())
        }
        newdataset.append (dataset)

        #Generate random seconds from 10 to 1000
        time_delta = { 'seconds' : random.randrange(3,400) }
        start_datetime = start_datetime + datetime.timedelta(**time_delta)

        #ADD Element to MyDataset table
        data = MyDataset(**dataset)
        data.save()

    template = loader.get_template('djrest/setup.html')
    context = {'created' : newdataset}
    return HttpResponse(template.render(context, request))

# ********************************************************************************
#                     PRIVATE FUNCTIONS
# ********************************************************************************

def _gt(value,check):
    if value > check : return 1
    return 0

def _lt(value,check):
    if value < check : return 1
    return 0

def _uptime():
    data_values = list(MyDataset.objects.all().values('server_id','application_id','start_timestamp'))
    data = []

    last_el = False
    number_of_items = len(data_values)

    for index,item in enumerate(data_values):
        application_time = 0 #This value calculate value from start_timestamp(index+1) - start_timestamp
        el = item
        next_index = index + 1

        if next_index == number_of_items :
            #Last Element can't be compare whit the next for this element the application time is > 300sec
            item ['uptime'] = 301
        else:
            next_item = data_values[next_index]
            item ['uptime'] = next_item['start_timestamp'] - item['start_timestamp']
    return data_values
