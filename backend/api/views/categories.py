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
    
    resp_data['corp_sectors'] = dict()
    for category in queryset:
        resp_data['corp_sectors'][category.corp_sector] = category.business
    
    managers = Manager.objects().all()
    resp_data['manager_names'] = []
    for manager in managers:
        resp_data['manager_names'].append(manager.manager_name)
    
    apps = Application.objects().all()
    resp_data['app_names'] = []
    for app in apps:
        resp_data['app_names'].append(app.name)
    
    return JsonResponse(resp_data, status=200)
