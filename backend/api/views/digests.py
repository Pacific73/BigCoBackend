# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from api.models import DetectResult
from api.helpers import *
import json


'''
/api/digests
Supported HTTP types -> [POST]

This api is used for querying related DetectResult items given
a query request. Function uses `corp_sector` and `business` to
do AND filtering and uses `app_name` and `manager_name` to do
text searching.

Request JSON format:
    app_name:       string              name of the app (optional)
    manager_name:   string              name of the manager (optional)
    corp_sector:    string              corporation sector it belongs to (optional)
    business:       string              business department it belongs to (optional)
    filters:        a list of strings   filtering list

Return:
    A JSON which is in following format:
    {
        "digest":       a list of records
    }
    where a record is in following format:
    {
        "app_name":     string
        "manager_name": string
        "corp_sector":  string
        "business":     string
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

    if request.method != 'POST':
        return JsonResponse(error_response('Only supports POST.'), 
                            status=403)
    # Only supports POST

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        print e
        return JsonResponse(error_response('Invalid JSON format.'), 
                            status=403)

    app_name = data.get('app_name')
    manager_name = data.get('manager_name')
    corp_sector = regularize_str(data.get('corp_sector'))
    business = regularize_str(data.get('business'))
    filters = data.get('filters')

    if filters is None:
        return JsonResponse(error_response('No filters.'), 
                            status=403)

    items = None
    if corp_sector and business:
        items = DetectResult.objects(corp_sector=corp_sector,
                                    business=business)
    elif corp_sector:
        items = DetectResult.objects(corp_sector=corp_sector)
    # Department filtering

    
    if not items and app_name:
        items = DetectResult.objects(app_name=app_name)
    elif app_name:
        items = items.filter(app_name=app_name)
    
    if not items and manager_name:
        items = DetectResult.objects(manager_name=manager_name)
    elif manager_name:
        items = items.filter(manager_name=manager_name)
    
    if items is None:
        items = DetectResult.objects

    resp_data = dict()
    resp_data['digest'] = []
    for res in items:
        item = dict()
        item['application'] = res.app_name
        item['lastUpdated'] = str(res.last_updated)[:10]

        cluster_result = cluster(res.result, filters)
        for filter in filters:
            item[filter] = reorganize(cluster_result, filter)
        
        resp_data['digest'].append(item)
    # Load info into JSON
    
    return JsonResponse(resp_data, status=200)


