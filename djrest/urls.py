# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from views import *

urlpatterns = {
    url(r'^dataset/$', MyDataViewSet.as_view()),
    url(r'^setup/(?P<how_many>[0-9]+)/$', init_dataset),
    url(r'^uptime/$', uptime),
    url(r'^check/(?P<gt>[0-9]+|)/(?P<lt>[0-9]+)/$', check_uptime),
    url(r'^filter/(?P<gt>[0-9]+|)/?(?P<lt>[0-9]+)/$', filter_uptime),
    url(r'^ref/(?P<rank>[0-9]+|)/$', ref_get),
    url(r'^chart/(?P<rank>[0-9]+|)/$', chart_one),
}

urlpatterns = format_suffix_patterns(urlpatterns)
