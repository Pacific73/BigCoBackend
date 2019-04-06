# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mongoengine import *
from backend.settings import DB_NAME, DB_ADDR, DB_PORT

connect(db=DB_NAME, 
        host=DB_ADDR,
        port=DB_PORT)

########### uncomment this if necessary ###############
# from backend.settings import DB_USERNAME, DB_PASSWORD
# connect(db=DB_NAME, 
#         host=DB_ADDR,
#         port=DB_PORT,
#         username=DB_USERNAME,
#         password=DB_PASSWORD)

class DetectResult(Document):
    identifier = StringField(max_length=512, required=True)

    app_name = StringField(max_length=512, required=True)
    manager_name = StringField(max_length=512)
    corp_sector = StringField(max_length=512)
    business = StringField(max_length=512)

    last_updated = DateTimeField(required=True)
    detected = BooleanField(required=True, default=False)
    result = MapField(field=ListField(field=StringField(max_length=100)))

    meta = {
        'collection': 'DetectResult',
        'indexes': [
            'identifier',
            { 
                'fields': [
                    '$app_name',
                    '$manager_name'
                ],
                'default_language': 'english',
                'weights': {'app_name': 1, 'manager_name': 1}
            },
            ('business', 'corp_sector')
        ]
    }
