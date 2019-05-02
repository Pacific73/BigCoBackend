# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, FileResponse
from api.models import DetectResult
from api.helpers import *
import json
import xlsxwriter
import datetime
import io

'''
/api/reports
Supported HTTP types -> [GET]

This api is used for getting a report file given
a query request. Function uses `corp_sector` and `business` to
do AND filtering and uses `app_name` and `manager_name` to do
text searching.

Request JSON format:
    app_name:       string  name of the app (optional)
    manager_name:   string  name of the manager (optional)
    corp_sector:    string  corporation sector it belongs to (optional)
    business:       string  business department it belongs to (optional)

Return:
    An xlsx file.
'''
def rest_report(request):
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
        item['app_name'] = res.app_name
        item['manager_name'] = res.manager_name
        item['corp_sector'] = res.corp_sector
        item['business'] = res.business
        item['last_updated'] = str(res.last_updated)[:10]

        # item['result'] = cluster(res.result, filters)
        cluster_result = cluster(res.result, filters)
        for filter in filters:
            item[filter] = reorganize(cluster_result, filter)
        
        resp_data['digest'].append(item)
    
    print resp_data

    output = io.BytesIO()
    book = xlsxwriter.Workbook(output)
    sheet = book.add_worksheet()

    title_format = book.add_format({
        'bold':     True,
        'align':    'center',
        'valign':   'vcenter'
    })

    sheet.merge_range(0, 0, 0, 6, 'Citi PII Report', title_format)

    sheet.set_column(0, 4, 20)

    sheet.write(1, 0, 'App Name')
    sheet.write(1, 1, 'Manager\'s Name')
    sheet.write(1, 2, 'Corp Sector')
    sheet.write(1, 3, 'Business')
    sheet.write(1, 4, 'Last Updated')
    for idx, filter in enumerate(filters):
        sheet.write(1, 5+idx, filter)
    for idx, app in enumerate(resp_data['digest']):
        sheet.write(idx+2, 0, app['app_name'])
        sheet.write(idx+2, 1, app['manager_name'])
        sheet.write(idx+2, 2, app['corp_sector'])
        sheet.write(idx+2, 3, app['business'])
        sheet.write(idx+2, 4, str(app['last_updated']))
        for j, filter in enumerate(filters):
            sheet.write(idx+2, 5+j, str(app[filter]) + '%')
    book.close()
    # Generate xlsx file

    output.seek(0)

    response = FileResponse(output)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="report.xlsx"'
    return response
    # Return


