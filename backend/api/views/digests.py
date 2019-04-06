# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from api.models import DetectResult
from api.helpers import *


'''
/api/digests
Supported HTTP types -> [GET]

This api is used for querying related DetectResult items given
a query request. Function uses `corp_sector` and `business` to
do AND filtering and uses `app_name` and `manager_name` to do
text searching.

Request JSON format:
    app_name:       string  name of the app (optional)
    manager_name:   string  name of the manager (optional)
    corp_sector:    string  corporation sector it belongs to (optional)
    business:       string  business department it belongs to (optional)

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