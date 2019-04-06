from django.conf.urls import url, include
from views import digests, reports, detections

urlpatterns = [
    url(r'^digests$', digests.rest_digest, name='rest_digest'),
    url(r'^reports$', reports.rest_report, name='rest_report'),
    url(r'^detections$', detections.rest_detection, name='rest_detection')
]
