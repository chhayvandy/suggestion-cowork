from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from suggestion_api import views

urlpatterns = [
    url(r'^suggestion/$', views.suggestion_list),
]
urlpatterns = format_suffix_patterns(urlpatterns)