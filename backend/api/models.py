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

    app_name = StringField(max_length=512, required=True)
    manager_name = StringField(max_length=512)
    corp_sector = StringField(max_length=512)
    business = StringField(max_length=512)

    last_updated = DateTimeField(required=True)
    result = MapField(field=ListField(field=FloatField()))

    meta = {
        'collection': 'DetectResult',
        'indexes': [
            'app_name',
            'manager_name',
            'corp_sector', 
            'business'
        ]
    }

class Category(Document):
    corp_sector = StringField(max_length=512, required=True, unique=True)
    business = ListField(field=StringField(max_length=100), required=True)

    meta = {
        'collection': 'Category',
        'indexes': ['corp_sector']
    }

class Manager(Document):
    manager_name = StringField(max_length=512, required=True, unique=True)

    meta = {
        'collection': 'Manager',
        'indexes': ['manager_name']
    }

class Application(Document):
    name = StringField(max_length=512, required=True, unique=True)

    meta = {
        'collection': 'Application',
        'indexes': ['name']
    }
