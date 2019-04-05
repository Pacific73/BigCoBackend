from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^digests$', views.rest_digest, name='rest_digest'),
    url(r'^reports$', views.rest_report, name='rest_report'),
    url(r'^detections$', views.rest_detection, name='rest_detection')
]
