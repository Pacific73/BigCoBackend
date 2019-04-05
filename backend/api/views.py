# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from models import DetectResult
from helpers import *
import json

# Create your views here.
def rest_digest(request):
    app_name = request.GET.get('app_name')
    manager_name = request.GET.get('manager_name')
    corp_sector = request.GET.get('corp_sector')
    business = request.GET.get('business')
    pass


    

def rest_report(request):
    pass

# detections -> [POST, PUT]
def rest_detection(request):

    if request.method not in ['POST', 'PUT']:
        return JsonResponse(error_response('Only supports PUT/POST.'), 
                            status=403)
    # Only supports POST and PUT

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        print e
        return JsonResponse(error_response('Invalid JSON format.'), 
                            status=403)
    # Parse JSON data
    
    app_name = regularize_str(data.get('app_name'))
    manager_name = regularize_str(data.get('manager_name'))
    corp_sector = regularize_str(data.get('corp_sector'))
    business = regularize_str(data.get('business'))
    identifier = get_identifier([app_name, manager_name, corp_sector, business])
    # Get regularized strings and identifier

    detected = data.get('detected')
    result = data.get('result', [])
    # Get detected and result
    
    if request.method == 'POST':

        items = DetectResult.objects(identifier=identifier)
        if items.count() != 0:
            return JsonResponse(
                error_response('Record already exists. You should use PUT.'))
        # If identifier already exists -> invalid POST

        res = DetectResult()
        res.app_name = app_name
        res.manager_name = manager_name
        res.corp_sector = corp_sector
        res.business = business
        res.identifier = identifier
        res.detected = detected
        res.result = result
        # New instance
        
        try:
            res.save()
        except Exception as e:
            print e
            return JsonResponse(error_response('Wrong format of some items in JSON.'), 
                                status=403)
        # Save

    elif request.method == 'PUT':
        items = DetectResult.objects(identifier=identifier)
        if items.count() == 0:
            return JsonResponse(
                error_response('Record doesn\'t exists You should use POST.'))
        # Record should exist in the database
        
        res = items.first()
        res.detected = detected
        res.result = result
        # Update detected and result

        try:
            res.save()
        except Exception as e:
            print e
            return JsonResponse(error_response('Wrong format of some items in JSON.'), 
                                status=403)
        # Save
    
    return JsonResponse(ok_response(), status=200)
    # Success





    

