from django.contrib import admin
from polls.models import Survey, Poll, CharChoice, Visitor, TextPoll


@admin.register(Survey, Poll, CharChoice, Visitor, TextPoll)
class PersonAdmin(admin.ModelAdmin):
    pass
