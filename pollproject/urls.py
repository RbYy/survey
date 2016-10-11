from django.conf.urls import url
from django.contrib import admin
from polls.views import *


# admin.site.index_template = 'admin/custom-index.html'

visitors = Visitor.objects.all().order_by('-filled')

urlpatterns = [
    url(r'^admin/',
        admin.site.urls,
        {'extra_context': {'visitors': visitors}}),
    # url(r'^$', index, name="index"),
    url(r'^(?P<survey_id>[0-9]+)/survey/$', build_survey, name='build_survey'),
    url(r'^thankyou/', thankyou, name="thankyou"),
    url(r'^build/', build_fixture, name="build"),
]
