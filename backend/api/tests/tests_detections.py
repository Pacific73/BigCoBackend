# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from api.models import DetectResult
from django.test import TestCase

class DetectionTest(TestCase):
    def setUp(self):
        DetectResult.drop_collection()
    

    def test_duplicate(self):
        pass