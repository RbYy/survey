from django.contrib import admin
from adminsortable.admin import\
    NonSortableParentAdmin, SortableStackedInline, SortableTabularInline
from polls.models import Survey, Poll, CharChoice


class ChoiceSortableTabularInline(SortableStackedInline):
    model = CharChoice
    exclude = ['created_by_visitor']
    extra = 0

    def get_queryset(self, request):
        qs = super(ChoiceSortableTabularInline, self).get_queryset(request)
        return qs.filter(created_by_visitor=False)


class MySortableTabularInline(SortableTabularInline):
    model = Poll
    extra = 0


class SurveyAdmin(NonSortableParentAdmin):
    model = Survey
    inlines = [MySortableTabularInline]


class PollAdmin(NonSortableParentAdmin):
    model = Poll
    inlines = [ChoiceSortableTabularInline]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Poll, PollAdmin)
