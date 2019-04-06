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
    sheet.set_column(5, 5, 50)
    sheet.set_column(6, 6, 30)

    sheet.write(1, 0, 'App Name')
    sheet.write(1, 1, 'Manager\'s Name')
    sheet.write(1, 2, 'Corp Sector')
    sheet.write(1, 3, 'Business')
    sheet.write(1, 4, 'Detected')
    sheet.write(1, 5, 'Detect Result')
    sheet.write(1, 6, 'Last Updated')
    for idx, app in enumerate(resp_data['digest']):
        sheet.write(idx+2, 0, app['app_name'])
        sheet.write(idx+2, 1, app['manager_name'])
        sheet.write(idx+2, 2, app['corp_sector'])
        sheet.write(idx+2, 3, app['business'])
        sheet.write(idx+2, 4, str(app['detected']))
        sheet.write(idx+2, 5, json.dumps(app['result']))
        sheet.write(idx+2, 6, str(app['last_updated']))
    book.close()
    # Generate xlsx file

    output.seek(0)

    response = FileResponse(output)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="report.xlsx"'
    return response
    # Return


