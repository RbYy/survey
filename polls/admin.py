from django.contrib import admin
from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline
from polls.models import Survey, Poll, CharChoice, Visitor


class PollInline(SortableStackedInline):
    model = Poll
    extra = 1


class SurveyAdmin(NonSortableParentAdmin):
    inlines = [PollInline]

admin.site.register(Survey, SurveyAdmin)


@admin.register(CharChoice, Poll, Visitor)
class PersonAdmin(admin.ModelAdmin):
    pass
