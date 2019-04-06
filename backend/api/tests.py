# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from models import DetectResult

class DetectionTest(TestCase):
    def setUp(self):
        DetectResult.drop_collection()
    

    def test_duplicate(self):
        pass


class DigestTest(TestCase):
    pass

class ReportTest(TestCase):
    pass
