# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from api.models import Category, Manager, Application
from api.helpers import *
import json

'''
/api/categories
Supported HTTP types -> [GET]

This api is used for querying corp_sector and business information.

Request:
    No parameters.

Return:
    A JSON which maps corp_sector to its business list.
    A typical result looks like this:
    {
        "Security": [
            "Management",
            "Innovation",
            "Hr"
        ],
        "Finance": [
            "Management",
            "Recruitment",
            "Risk Analysis",
            "Innovation"
        ]
    }
'''
def rest_category(request):
    if request.method != 'GET':
        return JsonResponse(error_response('Only supports GET.'), 
                            status=403)
    # Only supports GET

    resp_data = dict()

    queryset = Category.objects().all()
    
    resp_data['corpSector'] = dict()
    for category in queryset:
        corp_key = category.corp_sector.lower().replace(' ', '_')
        resp_data['corpSector'][corp_key] = dict()
        items = resp_data['corpSector'][corp_key]
        items['label'] = category.corp_sector
        items['business'] = list()
        for business_name in category.business:
            business_value = business_name.lower().replace(' ', '_')
            items['business'].append({'value': business_value, 'label': business_name})
    
    managers = Manager.objects().all()
    resp_data['appManager'] = []
    for manager in managers:
        manager_value = manager.manager_name.lower().replace(' ', '_')
        resp_data['appManager'].append({'value': manager_value, 'label': manager.manager_name})
    
    apps = Application.objects().all()
    resp_data['appName'] = []
    for app in apps:
        app_name_value = app.name.lower().replace(' ', '_')
        resp_data['appName'].append({'value': app_name_value, 'label': app.name})
    
    resp_data['filters'] = [
        { 'value': 'name', 'label': 'Name' },
        { 'value': 'gender', 'label': 'Gender' },
        { 'value': 'race', 'label': 'Race' },
        { 'value': 'marital', 'label': 'Marital' },
        { 'value': 'address', 'label': 'Address' },
        { 'value': 'age', 'label': 'Age' },
        { 'value': 'ssn', 'label': 'SSN' },
        { 'value': 'ip_address', 'label': 'IP Address' },
    ]
    
    return JsonResponse(resp_data, status=200)
