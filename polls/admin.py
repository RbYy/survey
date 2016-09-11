from django.contrib import admin
from polls.models import Survey, Poll, CharChoice, Visitor, EmailChoice


@admin.register(Survey, Poll, CharChoice, EmailChoice, Visitor)
class PersonAdmin(admin.ModelAdmin):
    pass
