from django.contrib import admin
from polls.models import Survey, Poll, CharChoice, Visitor


@admin.register(Survey, Poll, CharChoice, Visitor)
class PersonAdmin(admin.ModelAdmin):
    pass
