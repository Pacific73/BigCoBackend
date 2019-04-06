# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from api.models import Category
from api.helpers import *
import json

'''
/api/categories
Supported HTTP types -> [GET]

This api is used for querying business and corp_sector information.

Request:
    No parameters.

Return:
    A JSON which maps business to its corp_sector list.
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

    queryset = Category.objects().all()
    resp_data = dict()
    for category in queryset:
        resp_data[category.business] = category.corp_sector
    
    return JsonResponse(resp_data, status=200)
