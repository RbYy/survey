from django.conf.urls import url
from django.contrib import admin
from polls.views import *


urlpatterns = [
    url(r'^admin/',
        admin.site.urls),
    # url(r'^$', index, name="index"),
    url(r'^(?P<survey_id>[0-9]+)/survey/$', build_survey, name='build_survey'),
    url(r'^thankyou/', thankyou, name="thankyou"),
    url(r'^build/', build_fixture, name="build"),
    url(r'^register/', register, name="register"),
]
