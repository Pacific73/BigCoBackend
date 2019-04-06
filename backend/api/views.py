# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from models import DetectResult
from datetime import datetime
from helpers import *
import json

'''
/api/digests
Supported HTTP types -> [GET]

This api is used for querying related DetectResult items given
a query request.

Request JSON format:
    app_name:       Name of the app
    manager_name:   Name of the manager
    corp_sector:    Corporation sector it belongs to
    business:       Business department it belongs to

Return:
    A JSON which is in following format:
    {
        "digest": [record_0, record_1, ...] -> a list of records
    }
    where a record is in following format:
    {
        "app_name":     string
        "manager_name": string
        "corp_sector":  string
        "business":     string
        "detected":     boolean
        "last_updated": date_string
        "result":       a dict of detected columns
    }
    An example of record["result"] can be:
    {
        "col47":    ["Ssn", "Race"],
        "nameCol":  ["Name", "Gender"]
    }
'''
def rest_digest(request):

    if request.method != 'GET':
        return JsonResponse(error_response('Only supports GET.'), 
                            status=403)
    # Only supports GET

    app_name = request.GET.get('app_name')
    manager_name = request.GET.get('manager_name')
    corp_sector = regularize_str(request.GET.get('corp_sector'))
    business = regularize_str(request.GET.get('business'))

    queryset = None
    if corp_sector and business:
        queryset = DetectResult.objects(corp_sector=corp_sector,
                                        business=business)
    # Department filtering
    
    query_term = app_name if app_name else None
    if manager_name:
        if query_term: query_term += ' ' + manager_name
        else:    query_term = manager_name
    # Concatenate app_name and manager_name as query_term
    
    if queryset:
        queryset = queryset.search_text(query_term).order_by('$text_score')
    else:
        queryset = DetectResult.objects.search_text(query_term).order_by('$text_score')
    # Text search

    resp_data = dict()
    resp_data['digest'] = []
    for res in queryset:
        item = dict()
        item['app_name'] = res.app_name
        item['manager_name'] = res.manager_name
        item['corp_sector'] = res.corp_sector
        item['business'] = res.business
        item['detected'] = res.detected
        item['result'] = res.result
        item['last_updated'] = res.last_updated
        resp_data['digest'].append(item)
    # Load info into JSON
    
    return JsonResponse(resp_data, status=200)



    

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

    last_updated = datetime.utcnow()
    detected = data.get('detected')
    result = data.get('result', [])
    # Get detected and result

    for col in result.keys():
        for idx, pii_name in enumerate(result[col]):
            result[col][idx] = regularize_str(pii_name)
    # regularize
    
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
        res.last_updated = last_updated
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
        res.last_updated = last_updated
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
