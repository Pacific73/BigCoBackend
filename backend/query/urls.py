from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^get_digest', views.get_digest, name='get_digest'),
    url(r'^get_report', views.get_report, name='get_report')
]
