from django.contrib import admin
from adminsortable.admin import\
    SortableAdmin, NonSortableParentAdmin, SortableStackedInline, SortableTabularInline
from polls.models import Survey, Poll, CharChoice, Visitor


class ChoiceSortableTabularInline(SortableStackedInline):
    model = CharChoice
    extra = 1


class MySortableTabularInline(SortableTabularInline):
    model = Poll
    extra = 1
    inlines = [ChoiceSortableTabularInline]


class SurveyAdmin(NonSortableParentAdmin):
    model = Survey
    inlines = [MySortableTabularInline]


class PollAdmin(NonSortableParentAdmin):
    model = Poll
    inlines = [ChoiceSortableTabularInline]


admin.site.register(Survey,SurveyAdmin)
admin.site.register(Poll, PollAdmin)
# admin.site.register(CharChoice, ChoiceSortableTabularInline)


    
